# Copyright 2022 Acme Gating, LLC
#
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

import json

from zuul import change_matcher
from zuul import model
from zuul.lib.re2util import ZuulRegex
from zuul.zk.components import ComponentRegistry

from tests.base import (
    AnsibleZuulTestCase,
    ZuulTestCase,
    simple_layout,
    iterate_timeout,
)
from tests.base import ZuulWebFixture


def model_version(version):
    """Specify a model version for a model upgrade test

    This creates a dummy scheduler component with the specified model
    API version.  The component is created before any other, so it
    will appear to Zuul that it is joining an existing cluster with
    data at the old version.
    """

    def decorator(test):
        test.__model_version__ = version
        return test
    return decorator


class TestModelUpgrade(ZuulTestCase):
    tenant_config_file = "config/single-tenant/main-model-upgrade.yaml"
    scheduler_count = 1

    def getJobData(self, tenant, pipeline):
        item_path = f'/zuul/tenant/{tenant}/pipeline/{pipeline}/item'
        count = 0
        for item in self.zk_client.client.get_children(item_path):
            bs_path = f'{item_path}/{item}/buildset'
            for buildset in self.zk_client.client.get_children(bs_path):
                data = json.loads(self.getZKObject(
                    f'{bs_path}/{buildset}/job/check-job'))
                count += 1
                yield data
        if not count:
            raise Exception("No job data found")

    @model_version(0)
    @simple_layout('layouts/simple.yaml')
    def test_model_upgrade_0_1(self):
        component_registry = ComponentRegistry(self.zk_client)
        self.assertEqual(component_registry.model_api, 0)

        # Upgrade our component
        self.model_test_component_info.model_api = 1

        for _ in iterate_timeout(30, "model api to update"):
            if component_registry.model_api == 1:
                break

    @model_version(2)
    @simple_layout('layouts/pipeline-supercedes.yaml')
    def test_supercedes(self):
        """
        Test that pipeline supsercedes still work with model API 2,
        which uses deqeueue events.
        """
        self.executor_server.hold_jobs_in_build = True

        A = self.fake_gerrit.addFakeChange('org/project', 'master', 'A')
        self.fake_gerrit.addEvent(A.getPatchsetCreatedEvent(1))
        self.waitUntilSettled()

        self.assertEqual(len(self.builds), 1)
        self.assertEqual(self.builds[0].name, 'test-job')

        A.addApproval('Code-Review', 2)
        self.fake_gerrit.addEvent(A.addApproval('Approved', 1))
        self.waitUntilSettled()

        self.assertEqual(len(self.builds), 1)
        self.assertEqual(self.builds[0].name, 'test-job')
        self.assertEqual(self.builds[0].pipeline, 'gate')

        self.executor_server.hold_jobs_in_build = False
        self.executor_server.release()
        self.waitUntilSettled()

        self.assertEqual(len(self.builds), 0)
        self.assertEqual(A.reported, 2)
        self.assertEqual(A.data['status'], 'MERGED')
        self.assertHistory([
            dict(name='test-job', result='ABORTED', changes='1,1'),
            dict(name='test-job', result='SUCCESS', changes='1,1'),
        ], ordered=False)

    @model_version(4)
    def test_model_4(self):
        # Test that Zuul return values are correctly passed to child
        # jobs in version 4 compatibility mode.
        A = self.fake_gerrit.addFakeChange('org/project3', 'master', 'A')
        fake_data = [
            {'name': 'image',
             'url': 'http://example.com/image',
             'metadata': {
                 'type': 'container_image'
             }},
        ]
        self.executor_server.returnData(
            'project-merge', A,
            {'zuul': {'artifacts': fake_data}}
        )
        self.fake_gerrit.addEvent(A.getPatchsetCreatedEvent(1))
        self.waitUntilSettled()

        self.assertHistory([
            dict(name='project-merge', result='SUCCESS', changes='1,1'),
            dict(name='project-test1', result='SUCCESS', changes='1,1'),
            dict(name='project-test2', result='SUCCESS', changes='1,1'),
            dict(name='project1-project2-integration',
                 result='SUCCESS', changes='1,1'),
        ], ordered=False)
        # Verify that the child jobs got the data from the parent
        test1 = self.getJobFromHistory('project-test1')
        self.assertEqual(fake_data[0]['url'],
                         test1.parameters['zuul']['artifacts'][0]['url'])
        integration = self.getJobFromHistory('project1-project2-integration')
        self.assertEqual(fake_data[0]['url'],
                         integration.parameters['zuul']['artifacts'][0]['url'])

    @model_version(4)
    def test_model_4_5(self):
        # Changes share a queue, but with only one job, the first
        # merges before the second starts.
        self.executor_server.hold_jobs_in_build = True
        A = self.fake_gerrit.addFakeChange('org/project1', 'master', 'A')
        fake_data = [
            {'name': 'image',
             'url': 'http://example.com/image',
             'metadata': {
                 'type': 'container_image'
             }},
        ]
        self.executor_server.returnData(
            'project-merge', A,
            {'zuul': {'artifacts': fake_data}}
        )
        self.fake_gerrit.addEvent(A.getPatchsetCreatedEvent(1))
        self.waitUntilSettled()

        self.assertEqual(len(self.builds), 1)

        # Upgrade our component
        self.model_test_component_info.model_api = 5

        self.executor_server.hold_jobs_in_build = False
        self.executor_server.release()
        self.waitUntilSettled()

        self.assertHistory([
            dict(name='project-merge', result='SUCCESS', changes='1,1'),
            dict(name='project-test1', result='SUCCESS', changes='1,1'),
            dict(name='project-test2', result='SUCCESS', changes='1,1'),
            dict(name='project1-project2-integration',
                 result='SUCCESS', changes='1,1'),
        ], ordered=False)
        # Verify that the child job got the data from the parent
        test1 = self.getJobFromHistory('project-test1')
        self.assertEqual(fake_data[0]['url'],
                         test1.parameters['zuul']['artifacts'][0]['url'])

    @model_version(5)
    def test_model_5_6(self):
        # This exercises the min_ltimes=None case in configloader on
        # layout updates.
        first = self.scheds.first
        second = self.createScheduler()
        second.start()
        self.assertEqual(len(self.scheds), 2)
        for _ in iterate_timeout(10, "until priming is complete"):
            state_one = first.sched.local_layout_state.get("tenant-one")
            if state_one:
                break

        for _ in iterate_timeout(
                10, "all schedulers to have the same layout state"):
            if (second.sched.local_layout_state.get(
                    "tenant-one") == state_one):
                break

        with second.sched.layout_update_lock, second.sched.run_handler_lock:
            file_dict = {'zuul.d/test.yaml': ''}
            A = self.fake_gerrit.addFakeChange('org/project1', 'master', 'A',
                                               files=file_dict)
            A.setMerged()
            self.fake_gerrit.addEvent(A.getChangeMergedEvent())
            self.waitUntilSettled(matcher=[first])

            # Delete the layout data to simulate the first scheduler
            # being on model api 5 (we write the data regardless of
            # the cluster version since it's a new znode).
            self.scheds.first.sched.zk_client.client.delete(
                '/zuul/layout-data', recursive=True)
        self.waitUntilSettled()
        self.assertEqual(first.sched.local_layout_state.get("tenant-one"),
                         second.sched.local_layout_state.get("tenant-one"))

    # No test for model version 7 (secrets in blob store): old and new
    # code paths are exercised in existing tests since small secrets
    # don't use the blob store.

    @model_version(8)
    def test_model_8_9(self):
        # This excercises the upgrade to nodeset_alternates
        first = self.scheds.first
        second = self.createScheduler()
        second.start()
        self.assertEqual(len(self.scheds), 2)
        for _ in iterate_timeout(10, "until priming is complete"):
            state_one = first.sched.local_layout_state.get("tenant-one")
            if state_one:
                break

        for _ in iterate_timeout(
                10, "all schedulers to have the same layout state"):
            if (second.sched.local_layout_state.get(
                    "tenant-one") == state_one):
                break

        self.fake_nodepool.pause()
        with second.sched.layout_update_lock, second.sched.run_handler_lock:
            A = self.fake_gerrit.addFakeChange('org/project1', 'master', 'A')
            self.fake_gerrit.addEvent(A.getPatchsetCreatedEvent(1))
            self.waitUntilSettled(matcher=[first])

        self.model_test_component_info.model_api = 9
        with first.sched.layout_update_lock, first.sched.run_handler_lock:
            self.fake_nodepool.unpause()
            self.waitUntilSettled(matcher=[second])

        self.waitUntilSettled()
        self.assertHistory([
            dict(name='project-merge', result='SUCCESS', changes='1,1'),
            dict(name='project-test1', result='SUCCESS', changes='1,1'),
            dict(name='project-test2', result='SUCCESS', changes='1,1'),
            dict(name='project1-project2-integration',
                 result='SUCCESS', changes='1,1'),
        ], ordered=False)

    @model_version(11)
    def test_model_11_12(self):
        # This excercises the upgrade to store build/job versions
        first = self.scheds.first
        second = self.createScheduler()
        second.start()
        self.assertEqual(len(self.scheds), 2)
        for _ in iterate_timeout(10, "until priming is complete"):
            state_one = first.sched.local_layout_state.get("tenant-one")
            if state_one:
                break

        for _ in iterate_timeout(
                10, "all schedulers to have the same layout state"):
            if (second.sched.local_layout_state.get(
                    "tenant-one") == state_one):
                break

        self.executor_server.hold_jobs_in_build = True
        with second.sched.layout_update_lock, second.sched.run_handler_lock:
            A = self.fake_gerrit.addFakeChange('org/project1', 'master', 'A')
            self.fake_gerrit.addEvent(A.getPatchsetCreatedEvent(1))
            self.waitUntilSettled(matcher=[first])

        self.model_test_component_info.model_api = 12
        with first.sched.layout_update_lock, first.sched.run_handler_lock:
            self.executor_server.hold_jobs_in_build = False
            self.executor_server.release()
            self.waitUntilSettled(matcher=[second])

        self.waitUntilSettled()
        self.assertHistory([
            dict(name='project-merge', result='SUCCESS', changes='1,1'),
            dict(name='project-test1', result='SUCCESS', changes='1,1'),
            dict(name='project-test2', result='SUCCESS', changes='1,1'),
            dict(name='project1-project2-integration',
                 result='SUCCESS', changes='1,1'),
        ], ordered=False)

    @model_version(12)
    def test_model_12_13(self):
        # Initially queue items will still have the full trigger event
        # stored in Zookeeper. The trigger event will be converted to
        # an event info object after the model API update.
        self.executor_server.hold_jobs_in_build = True
        A = self.fake_gerrit.addFakeChange('org/project1', 'master', 'A')
        self.fake_gerrit.addEvent(A.getPatchsetCreatedEvent(1))
        self.waitUntilSettled()

        self.assertEqual(len(self.builds), 1)

        # Upgrade our component
        self.model_test_component_info.model_api = 13

        self.executor_server.hold_jobs_in_build = False
        self.executor_server.release()
        self.waitUntilSettled()

        self.assertHistory([
            dict(name='project-merge', result='SUCCESS', changes='1,1'),
            dict(name='project-test1', result='SUCCESS', changes='1,1'),
            dict(name='project-test2', result='SUCCESS', changes='1,1'),
            dict(name='project1-project2-integration',
                 result='SUCCESS', changes='1,1'),
        ], ordered=False)

    @model_version(16)
    def test_model_16_17(self):
        matcher = change_matcher.BranchMatcher(ZuulRegex('foo'))
        ser = matcher.serialize()
        self.assertEqual(ser, {'regex': 'foo', 'implied': False})
        matcher2 = change_matcher.BranchMatcher.deserialize(ser)
        self.assertEqual(matcher, matcher2)

        # Upgrade our component
        self.model_test_component_info.model_api = 17
        component_registry = ComponentRegistry(self.zk_client)
        for _ in iterate_timeout(30, "model api to update"):
            if component_registry.model_api == 17:
                break

        matcher = change_matcher.BranchMatcher(ZuulRegex('foo'))
        ser = matcher.serialize()
        self.assertEqual(ser, {
            'regex': {
                'negate': False,
                'pattern': 'foo',
            },
            'implied': False
        })
        matcher2 = change_matcher.BranchMatcher.deserialize(ser)
        self.assertEqual(matcher, matcher2)

    @model_version(18)
    def test_model_18(self):
        # Test backward compatibility with old name-based job storage
        # when not all components have updated yet.
        A = self.fake_gerrit.addFakeChange('org/project1', 'master', 'A')
        self.fake_gerrit.addEvent(A.getPatchsetCreatedEvent(1))
        self.waitUntilSettled()

        self.assertHistory([
            dict(name='project-merge', result='SUCCESS', changes='1,1'),
            dict(name='project-test1', result='SUCCESS', changes='1,1'),
            dict(name='project-test2', result='SUCCESS', changes='1,1'),
            dict(name='project1-project2-integration',
                 result='SUCCESS', changes='1,1'),
        ], ordered=False)

    @model_version(18)
    def test_model_18_19(self):
        # Test backward compatibility with existing job graphs that
        # still use the name-based job storage.
        self.executor_server.hold_jobs_in_build = True
        A = self.fake_gerrit.addFakeChange('org/project1', 'master', 'A')
        self.fake_gerrit.addEvent(A.getPatchsetCreatedEvent(1))
        self.waitUntilSettled()

        self.assertEqual(len(self.builds), 1)

        # Upgrade our component
        self.model_test_component_info.model_api = 19
        component_registry = ComponentRegistry(self.zk_client)
        for _ in iterate_timeout(30, "model api to update"):
            if component_registry.model_api == 19:
                break

        self.executor_server.hold_jobs_in_build = False
        self.executor_server.release()
        self.waitUntilSettled()

        self.assertHistory([
            dict(name='project-merge', result='SUCCESS', changes='1,1'),
            dict(name='project-test1', result='SUCCESS', changes='1,1'),
            dict(name='project-test2', result='SUCCESS', changes='1,1'),
            dict(name='project1-project2-integration',
                 result='SUCCESS', changes='1,1'),
        ], ordered=False)

    @model_version(20)
    def test_model_20_21(self):
        # Test backwards compat for job graph dependency freezing.
        # Note that these jobs have a dependency on project-merge.
        # First test the entire lifecycle under the old api.
        A = self.fake_gerrit.addFakeChange('org/project1', 'master', 'A')
        self.fake_gerrit.addEvent(A.getPatchsetCreatedEvent(1))
        self.waitUntilSettled()

        self.assertHistory([
            dict(name='project-merge', result='SUCCESS', changes='1,1'),
            dict(name='project-test1', result='SUCCESS', changes='1,1'),
            dict(name='project-test2', result='SUCCESS', changes='1,1'),
            dict(name='project1-project2-integration',
                 result='SUCCESS', changes='1,1'),
        ], ordered=False)

        # Then repeat the test with a mid-cycle upgrade.
        self.executor_server.hold_jobs_in_build = True
        B = self.fake_gerrit.addFakeChange('org/project1', 'master', 'B')
        self.fake_gerrit.addEvent(B.getPatchsetCreatedEvent(1))
        self.waitUntilSettled()

        self.assertEqual(len(self.builds), 1)

        # Upgrade our component
        self.model_test_component_info.model_api = 21
        component_registry = ComponentRegistry(self.zk_client)
        for _ in iterate_timeout(30, "model api to update"):
            if component_registry.model_api == 21:
                break

        self.executor_server.hold_jobs_in_build = False
        self.executor_server.release()
        self.waitUntilSettled()

        self.assertHistory([
            dict(name='project-merge', result='SUCCESS', changes='1,1'),
            dict(name='project-test1', result='SUCCESS', changes='1,1'),
            dict(name='project-test2', result='SUCCESS', changes='1,1'),
            dict(name='project1-project2-integration',
                 result='SUCCESS', changes='1,1'),
            dict(name='project-merge', result='SUCCESS', changes='2,1'),
            dict(name='project-test1', result='SUCCESS', changes='2,1'),
            dict(name='project-test2', result='SUCCESS', changes='2,1'),
            dict(name='project1-project2-integration',
                 result='SUCCESS', changes='2,1'),
        ], ordered=False)

    @model_version(20)
    @simple_layout('layouts/soft-dependencies.yaml')
    def test_20_soft_dependencies(self):
        A = self.fake_gerrit.addFakeChange('org/project', 'master', 'A')
        self.fake_gerrit.addEvent(A.getPatchsetCreatedEvent(1))
        self.waitUntilSettled()
        self.assertHistory([
            dict(name='deploy', result='SUCCESS', changes='1,1'),
        ], ordered=False)


