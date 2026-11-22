# RCP — Praxeology

Agency concerns the capacity to alter or regulate conditions, whereas an action is a situated attempt to exercise that capacity. An authorized action can fail, succeed without achieving the intended goal, or produce unintended consequences.

## Record types

| Type | Required fields and optional fields |
|---|---|
| `capability` | `agent_id: Ref`, `kind: string`, `description: string`; optional `parameter_contract: object` |
| `permission` | `grantor_id: Ref`, `grantee_id: Ref`, `capability_id: Ref`, `environment_id: Ref`, `target_ids: Ref[]`, `effect: allow/deny`, `valid_during: Interval`, `recorded_at: Instant`; optional `supersedes: Ref` |
| `goal` | `agent_id: Ref`, `condition_id: Ref`, `recorded_at: Instant`; optional `value_ids: Ref[]` |
| `action` | `actor_id: Ref`, `capability_id: Ref`, `environment_id: Ref`, `target_ids: Ref[]`, `parameters: object`, `recorded_at: Instant`; optional `goal_ids: Ref[]`, `precondition_ids: Ref[]`, `expected_effect_ids: Ref[]`, `permission_ids: Ref[]`, `reversibility: reversible/irreversible/unknown` |
| `plan` | `agent_id: Ref`, `goal_ids: Ref[]`, `action_ids: Ref[]`, `dependencies: [{before_id: Ref, after_id: Ref}]`, `recorded_at: Instant`; optional `stop_condition_ids: Ref[]` |
| `action_event` | `action_id: Ref`, `status: proposed/approved/executing/completed/failed/cancelled/verified`, `recorded_at: Instant`; optional `event_id: Ref`, `reason: string` |
| `outcome` | `action_id: Ref`, `execution: completed/failed/unknown`, `goal_result: achieved/not_achieved/unknown`, `observation_ids: Ref[]`, `recorded_at: Instant`; optional `unexpected_effect_ids: Ref[]`, `goal_ids: Ref[]` |

Actor, agent and grantee IDs target agents; grantor targets an entity or agent with separately established grant authority. Targets reference entities or relationships. Condition and effect IDs reference propositions. Outcome observations target observations; unexpected effects reference events. A permission's empty target list authorizes no targets; it is not a wildcard. A targetless action can be represented by an empty action target list but still requires explicitly applicable permission.

## Invariants

- A capability must belong to the actor; capability does not imply permission. Permission must match actor, capability, environment, target set and validity interval. A grant is not self-validating: an implementation MUST establish the grantor's authority independently. A matching denial, expired grant, or uncertain authority MUST prevent approval until resolved by applicable governance.
- Preconditions and constraints MUST be checked against the appropriate epistemic snapshot before execution; unknown is not satisfied. Approval MUST precede execution for actions requiring authorization. Abstention or escalation is valid.
- Action records describe proposed operations and MUST NOT be mutated to record success. Lifecycle events provide history: proposed → approved → executing → completed/failed → verified where verification is possible; cancellation may occur before completion. A completed execution is not proof of an achieved goal.
- Outcomes MUST distinguish execution from goal achievement. `achieved` requires observed evidence supporting the goal condition; absence of evidence requires `unknown`, not success. Effects are observations or events, not predicted effects relabeled as facts.
- Plan dependencies MUST refer to actions in the plan and be acyclic. Independent steps may execute concurrently if authorized. 0.3 will define transition and scheduling semantics beyond these constraints.
- High-impact or irreversible operations SHOULD require stronger evidence, explicit authority and appropriate confirmation. The feedback interface MUST preserve failures and unexpected effects.

## RCP interface

Inputs: goals, valuations, constraints, capabilities, permissions and beliefs. Outputs: plans, proposed actions, lifecycle events and evidence-bearing outcomes. Environment services remain responsible for applying permissible state transitions. RCE receives observed outcomes, not assumptions of success.
