"""Small regression suite for the illustrative 0.3 fixture, not full conformance."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from check_dynamics import validate  # noqa: E402

SOURCE = json.loads((ROOT / 'examples' / 'dynamics.json').read_text())


def rec(bundle, rid):
    return next(r for r in bundle['records'] if r['id'] == rid)


class DynamicsFixtureTests(unittest.TestCase):
    def setUp(self):
        self.data = copy.deepcopy(SOURCE)

    def failure(self, expected):
        errors = validate(self.data)
        self.assertTrue(errors, 'Expected a validation failure')
        self.assertTrue(any(expected in error for error in errors), errors)

    def test_valid_fixture(self):
        self.assertEqual(validate(self.data), [])
        self.assertEqual(len(self.data['records']), 64)

    def test_duplicate_id(self):
        self.data['records'].append(copy.deepcopy(rec(self.data, 'soil')))
        self.failure('duplicate identifier')

    def test_other_agents_belief(self):
        rec(self.data, 'context-alice')['belief_ids'] = ['bob-belief']
        self.failure('belief held by other agent')

    def test_other_agents_strategy_context(self):
        rec(self.data, 'run-retest')['context_id'] = 'context-bob'
        self.failure('operation/context agent mismatch')

    def test_reversed_strategy_time(self):
        rec(self.data, 'run-retest')['started_at'] = '2026-01-01T09:08:00Z'
        self.failure('run ends before starting')

    def test_selected_action_outside_candidates(self):
        rec(self.data, 'decision-alice')['selected_action_id'] = 'action-bob'
        self.failure('selected action not in candidate set')

    def test_deferred_cannot_select(self):
        rec(self.data, 'decision-bob')['decision'] = 'deferred'
        self.failure('nonselected deliberation has selected action')

    def test_action_context_mismatch(self):
        rec(self.data, 'request-bob')['context_id'] = 'context-alice'
        self.failure('action/context mismatch')

    def test_rejected_request_cannot_claim_effect(self):
        rec(self.data, 'result-bob')['result_state_ids'] = ['soil-after']
        self.failure('rejected with attributed effects')

    def test_feedback_without_observation_is_undetermined(self):
        rec(self.data, 'feedback-alice')['observation_ids'] = []
        self.failure('definite assessment without observation')

    def test_cycle_in_happens_before(self):
        self.data['records'].append({'id':'cycle','type':'ordering_edge','before_id':'result-bob','after_id':'result-alice','kind':'serialization','recorded_at':'2026-01-01T09:17:00Z'})
        self.failure('cycle in happens-before graph')

    def test_grant_not_applicable(self):
        rec(self.data, 'grant-alice')['grantee_id'] = 'bob-agent'
        self.failure('permission not applicable to action')

    def test_invalid_lifecycle(self):
        rec(self.data, 'alice-approved')['status'] = 'verified'
        self.failure('invalid event')

    def test_state_from_wrong_environment(self):
        self.data['records'].append({'id':'other-env','type':'environment','kind':'alternate'})
        self.data['records'].append({'id':'other-state','type':'state','subject_id':'soil','environment_id':'other-env','properties':{},'recorded_at':'2026-01-01T09:10:00Z'})
        rec(self.data, 'request-alice')['expected_state_ids'] = ['other-state']
        self.failure('expected state in other environment')

    def test_revision_preserves_agent(self):
        rec(self.data, 'revision-reaccept')['agent_id'] = 'bob-agent'
        self.failure('belief revision crosses agent or proposition')

    def test_revision_preserves_predecessor(self):
        rec(self.data, 'b-reaccept')['supersedes'] = 'b-accept'
        self.failure('revision predecessor not preserved')

    def test_unknown_cannot_assert_effect(self):
        rec(self.data,'result-alice')['status']='unknown'
        self.failure('unknown with asserted effects')


if __name__ == '__main__':
    unittest.main()
