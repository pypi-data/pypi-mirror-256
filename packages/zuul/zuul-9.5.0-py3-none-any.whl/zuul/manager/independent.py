# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from zuul import model
from zuul.lib.logutil import get_annotated_logger
from zuul.manager import PipelineManager, DynamicChangeQueueContextManager


class IndependentPipelineManager(PipelineManager):
    """PipelineManager that puts every Change into its own ChangeQueue."""

    changes_merge = False
    type = 'independent'

    def getChangeQueue(self, change, event, existing=None):
        log = get_annotated_logger(self.log, event)

        # We ignore any shared change queues on the pipeline and
        # instead create a new change queue for every change.
        if existing:
            return DynamicChangeQueueContextManager(existing)
        change_queue = model.ChangeQueue.new(
            self.pipeline.manager.current_context,
            pipeline=self.pipeline,
            dynamic=True)
        change_queue.addProject(change.project, None)
        self.pipeline.addQueue(change_queue)
        log.debug("Dynamically created queue %s", change_queue)
        return DynamicChangeQueueContextManager(change_queue)

    def enqueueChangesAhead(self, change, event, quiet, ignore_requirements,
                            change_queue, history=None, dependency_graph=None,
                            warnings=None):
        log = get_annotated_logger(self.log, event)

        history = history if history is not None else []
        if hasattr(change, 'number'):
            history.append(change)
        else:
            # Don't enqueue dependencies ahead of a non-change ref.
            return True

        abort, needed_changes = self.getMissingNeededChanges(
            change, change_queue, event,
            dependency_graph=dependency_graph)
        if abort:
            return False

        # Treat cycle dependencies as needed for the current change
        needed_changes.extend(
            self.getCycleDependencies(change, dependency_graph, event))

        if not needed_changes:
            return True
        log.debug("  Changes %s must be merged ahead of %s" % (
            needed_changes, change))
        for needed_change in needed_changes:
            # This differs from the dependent pipeline by enqueuing
            # changes ahead as "not live", that is, not intended to
            # have jobs run.  Pipeline requirements are still in place
            # in order to avoid unreviewed code being executed in
            # pipelines that require review.
            if needed_change not in history:
                r = self.addChange(needed_change, event, quiet=True,
                                   ignore_requirements=ignore_requirements,
                                   live=False,
                                   change_queue=change_queue,
                                   history=history,
                                   dependency_graph=dependency_graph)
                if not r:
                    return False
        return True

    def getMissingNeededChanges(self, change, change_queue, event,
                                dependency_graph=None):
        log = get_annotated_logger(self.log, event)

        if self.pipeline.ignore_dependencies:
            return False, []
        log.debug("Checking for changes needed by %s:" % change)
        # Return true if okay to proceed enqueing this change,
        # false if the change should not be enqueued.
        if not isinstance(change, model.Change):
            log.debug("  %s does not support dependencies" % type(change))
            return False, []
        if not change.getNeedsChanges(
                self.useDependenciesByTopic(change.project)):
            log.debug("  No changes needed")
            return False, []
        changes_needed = []
        abort = False
        for needed_change in self.resolveChangeReferences(
                change.getNeedsChanges(
                    self.useDependenciesByTopic(change.project))):
            log.debug("  Change %s needs change %s:" % (
                change, needed_change))
            if needed_change.is_merged:
                log.debug("  Needed change is merged")
                continue

            if dependency_graph is not None:
                log.debug("  Adding change %s to dependency graph for "
                          "change %s", needed_change, change)
                node = dependency_graph.setdefault(change, [])
                node.append(needed_change)

            if (self.pipeline.tenant.max_dependencies is not None and
                dependency_graph is not None and
                len(dependency_graph) > self.pipeline.tenant.max_dependencies):
                log.debug("  Dependency graph for change %s is too large",
                          change)
                return True, []

            if self.isChangeAlreadyInQueue(needed_change, change_queue):
                log.debug("  Needed change is already ahead in the queue")
                continue
            log.debug("  Change %s is needed" % needed_change)
            if needed_change not in changes_needed:
                changes_needed.append(needed_change)
                continue
            # This differs from the dependent pipeline check in not
            # verifying that the dependent change is mergable.
        return abort, changes_needed

    def dequeueItem(self, item, quiet=False):
        super(IndependentPipelineManager, self).dequeueItem(item, quiet)
        # An independent pipeline manager dynamically removes empty
        # queues
        if not item.queue.queue:
            self.pipeline.removeQueue(item.queue)
