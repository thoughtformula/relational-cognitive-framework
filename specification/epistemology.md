# RCE — Epistemology

## Record types

| Type | Required fields and optional fields |
|---|---|
| `proposition` | `predicate: string`, `arguments: [Term,...]`, `polarity: positive/negative`; optional `environment_id: Ref`, `valid_during: Interval` |
| `observation` | `observer_id: Ref`, `environment_id: Ref`, `method: string`, `data: JsonValue`, `recorded_at: Instant`; optional `observed_at: Instant`, `source_id: Ref` |
| `claim` | `proposition_id: Ref`, `source_id: Ref`, `acquisition: observed/reported/recalled/inferred/predicted`, `lifecycle: active/retracted`, `recorded_at: Instant`; optional `basis_ids: Ref[]`, `supersedes: Ref` |
| `evidence` | `proposition_id: Ref`, `basis_ids: Ref[]`, `relation: supports/contradicts/undercuts`, `source_id: Ref`, `recorded_at: Instant`; optional `confidence: Confidence`, `scope: string` |
| `belief` | `agent_id: Ref`, `proposition_id: Ref`, `stance: accepts/rejects/suspends`, `confidence: Confidence`, `evidence_ids: Ref[]`, `recorded_at: Instant`; optional `supersedes: Ref` |
| `inference` | `agent_id: Ref`, `premise_ids: Ref[]`, `conclusion_id: Ref`, `method: string`, `recorded_at: Instant` |
| `belief_revision` | `agent_id: Ref`, `prior_belief_id: Ref`, `result_belief_id: Ref`, `trigger_ids: Ref[]`, `method: string`, `recorded_at: Instant` |

`Term` is a tagged object `{kind: ref, id: Ref}`, `{kind: literal, value: JsonValue}`, or `{kind: symbol, value: string}`. Arguments are ordered by predicate signature; positive and negative polarity distinguish a proposition from its explicit negation. Predicates SHOULD have documented argument semantics; complex expressions may be represented by application-specific predicate vocabularies. A symbol need not resolve to an existing entity. A proposition asserts no truth by its mere presence.

`observer_id` and `agent_id` target `agent`. `source_id` targets an entity or agent; provenance bases target observations, claims, evidence, or inferences. Inference premises target propositions, observations, claims, or beliefs; conclusion targets proposition. Evidence and belief references target their respective types. Evidence basis lists and inference premise lists MUST be nonempty. Evidence records MUST NOT form a cyclic justification graph; repeated reports SHOULD preserve their common original basis.

## Evidence and stance

An observation preserves acquired data without asserting that a sensor is correct. A claim records an assertion. An evidence record is a contextual relationship between a basis and a proposition; supporting information may be relevant without being conclusive. `undercuts` challenges a justification rather than necessarily supporting the opposite proposition. Belief is an agent-specific relation to a proposition, not an attribute of that proposition or a global world state.

- A claim's acquisition and lifecycle are independent. Retraction creates a new claim with the same proposition and source and a supersedes link; it does not erase the observation or automatically negate the proposition.
- A revised belief MUST preserve the same agent and proposition as its predecessor, refer to the prior record through `supersedes`, and be accompanied by a revision record linking them. Revisions MUST be time-ordered and acyclic. A belief may suspend without assigning a probability of 0.5.
- The evidence IDs in a belief MUST refer to that proposition; evidence about a distinct proposition must be connected explicitly by inference or a new evidence record. Evidence may be conflicting, and two agents may maintain different stances. An agent with no recorded belief does not thereby reject the proposition.
- Contradiction requires matching predicate, arguments and scope with opposing polarity, or an explicit domain constraint; different temporal intervals need not conflict. An observation alone does not settle contradiction. Missing information is not proof of negation.
- Revision policies MUST preserve provenance and historical records; they MAY use Bayesian, logical, ordinal or other methods. This version does not select a default algorithm or confidence threshold.

## RCE interface

Inputs: observations, memory, reports, and inference records. Outputs: propositions, claims, evidence, beliefs and revisions. A receiving agent MUST preserve the distinction between acquisition, endorsement, and truth. Valuation and action consume explicit beliefs and uncertainty rather than reading another agent's state as omniscient fact.
