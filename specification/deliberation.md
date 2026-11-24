# RCF 0.3 — Deliberation, authorization, action, and feedback

This document refines RCP's existing action lifecycle without reducing RCA's plural values to one score. The relevant contracts are [dynamics](dynamics.md), [axiology](axiology.md), [praxeology](praxeology.md), and [epistemology](epistemology.md).

## 1. Deliberation

`deliberation` records preserve the agent's decision inputs and alternatives. The evaluator MUST identify the `decision_context` used to assess the choices. An agent MAY rank alternatives by Pareto dominance, hard constraints, priority ordering, human oversight, negotiation, or domain-specific rules. It MUST NOT assume all values have a common scalar measure.

Decision rules:

1. Enumerate candidate actions or abstention, and associate goals and values.
2. Resolve available evidence and relevant uncertainty using the decision context. Unknown preconditions MUST NOT be treated as satisfied.
3. Eliminate actions violating hard constraints; retain an explanation and affected constraints.
4. Identify permission uncertainty; a permissive belief does not substitute for authorization.
5. Compare remaining candidates under an explicit, inspectable method. A conflict unresolved by authorized policy MAY cause `deferred` or `abstained`.
6. Emit `deliberation` with `selected` (one chosen candidate), `abstained` (no chosen action), or `deferred` (decision postponed, awaiting evidence or authority). These are deliberative outcomes, not action outcomes.

Selection MUST NOT mutate the world; it is eligible to create a proposed action/request subject to RCP.

## 2. Authorization and action lifecycle

An authorized transition must have a valid, applicable grant issued by an entity whose grant authority can be established by the environment mechanism. `permission` records alone do not prove the grantor was authorized. Where scope/authority cannot be confirmed, the action MUST NOT be approved as permitted.

Allowed lifecycle edges:

```text
proposed ──→ approved ──→ executing ──→ completed ──→ verified
    │           │            │             └── (not verified if no evidence)
    └───────────┴────────────┴──────────→ cancelled (before terminal completion)
                             └────────→ failed
```

An implementation MUST reject impossible regressions (`executing → proposed`, `failed → verified`) within one action's event sequence. Identical status records with distinct IDs MUST NOT be mistaken for distinct successful executions. `failed`, `cancelled`, and `verified` are terminal for the same attempt. Retrying a non-idempotent action requires a new action/attempt identity or a proved-idempotent request using the service's declared semantics.

`transition_result.applied` records the environment's answer to a request; `action_event.completed` records execution completion; `outcome.goal_result=achieved` requires supporting observations under RCP. These statements are *not* equivalent. `transition_result.unknown` after network failure MUST NOT be converted to a negative result or retried blindly.

## 3. Feedback and learning

Feedback compares anticipated effects (`action.expected_effect_ids`) against post-intervention observations and outcomes. `feedback.assessment=undetermined` covers missing data, incompatible measurement procedures, temporally mismatched observations, and uncertainty about whether the request was applied. A match is not proof of causality; to assert causal attribution, a model must separately justify it by experiment, mechanistic constraints, or other explicit grounds.

Feedback MAY trigger belief revisions, changes in plans, or a new inquiry. It MUST NOT silently change stable identities, past states, past beliefs, or protected commitments. A policy adaptation with changed authorization MUST record the appropriate RCA governance evidence; a desire to improve reward does not constitute permission to change commitments.

## 4. Recovery and audit

For consequential operations, clients SHOULD record a recovery/reconciliation route and the limit of what can be reversed. Idempotency is not synonymous with compensation: returning a previous receipt for a duplicate request is different from undoing a confirmed effect. An execution service SHOULD log rejected and uncertain requests as carefully as successful ones.

Auditable correlation: `action` → `deliberation` → `transition_request` → `transition_result` → `action_event`/`outcome` → `feedback` → optional `belief_revision`. Not every step is present in every application, but a system claiming dynamics/execution conformance MUST preserve the links relevant to the actions it executed.
