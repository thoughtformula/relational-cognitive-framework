# RCO — Ontology

RCO describes entities and relationships, not an agent's necessarily fallible beliefs about them. In simulations a world service may own authoritative state; outside simulations the claimed state of the world remains subject to measurement and correction. An entity identifier is not a proof of existence.

## Record types

| Type | Required fields and optional fields |
|---|---|
| `entity` | `kind: string`; optional `name: string` and `persistence_criterion: string` |
| `environment` | `kind: string`; optional `entity_id: Ref`, `parent_ids: Ref[]`, `boundary: string` |
| `agent` | `entity_id: Ref`, `agency_kind: reactive/adaptive/cognitive/collective`, `regulation: string`; optional `capability_ids: Ref[]` |
| `relationship` | `kind: string`, `environment_id: Ref`, `participants: [{entity_id: Ref, role: string}]`, `directed: boolean`; optional `attributes: object`, `valid_during: Interval`, `supersedes: Ref` |
| `state` | `subject_id: Ref`, `environment_id: Ref`, `properties: object`, `recorded_at: Instant`; optional `valid_during: Interval`, `supersedes: Ref` |
| `event` | `environment_id: Ref`, `kind: string`, `participant_ids: Ref[]`, `recorded_at: Instant`; optional `occurred_at: Instant`, `prior_state_ids: Ref[]`, `result_state_ids: Ref[]` |

Environment references target `environment`; entity references target `entity`; state subject references target `entity` or `relationship`; event state references target `state`; capability references target `capability`.

## Identity, membership and boundaries

- Identity MUST NOT depend on mutable names or attributes. Distinct IDs are distinct referents unless an explicit identity-resolution relationship asserts otherwise; such an assertion is not automatically authoritative.
- A relationship has identity independent of its participants. It MUST contain at least two role-qualified participations, which may involve the same entity in different roles. Duplicated `(entity_id, role)` entries are invalid. Directed relationships require at least distinct source and target roles; order alone MUST NOT imply direction. Undirected participants are a set.
- Relationship kind defines the interpretation of roles and attributes. A relation may be n-ary (e.g., a delegation involving principal, delegate, and beneficiary). Relationship kinds SHOULD be documented by a domain vocabulary.
- Membership is a relationship (e.g., `member_of`, with member and community roles), not exclusive containment. Environments can overlap; declared parent links MUST form an acyclic graph. A boundary can be spatial, informational, organizational, or operational.
- If an environment itself acts, its `entity_id` may correspond to an agent's entity. Mere containment or state change is insufficient for agency. An agent MUST have a state-sensitive regulatory or action-selection mechanism. The agency classification need not imply consciousness or moral status.
- State records are contextual snapshots, not timeless attributes. Historical state is retained when a later snapshot supersedes it. Events record occurrences but do not establish causality solely from temporal sequence.

## RCO interface

Inputs: identity and relationship definitions, scoped states, events. Outputs: graph and time-scoped snapshots. Consumers MUST preserve IDs, roles, scope, and temporal semantics. RCE may refer to these objects without obtaining world-write access; RCP may propose changes but only the authorized environment mechanism can establish actual transitions.
