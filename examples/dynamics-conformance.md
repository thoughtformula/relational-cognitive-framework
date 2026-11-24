# RCF 0.3 — Dynamics conformance scenarios

The [self-contained fixture](dynamics.json) extends the same garden concepts as 0.2 with explicit decision contexts, cognitive strategy run, world transition requests/results, feedback and partial order. It is illustrative: steward grant authority and sensor calibration are **scenario assumptions** that a real implementation must verify separately.

## Expected reading

1. Alice accepts dry-soil evidence, suspends her belief when Bob reports contrary visual evidence, and accepts again after an independent probe. Each belief supersedes the previous one; counterevidence remains recorded.
2. The successful probe has a `cognitive_operation` and a `strategy_run`; the latter does not grant environmental write authority.
3. Alice and Bob deliberate using the **same** original `soil-before` snapshot (`r0`) and propose separate actions. Both receive apparent permission grants, whose grantor authority is *assumed*, not proven by the fixture.
4. The environmental authority applies Alice's action and emits `soil-after` (`r1`). It then rejects Bob's stale request. Bob's prior belief and deliberation are not retroactively rewritten.
5. Alice's completed execution, subsequent observation, verified status, goal outcome and feedback are distinct events. The claimed moisture match does not by itself prove causation.
6. Bob's rejected request emits no resultant state or environment event; his `feedback` remains `undetermined`.
7. A serialization edge orders the two receipts. It does not establish a causal relationship between Alice's intentions and Bob's intentions.

## Negative mutations

| Case | Mutation | Expected diagnostic |
|---|---|---|
| C01 | Change `context-alice.belief_ids` to Bob-owned belief | Incorrect agent ownership |
| C02 | Point `run-retest.context_id` to Bob's context | Incorrect strategy/agent association |
| C03 | Put `run-retest.started_at` after its recorded time | Nonmonotonic run time |
| C04 | Change `decision-alice.selected_action_id` to `action-bob` | Candidate/actor violation |
| C05 | Change `decision-bob.decision` to `deferred` without removing selected action | Deferred must not select |
| C06 | Point `request-bob.context_id` at Alice's context | Action/context mismatch |
| C07 | Set `result-bob.result_state_ids` to `soil-after` | Rejected request falsely claims an applied effect |
| C08 | Erase `feedback-alice.observation_ids` but retain `matches` | Unsupported definitive feedback |
| C09 | Reverse `serial-order` and add an opposite edge | Cyclic partial order |
| C10 | Change `grant-alice.grantee_id` to Bob | Grant/action mismatch |
| C11 | Change Alice's approved event to `verified` (before executing) | Invalid lifecycle transition |
| C12 | Change `request-alice.expected_state_ids` to another environment's state | Wrong environmental scope |

Test scripts in [tools](../tools/check_dynamics.py) check a deliberately bounded subset. Successful validation does not establish sensor reliability, actual authority, safe live concurrency or a full 0.3 runtime.
