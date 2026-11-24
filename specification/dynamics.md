# RCF 0.3 — Formal dynamics and state transitions

**Status:** normative for the 0.3 dynamics profile. This document extends, and does not replace, the 0.2 record contracts in [terminology](terminology.md), [ontology](ontology.md), [epistemology](epistemology.md), [axiology](axiology.md), and [praxeology](praxeology.md).

## 1. State spaces and authority

Let `W_t` denote the state exposed by an environment at a serialization boundary, `I_(a,t)` the internal state of agent `a`, `B_(a,t)` its selected current beliefs, `V_(a,t)` its active evaluations/commitments, and `L_t` the immutable record history. For an agent's **accessible** view, not omniscient access:

```text
o_(a,t)                 = Observe_a(W_t, I_(a,t), channels_a)
(B_(a,t+1), ΔB)         = Revise_a(B_(a,t), observations, evidence, policy_a)
D_(a,t)                 = Deliberate_a(B_(a,t+1), V_(a,t), goals, capabilities, constraints)
q_(a,t)                 = RequestTransition(D_(a,t), expected_world_revision)
(W_(t+1), receipt_t)    = ApplyIfAuthorized(W_t, q_(a,t), policy_world)
I_(a,t+1)               = Adapt_a(I_(a,t), receipt_t, subsequent_observations)
L_(t+1)                 = Append(L_t, generated_records)
```

These are interface signatures, not a required cognitive order. Observation may be delayed; revisions and actions may interleave. No normative assumption makes beliefs correspond to `W`, obliges agents to have all NTFS orientations, or guarantees deterministic transitions. External systems may not expose a canonical `W` at all: they MAY return `unknown` rather than claim an authoritative state change.

An environment's **authorized transition authority** decides which proposed changes it will apply; the actor's own report is never sufficient. `state` records are snapshots scoped to the environment and do not gain truth by being mentioned in a plan. `event` records describe occurrences; neither event order nor correlation alone proves causation.

## 2. Dynamic profile records

All records obey the 0.2 envelope (`id`, `type`, immutable history), reference resolution, `Instant` format, and version requirements. Fields below are required unless marked optional; unnamespaced unknown fields remain invalid.

| Record `type` | Fields and types | Purpose |
|---|---|---|
| `decision_context` | `agent_id: Ref`, `environment_id: Ref`, `state_ids: Ref[]`, `belief_ids: Ref[]`, `valuation_ids: Ref[]`, `constraint_ids: Ref[]`, `permission_ids: Ref[]`, `recorded_at: Instant`; optional `world_revision: string` | An agent's declared input view; not a claim of complete truth |
| `strategy_run` | `operation_id: Ref`, `context_id: Ref`, `status: completed/failed/abstained`, `started_at: Instant`, `recorded_at: Instant`; optional `error: string` | Accountable execution of a cognitive operation |
| `deliberation` | `agent_id: Ref`, `context_id: Ref`, `goal_ids: Ref[]`, `candidate_action_ids: Ref[]`, `valuation_ids: Ref[]`, `constraint_ids: Ref[]`, `decision: selected/abstained/deferred`, `recorded_at: Instant`; optional `selected_action_id: Ref`, `rationale: string`, `unresolved_ids: Ref[]` | Selects, abstains or defers without granting action authority |
| `transition_request` | `action_id: Ref`, `context_id: Ref`, `expected_state_ids: Ref[]`, `permission_ids: Ref[]`, `recorded_at: Instant`; optional `idempotency_key: string` | A request to the environmental authority, not an actual transition |
| `transition_result` | `issuer_id: Ref`, `request_id: Ref`, `status: applied/rejected/unknown`, `prior_state_ids: Ref[]`, `result_state_ids: Ref[]`, `event_ids: Ref[]`, `recorded_at: Instant`; optional `world_revision: string`, `reason: string` | Receipt issued by a trusted environment authority; its trust must be established externally |
| `feedback` | `action_id: Ref`, `result_id: Ref`, `predicted_effect_ids: Ref[]`, `observation_ids: Ref[]`, `assessment: matches/mismatch/undetermined`, `recorded_at: Instant`; optional `belief_revision_ids: Ref[]`, `notes: string` | Compares forecast and observation without upgrading a forecast into a fact |
| `ordering_edge` | `before_id: Ref`, `after_id: Ref`, `kind: program_order/dependency/serialization/communication`, `recorded_at: Instant` | Explicit happens-before constraint; **not** by itself an assertion of physical causality |

References: `decision_context.agent_id` and `deliberation.agent_id` target `agent`, context `environment_id` targets `environment`, `state_ids`/`expected_state_ids` target `state`, `belief_ids` target `belief`, `valuation_ids` target `valuation`, `constraint_ids` target `constraint`, `permission_ids` target `permission`, `operation_id` targets `cognitive_operation`, `context_id` targets `decision_context`, `goal_ids` target `goal`, candidate/selected/action IDs target `action`, `transition_result.issuer_id` targets `entity` or `agent` (recorded issuer, not proof of authority), `transition_result.request_id` targets `transition_request`, `prior_state_ids`/`result_state_ids` target `state`, `event_ids` target `event`, and `feedback.result_id` targets `transition_result`. Predicted effects target `proposition`, feedback observations target `observation`, and belief revisions target `belief_revision`. `ordering_edge` endpoints target `action_event`, `strategy_run`, `transition_request`, `transition_result`, or `feedback`.

