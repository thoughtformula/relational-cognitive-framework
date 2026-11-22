# RCA — Axiology

Values are situated assessments, not factual propositions or necessarily scalar rewards. The existence of a preference does not establish an obligation; the existence of an obligation does not establish an agent's permission to act.

## Record types

| Type | Required fields and optional fields |
|---|---|
| `value` | `holder_id: Ref`, `kind: instrumental/intrinsic/experiential/relational/epistemic/ecological`, `description: string`, `scope: string`, `mode: descriptive/normative`, `recorded_at: Instant`; optional `supersedes: Ref` |
| `preference` | `holder_id: Ref`, `preferred_id: Ref`, `alternative_id: Ref`, `value_ids: Ref[]`, `recorded_at: Instant` |
| `commitment` | `holder_id: Ref`, `value_id: Ref`, `revision_authority_id: Ref`, `recorded_at: Instant`; optional `supersedes: Ref`, `valid_during: Interval` |
| `constraint` | `holder_id: Ref`, `condition_id: Ref`, `mode: required/prohibited`, `strength: hard/soft`, `recorded_at: Instant`; optional `valid_during: Interval`, `authority_id: Ref` |
| `valuation` | `evaluator_id: Ref`, `subject_id: Ref`, `value_id: Ref`, `judgment: favorable/unfavorable/neutral/unknown`, `recorded_at: Instant`; optional `stakeholder_ids: Ref[]`, `belief_ids: Ref[]`, `confidence: Confidence`, `rationale: string` |
| `value_conflict` | `valuation_ids: Ref[]`, `alternative_ids: Ref[]`, `status: unresolved/resolved/deferred`, `recorded_at: Instant`; optional `resolution: string`, `authority_id: Ref`, `supersedes: Ref` |

Holders, evaluators, authority and stakeholders reference agents or entities; commitment revision authority is an entity or agent. Conditions reference propositions; subjects and alternatives reference entities, relationships, propositions, goals, plans, or proposed actions. `value_ids`, `belief_ids`, and `valuation_ids` target corresponding record types.

## Rules

- An evaluator MAY represent another agent's interests but MUST distinguish the holder from the evaluator; a valuation does not change the holder's preference.
- Preferences are comparative; preferred and alternative IDs MUST differ. No assumption of completeness, transitivity, or universal comparability is imposed.
- A commitment's revision MUST identify the same holder and preserve history. Protected changes require the recorded revision authority; evidence that a change is authorized MUST be available to the implementing governance mechanism. Reward or preference change alone confers no authority.
- A hard constraint MUST NOT be treated as merely a negative contribution to a numerical utility score. Uncertain applicability requires evaluation or deferral rather than assuming permission.
- Conflicts MUST identify at least two valuations or alternatives and remain explicit until resolved or deferred; resolution MUST preserve the rationale and affected values. Resolution does not prove agreement among stakeholders.
- Descriptive beliefs about values may be represented in RCE, but cannot silently substitute for these normative or relational records.

## RCA interface

Inputs: scoped world referents, beliefs about consequences, values, commitments, norms and stakeholder perspectives. Outputs: valuations, preferences, constraints and conflict records. RCP evaluates possible actions against these outputs; governance authority is separate from preference ranking.