class TestGithubModelUpgrade(ZuulTestCase):
    config_file = 'zuul-github-driver.conf'
    scheduler_count = 1

    @model_version(3)
    @simple_layout('layouts/gate-github.yaml', driver='github')
    def test_status_checks_removal(self):
        # This tests the old behavior -- that changes are not dequeued
        # once their required status checks are removed -- since the
        # new behavior requires a flag in ZK.
        # Contrast with test_status_checks_removal.
        github = self.fake_github.getGithubClient()
        repo = github.repo_from_project('org/project')
        repo._set_branch_protection(
            'master', contexts=['something/check', 'tenant-one/gate'])

        A = self.fake_github.openFakePullRequest('org/project', 'master', 'A')
        self.fake_github.emitEvent(A.getPullRequestOpenedEvent())
        self.waitUntilSettled()

        self.executor_server.hold_jobs_in_build = True
        # Since the required status 'something/check' is not fulfilled,
        # no job is expected
        self.assertEqual(0, len(self.history))

        # Set the required status 'something/check'
        repo.create_status(A.head_sha, 'success', 'example.com', 'description',
                           'something/check')

        self.fake_github.emitEvent(A.getPullRequestOpenedEvent())
        self.waitUntilSettled()

        # Remove it and verify the change is not dequeued (old behavior).
        repo.create_status(A.head_sha, 'failed', 'example.com', 'description',
                           'something/check')
        self.fake_github.emitEvent(A.getCommitStatusEvent('something/check',
                                                          state='failed',
                                                          user='foo'))
        self.waitUntilSettled()

        self.executor_server.hold_jobs_in_build = False
        self.executor_server.release()
        self.waitUntilSettled()

        # the change should have entered the gate
        self.assertHistory([
            dict(name='project-test1', result='SUCCESS'),
            dict(name='project-test2', result='SUCCESS'),
        ], ordered=False)
        self.assertTrue(A.is_merged)

    @model_version(10)
    @simple_layout('layouts/github-merge-mode.yaml', driver='github')
    def test_merge_method_syntax_check(self):
        """
        Tests that the merge mode gets forwarded to the reporter and the
        PR was rebased.
        """
        webfixture = self.useFixture(
            ZuulWebFixture(self.changes, self.config,
                           self.additional_event_queues, self.upstream_root,
                           self.poller_events,
                           self.git_url_with_auth, self.addCleanup,
                           self.test_root))
        sched = self.scheds.first.sched
        web = webfixture.web

        github = self.fake_github.getGithubClient()
        repo = github.repo_from_project('org/project')
        repo._repodata['allow_rebase_merge'] = False
        self.scheds.execute(lambda app: app.sched.reconfigure(app.config))
        self.waitUntilSettled()

        # Verify that there are no errors with model version 9 (we
        # should be using the defaultdict that indicates all merge
        # modes are supported).
        tenant = sched.abide.tenants.get('tenant-one')
        self.assertEquals(len(tenant.layout.loading_errors), 0)

        # Upgrade our component
        self.model_test_component_info.model_api = 11

        # Perform a smart reconfiguration which should not clear the
        # cache; we should continue to see no errors because we should
        # still be using the defaultdict.
        self.scheds.first.smartReconfigure()
        tenant = sched.abide.tenants.get('tenant-one')
        self.assertEquals(len(tenant.layout.loading_errors), 0)

        # Wait for web to have the same config
        for _ in iterate_timeout(10, "config is synced"):
            if (web.tenant_layout_state.get('tenant-one') ==
                web.local_layout_state.get('tenant-one')):
                break

        # Repeat the check
        tenant = web.abide.tenants.get('tenant-one')
        self.assertEquals(len(tenant.layout.loading_errors), 0)

        # Perform a full reconfiguration which should cause us to
        # actually query, update the branch cache, and report an
        # error.
        self.scheds.first.fullReconfigure()
        self.waitUntilSettled()

        tenant = sched.abide.tenants.get('tenant-one')
        loading_errors = tenant.layout.loading_errors
        self.assertEquals(
            len(tenant.layout.loading_errors), 1,
            "An error should have been stored in sched")
        self.assertIn(
            "rebase not supported",
            str(loading_errors[0].error))

        # Wait for web to have the same config
        for _ in iterate_timeout(10, "config is synced"):
            if (web.tenant_layout_state.get('tenant-one') ==
                web.local_layout_state.get('tenant-one')):
                break

        # Repoat the check for web
        tenant = web.abide.tenants.get('tenant-one')
        loading_errors = tenant.layout.loading_errors
        self.assertEquals(
            len(tenant.layout.loading_errors), 1,
            "An error should have been stored in web")
        self.assertIn(
            "rebase not supported",
            str(loading_errors[0].error))

    @model_version(17)
    @simple_layout('layouts/github-merge-mode.yaml', driver='github')
    def test_default_merge_mode(self):
        tenant = self.scheds.first.sched.abide.tenants.get('tenant-one')
        md = tenant.layout.getProjectMetadata('github.com/org/project1')
        self.assertEqual(model.MERGER_MERGE, md.merge_mode)

        tpc = tenant.project_configs['github.com/org/project1']
        # Force a re-fetch of the project branches, which also updates
        # the supported merge modes.
        gh = tpc.project.source.connection
        gh.updateProjectBranches(tpc.project)
        merge_modes = tpc.project.source.getProjectMergeModes(
            tpc.project, tenant)
        # Branch cache shouldn't contain new merge modes for model API < 18
        self.assertEqual([1, 2, 4, 5], merge_modes)

        # Upgrade our component
        self.model_test_component_info.model_api = 18

        component_registry = ComponentRegistry(self.zk_client)
        for _ in iterate_timeout(30, "model api to update"):
            if component_registry.model_api == 18:
                break

        merge_modes = tpc.project.source.getProjectMergeModes(
            tpc.project, tenant)
        # Branch cache still contains only the old merge modes
        self.assertEqual([1, 2, 4, 5], merge_modes)

        # Test that we can still process changes with the project branch
        # cache not containing the new default merge mode.
        A = self.fake_github.openFakePullRequest('org/project1', 'master', 'A',
                                                 files={"zuul.yaml": ""})
        self.fake_github.emitEvent(A.getPullRequestOpenedEvent())
        self.waitUntilSettled()
        self.assertEqual(len(self.history), 1)

        # Re-fetch the project branches once more.
        gh.updateProjectBranches(tpc.project)
        merge_modes = tpc.project.source.getProjectMergeModes(
            tpc.project, tenant)

        # The cache should now contain the new merge modes, but not the TPC.
        self.assertEqual([1, 2, 6, 7, 4, 5], merge_modes)
        self.assertEqual([1, 2, 4, 5], tpc.merge_modes)

        # Test that we can still process changes with the TPC not using the
        # new supported merge modes.
        self.fake_github.emitEvent(A.getPullRequestOpenedEvent())
        self.waitUntilSettled()
        self.assertEqual(len(self.history), 2)

        # Perform a full reconfiguration which should cause us to
        # re-fetch the merge modes.
        self.scheds.first.fullReconfigure()
        self.waitUntilSettled()

        # Now the TPC should also contain the new merge modes.
        tenant = self.scheds.first.sched.abide.tenants.get('tenant-one')
        tpc = tenant.project_configs['github.com/org/project1']
        self.assertEqual([1, 2, 6, 7, 4, 5], tpc.merge_modes)

        layout = self.scheds.first.sched.abide.tenants.get('tenant-one').layout
        md = layout.getProjectMetadata('github.com/org/project1')
        self.assertEqual(model.MERGER_MERGE_ORT, md.merge_mode)


