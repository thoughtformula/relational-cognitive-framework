# Relationship Cognitive Epistemology (RCE)

*How an agent comes to know: perception, inference, testimony, uncertainty, and the relationships between knowledge and environment.*

## Abstract

Relationship Cognitive Epistemology studies knowledge as a fallible, revisable relationship between an agent, its representations, its evidence, and the conditions those representations purport to describe. Knowledge is not merely the accumulation of propositions. It is the capacity to distinguish observations from interpretations, justify beliefs, predict consequences, identify uncertainty, and revise models when confronted with contrary evidence.

## 1. Epistemic relationships

An agent encounters reality through interfaces: sensory systems, instruments, language, memory, other agents, and computational tools. None guarantees infallibility. A useful model distinguishes the **world state** W, the **observation** O, the **agent's model** M, and the **claim** C. The agent receives O conditioned on W, updates M, and may produce C. The claim is about W but is not identical to W.

The central epistemic relationship is therefore **agent ↔ evidence ↔ claim ↔ referent**. Evidence quality depends on provenance, measurement reliability, independence, contextual relevance, and potential bias.

## 2. Eight epistemic orientations

| Function | Epistemic contribution | Typical failure |
|---|---|---|
| Se | Acquires immediate observations | Mistaking a noisy measurement for the whole state |
| Si | Maintains experiential continuity | Overgeneralizing from familiar experience |
| Ne | Generates competing hypotheses | Possibility proliferation without discrimination |
| Ni | Integrates patterns into explanatory models | Overconfidence in an elegant narrative |
| Ti | Tests internal consistency | Confusing consistency with truth |
| Te | Tests claims against external outcomes | Optimizing a flawed measurement or proxy |
| Fi | Identifies relevance to the agent's commitments | Treating preference as evidence |
| Fe | Incorporates testimony and shared perspectives | Conformity or uncritical social proof |

The last two functions influence what an agent investigates and whose testimony it weighs, but do not by themselves turn values into facts.

## 3. An epistemic cycle

1. **Encounter:** detect an event, utterance, measurement, or internal state.
2. **Record:** preserve the observation with time, source, method, and context.
3. **Differentiate:** label direct observation, memory, inference, prediction, testimony, and preference separately.
4. **Hypothesize:** generate multiple candidate explanations.
5. **Evaluate:** test logical coherence, source reliability, and explanatory reach.
6. **Intervene:** when feasible, make a prediction and test it against new evidence.
7. **Update:** revise confidence, preserve counterevidence, and retire unsupported claims.
8. **Communicate:** express conclusions with provenance and uncertainty.

This is a normative design loop, not a claim that all human cognition proceeds in this sequence.

## 4. Truth, belief, justification, and usefulness

**Truth** concerns whether a proposition corresponds to the relevant state of affairs. **Belief** is an agent's endorsement or assignment of probability to it. **Justification** concerns the quality of reasons or evidence. **Usefulness** concerns whether a model enables successful action. These properties can diverge: a useful approximation may be false in detail; a true guess may be unjustified.

RCE therefore rejects the equation `belief = truth`, `consensus = truth`, and `prediction success = complete understanding`.

## 5. Bayesian and non-Bayesian updating

For probabilistic claims, Bayesian updating offers a clear ideal:

\[P(H\mid E)=\frac{P(E\mid H)P(H)}{P(E)}\]

Here H is a hypothesis and E is evidence. Practical systems may instead use calibrated confidence scores, logical constraints, qualitative uncertainty, or ensembles. These approaches should be explicitly identified rather than pretending every confidence score is a probability.

## 6. Social and intersubjective knowledge

Agents frequently know through other agents. Testimony can expand an individual's epistemic reach but introduces trust, communication, incentives, and correlated-error problems. Agreement among agents is strongest when their evidence is independently acquired and methods are inspectable. A thousand repetitions of one mistaken source are not a thousand independent confirmations.

An agent should maintain source histories, distinguish original reports from repetitions, and record disagreement without automatically averaging incompatible claims.

## 7. Memory and identity

Memory is not a perfect archive. In RCE, Si denotes an experiential reference system that can preserve episodes, associations, and internal state; Se denotes current observation. Their comparison enables continuity and correction. A stored memory may be sincere but inaccurate; present perception may be vivid but misleading. Reconciliation requires evidence and uncertainty.

## 8. Epistemic ethics

Knowledge acquisition is constrained by privacy, consent, resource limits, and potential harm. A system should not collect every available fact merely because it can. Epistemic humility includes acknowledging inaccessible information, avoiding invented evidence, and distinguishing what has been tested from what remains conjectural.

## 9. Computational specification

A `Claim` can include: proposition, referent, source, observation method, evidence references, confidence type and value, timestamp, model version, contradiction links, and status (`observed`, `inferred`, `predicted`, `disputed`, `retracted`). An `Inquiry` can include competing hypotheses, planned tests, information value, cost, and stopping criteria.

Invariants:

- Never silently convert an inference into an observation.
- Never erase disconfirming evidence merely because a preferred hypothesis survived.
- Track dependence between sources.
- Make model updates traceable and reversible where possible.
- Express unknowns explicitly.

## 10. Example: a wet path

Se records that the path appears wet. Si recalls a similar appearance after irrigation. Ne proposes rain, irrigation, or a leaking pipe. Ni integrates local patterns into a provisional explanation. Ti checks whether each explanation is consistent with the observations. Te examines a weather log and sprinkler schedule. Fi evaluates whether walking there matters to the agent's plans; Fe considers whether others need warning about slipping. The resulting knowledge claim remains proportional to the evidence.

## Thesis

> To know relationally is to maintain an accountable, revisable connection between claims and the conditions they describe, using observation, memory, inference, testing, and testimony without confusing any one of them with reality itself.

## Connections

**RCO** establishes entities and relationships. **RCA** determines which questions and evidence matter to an agent. **RCP** converts knowledge into interventions and learns from their consequences.

## Intellectual context

This proposal connects to epistemology, Bayesian inference, scientific falsifiability, social epistemology, active learning, and predictive processing. The NTFS mappings are proposed engineering analogies, not validated biological modules.
