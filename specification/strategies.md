# RCF 0.3 — Cognitive strategies and epistemic revision

This document turns the inspectable `cognitive_operation` and `belief_revision` records of 0.2 into behavioral contracts. Strategy names, including NTFS orientations, describe implementation choices and MUST NOT alter the epistemic type of their outputs.

## 1. Strategy protocol

A strategy has a stable implementation identifier (such as `probe-v1`, `conservative-conflict-v1`), an input contract, a set of potential output record types, a declared domain and reference frame, and known limitations. An invoker supplies an agent, `decision_context`, input IDs, and bounded execution policy. The strategy may output domain records or abstain; its observations and inferences remain ordinary RCE records.

```text
Strategy.invoke(context, inputs, limits)
    -> completed(outputs, evidence, limitations)
     | abstained(reason)
     | failed(error)
```

An invocation MUST validate input references and access permissions. It MUST NOT pretend that a predicted event occurred, modify a protected commitment, issue an executable authorization, or mutate world state directly. Side-effectful sensing or experiments MUST be separately authorized through the relevant capability and RCP path. Execution SHOULD be bounded by explicit time/compute/resource limits. An agent MUST preserve the strategy identifier, sources, limitations, and returned record IDs in `cognitive_operation` and `strategy_run`.

Input/output contract conformance is independent of the cognitive orientation label. `Se` need not correspond to a direct hardware sensor, and `Ni` does not imply an accurate prediction. Parallel strategies can disagree; agreement is not automatically independent evidence.

## 2. Belief revision policy protocol

A revision policy accepts a proposition, the agent's current belief (if any), newly available evidence and its provenance dependencies, temporal scope, and policy configuration. Its result is a proposed stance/confidence and an auditable rationale. If it changes an existing belief, it MUST emit a new `belief` with `supersedes` and a corresponding `belief_revision` preserving the prior and result IDs. Previous evidence MUST remain recoverable.

```text
Revise(proposition, prior_belief?, incoming_evidence, source_graph, context)
    -> proposed_belief + revision_record
     | unchanged(reason)
     | suspended(reason)
     | abstained(reason)
```

Policies MUST distinguish `supports`, `contradicts`, and `undercuts`; preserve time scope; and track shared-origin reports so that repeated copies do not automatically count as independent confirmation. A belief's ordinal confidence MUST NOT be treated as a probability. When a policy cannot evaluate source independence, it SHOULD suspend or explicitly record this limitation rather than inventing independence. Bayesian policies MAY be used only when priors and likelihood assumptions are expressible and independently reviewable. Unknown confidence is not 0.5 probability.

### Informative policy: conservative-conflict-v1

This is a reproducible example, **not** a required global epistemic policy:

1. Begin with the current belief for the same `(agent, proposition)` and gather new evidence and its dependency graph.
2. Group derivative reports sharing a single ultimate source to avoid duplicate amplification.
3. Reject structurally invalid or out-of-scope input records; preserve them for audit but do not treat them as current support.
4. If credible, presently unresolved conflicting evidence exists and no preference rule is justified, emit a **suspended** belief with `confidence: {"kind":"unknown"}`.
5. If an independent measurement of sufficiently documented quality resolves the conflict, a new belief may accept/reject using an explicit ordinal rationale.
6. Emit a `belief_revision` with precise triggers; never delete the prior belief, evidence, or counterevidence.

This algorithm is *normative only for an implementation that explicitly claims* `conservative-conflict-v1` conformance. The specification otherwise allows alternatives that satisfy provenance and lifecycle invariants.

## 3. Revision and consistency invariants

- Evidence updates and belief updates are separate. An observation of data is not a proposition's truth; a conclusion remains attributed to the agent.
- A policy MUST detect conflicting positive/negative propositions only when predicate signature, arguments, and overlapping temporal/environmental scope establish conflict, or when an explicit domain constraint does.
- Two agents MAY preserve incompatible beliefs. One agent's revision MUST NOT rewrite another agent's belief without that agent's authorized policy.
- Results MUST be reproducible from the recorded inputs and policy/version **where the policy claims determinism**. Nondeterministic strategies MUST record enough invocation context and provenance to support audit; byte-for-byte replay is not guaranteed.
- `belief_revision.method` MUST identify the policy/procedure at least at a human-inspectable level. Consumers MUST NOT manufacture a numeric confidence when none was supplied.

## 4. Cognition composition and scheduling

Strategies may operate concurrently or recursively. A child `cognitive_operation` uses `parent_operation_ids` to show logical composition; this graph MUST remain acyclic. A completed `strategy_run` binds an operation to a particular `decision_context`. Logical composition does not imply dataflow: where output of operation A is consumed by B, B MUST reference A's resulting record IDs in its `input_ids`.

If a strategy consumes an outdated context, the runtime MAY keep the resulting information as historical analysis, but it MUST NOT treat an action recommendation as automatically current. Reconciliation and reauthorization are required at the effectful action boundary.

## 5. Implementation-independent examples

- Se/Te sensing: input `soil`, output `observation` from an authorized probe, plus an `evidence` record; neither becomes world truth by naming it an observation.
- Ne exploration: input competing beliefs, output several `proposition` hypotheses; no generated possibility automatically becomes an accepted belief.
- Ti validation: input premises, output an `inference` and cited conclusion; internal consistency does not prove premises.
- Fi/Fe valuation: input commitments and stakeholder views, output `valuation` records; no stakeholder preference becomes universal obligation by default.

**Implementation note:** strategy code, dispatch, process isolation, and benchmark harnesses belong to 0.4+, not to the normative 0.3 documentation.
