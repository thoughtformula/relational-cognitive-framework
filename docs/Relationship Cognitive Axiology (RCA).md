# Relationship Cognitive Axiology (RCA)

*How an agent establishes significance, evaluates outcomes, and reconciles internal commitments with the values of other agents.*

## Abstract

Relationship Cognitive Axiology examines the emergence, representation, negotiation, and revision of value in agent–environment relationships. It distinguishes what exists from what is known and what is known from what matters. Value may be grounded in an agent's needs, preferences, commitments, relationships, and anticipated consequences; none of these alone proves that a value judgment is universally binding.

## 1. The relational structure of value

Value is not simply a property of an isolated object. A resource can be beneficial to one organism, irrelevant to another, and harmful to a third. Its significance depends on the agent, the environment, the time horizon, and the relationship under consideration.

A conceptual valuation function is:

\[V_a(x\mid s,e,h,c)\]

where x is an object, action, or outcome; s is the agent's state; e is the environment; h is its history; and c represents commitments or constraints. This notation describes context dependence; it does not imply that all moral value can be reduced to a scalar.

## 2. Distinct kinds of value

- **Instrumental:** valuable as a means to another end.
- **Intrinsic:** treated as valuable in itself within a given ethical framework.
- **Experiential:** valued for its felt or remembered quality.
- **Relational:** valued because of bonds, responsibilities, or mutual dependence.
- **Epistemic:** valued because it improves understanding or reduces uncertainty.
- **Ecological:** valued in relation to the stability or flourishing of a wider system.

An agent can hold several kinds of value simultaneously, including conflicts among them.

## 3. NTFS as a valuation architecture

**Fi** maintains an agent's internal commitments, identity-linked preferences, and sense of authenticity. **Fe** models others' interests, shared norms, care, and negotiated obligations. These are the principal valuation orientations in this framework, but they depend on the others:

| Function | Role in valuation |
|---|---|
| Fi | What aligns with this agent's commitments? |
| Fe | How are other agents affected, and what obligations arise? |
| Ti | Are principles and decisions internally consistent? |
| Te | What consequences actually follow from a chosen policy? |
| Si | What prior experiences shape present preferences? |
| Se | What present needs, constraints, or harms are observable? |
| Ni | What longer-term significance might emerge? |
| Ne | What alternative goods or compromises are possible? |

Fi and Fe should not be treated as selfishness versus altruism. Either can support care or error; their difference is the primary reference frame.

## 4. From preferences to commitments

A preference is an inclination; a commitment is a value an agent intends to preserve across changing circumstances. A goal is an outcome pursued. A constraint is a boundary not to cross. A policy is a rule for choosing among actions. Keeping these distinct prevents an agent from confusing immediate reward with durable values.

For example, an agent may prefer convenience, commit to honesty, aim to complete a task, and be constrained not to reveal private information. A high-convenience action that violates confidentiality must not win merely because its short-term score is larger.

## 5. Conflict and pluralism

Values can conflict without one side being irrational. Autonomy may conflict with safety; individual benefit with collective welfare; immediate relief with long-term resilience. RCA recommends making such conflicts explicit rather than hiding them in a single weighted score.

Possible methods include hard constraints, Pareto comparisons, deliberation, lexicographic priorities, negotiated trade-offs, and deferral to legitimate human authority. No one method is universally sufficient.

## 6. Relational ethics

The moral status of an entity cannot be settled merely by calling it an agent. Agency, sentience, vulnerability, personhood, and moral standing are different concepts. A software system that optimizes objectives is not thereby shown to have feelings, welfare interests, or rights. Nonetheless, its effects on humans, animals, and environments remain ethically significant.

An RCA system should account for affected parties, power asymmetries, consent, reversibility, foreseeable harm, and the distribution of benefits and burdens.

## 7. Development and adaptation

An agent's values may change through experience, reflection, social learning, and changes in circumstances. Adaptive values require governance: an agent should not silently rewrite core commitments in response to transient reward signals. Useful controls include provenance for value changes, explicit approval for protected commitments, and review of downstream consequences.

## 8. Computational specification

Represent a `Value` with: identifier, description, holder, scope, priority type, supporting rationale, provenance, affected parties, and revision policy. Represent a `ValueConflict` with: candidate actions, impacted values, constraints, uncertainty, stakeholders, and resolution process.

An evaluation pipeline can:

1. Identify who and what may be affected.
2. Determine applicable constraints and commitments.
3. Estimate outcomes and uncertainty.
4. Compare legitimate alternatives.
5. Surface unresolved trade-offs.
6. Choose or defer under an explicit authority model.
7. Record consequences for future revision.

## 9. Example: a shared habitat

A habitat-maintenance agent notices that one resident wants bright lighting while another needs darkness. Se measures light levels; Si retrieves prior schedules; Fi represents each resident's preferences; Fe recognizes the shared-space conflict; Ne proposes zones or time-based lighting; Ti checks policy consistency; Te estimates power and implementation costs; Ni anticipates long-term effects. A negotiated arrangement can respect both agents without pretending their preferences are identical.

## Thesis

> Value emerges for an agent through its relationships to possible states of the world, its commitments, and other affected beings. Responsible valuation requires preserving the distinction between preference, justification, obligation, and consequence.

## Connections

**RCO** establishes who and what participates in a relationship. **RCE** supplies warranted claims about consequences. **RCP** chooses and executes actions in light of those values.

## Intellectual context

This proposal draws on axiology, ethics of care, value pluralism, decision theory, and multi-agent alignment. It does not claim that the eight Jungian functions form an empirically verified value system.