### 2.1 Cross-domain invariants

1. A `decision_context` MUST identify an agent, the environment considered, and explicit lists of considered records. Its `belief_ids` MUST all be beliefs held by that agent. Its `state_ids` MUST be states scoped to that environment. Omission from the view MUST NOT imply negation or permission.
2. A `strategy_run` MUST refer to an operation of the context's agent. Its `started_at` MUST NOT be after `recorded_at`. `completed` requires that the referenced operation's outputs be present; a `failed` or `abstained` run MUST NOT claim inferred domain outputs from the failed attempt as observed facts. A strategy run is not authorization to mutate an environment.
3. A `deliberation` MUST refer to a context belonging to its agent. All candidate actions MUST have this agent as actor. `selected` requires `selected_action_id` in `candidate_action_ids`; `abstained` or `deferred` MUST omit `selected_action_id`. A selection does not establish authorization or effect.
4. A `transition_request` MUST target an action whose actor and environment match the `decision_context`. Its permissions MUST be applicable to that action under RCP, not inferred from the presence of IDs. Expected state records MUST be from the same environment and represent the view the actor relied on; an empty list means no state precondition was asserted, not permission to override concurrency rules.
5. A `transition_result` MUST refer to a single request. `applied` requires at least one attributable `event` or `result_state` record and must identify the authoritative source independently of the record's text; `rejected` MUST have no claimed result states or events **from that request**; `unknown` MUST NOT claim that an effect definitely occurred or did not occur. The receiver MUST treat an unauthenticated receipt as a report, not world truth. An `unknown` result MAY be issued by a client recording a timeout, but MUST NOT impersonate the environment authority. `issuer_id` identifies the recorded source, not verified authority.
6. `feedback` MUST refer to the same action as its `transition_result`'s request. `matches` and `mismatch` require at least one observation bearing upon a predicted effect; if there are no observations, `assessment` MUST be `undetermined`. `feedback` MUST NOT silently rewrite or delete beliefs, states, actions, or predictions.
7. `ordering_edge` MUST NOT self-reference; the graph of edges MUST be acyclic. Program order applies within a process; serialization edges are asserted by an authority; message send/receive links establish partial ordering. Wall-clock proximity is insufficient for an ordering edge.
8. Multiple records may describe one world condition from different perspectives. A consumer MUST distinguish **current within a given view** from globally authoritative state. A consumer MUST NOT overwrite a historical record when revisions occur.

## 3. Transition stages

```text
read snapshot → propose action → evaluate constraints → authorize
     → execute/request → environment applies/rejects/unknown
     → observe → verify goal/effects → feedback/revision
```

Action-event lifecycle remains governed by RCP: `proposed → approved → executing → completed|failed` (with `cancelled` as an allowed terminal before completion), and `completed → verified` only after independent confirmation. `transition_result.status=applied` says that the environmental service applied a transition; it does NOT entail `goal_result=achieved`, a verified observation, or harmless side effects. `unknown` (e.g. network timeout after sending an action) is intentionally different from `rejected`, `failed`, and `cancelled`. Reconciliation MUST precede retry when there is any chance of a non-idempotent effect.

## 4. Safety and temporal boundaries

Approval MUST use a context whose permissions and constraints were evaluated as of the approval decision. Before effectful execution, the environment authority MUST recheck relevant hard constraints and grant validity against its authoritative state, or reject with `unknown`/`rejected` when unable. Approval based on a stale snapshot is insufficient.

A `transition_request.expected_state_ids` list is optimistic-concurrency evidence, not a hard-coded lock implementation. A service accepting this profile MUST compare material preconditions against its current state or use an equivalent serializable mechanism. If the relevant state changed since the context was produced, the service MUST reject or revalidate under an explicit policy; it MUST NOT silently write based on stale state.

For a nondeterministic or externally mediated action, `transition_result=unknown` is legitimate; do not fabricate a definitive world snapshot. Irreversible actions SHOULD include documented risk and authority checks. Idempotency keys are scoped to `(environment, actor, capability)` by the execution service; identical key and payload SHOULD return the original result, while changed payloads with the same key MUST be rejected. A key alone does not guarantee external idempotency.

## 5. Compatibility

A valid 0.2 bundle remains meaningful as a historical exchange; it MUST NOT be re-labeled `0.3.0` unless its consumer declares that the 0.3 dynamics profile is applicable or the bundle explicitly identifies it as record-only. New 0.3 dynamic records require `rcf_version: "0.3.0"`. Existing 0.2 record shapes and meanings are unchanged. An implementation MAY conform to the 0.3 **record-only** profile without implementing action execution; it MUST NOT claim dynamics/execution conformance in that case.

**Non-goals:** prescribing a universal truth oracle, universal moral utility, distributed consensus algorithm, scheduling fairness guarantee, or compulsory sequence for NTFS operations. A minimal executable reference implementation remains 0.4 work.
