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
import collections
import contextlib
import itertools
import logging
import textwrap
import time
import urllib
from abc import ABCMeta, abstractmethod

from zuul import exceptions
from zuul import model
from zuul.lib.dependson import find_dependency_headers
from zuul.lib.logutil import get_annotated_logger
from zuul.lib.tarjan import strongly_connected_components
import zuul.lib.tracing as tracing
from zuul.model import (
    Change, DequeueEvent, PipelineState, PipelineChangeList, QueueItem,
    filter_severity
)
from zuul.zk.change_cache import ChangeKey
from zuul.zk.components import COMPONENT_REGISTRY
from zuul.zk.exceptions import LockException
from zuul.zk.locks import pipeline_lock

from opentelemetry import trace


class DynamicChangeQueueContextManager(object):
    def __init__(self, change_queue):
        self.change_queue = change_queue

    def __enter__(self):
        return self.change_queue

    def __exit__(self, etype, value, tb):
        if self.change_queue and not self.change_queue.queue:
            self.change_queue.pipeline.removeQueue(self.change_queue)


class StaticChangeQueueContextManager(object):
    def __init__(self, change_queue):
        self.change_queue = change_queue

    def __enter__(self):
        return self.change_queue

    def __exit__(self, etype, value, tb):
        pass


class PipelineManager(metaclass=ABCMeta):
    """Abstract Base Class for enqueing and processing Changes in a Pipeline"""

    def __init__(self, sched, pipeline):
        self.log = logging.getLogger("zuul.Pipeline.%s.%s" %
                                     (pipeline.tenant.name,
                                      pipeline.name,))
        self.sched = sched
        self.pipeline = pipeline
        self.event_filters = []
        self.ref_filters = []
        # Cached dynamic layouts (layout uuid -> layout)
        self._layout_cache = {}
        # A small local cache to avoid hitting the ZK-based connection
        # change cache for multiple hits in the same pipeline run.
        self._change_cache = {}
        # Current ZK context when the pipeline is locked
        self.current_context = None
        # The pipeline summary used by zuul-web that is updated by the
        # schedulers after processing a pipeline.
        self.pipeline.summary = model.PipelineSummary()
        self.pipeline.summary._set(pipeline=self.pipeline)

        if sched:
            self.sql = sched.sql

    def __str__(self):
        return "<%s %s>" % (self.__class__.__name__, self.pipeline.name)

    @contextlib.contextmanager
    def currentContext(self, ctx):
        try:
            self.current_context = ctx
            yield
        finally:
            self.current_context = None

    def _postConfig(self):
        layout = self.pipeline.tenant.layout
        self.buildChangeQueues(layout)
        # Make sure we have state and change list objects.  We
        # don't actually ensure they exist in ZK here; these are
        # just local objects until they are serialized the first
        # time.  Since we don't hold the pipeline lock, we can't
        # reliably perform any read or write operations; we just
        # need to ensure we have in-memory objects to work with
        # and they will be initialized or loaded on the next
        # refresh.

        # These will be out of date until they are refreshed later.
        self.pipeline.state = PipelineState.create(
            self.pipeline, self.pipeline.state)
        self.pipeline.change_list = PipelineChangeList.create(
            self.pipeline)

        # Now, try to acquire a non-blocking pipeline lock and refresh
        # them for the side effect of initializing them if necessary.
        # In the case of a new pipeline, no one else should have a
        # lock anyway, and this helps us avoid emitting a whole bunch
        # of errors elsewhere on startup when these objects don't
        # exist.  If the pipeline already exists and we can't acquire
        # the lock, that's fine, we're much less likely to encounter
        # read errors elsewhere in that case anyway.
        try:
            with (pipeline_lock(
                    self.sched.zk_client, self.pipeline.tenant.name,
                    self.pipeline.name, blocking=False) as lock,
                    self.sched.createZKContext(lock, self.log) as ctx,
                    self.currentContext(ctx)):
                if not self.pipeline.state.exists(ctx):
                    # We only do this if the pipeline doesn't exist in
                    # ZK because in that case, this process should be
                    # fast since it's empty.  If it does exist,
                    # refreshing it may be slow and since other actors
                    # won't encounter errors due to its absence, we
                    # would rather defer the work to later.
                    self.pipeline.state.refresh(ctx)
                    self.pipeline.change_list.refresh(ctx)
        except LockException:
            pass

    def buildChangeQueues(self, layout):
        self.log.debug("Building relative_priority queues")
        change_queues = self.pipeline.relative_priority_queues
        tenant = self.pipeline.tenant
        layout_project_configs = layout.project_configs

        for project_name, project_configs in layout_project_configs.items():
            (trusted, project) = tenant.getProject(project_name)
            queue_name = None
            project_in_pipeline = False
            for project_config in layout.getAllProjectConfigs(project_name):
                project_pipeline_config = project_config.pipelines.get(
                    self.pipeline.name)
                if not queue_name:
                    queue_name = project_config.queue_name
                if project_pipeline_config is None:
                    continue
                project_in_pipeline = True
            if not project_in_pipeline:
                continue

            if not queue_name:
                continue
            if queue_name in change_queues:
                change_queue = change_queues[queue_name]
            else:
                change_queue = []
                change_queues[queue_name] = change_queue
                self.log.debug("Created queue: %s" % queue_name)
            change_queue.append(project)
            self.log.debug("Added project %s to queue: %s" %
                           (project, queue_name))

    def getSubmitAllowNeeds(self):
        # Get a list of code review labels that are allowed to be
        # "needed" in the submit records for a change, with respect
        # to this queue.  In other words, the list of review labels
        # this queue itself is likely to set before submitting.
        allow_needs = set()
        for action_reporter in self.pipeline.success_actions:
            allow_needs.update(action_reporter.getSubmitAllowNeeds())
        return allow_needs

    def eventMatches(self, event, change):
        log = get_annotated_logger(self.log, event)
        if event.forced_pipeline:
            if event.forced_pipeline == self.pipeline.name:
                log.debug("Event %s for change %s was directly assigned "
                          "to pipeline %s" % (event, change, self))
                return True
            else:
                return False
        for ef in self.event_filters:
            match_result = ef.matches(event, change)
            if match_result:
                log.debug("Event %s for change %s matched %s "
                          "in pipeline %s" % (event, change, ef, self))
                return True
            else:
                log.debug("Event %s for change %s does not match %s "
                          "in pipeline %s because %s" % (
                              event, change, ef, self, str(match_result)))
        return False

    def getNodePriority(self, item):
        queue = self.pipeline.getRelativePriorityQueue(item.change.project)
        items = self.pipeline.getAllItems()
        items = [i for i in items
                 if i.change.project in queue and
                 i.live]
        index = items.index(item)
        # Quantize on a logarithmic scale so that we don't constantly
        # needlessly adjust thousands of node requests.
        # If we're in the top 10 changes, return the accurate number.
        if index < 10:
            return index
        # After 10, batch then in groups of 10 (so items 10-19 are all
        # at node priority 10, 20-29 at 20, etc).
        if index < 100:
            return index // 10 * 10
        # After 100, batch in groups of 100.
        return index // 100 * 100

    def resolveChangeReferences(self, change_references):
        return self.resolveChangeKeys(
            [ChangeKey.fromReference(r) for r in change_references])

    def resolveChangeKeys(self, change_keys):
        resolved_changes = []
        for key in change_keys:
            change = self._change_cache.get(key.reference)
            if change is None:
                source = self.sched.connections.getSource(key.connection_name)
                change = source.getChange(key)
                if change is None:
                    self.log.error("Unable to resolve change from key %s", key)

                if isinstance(change, model.Change):
                    update_commit_dependencies = (
                        change.commit_needs_changes is None)
                    update_topic_dependencies = (
                        change.topic_needs_changes is None
                        and self.useDependenciesByTopic(change.project))
                    if (update_commit_dependencies
                            or update_topic_dependencies):
                        self.updateCommitDependencies(change, event=None)
                self._change_cache[change.cache_key] = change
            resolved_changes.append(change)
        return resolved_changes

    def clearCache(self):
        self._change_cache.clear()

    def _maintainCache(self):
        active_layout_uuids = set()
        referenced_change_keys = set()
        for item in self.pipeline.getAllItems():
            if item.layout_uuid:
                active_layout_uuids.add(item.layout_uuid)

            if isinstance(item.change, model.Change):
                referenced_change_keys.update(item.change.getNeedsChanges(
                    self.useDependenciesByTopic(item.change.project)))
                referenced_change_keys.update(item.change.getNeededByChanges())

        # Clean up unused layouts in the cache
        unused_layouts = set(self._layout_cache.keys()) - active_layout_uuids
        if unused_layouts:
            self.log.debug("Removing unused layouts %s from cache",
                           unused_layouts)
            for uid in unused_layouts:
                with contextlib.suppress(KeyError):
                    del self._layout_cache[uid]

        # Clean up change cache
        unused_keys = set(self._change_cache.keys()) - referenced_change_keys
        for key in unused_keys:
            with contextlib.suppress(KeyError):
                del self._change_cache[key]

    def isChangeAlreadyInPipeline(self, change):
        # Checks live items in the pipeline
        for item in self.pipeline.getAllItems():
            if item.live and change.equals(item.change):
                return True
        return False

    def isChangeRelevantToPipeline(self, change):
        # Checks if any version of the change or its deps matches any
        # item in the pipeline.
        for change_key in self.pipeline.change_list.getChangeKeys():
            if change.cache_stat.key.isSameChange(change_key):
                return True
        if isinstance(change, model.Change):
            for dep_change_ref in change.getNeedsChanges(
                    self.useDependenciesByTopic(change.project)):
                dep_change_key = ChangeKey.fromReference(dep_change_ref)
                if change.cache_stat.key.isSameChange(dep_change_key):
                    return True
        return False

    def isChangeAlreadyInQueue(self, change, change_queue):
        # Checks any item in the specified change queue
        for item in change_queue.queue:
            if change.equals(item.change):
                return True
        return False

    def refreshDeps(self, change, event):
        if not isinstance(change, model.Change):
            return

        to_refresh = set()
        for item in self.pipeline.getAllItems():
            if not isinstance(item.change, model.Change):
                continue
            if item.change.equals(change):
                to_refresh.add(item.change)
            for dep_change_ref in item.change.commit_needs_changes:
                dep_change_key = ChangeKey.fromReference(dep_change_ref)
                if dep_change_key.isSameChange(change.cache_stat.key):
                    to_refresh.add(item.change)

        for existing_change in to_refresh:
            self.updateCommitDependencies(existing_change, event)

    def reportEnqueue(self, item):
        if not self.pipeline.state.disabled:
            self.log.info("Reporting enqueue, action %s item %s" %
                          (self.pipeline.enqueue_actions, item))
            ret = self.sendReport(self.pipeline.enqueue_actions, item)
            if ret:
                self.log.error("Reporting item enqueued %s received: %s" %
                               (item, ret))

    def reportStart(self, item):
        if not self.pipeline.state.disabled:
            self.log.info("Reporting start, action %s item %s" %
                          (self.pipeline.start_actions, item))
            ret = self.sendReport(self.pipeline.start_actions, item)
            if ret:
                self.log.error("Reporting item start %s received: %s" %
                               (item, ret))

    def reportNormalBuildsetEnd(self, build_set, action, final, result=None):
        # Report a buildset end if there are jobs or errors
        if ((build_set.job_graph and len(build_set.job_graph.jobs) > 0) or
            build_set.has_blocking_errors or
            build_set.unable_to_merge):
            self.sql.reportBuildsetEnd(build_set, action,
                                       final, result)

    def reportDequeue(self, item, quiet=False):
        if not (self.pipeline.state.disabled or quiet):
            self.log.info(
                "Reporting dequeue, action %s item%s",
                self.pipeline.dequeue_actions,
                item,
            )
            ret = self.sendReport(self.pipeline.dequeue_actions, item)
            if ret:
                self.log.error(
                    "Reporting item dequeue %s received: %s", item, ret
                )
        # This might be called after canceljobs, which also sets a
        # non-final 'cancel' result.
        self.reportNormalBuildsetEnd(item.current_build_set, 'dequeue',
                                     final=False)

    def sendReport(self, action_reporters, item, phase1=True, phase2=True):
        """Sends the built message off to configured reporters.

        Takes the action_reporters and item and sends them to the
        pluggable reporters.

        """
        log = get_annotated_logger(self.log, item.event)
        report_errors = []
        if len(action_reporters) > 0:
            for reporter in action_reporters:
                try:
                    ret = reporter.report(item, phase1=phase1, phase2=phase2)
                    if ret:
                        report_errors.append(ret)
                except Exception as e:
                    item.setReportedResult('ERROR')
                    log.exception("Exception while reporting")
                    report_errors.append(str(e))
        return report_errors

    def isChangeReadyToBeEnqueued(self, change, event):
        return True

    def enqueueChangesAhead(self, change, event, quiet, ignore_requirements,
                            change_queue, history=None, dependency_graph=None,
                            warnings=None):
        return True

    def enqueueChangesBehind(self, change, event, quiet, ignore_requirements,
                             change_queue, history=None,
                             dependency_graph=None):
        return True

    def getMissingNeededChanges(self, change, change_queue, event,
                                dependency_graph=None):
        """Check that all needed changes are ahead in the queue.

        Return a list of any that are missing.  If it is not possible
        to correct the missing changes, "abort" will be true.

        :returns: (abort, needed_changes)
        """
        return False, []

    def getFailingDependentItems(self, item, nnfi):
        return None

    def getItemForChange(self, change, change_queue=None):
        if change_queue is not None:
            items = change_queue.queue
        else:
            items = self.pipeline.getAllItems()

        for item in items:
            if item.change.equals(change):
                return item
        return None

    def findOldVersionOfChangeAlreadyInQueue(self, change):
        for item in self.pipeline.getAllItems():
            if not item.live:
                continue
            if change.isUpdateOf(item.change):
                return item
        return None

    def removeOldVersionsOfChange(self, change, event):
        if not self.pipeline.dequeue_on_new_patchset:
            return
        old_item = self.findOldVersionOfChangeAlreadyInQueue(change)
        if old_item:
            log = get_annotated_logger(self.log, event)
            log.debug("Change %s is a new version of %s, removing %s",
                      change, old_item.change, old_item)
            self.removeItem(old_item)

    def removeAbandonedChange(self, change, event):
        log = get_annotated_logger(self.log, event)
        log.debug("Change %s abandoned, removing." % change)
        for item in self.pipeline.getAllItems():
            if not item.live:
                continue
            if item.change.equals(change):
                self.removeItem(item)

    @abstractmethod
    def getChangeQueue(self, change, event, existing=None):
        pass

    def reEnqueueItem(self, item, last_head, old_item_ahead, item_ahead_valid):
        log = get_annotated_logger(self.log, item.event)
        with self.getChangeQueue(item.change, item.event,
                                 last_head.queue) as change_queue:
            if change_queue:
                log.debug("Re-enqueing change %s in queue %s",
                          item.change, change_queue)
                change_queue.enqueueItem(item)

                # If the old item ahead was re-enqued, this value will
                # be true, so we should attempt to move the item back
                # to where it was in case an item ahead is already
                # failing.
                if item_ahead_valid:
                    change_queue.moveItem(item, old_item_ahead)

                # Get an updated copy of the layout, but if we have a
                # job graph already, then keep it (our repo state and
                # jobs are frozen and will now only update if the item
                # ahead changes).  This resumes the buildset merge
                # state machine.  If we have an up-to-date layout, it
                # will go ahead and refresh the job graph if there
                # isn't one; or it will send a new merge job if
                # necessary, or it will do nothing if we're waiting on
                # a merge job.
                has_job_graph = bool(item.current_build_set.job_graph)
                if item.live:
                    # Only reset the layout for live items as we don't need to
                    # re-create the layout in independent pipelines.
                    item.updateAttributes(self.current_context,
                                          layout_uuid=None)

                # If the item is no longer active, but has a job graph we
                # will make sure to update it.
                if item.active or has_job_graph:
                    self.prepareItem(item)

                # Re-set build results in case any new jobs have been
                # added to the tree.
                for build in item.current_build_set.getBuilds():
                    if build.result:
                        item.setResult(build)
                # Similarly, reset the item state.
                if item.current_build_set.unable_to_merge:
                    item.setUnableToMerge()
                if item.current_build_set.has_blocking_errors:
                    item.setConfigErrors(item.getConfigErrors())
                if item.dequeued_needing_change:
                    item.setDequeuedNeedingChange(item.dequeued_needing_change)
                if item.dequeued_missing_requirements:
                    item.setDequeuedMissingRequirements()

                # It can happen that all in-flight builds have been removed
                # which would lead to paused parent jobs not being resumed.
                # To prevent that resume parent jobs if necessary.
                self._resumeBuilds(item.current_build_set)

                self.reportStats(item)
                return True
            else:
                log.error("Unable to find change queue for project %s",
                          item.change.project)
                return False

    def addChange(self, change, event, quiet=False, enqueue_time=None,
                  ignore_requirements=False, live=True,
                  change_queue=None, history=None, dependency_graph=None,
                  skip_presence_check=False):
        log = get_annotated_logger(self.log, event)
        log.debug("Considering adding change %s" % change)

        history = history if history is not None else []
        log.debug("History: %s", history)

        # Ensure the dependency graph is created when the first change is
        # processed to allow cycle detection with the Tarjan algorithm
        dependency_graph = dependency_graph or collections.OrderedDict()
        log.debug("Dependency graph: %s", dependency_graph)

        # If we are adding a live change, check if it's a live item
        # anywhere in the pipeline.  Otherwise, we will perform the
        # duplicate check below on the specific change_queue.
        if (live and
            self.isChangeAlreadyInPipeline(change) and
            not skip_presence_check):
            log.debug("Change %s is already in pipeline, ignoring" % change)
            return True

        if ((not self.pipeline.allow_other_connections) and
            (change.project.connection_name not in self.pipeline.connections)):
            log.debug("Change %s is not from a connection known to %s ",
                      change, self.pipeline)
            return False

        if not ignore_requirements:
            for f in self.ref_filters:
                if f.connection_name != change.project.connection_name:
                    log.debug("Filter %s skipped for change %s due "
                              "to mismatched connections" % (f, change))
                    continue
                match_result = f.matches(change)
                if not match_result:
                    log.debug("Change %s does not match pipeline "
                              "requirement %s because %s" % (
                                  change, f, str(match_result)))
                    return False

        if not self.isChangeReadyToBeEnqueued(change, event):
            log.debug("Change %s is not ready to be enqueued, ignoring" %
                      change)
            return False

        # We know this change isn't in this pipeline, but it may be in
        # others.  If it is, then presumably its commit_needs are up
        # to date and this is a noop; otherwise, we need to refresh
        # them anyway.
        if isinstance(change, model.Change):
            self.updateCommitDependencies(change, event)

        with self.getChangeQueue(change, event, change_queue) as change_queue:
            if not change_queue:
                log.debug("Unable to find change queue for "
                          "change %s in project %s" %
                          (change, change.project))
                return False

            warnings = []
            if not self.enqueueChangesAhead(change, event, quiet,
                                            ignore_requirements,
                                            change_queue, history=history,
                                            dependency_graph=dependency_graph,
                                            warnings=warnings):
                self.dequeueIncompleteCycle(change, dependency_graph, event,
                                            change_queue)
                log.debug("Failed to enqueue changes ahead of %s" % change)
                if warnings:
                    self._reportNonEqueuedItem(change_queue, change,
                                               event, warnings)
                return False

            log.debug("History after enqueuing changes ahead: %s", history)

            if self.isChangeAlreadyInQueue(change, change_queue):
                if not skip_presence_check:
                    log.debug("Change %s is already in queue, ignoring",
                              change)
                    return True

            cycle = []
            if isinstance(change, model.Change):
                cycle = self.cycleForChange(change, dependency_graph, event)
                if cycle and not self.canProcessCycle(change.project):
                    log.info("Dequeing change %s since the project "
                             "does not allow circular dependencies", change)
                    warnings = ["Dependency cycle detected and project "
                                f"{change.project.name} doesn't allow "
                                "circular dependencies"]
                    self._reportNonEqueuedItem(change_queue,
                                               cycle[-1], event, warnings)
                    return False

            log.info("Adding change %s to queue %s in %s" %
                     (change, change_queue, self.pipeline))
            if enqueue_time is None:
                enqueue_time = time.time()

            event_span = tracing.restoreSpanContext(event.span_context)
            link_attributes = {"rel": type(event).__name__}
            link = trace.Link(event_span.get_span_context(),
                              attributes=link_attributes)
            span_info = tracing.startSavedSpan(
                'QueueItem', start_time=enqueue_time, links=[link])

            item = change_queue.enqueueChange(change, event,
                                              span_info=span_info,
                                              enqueue_time=enqueue_time)
            self.updateBundle(item, change_queue, cycle)

            with item.activeContext(self.current_context):
                if enqueue_time:
                    item.enqueue_time = enqueue_time
                item.live = live
                self.reportStats(item, trigger_event=event)
                item.quiet = quiet

            if item.live:
                self.reportEnqueue(item)

            # Items in a dependency cycle are expected to be enqueued after
            # each other. To prevent non-cycle items from being enqueued
            # between items of the same cycle, enqueue items behind each item
            # in the cycle once all items in the cycle are enqueued.
            if all([self.isChangeAlreadyInQueue(c, change_queue)
                    for c in cycle]):
                if cycle:
                    self.log.debug("Cycle complete, enqueing changes behind")
                for c in cycle or [change]:
                    self.enqueueChangesBehind(c, event, quiet,
                                              ignore_requirements,
                                              change_queue, history,
                                              dependency_graph)

            zuul_driver = self.sched.connections.drivers['zuul']
            tenant = self.pipeline.tenant
            with trace.use_span(tracing.restoreSpan(item.span_info)):
                zuul_driver.onChangeEnqueued(
                    tenant, item.change, self.pipeline, event)
            self.dequeueSupercededItems(item)
            return True

    def _reportNonEqueuedItem(self, change_queue, change, event, warnings):
        # Enqueue an item which otherwise can not be enqueued in order
        # to report a message to the user.
        actions = self.pipeline.failure_actions
        ci = change_queue.enqueueChange(change, event)
        try:
            for w in warnings:
                ci.warning(w)
            ci.setReportedResult('FAILURE')

            # Only report the item if the project is in the current
            # pipeline. Otherwise the change could be spammed by
            # reports from unrelated pipelines.
            if self.pipeline.tenant.layout.getProjectPipelineConfig(ci):
                self.sendReport(actions, ci)
        finally:
            # Ensure that the item is dequeued in any case. Otherwise we
            # might leak items caused by this temporary enqueue.
            self.dequeueItem(ci)
        # We don't use reportNormalBuildsetEnd here because we want to
        # report even with no jobs.
        self.sql.reportBuildsetEnd(ci.current_build_set,
                                   'failure', final=True)

    def cycleForChange(self, change, dependency_graph, event, debug=True):
        if debug:
            log = get_annotated_logger(self.log, event)
            log.debug("Running Tarjan's algorithm on current dependencies: %s",
                      dependency_graph)
        sccs = [s for s in strongly_connected_components(dependency_graph)
                if len(s) > 1]
        if debug:
            log.debug("Strongly connected components (cyles): %s", sccs)
        for scc in sccs:
            if change in scc:
                if debug:
                    log.debug("Dependency cycle detected for "
                              "change %s in project %s",
                              change, change.project)
                # Change can not be part of multiple cycles, so we can return
                return scc
        return []

    def getCycleDependencies(self, change, dependency_graph, event):
        cycle = self.cycleForChange(change, dependency_graph, event)
        return set(
            itertools.chain.from_iterable(
                dependency_graph[c] for c in cycle if c != change)
        ) - set(cycle)

    def getDependencyGraph(self, change, dependency_graph, event,
                           history=None):
        if self.pipeline.ignore_dependencies:
            return
        if not isinstance(change, model.Change):
            return
        if not change.getNeedsChanges(
                self.useDependenciesByTopic(change.project)):
            return
        if history is None:
            history = set()
        history.add(change)
        for needed_change in self.resolveChangeReferences(
                change.getNeedsChanges(
                    self.useDependenciesByTopic(change.project))):
            if needed_change.is_merged:
                continue

            node = dependency_graph.setdefault(change, [])
            node.append(needed_change)
            if needed_change not in history:
                self.getDependencyGraph(needed_change, dependency_graph,
                                        event, history)

    def getQueueConfig(self, project):
        layout = self.pipeline.tenant.layout
        queue_name = None
        for project_config in layout.getAllProjectConfigs(
            project.canonical_name
        ):
            if not queue_name:
                queue_name = project_config.queue_name

            project_pipeline_config = project_config.pipelines.get(
                self.pipeline.name)

            if project_pipeline_config is None:
                continue

        return layout.queues.get(queue_name)

    def canProcessCycle(self, project):
        queue_config = self.getQueueConfig(project)
        if queue_config is None:
            return False

        return queue_config.allow_circular_dependencies

    def useDependenciesByTopic(self, project):
        queue_config = self.getQueueConfig(project)
        if queue_config is None:
            return False

        return queue_config.dependencies_by_topic

    def getNonMergeableCycleChanges(self, bundle):

        """Return changes in the cycle that do not fulfill
        the pipeline's ready criteria."""
        return []

    def updateBundle(self, item, change_queue, cycle):
        if not cycle:
            return

        log = get_annotated_logger(self.log, item.event)
        item.updateAttributes(self.current_context, bundle=model.Bundle())

        # Try to find already enqueued items of this cycle, so we use
        # the same bundle
        for needed_change in (c for c in cycle if c is not item.change):
            needed_item = self.getItemForChange(needed_change, change_queue)
            if not needed_item:
                continue
            # Use a common bundle for the cycle
            item.updateAttributes(self.current_context,
                                  bundle=needed_item.bundle)
            break

        log.info("Adding cycle item %s to bundle %s", item, item.bundle)
        bundle = item.bundle
        bundle.add_item(item)

        # Write out the updated bundle info to Zookeeper for all items
        # since it may have mutated since our last write.
        for bundle_item in bundle.items:
            bundle_item.updateAttributes(self.current_context,
                                         bundle=bundle)

    def dequeueIncompleteCycle(self, change, dependency_graph, event,
                               change_queue):
        log = get_annotated_logger(self.log, event)
        cycle = self.cycleForChange(change, dependency_graph, event)
        enqueued_cycle_items = [i for i in (self.getItemForChange(c,
                                                                  change_queue)
                                            for c in cycle) if i is not None]
        if enqueued_cycle_items:
            log.info("Dequeuing incomplete cycle items: %s",
                     enqueued_cycle_items)
            for cycle_item in enqueued_cycle_items:
                self.dequeueItem(cycle_item)

    def dequeueItem(self, item, quiet=False):
        log = get_annotated_logger(self.log, item.event)
        log.debug("Removing change %s from queue", item.change)
        # In case a item is dequeued that doesn't have a result yet
        # (success/failed/...) we report it as dequeued.
        # Without this check, all items with a valid result would be reported
        # twice.
        if not item.current_build_set.result and item.live:
            item.setReportedResult('DEQUEUED')
            if not item.reported_start:
                # If we haven't reported start, we don't know if Zuul
                # was supposed to act on the item at all, so keep it
                # quiet.
                quiet = True
            self.reportDequeue(item, quiet)
        item.queue.dequeueItem(item)

        span_attrs = {
            'zuul_event_id': item.event.zuul_event_id,
            'zuul_tenant': self.pipeline.tenant.name,
            'zuul_pipeline': self.pipeline.name,
        }
        for k, v in item.change.getSafeAttributes().toDict().items():
            span_attrs['ref_' + k] = v
        tracing.endSavedSpan(item.current_build_set.span_info)
        tracing.endSavedSpan(item.span_info,
                             attributes=span_attrs)

    def removeItem(self, item):
        log = get_annotated_logger(self.log, item.event)
        # Remove an item from the queue, probably because it has been
        # superseded by another change.
        log.debug("Canceling builds behind change: %s "
                  "because it is being removed.", item.change)
        self.cancelJobs(item)
        self.dequeueItem(item)
        self.reportStats(item)

        if item.bundle is None:
            return

        log.debug("Dequeueing items in bundle %s", item.bundle)
        bundle_iter = (i for i in item.bundle.items if i is not item)
        for bundle_item in bundle_iter:
            self.cancelJobs(bundle_item)
            self.dequeueItem(bundle_item)
            self.reportStats(bundle_item)

    def dequeueSupercededItems(self, item):
        change_id = (
            item.change._id() if isinstance(item.change, Change)
            else None
        )
        for other_name in self.pipeline.supercedes:
            other_pipeline = self.pipeline.tenant.layout.pipelines.get(
                other_name)
            if not other_pipeline:
                continue

            # MODEL_API: >2
            if COMPONENT_REGISTRY.model_api > 2:
                event = model.SupercedeEvent(
                    other_pipeline.tenant.name,
                    other_pipeline.name,
                    item.change.project.canonical_hostname,
                    item.change.project.name,
                    change_id,
                    item.change.ref)
                self.sched.pipeline_trigger_events[
                    self.pipeline.tenant.name][other_pipeline.name
                        ].put_supercede(event)
            else:
                # Note: Iterating over the pipelines w/o locking and
                # refreshing them is wrong and only kept for backward
                # compatibility.
                found = None
                for other_item in other_pipeline.getAllItems():
                    if (other_item.live
                            and other_item.change.equals(item.change)):
                        found = other_item
                        break
                if found:
                    self.log.info("Item %s is superceded by %s, dequeuing",
                                  found, item)
                    event = DequeueEvent(
                        other_pipeline.tenant.name,
                        other_pipeline.name,
                        item.change.project.canonical_hostname,
                        item.change.project.name,
                        change_id,
                        item.change.ref)
                    self.sched.pipeline_management_events[
                        self.pipeline.tenant.name][other_pipeline.name].put(
                            event, needs_result=False)

    def updateCommitDependencies(self, change, event):
        log = get_annotated_logger(self.log, event)

        must_update_commit_deps = (
            not hasattr(event, "zuul_event_ltime")
            or change.commit_needs_changes is None
            or change.cache_stat.mzxid <= event.zuul_event_ltime
        )

        must_update_topic_deps = (
            self.useDependenciesByTopic(change.project) and (
                not hasattr(event, "zuul_event_ltime")
                or change.topic_needs_changes is None
                or change.cache_stat.mzxid <= event.zuul_event_ltime
            )
        )

        update_attrs = {}
        if must_update_commit_deps:
            # Search for Depends-On headers and find appropriate changes
            log.debug("  Updating commit dependencies for %s", change)
            dependencies = []
            seen = set()
            for match in find_dependency_headers(change.message):
                log.debug("  Found Depends-On header: %s", match)
                if match in seen:
                    continue
                seen.add(match)
                try:
                    url = urllib.parse.urlparse(match)
                except ValueError:
                    continue
                source = self.sched.connections.getSourceByHostname(
                    url.hostname)
                if not source:
                    continue
                log.debug("  Found source: %s", source)
                dep = source.getChangeByURLWithRetry(match, event)
                if dep and (not dep.is_merged) and dep not in dependencies:
                    log.debug("  Adding dependency: %s", dep)
                    dependencies.append(dep)
            new_commit_needs_changes = [d.cache_key for d in dependencies]

            update_attrs = dict(commit_needs_changes=new_commit_needs_changes)

        # Ask the source for any tenant-specific changes (this allows
        # drivers to implement their own way of collecting deps):
        source = self.sched.connections.getSource(
            change.project.connection_name)
        if must_update_topic_deps:
            log.debug("  Updating topic dependencies for %s", change)
            new_topic_needs_changes = []
            for dep in source.getChangesByTopic(change.topic):
                if dep and (not dep.is_merged):
                    log.debug("  Adding dependency: %s", dep)
                    new_topic_needs_changes.append(dep.cache_key)
            update_attrs['topic_needs_changes'] = new_topic_needs_changes

        if update_attrs:
            source.setChangeAttributes(change, **update_attrs)

    def provisionNodes(self, item):
        log = item.annotateLogger(self.log)
        jobs = item.findJobsToRequest(item.pipeline.tenant.semaphore_handler)
        if not jobs:
            return False
        build_set = item.current_build_set
        log.debug("Requesting nodes for change %s", item.change)
        if self.sched.globals.use_relative_priority:
            relative_priority = item.getNodePriority()
        else:
            relative_priority = 0
        parent_span = tracing.restoreSpan(build_set.span_info)
        with trace.use_span(parent_span):
            for job in jobs:
                self._makeNodepoolRequest(
                    log, build_set, job, relative_priority)
        return True

    def _makeNodepoolRequest(self, log, build_set, job, relative_priority,
                             alternative=0):
        provider = self._getPausedParentProvider(build_set, job)
        priority = self._calculateNodeRequestPriority(build_set, job)
        tenant_name = build_set.item.pipeline.tenant.name
        pipeline_name = build_set.item.pipeline.name
        item = build_set.item
        req = self.sched.nodepool.requestNodes(
            build_set.uuid, job, tenant_name, pipeline_name, provider,
            priority, relative_priority, event=item.event)
        log.debug("Adding node request %s for job %s to item %s",
                  req, job, item)
        build_set.setJobNodeRequestID(job, req.id)
        if req.fulfilled:
            nodeset = self.sched.nodepool.getNodeSet(req, job.nodeset)
            job = build_set.item.getJob(req._job_id)
            build_set.jobNodeRequestComplete(job, nodeset)
        else:
            job.setWaitingStatus(f'node request: {req.id}')

    def _getPausedParent(self, build_set, job):
        job_graph = build_set.job_graph
        if job_graph:
            for parent in job_graph.getParentJobsRecursively(job):
                build = build_set.getBuild(parent)
                if build.paused:
                    return build
        return None

    def _getPausedParentProvider(self, build_set, job):
        parent_build = self._getPausedParent(build_set, job)
        if parent_build:
            return build_set.getJobNodeProvider(parent_build.job)
        return None

    def _calculateNodeRequestPriority(self, build_set, job):
        precedence_adjustment = 0
        precedence = build_set.item.pipeline.precedence
        if self._getPausedParent(build_set, job):
            precedence_adjustment = -1
        initial_precedence = model.PRIORITY_MAP[precedence]
        return max(0, initial_precedence + precedence_adjustment)

    def _executeJobs(self, item, jobs):
        log = get_annotated_logger(self.log, item.event)
        log.debug("Executing jobs for change %s", item.change)
        build_set = item.current_build_set
        for job in jobs:
            log.debug("Found job %s for change %s", job, item.change)
            try:
                zone = build_set.getJobNodeExecutorZone(job)
                nodes = build_set.getJobNodeList(job)
                self.sched.executor.execute(
                    job, nodes, item, self.pipeline, zone,
                    build_set.dependent_changes,
                    build_set.merger_items)
                job.setWaitingStatus('executor')
            except Exception:
                log.exception("Exception while executing job %s "
                              "for change %s:", job, item.change)
                try:
                    # If we hit an exception we don't have a build in the
                    # current item so a potentially aquired semaphore must be
                    # released as it won't be released on dequeue of the item.
                    tenant = item.pipeline.tenant
                    pipeline = build_set.item.pipeline
                    event_queue = self.sched.pipeline_result_events[
                        tenant.name][pipeline.name]
                    tenant.semaphore_handler.release(event_queue, item, job)
                except Exception:
                    log.exception("Exception while releasing semaphore")

    def executeJobs(self, item):
        # TODO(jeblair): This should return a value indicating a job
        # was executed.  Appears to be a longstanding bug.
        if not item.current_build_set.job_graph:
            return False

        jobs = item.findJobsToRun(
            item.pipeline.tenant.semaphore_handler)
        if jobs:
            self._executeJobs(item, jobs)

    def cancelJobs(self, item, prime=True):
        log = get_annotated_logger(self.log, item.event)
        log.debug("Cancel jobs for change %s", item.change)
        canceled = False
        old_build_set = item.current_build_set
        jobs_to_cancel = item.getJobs()

        for job in jobs_to_cancel:
            self.sched.cancelJob(old_build_set, job, final=True)

        # Don't reset builds for a failing bundle when it has already started
        # reporting, to keep available build results. Those items will be
        # reported immediately afterwards during queue processing.
        if (prime and item.current_build_set.ref and not
                item.didBundleStartReporting()):
            # Force a dequeued result here because we haven't actually
            # reported the item, but we are done with this buildset.
            self.reportNormalBuildsetEnd(
                item.current_build_set, 'dequeue', final=False,
                result='DEQUEUED')
            tracing.endSavedSpan(item.current_build_set.span_info)
            item.resetAllBuilds()

        for item_behind in item.items_behind:
            log.debug("Canceling jobs for change %s, behind change %s",
                      item_behind.change, item.change)
            if self.cancelJobs(item_behind, prime=prime):
                canceled = True
        return canceled

    def _findRelevantErrors(self, item, layout):
        # First collect all the config errors that are not related to the
        # current item.
        parent_error_keys = list(
            self.pipeline.tenant.layout.loading_errors.error_keys)
        for item_ahead in item.items_ahead:
            parent_error_keys.extend(
                e.key for e in item.item_ahead.getConfigErrors())

        # Then find config errors which aren't in the parent.  But
        # include errors in this project-branch because the error
        # detection hash is imperfect and someone attempting to fix an
        # error may create a near duplicate error and it would go
        # undetected.  Or if there are two errors and the user only
        # fixes one, then they may not realize their work is
        # incomplete.
        relevant_errors = []
        severity_error = False
        for err in layout.loading_errors.errors:
            econtext = err.key.context
            if ((err.key not in parent_error_keys) or
                (econtext.project_name == item.change.project.name and
                 econtext.branch == item.change.branch)):
                relevant_errors.append(err)
                if err.severity == model.SEVERITY_ERROR:
                    severity_error = True
        return relevant_errors, severity_error

    def _loadDynamicLayout(self, item):
        log = get_annotated_logger(self.log, item.event)
        # Load layout
        # Late import to break an import loop
        import zuul.configloader
        loader = zuul.configloader.ConfigLoader(
            self.sched.connections, self.sched.zk_client, self.sched.globals,
            self.sched.statsd, self.sched)

        log.debug("Loading dynamic layout")

        (trusted_updates, untrusted_updates) = item.includesConfigUpdates()
        build_set = item.current_build_set
        trusted_layout = None
        trusted_errors = False
        untrusted_layout = None
        untrusted_errors = False
        additional_project_branches = self._getProjectBranches(item)
        try:
            # First parse the config as it will land with the
            # full set of config and project repos.  This lets us
            # catch syntax errors in config repos even though we won't
            # actually run with that config.
            if trusted_updates:
                log.debug("Loading dynamic layout (phase 1)")
                trusted_layout = loader.createDynamicLayout(
                    item,
                    build_set.files,
                    additional_project_branches,
                    self.sched.ansible_manager,
                    include_config_projects=True,
                    zuul_event_id=None)
                trusted_errors = len(filter_severity(
                    trusted_layout.loading_errors.errors,
                    errors=True, warnings=False)) > 0

            # Then create the config a second time but without changes
            # to config repos so that we actually use this config.
            if untrusted_updates:
                log.debug("Loading dynamic layout (phase 2)")
                untrusted_layout = loader.createDynamicLayout(
                    item,
                    build_set.files,
                    additional_project_branches,
                    self.sched.ansible_manager,
                    include_config_projects=False,
                    zuul_event_id=None)
                untrusted_errors = len(filter_severity(
                    untrusted_layout.loading_errors.errors,
                    errors=True, warnings=False)) > 0

            # Configuration state handling switchboard. Intentionally verbose
            # and repetetive to be exceptionally clear that we handle all
            # possible cases correctly. Note we never return trusted_layout
            # from a dynamic update.

            # No errors found at all use dynamic untrusted layout
            if (trusted_layout and not trusted_errors and
                    untrusted_layout and not untrusted_errors):
                log.debug("Loading dynamic layout complete")
                return untrusted_layout
            # No errors in untrusted only layout update
            elif (not trusted_layout and
                    untrusted_layout and not untrusted_errors):
                log.debug("Loading dynamic layout complete")
                return untrusted_layout
            # No errors in trusted only layout update
            elif (not untrusted_layout and
                    trusted_layout and not trusted_errors):
                # We're a change to a config repo (with no untrusted
                # config items ahead), so just use the current pipeline
                # layout.
                log.debug("Loading dynamic layout complete")
                return item.queue.pipeline.tenant.layout
            # Untrusted layout only works with trusted updates
            elif (trusted_layout and not trusted_errors and
                    untrusted_layout and untrusted_errors):
                log.info("Configuration syntax error in dynamic layout")
                # The config is good if we include config-projects,
                # but is currently invalid if we omit them.  Instead
                # of returning the whole error message, just leave a
                # note that the config will work once the dependent
                # changes land.
                msg = "This change depends on a change "\
                      "to a config project.\n\n"
                msg += textwrap.fill(textwrap.dedent("""\
                The syntax of the configuration in this change has
                been verified to be correct once the config project
                change upon which it depends is merged, but it can not
                be used until that occurs."""))
                item.setConfigError(msg)
                return None
            # Untrusted layout is broken and trusted is broken or not set
            elif untrusted_layout and untrusted_errors:
                # Find a layout loading error that match
                # the current item.change and only report
                # if one is found.
                relevant_errors, severity_error = self._findRelevantErrors(
                    item, untrusted_layout)
                if relevant_errors:
                    item.setConfigErrors(relevant_errors)
                if severity_error:
                    return None
                log.info(
                    "Configuration syntax error not related to "
                    "change context. Error won't be reported.")
                return untrusted_layout
            # Trusted layout is broken
            elif trusted_layout and trusted_errors:
                # Find a layout loading error that match
                # the current item.change and only report
                # if one is found.
                relevant_errors, severity_error = self._findRelevantErrors(
                    item, trusted_layout)
                if relevant_errors:
                    item.setConfigErrors(relevant_errors)
                if severity_error:
                    return None
                log.info(
                    "Configuration syntax error not related to "
                    "change context. Error won't be reported.")
                # We're a change to a config repo with errors not relevant
                # to this repo. We use the pipeline layout.
                return item.queue.pipeline.tenant.layout
            else:
                raise Exception("We have reached a configuration error that is"
                                "not accounted for.")

        except Exception:
            log.exception("Error in dynamic layout")
            item.setConfigError("Unknown configuration error")
            return None

    def _getProjectBranches(self, item):
        # Get the branches of the item and all items ahead
        project_branches = {}
        while item:
            if hasattr(item.change, 'branch'):
                this_project_branches = project_branches.setdefault(
                    item.change.project.canonical_name, set())
                this_project_branches.add(item.change.branch)
            item = item.item_ahead
        return project_branches

    def getFallbackLayout(self, item):
        parent_item = item.item_ahead
        if not parent_item:
            return item.pipeline.tenant.layout

        return self.getLayout(parent_item)

    def getLayout(self, item):
        log = get_annotated_logger(self.log, item.event)
        layout = self._layout_cache.get(item.layout_uuid)
        if layout:
            log.debug("Using cached layout %s for item %s", layout.uuid, item)
            return layout

        if item.layout_uuid:
            log.debug("Re-calculating layout for item %s", item)

        layout = self._getLayout(item)
        if layout:
            item.updateAttributes(self.current_context,
                                  layout_uuid=layout.uuid)
            self._layout_cache[item.layout_uuid] = layout
        return layout

    def _getLayout(self, item):
        log = get_annotated_logger(self.log, item.event)
        if item.item_ahead:
            if (
                (item.item_ahead.live and
                 not item.item_ahead.current_build_set.job_graph) or
                (not item.item_ahead.live and not item.item_ahead.layout_uuid)
            ):
                # We're probably waiting on a merge job for the item ahead.
                return None

        # If the current change does not update the layout, use its parent.
        # If the bundle doesn't update the config or the bundle updates the
        # config but the current change's project is not part of the tenant
        # (e.g. when dealing w/ cross-tenant cycles), use the parent layout.
        if not (
            item.change.updatesConfig(item.pipeline.tenant) or
            (
                item.bundle
                and item.bundle.updatesConfig(item.pipeline.tenant)
                and item.pipeline.tenant.getProject(
                    item.change.project.canonical_name
                )[1] is not None
            )
        ):
            return self.getFallbackLayout(item)
        # Else this item updates the config,
        # ask the merger for the result.
        build_set = item.current_build_set
        if build_set.merge_state != build_set.COMPLETE:
            return None
        if build_set.unable_to_merge:
            return self.getFallbackLayout(item)

        log.debug("Preparing dynamic layout for: %s" % item.change)
        start = time.time()
        layout = self._loadDynamicLayout(item)
        self.reportPipelineTiming('layout_generation_time', start)
        return layout

    def _branchesForRepoState(self, projects, tenant, items=None):
        items = items or []
        if all(tenant.getExcludeUnprotectedBranches(project)
               for project in projects):
            branches = set()

            # Add all protected branches of all involved projects
            for project in projects:
                branches.update(
                    tenant.getProjectBranches(project.canonical_name))

            # Additionally add all target branches of all involved items.
            branches.update(item.change.branch for item in items
                            if hasattr(item.change, 'branch'))

            # Make sure override-checkout targets are part of the repo state
            for item in items:
                if not item.current_build_set.job_graph:
                    continue

                for job in item.current_build_set.job_graph.getJobs():
                    if job.override_checkout:
                        branches.add(job.override_checkout)

                    for p in job.required_projects.values():
                        if p.override_checkout:
                            branches.add(p.override_checkout)

            branches = list(branches)
        else:
            branches = None
        return branches

    def scheduleMerge(self, item, files=None, dirs=None):
        log = item.annotateLogger(self.log)
        build_set = item.bundle_build_set
        if build_set.item is not item:
            # This is a bundle, but this isn't the bundle buildset.
            # Just say we're not ready and let the real one get
            # scheduled later.
            return False

        log.debug("Scheduling merge for item %s (files: %s, dirs: %s)" %
                  (item, files, dirs))

        # If the involved projects exclude unprotected branches we should also
        # exclude them from the merge and repo state except the branch of the
        # change that is tested.
        tenant = item.pipeline.tenant
        items = list(item.items_ahead) + [item]
        if item.bundle:
            items.extend(item.bundle.items)
        projects = {
            item.change.project for item in items
            if tenant.getProject(item.change.project.canonical_name)[1]
        }
        branches = self._branchesForRepoState(projects=projects, tenant=tenant,
                                              items=items)

        if isinstance(item.change, model.Change):
            self.sched.merger.mergeChanges(build_set.merger_items,
                                           build_set, files, dirs,
                                           precedence=self.pipeline.precedence,
                                           event=item.event,
                                           branches=branches)
        else:
            self.sched.merger.getRepoState(build_set.merger_items,
                                           build_set,
                                           precedence=self.pipeline.precedence,
                                           event=item.event,
                                           branches=branches)
        build_set.updateAttributes(self.current_context,
                                   merge_state=build_set.PENDING)
        return False

    def scheduleFilesChanges(self, item):
        log = item.annotateLogger(self.log)
        log.debug("Scheduling fileschanged for item %s", item)
        build_set = item.current_build_set

        # if base_sha is not available, fallback to branch
        to_sha = getattr(item.change, "base_sha", None)
        if to_sha is None:
            to_sha = getattr(item.change, "branch", None)

        self.sched.merger.getFilesChanges(
            item.change.project.connection_name, item.change.project.name,
            item.change.ref, to_sha, build_set=build_set,
            event=item.event)
        build_set.updateAttributes(self.current_context,
                                   files_state=build_set.PENDING)
        return False

    def scheduleGlobalRepoState(self, item: QueueItem) -> bool:
        log = item.annotateLogger(self.log)

        tenant = item.pipeline.tenant
        jobs = item.current_build_set.job_graph.getJobs()
        project_cnames = set()
        for job in jobs:
            log.debug('Processing job %s', job.name)
            project_cnames.update(job.affected_projects)
            log.debug('Needed projects: %s', project_cnames)

        # Filter projects for ones that are already in repo state
        repo_state = item.current_build_set.repo_state
        connections = self.sched.connections.connections
        for connection in repo_state.keys():
            canonical_hostname = connections[connection].canonical_hostname
            for project in repo_state[connection].keys():
                canonical_project_name = canonical_hostname + '/' + project
                project_cnames.discard(canonical_project_name)

        if not project_cnames:
            item.current_build_set.updateAttributes(
                self.current_context,
                repo_state_state=item.current_build_set.COMPLETE)
            return True

        log.info('Scheduling global repo state for item %s', item)
        # At this point we know we're going to request a merge job;
        # set the waiting state on all the item's jobs so users know
        # what we're waiting on.
        for job in jobs:
            job.setWaitingStatus('repo state')

        projects = []
        for project_cname in project_cnames:
            projects.append(tenant.getProject(project_cname)[1])

        branches = self._branchesForRepoState(
            projects=projects, tenant=tenant, items=[item])

        new_items = list()
        build_set = item.current_build_set
        # If we skipped the initial repo state (for branch/ref items),
        # we need to include the merger items for the final repo state.
        if build_set.merge_repo_state is None:
            new_items.extend(build_set.merger_items)

        for project in projects:
            new_item = dict()
            new_item['project'] = project.name
            new_item['connection'] = project.connection_name
            new_items.append(new_item)

        # Get state for not yet tracked projects
        self.sched.merger.getRepoState(items=new_items,
                                       build_set=item.current_build_set,
                                       event=item.event,
                                       branches=branches)
        item.current_build_set.updateAttributes(
            self.current_context,
            repo_state_request_time=time.time(),
            repo_state_state=item.current_build_set.PENDING)
        return True

    def prepareItem(self, item: QueueItem) -> bool:
        build_set = item.current_build_set
        tenant = item.pipeline.tenant
        # We always need to set the configuration of the item if it
        # isn't already set.
        tpc = tenant.project_configs.get(item.change.project.canonical_name)
        if not build_set.ref:
            build_set.setConfiguration(self.current_context)

        # Next, if a change ahead has a broken config, then so does
        # this one.  Record that and don't do anything else.
        if (item.item_ahead and item.item_ahead.current_build_set and
            item.item_ahead.current_build_set.has_blocking_errors):
            msg = "This change depends on a change "\
                  "with an invalid configuration.\n"
            item.setConfigError(msg)
            # Find our layout since the reporter will need it to
            # determine if the project is in the pipeline.
            self.getLayout(item)
            return False

        # The next section starts between 0 and 2 remote merger
        # operations in parallel as needed.
        ready = True
        # If the project is in this tenant, fetch missing files so we
        # know if it updates the config.
        if tpc:
            if build_set.files_state == build_set.NEW:
                ready = self.scheduleFilesChanges(item)
            if build_set.files_state == build_set.PENDING:
                ready = False
        # If this change alters config or is live, schedule merge and
        # build a layout.
        # If we are dealing w/ a bundle and the bundle updates config we also
        # have to merge since a config change in any of the bundle's items
        # applies to all items. This is, unless the current item is not part
        # of this tenant (e.g. cross-tenant cycle).
        if build_set.merge_state == build_set.NEW:
            if item.live or item.change.updatesConfig(tenant) or (
                item.bundle and
                item.bundle.updatesConfig(tenant) and tpc is not None
            ):
                # Collect extra config files and dirs of required changes.
                extra_config_files = set()
                extra_config_dirs = set()
                for merger_item in item.current_build_set.merger_items:
                    source = self.sched.connections.getSource(
                        merger_item["connection"])
                    project = source.getProject(merger_item["project"])
                    tpc = tenant.project_configs.get(project.canonical_name)
                    if tpc:
                        extra_config_files.update(tpc.extra_config_files)
                        extra_config_dirs.update(tpc.extra_config_dirs)

                ready = self.scheduleMerge(
                    item,
                    files=(['zuul.yaml', '.zuul.yaml'] +
                           list(extra_config_files)),
                    dirs=(['zuul.d', '.zuul.d'] +
                          list(extra_config_dirs)))
        if build_set.merge_state == build_set.PENDING:
            ready = False

        # If a merger op is outstanding, we're not ready.
        if not ready:
            return False

        # If the change can not be merged or has config errors, don't
        # run jobs.
        if build_set.unable_to_merge or build_set.has_blocking_errors:
            # Find our layout since the reporter will need it to
            # determine if the project is in the pipeline.
            self.getLayout(item)
            return False

        # With the merges done, we have the info needed to get a
        # layout.  This may return the pipeline layout, a layout from
        # a change ahead, a newly generated layout for this change, or
        # None if there was an error that makes the layout unusable.
        # In the last case, it will have set the config_errors on this
        # item, which may be picked up by the next item.
        if not (item.layout_uuid or item.current_build_set.job_graph):
            layout = self.getLayout(item)
            if not layout:
                return False

        # We don't need to build a job graph for a non-live item, we
        # just need the layout.
        if not item.live:
            return False

        # At this point we have a layout for the item, and it's live,
        # so freeze the job graph.
        log = item.annotateLogger(self.log)
        if not item.current_build_set.job_graph:
            try:
                log.debug("Freezing job graph for %s" % (item,))
                start = time.time()
                item.freezeJobGraph(self.getLayout(item),
                                    self.current_context,
                                    skip_file_matcher=False,
                                    redact_secrets_and_keys=False)
                self.reportPipelineTiming('job_freeze_time', start)
            except Exception as e:
                # TODOv3(jeblair): nicify this exception as it will be reported
                log.exception("Error freezing job graph for %s" % (item,))
                item.setConfigError("Unable to freeze job graph: %s" %
                                    (str(e)))
                return False
            if (item.current_build_set.job_graph and
                len(item.current_build_set.job_graph.jobs) > 0):
                self.sql.reportBuildsetStart(build_set)

        # At this point we know all frozen jobs and their repos so update the
        # repo state with all missing repos.
        if build_set.repo_state_state == build_set.NEW:
            self.scheduleGlobalRepoState(item)
        if build_set.repo_state_state == build_set.PENDING:
            return False

        while item.deduplicateJobs(log):
            # If we deduplicated a build, then we may need to apply
            # its parent data to child jobs, so keep running this
            # until we stop deduplicating builds.
            pass
        return True

    def _processOneItem(self, item, nnfi):
        log = item.annotateLogger(self.log)
        changed = False
        ready = False
        dequeued = False
        failing_reasons = []  # Reasons this item is failing

        item_ahead = item.item_ahead
        if item_ahead and (not item_ahead.live):
            item_ahead = None
        change_queue = item.queue

        if COMPONENT_REGISTRY.model_api > 3:
            # This sets a QueueItem flag which is only understood by
            # api 4.
            meets_reqs = self.isChangeReadyToBeEnqueued(
                item.change, item.event)
        else:
            meets_reqs = True
        abort, needs_changes = self.getMissingNeededChanges(
            item.change, change_queue, item.event)
        if not (meets_reqs and not needs_changes):
            # It's not okay to enqueue this change, we should remove it.
            log.info("Dequeuing change %s because "
                     "it can no longer merge" % item.change)
            self.cancelJobs(item)
            quiet_dequeue = False
            if item.isBundleFailing():
                item.setDequeuedBundleFailing('Bundle is failing')
            elif not meets_reqs:
                item.setDequeuedMissingRequirements()
            else:
                clist = ', '.join([c.url for c in needs_changes])
                if len(needs_changes) > 1:
                    msg = f'Changes {clist} are needed.'
                else:
                    msg = f'Change {clist} is needed.'
                item.setDequeuedNeedingChange(msg)
                # If all the dependencies are already in the pipeline
                # (but not ahead of this change), then we probably
                # just added updated versions of them, possibly
                # updating a cycle.  In that case, attempt to
                # re-enqueue this change with the updated deps.
                if (item.live and
                    all([self.isChangeAlreadyInPipeline(c)
                         for c in needs_changes])):
                    # Try enqueue, if that succeeds, keep this dequeue quiet
                    try:
                        log.info("Attempting re-enqueue of change %s",
                                 item.change)
                        quiet_dequeue = self.addChange(
                            item.change, item.event,
                            enqueue_time=item.enqueue_time,
                            quiet=True,
                            skip_presence_check=True)
                    except Exception:
                        log.exception("Unable to re-enqueue change %s "
                                      "which is missing dependencies",
                                      item.change)
            if item.live and not quiet_dequeue:
                try:
                    self.reportItem(item)
                except exceptions.MergeFailure:
                    pass
            self.dequeueItem(item, quiet_dequeue)
            return (True, nnfi)

        # Safety check: verify that the bundle dependency graph is correct
        dependency_graph = collections.OrderedDict()
        self.getDependencyGraph(item.change, dependency_graph, item.event)
        cycle = self.cycleForChange(
            item.change, dependency_graph, item.event, debug=False)
        if item.bundle:
            bundle_cycle = {i.change for i in item.bundle.items}
        else:
            bundle_cycle = set()
        if (item.live and
            set(cycle) != bundle_cycle and
            not item.didBundleStartReporting()):
            log.info("Item bundle has changed: %s, now: %s, was: %s", item,
                     set(cycle), bundle_cycle)
            self.removeItem(item)
            return (True, nnfi)

        actionable = change_queue.isActionable(item)
        item.updateAttributes(self.current_context, active=actionable)

        dep_items = self.getFailingDependentItems(item, nnfi)
        if dep_items:
            failing_reasons.append('a needed change is failing')
            self.cancelJobs(item, prime=False)
        else:
            item_ahead_merged = False
            if (item_ahead and
                hasattr(item_ahead.change, 'is_merged') and
                item_ahead.change.is_merged):
                item_ahead_merged = True
            if (item_ahead != nnfi and not item_ahead_merged):
                # Our current base is different than what we expected,
                # and it's not because our current base merged.  Something
                # ahead must have failed.
                log.info("Resetting builds for change %s because the "
                         "item ahead, %s, is not the nearest non-failing "
                         "item, %s" % (item.change, item_ahead, nnfi))
                change_queue.moveItem(item, nnfi)
                changed = True
                self.cancelJobs(item)
            if actionable:
                ready = self.prepareItem(item)
                # Starting jobs reporting should only be done once if there are
                # jobs to run for this item.
                if ready and len(self.pipeline.start_actions) > 0 \
                        and len(item.current_build_set.job_graph.jobs) > 0 \
                        and not item.reported_start \
                        and not item.quiet:
                    self.reportStart(item)
                    item.updateAttributes(self.current_context,
                                          reported_start=True)
                if item.current_build_set.unable_to_merge:
                    failing_reasons.append("it has a merge conflict")
                if item.current_build_set.has_blocking_errors:
                    failing_reasons.append("it has an invalid configuration")
                if ready and self.provisionNodes(item):
                    changed = True
                if ready and item.bundle and item.didBundleFinish():
                    # Since the bundle finished we need to check if any item
                    # can report. If that's the case we need to process the
                    # queue again.
                    changed = changed or any(
                        i.item_ahead is None for i in item.bundle.items)
        if ready and self.executeJobs(item):
            changed = True

        if item.hasAnyJobFailed():
            failing_reasons.append("at least one job failed")
        if (not item.live) and (not item.items_behind) and (not dequeued):
            failing_reasons.append("is a non-live item with no items behind")
            self.dequeueItem(item)
            changed = dequeued = True

        can_report = not item_ahead and item.areAllJobsComplete() and item.live
        if can_report and item.bundle:
            can_report = can_report and (
                item.isBundleFailing() or item.didBundleFinish()
            )
            # Before starting to merge the cycle items, make sure they
            # can still be merged, to reduce the chance of a partial merge.
            if can_report and not item.bundle.started_reporting:
                non_mergeable_cycle_changes = self.getNonMergeableCycleChanges(
                    item.bundle)
                if non_mergeable_cycle_changes:
                    clist = ', '.join([
                        c.url for c in non_mergeable_cycle_changes])
                    if len(non_mergeable_cycle_changes) > 1:
                        msg = f'Changes {clist} can not be merged.'
                    else:
                        msg = f'Change {clist} can not be merged.'
                    item.bundle.cannot_merge = msg
                    failing_reasons.append("cycle can not be merged")
                    log.debug(
                        "Dequeuing item %s because cycle can no longer merge",
                        item
                    )
            item.bundle.started_reporting = can_report

        if can_report:
            # If we're starting to report a successful bundle, enable
            # two-phase reporting.  Report the first phase for every item
            # in the bundle, then the second.
            phase1 = True
            phase2 = True
            if (self.changes_merge
                and item.bundle
                and (not item.cannotMergeBundle())
                and (not item.isBundleFailing())):
                for i in item.bundle.items:
                    if not i.reported:
                        self.log.debug("Report phase1 for bundle item %s", i)
                        self.reportItem(i, phase1=True, phase2=False)
                phase1 = False

            try:
                self.reportItem(item, phase1=phase1, phase2=phase2)
            except exceptions.MergeFailure:
                failing_reasons.append("it did not merge")
                for item_behind in item.items_behind:
                    log.info("Resetting builds for change %s because the "
                             "item ahead, %s, failed to merge" %
                             (item_behind.change, item))
                    self.cancelJobs(item_behind)
                # Only re-report items in the cycle when we encounter a merge
                # failure for a successful bundle.
                if (item.bundle and not (
                        item.isBundleFailing() or item.cannotMergeBundle())):
                    item.bundle.failed_reporting = True
                    self.reportProcessedBundleItems(item)
            self.dequeueItem(item)
            changed = dequeued = True
        elif not failing_reasons and item.live:
            nnfi = item
        if not dequeued:
            item.current_build_set.updateAttributes(
                self.current_context, failing_reasons=failing_reasons)
        if failing_reasons:
            log.debug("%s is a failing item because %s" %
                      (item, failing_reasons))
        if (item.live and not dequeued
                and self.sched.globals.use_relative_priority):
            priority = item.getNodePriority()
            for _, request_id in item.current_build_set.getNodeRequests():
                node_request = self.sched.nodepool.zk_nodepool.getNodeRequest(
                    request_id, cached=True)
                if not node_request:
                    continue
                if node_request.state != model.STATE_REQUESTED:
                    # If the node request was locked and accepted by a
                    # provider, we can no longer update the relative priority.
                    continue
                if node_request.relative_priority != priority:
                    self.sched.nodepool.reviseRequest(
                        node_request, priority)
        return (changed, nnfi)

    def reportProcessedBundleItems(self, item):
        """Report failure to already reported bundle items.

        In case we encounter e.g. a merge failure when we already successfully
        reported some items, we need to go back and report again.
        """
        reported_items = [i for i in item.bundle.items if i.reported]

        actions = self.pipeline.failure_actions
        for ri in reported_items:
            self.sendReport(actions, ri)
            if ri is not item:
                # Don't override the reported sql result for the item
                # that "really" failed.
                ri.setReportedResult('FAILURE')
                self.reportNormalBuildsetEnd(ri.current_build_set,
                                             'failure', final=True)

    def processQueue(self):
        # Do whatever needs to be done for each change in the queue
        self.log.debug("Starting queue processor: %s" % self.pipeline.name)
        changed = False
        change_keys = set()
        for queue in self.pipeline.queues[:]:
            queue_changed = False
            nnfi = None  # Nearest non-failing item
            for item in queue.queue[:]:
                item_changed, nnfi = self._processOneItem(
                    item, nnfi)
                if item_changed:
                    queue_changed = True
                self.reportStats(item)
                change_keys.add(item.change.cache_stat.key)
            if queue_changed:
                changed = True
                status = ''
                for item in queue.queue:
                    status += item.formatStatus()
                if status:
                    self.log.debug("Queue %s status is now:\n %s" %
                                   (queue.name, status))

        self.pipeline.change_list.setChangeKeys(
            self.pipeline.manager.current_context,
            change_keys)
        self._maintainCache()
        self.log.debug("Finished queue processor: %s (changed: %s)" %
                       (self.pipeline.name, changed))
        return changed

    def onBuildStarted(self, build):
        log = get_annotated_logger(self.log, build.zuul_event_id)
        log.debug("Build %s started", build)
        self.sql.reportBuildStart(build)
        self.reportPipelineTiming('job_wait_time',
                                  build.execute_time, build.start_time)
        if not build.build_set.item.first_job_start_time:
            # Only report this for the first job in a queue item so
            # that we don't include gate resets.
            build.build_set.item.updateAttributes(
                self.current_context,
                first_job_start_time=build.start_time)
            self.reportPipelineTiming('event_job_time',
                                      build.build_set.item.event.timestamp,
                                      build.start_time)
        return True

    def onBuildPaused(self, build):
        log = get_annotated_logger(self.log, build.zuul_event_id)
        item = build.build_set.item
        log.debug("Build %s of %s paused", build, item.change)
        for item_with_build in self._getItemsWithBuild(build):
            item_with_build.setResult(build)

        # We need to resume builds because we could either have no children
        # or have children that are already skipped.
        self._resumeBuilds(build.build_set)
        return True

    def _legacyGetJob(self, item, job):
        # TODO (model_api<21): The "this_job" indirection can be
        # removed when the circular dependency refactor is complete.
        # Until then, we can't assume that the build (and therefore
        # job) is within the current buildset (if it has been
        # deduplicated).
        try:
            this_uuid = item.current_build_set.job_graph.getUuidForJobName(
                job.name)
        except ValueError:
            # This doesn't currently raise a ValueError, it just
            # returns None, but that could easily change during
            # refactoring so let's go ahead and handle both.
            this_uuid = None
        if this_uuid is None:
            # This is the model_api < 18 case, we're going to end up
            # looking up dependencies by name anyway so the specific
            # frozen job object doesn't matter.
            return job
        return item.current_build_set.job_graph.getJobFromUuid(this_uuid)

    def _resumeBuilds(self, build_set):
        """
        Resumes all paused builds of a buildset that may be resumed.
        """
        for build in build_set.getBuilds():
            if not build.paused:
                continue
            # check if all child jobs are finished
            child_builds = []
            for item in self._getItemsWithBuild(build):
                job_graph = item.current_build_set.job_graph
                _this_job = self._legacyGetJob(item, build.job)
                child_builds += [
                    item.current_build_set.getBuild(x)
                    for x in job_graph.getDependentJobsRecursively(
                        _this_job)]
            all_completed = True
            for child_build in child_builds:
                if not child_build or not child_build.result:
                    all_completed = False
                    break

            if all_completed:
                self.sched.executor.resumeBuild(build)
                with build.activeContext(self.current_context):
                    build.paused = False
                    build.addEvent(
                        model.BuildEvent(
                            event_time=time.time(),
                            event_type=model.BuildEvent.TYPE_RESUMED))

    def _resetDependentBuilds(self, build_set, build):
        job_graph = build_set.job_graph

        _this_job = self._legacyGetJob(build_set.item, build.job)
        for job in job_graph.getDependentJobsRecursively(_this_job):
            self.sched.cancelJob(build_set, job)
            build = build_set.getBuild(job)
            if build:
                build_set.removeBuild(build)

        # Re-set build results in case we resetted builds that were skipped
        # not by this build/
        for build in build_set.getBuilds():
            if build.result:
                build_set.item.setResult(build)

    def _cancelRunningBuilds(self, build_set):
        item = build_set.item
        for job in item.getJobs():
            build = build_set.getBuild(job)
            if not build or not build.result:
                self.sched.cancelJob(build_set, job, final=True)

    def _getItemsWithBuild(self, build):
        # If the build was for deduplicated jobs, apply the results to
        # all the items that use this build.
        item = build.build_set.item
        build_in_items = [item]

        for bundle in item.findDuplicateBundles():
            for other_item in bundle.items:
                if other_item in build_in_items:
                    continue
                if build in other_item.current_build_set.getBuilds():
                    build_in_items.append(other_item)

        return build_in_items

    def onBuildCompleted(self, build):
        log = get_annotated_logger(self.log, build.zuul_event_id)
        item = build.build_set.item

        log.debug("Build %s of %s completed" % (build, item.change))

        event_queue = self.sched.pipeline_result_events[
            item.pipeline.tenant.name][item.pipeline.name]
        item.pipeline.tenant.semaphore_handler.release(
            event_queue, item, build.job)

        if item.getJob(build.job.name) is None:
            log.info("Build %s no longer in job graph for item %s",
                     build, item)
            return

        for item in self._getItemsWithBuild(build):
            # We don't care about some actions below if this build
            # isn't in the current buildset, so determine that before
            # it is potentially removed with setResult.
            if build not in item.current_build_set.getBuilds():
                current = False
            else:
                current = True
            item.setResult(build)
            log.debug("Item %s status is now:\n %s", item, item.formatStatus())

            if not current:
                continue
            build_set = item.current_build_set

            if build.retry:
                if build_set.getJobNodeSetInfo(build.job):
                    build_set.removeJobNodeSetInfo(build.job)

                # in case this was a paused build we need to retry all
                # child jobs
                self._resetDependentBuilds(build_set, build)

            self._resumeBuilds(build_set)

            if (build_set.fail_fast and
                build.failed and build.job.voting and not build.retry):
                # If fail-fast is set and the build is not successful
                # cancel all remaining jobs.
                log.debug("Build %s failed and fail-fast enabled, canceling "
                          "running builds", build)
                self._cancelRunningBuilds(build_set)

        return True

    def onFilesChangesCompleted(self, event, build_set):
        item = build_set.item
        source = self.sched.connections.getSource(
            item.change.project.connection_name)
        source.setChangeAttributes(item.change, files=event.files)
        build_set.updateAttributes(self.current_context,
                                   files_state=build_set.COMPLETE)
        if build_set.merge_state == build_set.COMPLETE:
            # We're the second of the files/merger pair, report the stat
            self.reportPipelineTiming('merge_request_time',
                                      build_set.configured_time)
        if event.elapsed_time:
            self.reportPipelineTiming('merger_files_changes_op_time',
                                      event.elapsed_time, elapsed=True)

    def onMergeCompleted(self, event, build_set):
        if build_set.merge_state == build_set.COMPLETE:
            self._onGlobalRepoStateCompleted(event, build_set)
            self.reportPipelineTiming('repo_state_time',
                                      build_set.repo_state_request_time)
            if event.elapsed_time:
                self.reportPipelineTiming('merger_repo_state_op_time',
                                          event.elapsed_time, elapsed=True)
        else:
            self._onMergeCompleted(event, build_set)
            if build_set.files_state == build_set.COMPLETE:
                # We're the second of the files/merger pair, report the stat
                self.reportPipelineTiming('merge_request_time',
                                          build_set.configured_time)
            if event.elapsed_time:
                self.reportPipelineTiming('merger_merge_op_time',
                                          event.elapsed_time, elapsed=True)

    def _onMergeCompleted(self, event, build_set):
        item = build_set.item
        log = get_annotated_logger(self.log, item.event)
        source = self.sched.connections.getSource(
            item.change.project.connection_name)
        if isinstance(item.change, model.Tag):
            source.setChangeAttributes(
                item.change, containing_branches=event.item_in_branches)
        for other_item in item.bundle_items:
            other_build_set = other_item.current_build_set
            with other_build_set.activeContext(self.current_context):
                other_build_set.setMergeRepoState(event.repo_state)
                other_build_set.merge_state = other_build_set.COMPLETE
                if event.merged:
                    other_build_set.commit = event.commit
                    other_build_set.setFiles(event.files)
                elif event.updated:
                    other_build_set.commit = (
                        item.change.newrev or
                        '0000000000000000000000000000000000000000')
            if not other_build_set.commit:
                log.info("Unable to merge change %s" % item.change)
                item.setUnableToMerge(event.errors)

    def _onGlobalRepoStateCompleted(self, event, build_set):
        item = build_set.item
        if not event.updated:
            self.log.info("Unable to get global repo state for change %s"
                          % item.change)
            item.setUnableToMerge(event.errors)
        else:
            self.log.info("Received global repo state for change %s"
                          % item.change)
            with build_set.activeContext(self.current_context):
                build_set.setExtraRepoState(event.repo_state)
                build_set.repo_state_state = build_set.COMPLETE

    def _handleNodeRequestFallback(self, log, build_set, job, old_request):
        if len(job.nodeset_alternatives) <= job.nodeset_index + 1:
            # No alternatives to fall back upon
            return False

        # Increment the nodeset index and remove the old request
        with job.activeContext(self.current_context):
            job.nodeset_index = job.nodeset_index + 1

        log.info("Re-attempting node request for job "
                 f"{job.name} of item {build_set.item} "
                 f"with nodeset alternative {job.nodeset_index}")

        build_set.removeJobNodeRequestID(job)

        # Make a new request
        if self.sched.globals.use_relative_priority:
            relative_priority = build_set.item.getNodePriority()
        else:
            relative_priority = 0
        log = build_set.item.annotateLogger(self.log)
        self._makeNodepoolRequest(log, build_set, job, relative_priority)
        return True

    def onNodesProvisioned(self, request, nodeset, build_set):
        log = get_annotated_logger(self.log, request.event_id)

        self.reportPipelineTiming('node_request_time', request.created_time)
        job = build_set.item.getJob(request._job_id)
        # First see if we need to retry the request
        if not request.fulfilled:
            log.info("Node request %s: failure for %s",
                     request, job.name)
            if self._handleNodeRequestFallback(log, build_set, job, request):
                return
        # No more fallbacks -- tell the buildset the request is complete
        if nodeset is not None:
            build_set.jobNodeRequestComplete(job, nodeset)
        # Put a fake build through the cycle to clean it up.
        if not request.fulfilled:
            build_set.item.setNodeRequestFailure(
                job, f'Node request {request.id} failed')
            self._resumeBuilds(build_set)
            pipeline = build_set.item.pipeline
            tenant = pipeline.tenant
            event_queue = self.sched.pipeline_result_events[
                tenant.name][pipeline.name]
            tenant.semaphore_handler.release(
                event_queue, build_set.item, job)

        log.info("Completed node request %s for job %s of item %s "
                 "with nodes %s",
                 request, job.name, build_set.item, request.nodes)

    def reportItem(self, item, phase1=True, phase2=True):
        log = get_annotated_logger(self.log, item.event)
        action = None

        already_reported = item.reported
        if phase2 and not phase1:
            already_reported = False
        if not already_reported:
            action, reported = self._reportItem(item, phase1, phase2)
            item.updateAttributes(self.current_context,
                                  reported=reported)
        if not phase2:
            return
        if self.changes_merge:
            succeeded = item.didAllJobsSucceed() and not item.isBundleFailing()
            merged = item.reported
            source = item.change.project.source
            if merged:
                merged = source.isMerged(item.change, item.change.branch)
            if action:
                if action == 'success' and not merged:
                    log.debug("Overriding result for %s to merge failure",
                              item.change)
                    action = 'merge-failure'
                    item.setReportedResult('MERGE_FAILURE')
                self.reportNormalBuildsetEnd(item.current_build_set,
                                             action, final=True)
            change_queue = item.queue
            if not (succeeded and merged):
                if (not item.current_build_set.job_graph or
                    not item.current_build_set.job_graph.jobs):
                    error_reason = "did not have any jobs configured"
                elif not succeeded:
                    error_reason = "failed tests"
                else:
                    error_reason = "failed to merge"
                log.info("Reported change %s did not merge because it %s, "
                         "status: all-succeeded: %s, merged: %s",
                         item.change, error_reason, succeeded, merged)
                if not succeeded:
                    change_queue.decreaseWindowSize()
                    log.debug("%s window size decreased to %s",
                              change_queue, change_queue.window)
                raise exceptions.MergeFailure(
                    "Change %s failed to merge" % item.change)
            else:
                self.reportNormalBuildsetEnd(item.current_build_set,
                                             action, final=True)
                log.info("Reported change %s status: all-succeeded: %s, "
                         "merged: %s", item.change, succeeded, merged)
                change_queue.increaseWindowSize()
                log.debug("%s window size increased to %s",
                          change_queue, change_queue.window)

                zuul_driver = self.sched.connections.drivers['zuul']
                tenant = self.pipeline.tenant
                with trace.use_span(tracing.restoreSpan(item.span_info)):
                    zuul_driver.onChangeMerged(tenant, item.change, source)
        elif action:
            self.reportNormalBuildsetEnd(item.current_build_set,
                                         action, final=True)

    def _reportItem(self, item, phase1, phase2):
        log = get_annotated_logger(self.log, item.event)
        log.debug("Reporting phase1: %s phase2: %s change: %s",
                  phase1, phase2, item.change)
        ret = True  # Means error as returned by trigger.report

        # In the case of failure, we may not have completed an initial
        # merge which would get the layout for this item, so in order
        # to determine whether this item's project is in this
        # pipeline, use the dynamic layout if available, otherwise,
        # fall back to the current static layout as a best
        # approximation.  However, if we ran jobs, then we obviously
        # were in the pipeline config.
        project_in_pipeline = bool(item.getJobs())

        if not project_in_pipeline:
            layout = None
            if item.layout_uuid:
                layout = self.getLayout(item)
            if not layout:
                layout = self.pipeline.tenant.layout

            try:
                project_in_pipeline = bool(
                    layout.getProjectPipelineConfig(item))
            except Exception:
                log.exception("Invalid config for change %s", item.change)
        if not project_in_pipeline:
            log.debug("Project %s not in pipeline %s for change %s",
                      item.change.project, self.pipeline, item.change)
            project_in_pipeline = False
            action = 'no-jobs'
            actions = self.pipeline.no_jobs_actions
            item.setReportedResult('NO_JOBS')
        elif item.current_build_set.has_blocking_errors:
            log.debug("Invalid config for change %s", item.change)
            action = 'config-error'
            actions = self.pipeline.config_error_actions
            item.setReportedResult('CONFIG_ERROR')
        elif item.didMergerFail():
            log.debug("Merge conflict")
            action = 'merge-conflict'
            actions = self.pipeline.merge_conflict_actions
            item.setReportedResult('MERGE_CONFLICT')
        elif item.wasDequeuedNeedingChange():
            log.debug("Dequeued needing change")
            action = 'failure'
            actions = self.pipeline.failure_actions
            item.setReportedResult('FAILURE')
        elif item.wasDequeuedMissingRequirements():
            log.debug("Dequeued missing merge requirements")
            action = 'failure'
            actions = self.pipeline.failure_actions
            item.setReportedResult('FAILURE')
        elif not item.getJobs():
            # We don't send empty reports with +1
            log.debug("No jobs for change %s", item.change)
            action = 'no-jobs'
            actions = self.pipeline.no_jobs_actions
            item.setReportedResult('NO_JOBS')
        elif item.cannotMergeBundle():
            log.debug("Bundle can not be merged")
            action = 'failure'
            actions = self.pipeline.failure_actions
            item.setReportedResult("FAILURE")
        elif item.isBundleFailing():
            log.debug("Bundle is failing")
            action = 'failure'
            actions = self.pipeline.failure_actions
            item.setReportedResult("FAILURE")
            if not item.didAllJobsSucceed():
                with self.pipeline.state.activeContext(self.current_context):
                    self.pipeline.state.consecutive_failures += 1
        elif item.didAllJobsSucceed() and not item.isBundleFailing():
            log.debug("success %s", self.pipeline.success_actions)
            action = 'success'
            actions = self.pipeline.success_actions
            item.setReportedResult('SUCCESS')
            with self.pipeline.state.activeContext(self.current_context):
                self.pipeline.state.consecutive_failures = 0
        else:
            action = 'failure'
            actions = self.pipeline.failure_actions
            item.setReportedResult('FAILURE')
            with self.pipeline.state.activeContext(self.current_context):
                self.pipeline.state.consecutive_failures += 1
        if project_in_pipeline and self.pipeline.state.disabled:
            actions = self.pipeline.disabled_actions
        # Check here if we should disable so that we only use the disabled
        # reporters /after/ the last disable_at failure is still reported as
        # normal.
        if (self.pipeline.disable_at and not self.pipeline.state.disabled and
            self.pipeline.state.consecutive_failures
                >= self.pipeline.disable_at):
            self.pipeline.state.updateAttributes(
                self.current_context, disabled=True)
        if actions:
            log.info("Reporting item %s, actions: %s", item, actions)
            ret = self.sendReport(actions, item, phase1, phase2)
            if ret:
                log.error("Reporting item %s received: %s", item, ret)
        return action, (not ret)

    def reportStats(self, item, trigger_event=None):
        if not self.sched.statsd:
            return
        try:
            # Update the gauge on enqueue and dequeue, but timers only
            # when dequeing.
            if item.dequeue_time:
                dt = (item.dequeue_time - item.enqueue_time) * 1000
            else:
                dt = None
            items = len(self.pipeline.getAllItems())

            tenant = self.pipeline.tenant
            basekey = 'zuul.tenant.%s' % tenant.name
            key = '%s.pipeline.%s' % (basekey, self.pipeline.name)
            # stats.timers.zuul.tenant.<tenant>.pipeline.<pipeline>.resident_time
            # stats_counts.zuul.tenant.<tenant>.pipeline.<pipeline>.total_changes
            # stats.gauges.zuul.tenant.<tenant>.pipeline.<pipeline>.current_changes
            # stats.gauges.zuul.tenant.<tenant>.pipeline.<pipeline>.window
            self.sched.statsd.gauge(key + '.current_changes', items)
            self.sched.statsd.gauge(key + '.window', item.pipeline.window)
            if dt:
                self.sched.statsd.timing(key + '.resident_time', dt)
                self.sched.statsd.incr(key + '.total_changes')
            if item.queue and item.queue.name:
                queuename = (item.queue.name.
                             replace('.', '_').replace('/', '.'))
                # stats.gauges.zuul.tenant.<tenant>.pipeline.<pipeline>.queue.<queue>.resident_time
                # stats.gauges.zuul.tenant.<tenant>.pipeline.<pipeline>.queue.<queue>.total_changes
                # stats.gauges.zuul.tenant.<tenant>.pipeline.<pipeline>.queue.<queue>.current_changes
                # stats.gauges.zuul.tenant.<tenant>.pipeline.<pipeline>.queue.<queue>.window
                queuekey = '%s.queue.%s' % (key, queuename)
                self.sched.statsd.gauge(queuekey + '.current_changes',
                                        len(item.queue.queue))
                self.sched.statsd.gauge(queuekey + '.window',
                                        item.queue.window)
                if dt:
                    self.sched.statsd.timing(queuekey + '.resident_time', dt)
                    self.sched.statsd.incr(queuekey + '.total_changes')
            if hasattr(item.change, 'branch'):
                hostname = (item.change.project.canonical_hostname.
                            replace('.', '_'))
                projectname = (item.change.project.name.
                               replace('.', '_').replace('/', '.'))
                projectname = projectname.replace('.', '_').replace('/', '.')
                branchname = item.change.branch.replace('.', '_').replace(
                    '/', '.')
                # stats.timers.zuul.tenant.<tenant>.pipeline.<pipeline>.
                #   project.<host>.<project>.<branch>.resident_time
                # stats_counts.zuul.tenant.<tenant>.pipeline.<pipeline>.
                #   project.<host>.<project>.<branch>.total_changes
                key += '.project.%s.%s.%s' % (hostname, projectname,
                                              branchname)
                if dt:
                    self.sched.statsd.timing(key + '.resident_time', dt)
                    self.sched.statsd.incr(key + '.total_changes')
            if (
                trigger_event
                and hasattr(trigger_event, 'arrived_at_scheduler_timestamp')
            ):
                now = time.time()
                arrived = trigger_event.arrived_at_scheduler_timestamp
                processing = (now - arrived) * 1000
                elapsed = (now - trigger_event.timestamp) * 1000
                self.sched.statsd.timing(
                    basekey + '.event_enqueue_processing_time',
                    processing)
                self.sched.statsd.timing(
                    basekey + '.event_enqueue_time', elapsed)
                self.reportPipelineTiming('event_enqueue_time',
                                          trigger_event.timestamp)
        except Exception:
            self.log.exception("Exception reporting pipeline stats")

    def reportPipelineTiming(self, key, start, end=None, elapsed=False):
        if not self.sched.statsd:
            return
        if not start:
            return
        if end is None:
            end = time.time()
        pipeline = self.pipeline
        tenant = pipeline.tenant
        stats_key = f'zuul.tenant.{tenant.name}.pipeline.{pipeline.name}'
        if elapsed:
            dt = start
        else:
            dt = (end - start) * 1000
        self.sched.statsd.timing(f'{stats_key}.{key}', dt)
