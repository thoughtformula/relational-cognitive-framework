# Relationship Cognitive Praxeology (RCP)

*How agents turn knowledge and value into consequential action, and how action changes both agents and environments.*

## Abstract

Relationship Cognitive Praxeology studies action as the practical expression of agency within a relational world. Action connects an agent's perceived circumstances, knowledge, values, capacities, and constraints to changes in its environment. Effective agency requires not only selecting actions but anticipating consequences, coordinating with others, monitoring feedback, and correcting failures.

## 1. Action as a relationship

An action is not simply a command issued by an isolated agent. It is a state-changing interaction whose consequences depend on the environment and other agents. The same behavior can succeed, fail, or cause harm under different conditions.

A useful transition model is:

\[s_{t+1}\sim T(s_t,a_t,e_t)\]

where s is a relevant state, a an action, e environmental conditions, and T the transition process. The model can be deterministic or probabilistic. The agent generally has only partial access to the true state.

## 2. Agency, intention, and control

**Capability** is what an agent can do. **Permission** is what it is authorized to do. **Intention** is what it seeks to accomplish. **Control** is how reliably it can influence outcomes. **Responsibility** concerns the obligations attached to exercising influence. These concepts must not be collapsed: the ability to execute an action does not establish authority to perform it.

## 3. The eight functions in action

| Function | Praxeological contribution |
|---|---|
| Se | Detect current conditions and immediate changes |
| Si | Recall prior attempts and operational context |
| Ne | Generate possible interventions |
| Ni | Model trajectories and longer-term consequences |
| Ti | Check causal and procedural consistency |
| Te | Organize execution, resources, tests, and metrics |
| Fi | Check alignment with the agent's commitments |
| Fe | Coordinate permissions, obligations, and other agents |

These functions form a repertoire rather than a mandatory linear pipeline.

## 4. The action cycle

1. **Orient:** identify the situation and the agent's available information.
2. **Specify:** distinguish the desired outcome from the action used to pursue it.
3. **Constrain:** establish permissions, safety boundaries, costs, and obligations.
4. **Generate:** produce alternative plans, including doing nothing or asking for help.
5. **Predict:** estimate likely consequences and uncertainty.
6. **Select:** choose an authorized action consistent with values and evidence.
7. **Execute:** act through a defined interface.
8. **Observe:** compare results with predictions and detect side effects.
9. **Adapt:** update models, strategies, and—when authorized—policies.

## 5. Affordances and environment

An affordance is an opportunity for action relative to an agent's capabilities and context. A staircase affords climbing to a mobile person but not necessarily to a wheeled robot. A web API affords operations only when the agent has credentials, connectivity, and authorization. Agency therefore depends on the match between an agent's capacities and its environment's available interfaces.

## 6. Multi-agent action

When agents share an environment, actions have externalities. Coordination requires identifying dependencies, shared resources, conflicting objectives, authority boundaries, and communication protocols. A collective may exercise agency through voting, delegation, contracts, consensus, or centralized orchestration; these are different governance arrangements with different failure modes.

## 7. Reversibility and safety

Actions should be classified by impact and reversibility. Reading a document, modifying a local draft, publishing a statement, deleting a repository, and transferring funds require different safeguards. Higher-impact actions should demand stronger evidence, explicit authority, and appropriate confirmation. A successful command is not equivalent to a desirable outcome.

## 8. Learning through consequences

Praxeological learning compares intended outcomes with observed effects. Prediction errors may reveal flawed knowledge, insufficient capabilities, unforeseen environmental changes, or mistaken values. RCP separates these causes instead of treating every failed action as a planning error.

A useful operational record includes intent, preconditions, authority, action, observed outcome, side effects, uncertainty, rollback path, and lessons learned.

## 9. Computational specification

An `Action` can include: actor, target, preconditions, required permissions, expected effects, cost, risk, reversibility, and execution interface. An `Outcome` can include: observed effects, unexpected effects, success criteria, evidence, and timestamps. A `Plan` can include dependencies, alternatives, stop conditions, and recovery strategies.

Core invariants:

- Check authorization independently of technical capability.
- Distinguish proposed, approved, executing, completed, and verified actions.
- Do not assume an action succeeded without observation.
- Preserve auditability for consequential operations.
- Prefer reversible experiments when uncertainty is high.
- Replan when the environment changes materially.

## 10. Example: repairing a digital habitat

A habitat agent observes an unresponsive water-control simulation. Se detects the failed signal; Si recalls previous faults; Ne proposes several repair routes; Ni anticipates systemic effects; Ti checks the dependency graph; Te prepares a test and rollback plan; Fi verifies alignment with its stewardship objectives; Fe coordinates with resident agents affected by the repair. It runs a reversible diagnostic, evaluates results, then requests authorization for any consequential change.

## 11. From individual to collective agency

A habitat can be modeled as an agent when it possesses persistent state, monitoring, goals or regulatory objectives, and a mechanism for coordinated action. Its constituent agents retain their own identities and may have conflicting values. Collective agency does not erase individual agency.

## Thesis

> Agency is the situated capacity to transform possible outcomes into actual consequences through authorized, informed, value-sensitive interaction with an environment, while remaining responsive to feedback and to the agency of others.

## Connections

**RCO** defines entities, relations, and environments. **RCE** grounds decisions in evidence. **RCA** defines significance and legitimate constraints. **RCP** implements action and returns its consequences to the other three domains.

## Intellectual context

This proposal relates to affordance theory, control theory, reinforcement learning, planning, cybernetics, and multi-agent systems. Its NTFS mapping is a conceptual design, not a scientific demonstration of eight discrete action faculties.