class TestDefaultBranchUpgrade(ZuulTestCase):
    config_file = "zuul-gerrit-github.conf"
    scheduler_count = 1

    @model_version(15)
    @simple_layout('layouts/default-branch.yaml', driver='github')
    def test_default_branch(self):
        self.waitUntilSettled()

        github = self.fake_github.getGithubClient()
        repo = github.repo_from_project('org/project-default')
        repo._repodata['default_branch'] = 'foobar'
        self.scheds.execute(lambda app: app.sched.reconfigure(app.config))
        self.waitUntilSettled()

        # Verify we use the default from the defaultdict.
        layout = self.scheds.first.sched.abide.tenants.get('tenant-one').layout
        md = layout.getProjectMetadata(
            'github.com/org/project-default')
        self.assertEqual('master', md.default_branch)

        # Upgrade our component
        self.model_test_component_info.model_api = 16

        # Perform a smart reconfiguration which should not clear the
        # cache; we should continue to see no change because we should
        # still be using the defaultdict.
        self.scheds.first.smartReconfigure()
        layout = self.scheds.first.sched.abide.tenants.get('tenant-one').layout
        md = layout.getProjectMetadata(
            'github.com/org/project-default')
        self.assertEqual('master', md.default_branch)

        # Perform a full reconfiguration which should cause us to
        # actually query and update the branch cache.
        self.scheds.first.fullReconfigure()
        self.waitUntilSettled()

        layout = self.scheds.first.sched.abide.tenants.get('tenant-one').layout
        md = layout.getProjectMetadata(
            'github.com/org/project-default')
        self.assertEqual('foobar', md.default_branch)


