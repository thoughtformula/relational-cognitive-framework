# NTFS — Cognitive operations

NTFS is a vocabulary of optional cognitive orientations inspired by Jung, not an exhaustive or empirically established decomposition of human cognition. Neither a label nor participation in an operation establishes consciousness. Introversion and extraversion refer to the principal reference frame, not the direction of data flow.

| Orientation | Reference frame | Operation | Typical output |
|---|---|---|---|
| Ni | Internal patterns | Synthesis and prediction | Proposition, inference |
| Ne | External possibilities | Exploration and alternatives | Proposition, plan candidate |
| Ti | Internal principles | Logical assessment | Inference, evidence |
| Te | External conditions | Empirical verification, organization | Observation, evidence, plan |
| Fi | Internal commitments | Personal valuation | Valuation, preference |
| Fe | Relational conditions | Stakeholder valuation and testimony | Valuation, claim |
| Si | Internal experience | Recollection and contextualization | Claim, evidence |
| Se | External conditions | Observation | Observation |

These are typical outputs, not exclusive ownership rules. Any strategy may consume the same domain records. An output's type depends on its semantics, not its cognitive label.

## Record types

`cognitive_operation` requires `id`, `type`, `agent_id: Ref`, `orientations: string[]`, `strategy: string`, `input_ids: Ref[]`, `output_ids: Ref[]`, `recorded_at: Instant`; optional `evidence_ids: Ref[]`, `limitations: string[]`, `confidence: Confidence`, `parent_operation_ids: Ref[]`.

The agent ID targets an agent; input and output IDs may target any supported domain record. Evidence IDs target evidence; parent IDs target cognitive operations. Orientations are a set drawn from `Ni`, `Ne`, `Ti`, `Te`, `Fi`, `Fe`, `Si`, `Se`; an empty list identifies an unlabeled strategy. Operation IDs MUST be distinct from their output IDs. Parent operation links MUST NOT form a cycle. Strategy identifies a reproducible method or implementation version where available.

## Composition

- Cognitive operations MAY run concurrently, recursively, or selectively. The record identifies inputs and outputs rather than imposing a fixed NTFS stack or ordering.
- Operations MUST NOT promote hypotheses to observations, value judgments to objective facts, or capability to authority by changing labels.
- A strategy may examine alternatives or abstain; it does not need to invent output when information is unavailable. Any action it proposes remains subject to RCP authorization.
- Agents are not required to implement every orientation. A reactive agent may have no cognitive-operation records. The runtime coordinates operations rather than owning domain semantics.

Future work defines strategy interfaces, scheduling, and empirical comparisons. 0.2 makes cognitive operations inspectable and exchangeable without standardizing their algorithms.