class TestDeduplication(ZuulTestCase):
    config_file = "zuul-gerrit-github.conf"
    tenant_config_file = "config/circular-dependencies/main.yaml"
    scheduler_count = 1

    def _test_job_deduplication(self):
        A = self.fake_gerrit.addFakeChange('org/project1', 'master', 'A')
        B = self.fake_gerrit.addFakeChange('org/project2', 'master', 'B')

        # A <-> B
        A.data["commitMessage"] = "{}\n\nDepends-On: {}\n".format(
            A.subject, B.data["url"]
        )
        B.data["commitMessage"] = "{}\n\nDepends-On: {}\n".format(
            B.subject, A.data["url"]
        )

        A.addApproval('Code-Review', 2)
        B.addApproval('Code-Review', 2)

        self.fake_gerrit.addEvent(A.addApproval('Approved', 1))
        self.fake_gerrit.addEvent(B.addApproval('Approved', 1))

        self.waitUntilSettled()

        self.assertEqual(A.data['status'], 'MERGED')
        self.assertEqual(B.data['status'], 'MERGED')

    @simple_layout('layouts/job-dedup-auto-shared.yaml')
    @model_version(7)
    def test_job_deduplication_auto_shared(self):
        self._test_job_deduplication()
        self.assertHistory([
            dict(name="project1-job", result="SUCCESS", changes="2,1 1,1"),
            dict(name="common-job", result="SUCCESS", changes="2,1 1,1"),
            dict(name="project2-job", result="SUCCESS", changes="2,1 1,1"),
            # This would be deduplicated
            dict(name="common-job", result="SUCCESS", changes="2,1 1,1"),
        ], ordered=False)
        self.assertEqual(len(self.fake_nodepool.history), 4)


class TestDataReturn(AnsibleZuulTestCase):
    tenant_config_file = 'config/data-return/main.yaml'

    @model_version(19)
    def test_data_return(self):
        # Test backward compatibility handling
        A = self.fake_gerrit.addFakeChange('org/project', 'master', 'A')
        self.fake_gerrit.addEvent(A.getPatchsetCreatedEvent(1))
        self.waitUntilSettled()
        self.assertHistory([
            dict(name='data-return', result='SUCCESS', changes='1,1'),
            dict(name='data-return-relative', result='SUCCESS', changes='1,1'),
            dict(name='child', result='SUCCESS', changes='1,1'),
        ], ordered=False)
        self.assertIn('- data-return https://zuul.example.com/',
                      A.messages[-1])
        self.assertIn('- data-return-relative https://zuul.example.com',
                      A.messages[-1])

    # To 21
    @model_version(18)
    def test_model_18_21(self):
        self._test_circ_dep_refactor(21)

    @model_version(20)
    def test_model_20_21(self):
        self._test_circ_dep_refactor(21)

    # To 22
    @model_version(18)
    def test_model_18_22(self):
        self._test_circ_dep_refactor(22)

    @model_version(20)
    def test_model_20_22(self):
        self._test_circ_dep_refactor(22)

    @model_version(21)
    def test_model_21_22(self):
        self._test_circ_dep_refactor(22)

    # To 23
    @model_version(18)
    def test_model_18_23(self):
        self._test_circ_dep_refactor(23)

    @model_version(20)
    def test_model_20_23(self):
        self._test_circ_dep_refactor(23)

    @model_version(21)
    def test_model_21_23(self):
        self._test_circ_dep_refactor(23)

    @model_version(22)
    def test_model_22_23(self):
        self._test_circ_dep_refactor(23)

    # To 24
    @model_version(18)
    def test_model_18_24(self):
        self._test_circ_dep_refactor(24)

    @model_version(20)
    def test_model_20_24(self):
        self._test_circ_dep_refactor(24)

    @model_version(21)
    def test_model_21_24(self):
        self._test_circ_dep_refactor(24)

    @model_version(22)
    def test_model_22_24(self):
        self._test_circ_dep_refactor(24)

    @model_version(23)
    def test_model_23_24(self):
        self._test_circ_dep_refactor(24)

    # To 25
    @model_version(18)
    def test_model_18_25(self):
        self._test_circ_dep_refactor(25)

    @model_version(20)
    def test_model_20_25(self):
        self._test_circ_dep_refactor(25)

    @model_version(21)
    def test_model_21_25(self):
        self._test_circ_dep_refactor(25)

    @model_version(22)
    def test_model_22_25(self):
        self._test_circ_dep_refactor(25)

    @model_version(23)
    def test_model_23_25(self):
        self._test_circ_dep_refactor(25)

    @model_version(24)
    def test_model_24_25(self):
        self._test_circ_dep_refactor(25)

    def _test_circ_dep_refactor(self, final_model_api):
        # Test backwards compat for job graph dependency freezing.
        # First test the entire lifecycle under the old api.
        A = self.fake_gerrit.addFakeChange('org/project6', 'master', 'A')
        self.fake_gerrit.addEvent(A.getPatchsetCreatedEvent(1))
        self.waitUntilSettled()

        self.assertHistory([
            dict(name='data-return', result='SUCCESS', changes='1,1'),
            dict(name='paused-data-return-child-jobs',
                 result='SUCCESS', changes='1,1'),
        ], ordered=True)
        self.assertEqual(set(['data-return', 'child']),
                         set(self.history[1].parameters['zuul']['child_jobs']))

        # Then repeat the test with a mid-cycle upgrade.
        self.executor_server.hold_jobs_in_build = True
        B = self.fake_gerrit.addFakeChange('org/project6', 'master', 'B')
        self.fake_gerrit.addEvent(B.getPatchsetCreatedEvent(1))
        self.waitUntilSettled()

        self.assertEqual(len(self.builds), 1)

        # Upgrade our component
        self.model_test_component_info.model_api = final_model_api
        component_registry = ComponentRegistry(self.zk_client)
        for _ in iterate_timeout(30, "model api to update"):
            if component_registry.model_api == final_model_api:
                break

        self.executor_server.hold_jobs_in_build = False
        self.executor_server.release()
        self.waitUntilSettled()

        self.assertHistory([
            dict(name='data-return', result='SUCCESS', changes='1,1'),
            dict(name='paused-data-return-child-jobs',
                 result='SUCCESS', changes='1,1'),
            dict(name='data-return', result='SUCCESS', changes='2,1'),
            dict(name='paused-data-return-child-jobs',
                 result='SUCCESS', changes='2,1'),
        ], ordered=True)
        self.assertEqual(set(['data-return', 'child']),
                         set(self.history[1].parameters['zuul']['child_jobs']))
        self.assertEqual(set(['data-return', 'child']),
                         set(self.history[3].parameters['zuul']['child_jobs']))
