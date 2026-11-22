# Relational Cognitive Framework (RCF)
## Formal Ontology and Computational Architecture
**Version:** 0.2.0 — formal vocabulary and domain contracts

The four companion essays establish the conceptual foundation. Version 0.2.0 adds the language-independent [normative specification](specification/README.md), a [worked exchange example](examples/garden.json), and [conformance scenarios](examples/conformance.md). The normative specification takes precedence over illustrative prose and Python snippets when defining interoperable records.

### Companion essays

- [RCO — Ontology](docs/Relationship%20Cognitive%20Ontology%20%28RCO%29.md)
- [RCE — Epistemology](docs/Relationship%20Cognitive%20Epistemology%20%28RCE%29.md)
- [RCA — Axiology](docs/Relationship%20Cognitive%20Axiology%20%28RCA%29.md)
- [RCP — Praxeology](docs/Relationship%20Cognitive%20Praxeology%20%28RCP%29.md)

## Abstract
RCF integrates Relational Cognitive Ontology (RCO), Epistemology (RCE), Axiology (RCA), and Praxeology (RCP) into a recursive model of agents embedded in environments. Entities and relationships establish a world state; observations and inferences produce beliefs; values evaluate possible states; and actions transform states. The eight NTFS cognitive orientations are optional processing capabilities spanning these domains, not validated psychological modules or mandatory stages.

## 1. Foundational commitments
1. **Realism without omniscience.** A world state is not identical to any agent's representation of it.
2. **Relational context.** Entity identity, capabilities, and significance may depend on relations and context, without requiring that all existence is relationship-dependent.
3. **Agency is graded.** An agent is a bounded system capable of state-sensitive regulation or action. Cognition and consciousness are not prerequisites.
4. **Knowledge is fallible.** Claims must distinguish observation, inference, prediction, preference, and report; uncertainty and provenance matter.
5. **Values are plural.** Preferences, commitments, and interpersonal norms may conflict; no single scalar utility is required.
6. **Actions are consequential.** Actions may modify the environment, other agents, and the acting agent itself.
7. **Recursive composition.** A system may be an environment at one level and an agent at another only if it meets an explicit agency criterion.

## 2. Core ontology
- **Entity:** An identifiable participant with a type, state, and optional persistence criterion.
- **Environment:** A contextual boundary defining accessible entities, relations, constraints, and dynamics.
- **Relationship:** A typed, directed or undirected, potentially time-bounded association among two or more entities. May have attributes, evidence, permissions, and history.
- **State:** A time-indexed assignment of properties to entities and relationships.
- **Event:** A record of an occurrence or state transition, with causal attribution distinguished from mere temporal correlation.
- **Agent:** An entity with a policy or regulatory process capable of selecting or producing actions contingent on state or information.
- **Capability:** A bounded operation an agent can perform, subject to permissions and environmental constraints.

A relationship is first-class: `Relationship(id, kind, participants, attributes, valid_interval, provenance)`. Hyper-relations with more than two participants are permitted.

## 3. Four domain contracts
### RCO — What exists?
**Inputs:** environment definitions, entities, state transitions. **Outputs:** typed entity/relation graph and world snapshots. **Invariants:** stable identifiers, explicit scope, temporal versioning, referential integrity where appropriate.

### RCE — What is believed, and why?
**Inputs:** observations, testimony, memory, hypotheses. **Outputs:** claims/beliefs with source, evidence, confidence, temporal scope, and defeaters. **Invariants:** belief is not world truth; claims must retain provenance; confidence is calibrated to evidence rather than asserted certainty.

### RCA — What matters?
**Inputs:** beliefs, internal preferences, commitments, norms, stakeholders, anticipated consequences. **Outputs:** context-dependent valuations, priorities, conflicts, and constraints. **Invariants:** distinguish descriptive claims from normative commitments; preserve conflicts; do not silently equate agent preference with universal good.

### RCP — What can be done?
**Inputs:** goals, valuations, capabilities, predicted outcomes, constraints. **Outputs:** plans, authorized actions, outcomes, feedback. **Invariants:** check preconditions and permissions; record effects and failures; distinguish intended from observed outcomes.

## 4. Cognitive function interfaces
The eight NTFS orientations are interpretive abstractions, not an exhaustive or scientifically established decomposition of human cognition.

| Orientation | Processing role | Typical artifact |
|---|---|---|
| Se | Register present external conditions | Observation |
| Si | Contextualize against embodied/episodic experience | Memory comparison |
| Ne | Generate alternative possibilities | Hypothesis set |
| Ni | Synthesize patterns and trajectories | Predictive model |
| Ti | Test internal conceptual consistency | Logical assessment |
| Te | Test operational and empirical effectiveness | Experiment/result |
| Fi | Evaluate against internal commitments | Personal valuation |
| Fe | Evaluate relational and stakeholder effects | Social valuation |

These functions may execute concurrently or recursively. Each should expose `inputs`, `outputs`, `evidence`, `limitations`, and `confidence` where applicable. None guarantees truth or moral correctness.

## 5. Formal dynamics
Let a world state be `W_t`, agent internal state `I_a,t`, observation function `O_a`, belief update `U_a`, valuation `V_a`, policy `π_a`, and transition function `T`.

- `o_a,t = O_a(W_t, I_a,t)`
- `B_a,t+1 = U_a(B_a,t, o_a,t, memory_a, evidence_a)`
- `v_a,t = V_a(B_a,t+1, commitments_a, stakeholders_a)`
- `action_a,t = π_a(B_a,t+1, v_a,t, capabilities_a, constraints_t)`
- `W_t+1 = T(W_t, {action_a,t}, exogenous_events_t)`
- `I_a,t+1 = Adapt(I_a,t, action_a,t, observed_outcome_a,t)`

These are interface-level equations, not assumptions that observations are perfect, actions deterministic, or values reducible to a number. Concurrent agents may act on stale or conflicting beliefs.

## 6. Historical illustrative data contracts (Python, 0.1.0)

These examples illustrate the original architecture, not the normative 0.2 exchange format. In particular, `Claim.status` in this historical sketch denotes acquisition method; 0.2 separates acquisition, assertion lifecycle, and agent-specific epistemic stance. See [terminology](specification/terminology.md) and [epistemology](specification/epistemology.md) for the current contracts.
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal

@dataclass(frozen=True)
class Entity:
    id: str
    kind: str

@dataclass(frozen=True)
class Relationship:
    id: str
    kind: str
    participants: tuple[str, ...]
    attributes: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class Claim:
    proposition: str
    source_ids: tuple[str, ...]
    status: Literal['observed', 'reported', 'inferred', 'predicted']
    confidence: float | None = None
    observed_at: datetime | None = None

@dataclass(frozen=True)
class Valuation:
    subject_id: str
    criterion: str
    judgment: Any
    stakeholder_ids: tuple[str, ...] = ()

@dataclass(frozen=True)
class Action:
    actor_id: str
    capability: str
    target_ids: tuple[str, ...]
    parameters: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class Outcome:
    action: Action
    succeeded: bool
    observed_changes: tuple[str, ...]
    evidence_ids: tuple[str, ...] = ()
```
These are illustrative contracts. A production implementation should add schema validation, versioning, permissions, causal/event semantics, and a typed proposition language rather than relying on free-text claims.

## 7. Worked example: a shared garden
1. **RCO:** A garden, plants, two people, and a water supply exist in a local environment; each has states and relationships.
2. **RCE / Se:** Agent A observes dry soil. **Si:** It recalls prior dry periods. **Ne:** It considers drought, sensor error, or a broken irrigation line. **Ni:** It predicts plant stress. **Ti:** It checks whether the hypotheses cohere. **Te:** It measures moisture and tests irrigation.
3. **RCA / Fi:** Agent A values plant health. **Fe:** It accounts for Agent B's water-use agreement and the community's conservation goals. The priorities may conflict.
4. **RCP:** Agent A chooses an authorized, limited watering action, records water used, and checks the plants afterward.
5. **Feedback:** The observed outcome updates beliefs, valuations, and future policy. The garden's state changes, but a successful intention is not assumed to imply a successful outcome.

## 8. Architectural separation
```
world/           entities, relationships, snapshots, event history
knowledge/       claims, evidence, provenance, uncertainty
values/          preferences, norms, commitments, trade-offs
agency/          capabilities, goals, planning, authorization, outcomes
cognition/       optional NTFS-inspired processing strategies
runtime/         scheduling, message passing, persistence, instrumentation
```
Dependencies should point toward stable shared contracts; avoid circular imports between domains. The runtime coordinates interaction without owning domain semantics. Cognitive strategies can be swapped independently of world representation.

## 9. Testable propositions
- Provenance-aware agents should more reliably distinguish observation from inference than agents without provenance tracking.
- First-class relationships should improve modeling of multi-party dependencies relative to property-only entity models for suitably relational tasks.
- Explicitly representing value conflicts should make stakeholder trade-offs more inspectable than a single opaque score.
- Feedback and outcome logging should improve error correction compared with action-only logs.

Each proposition needs an operational benchmark, baseline, and falsification criterion. These are research hypotheses, not established results.

## 10. Open questions
1. What is the minimum threshold for agency, and does it require goals or merely regulation?
2. Which relationships are ontologically primitive versus derived from state?
3. How should conflicting observations and epistemic trust be resolved?
4. Can valuation be compared across agents without assuming a universal scale?
5. How are power, consent, and irreversible actions represented?
6. When can a collective environment legitimately be modeled as an agent?
7. What empirical evidence would justify retaining the NTFS labels rather than replacing them with domain-specific names?

## 11. Suggested development milestones
**0.1 — Conceptual framework:** four essays and NTFS-inspired processing model.

**0.2 — Formal vocabulary and domain contracts:** identity, scoped relationships, propositions, evidence, values, actions, and cognitive operations; interoperable records and conformance scenarios.

**0.3 — Dynamics:** transition, revision, deliberation, action lifecycle, feedback and concurrent operations.

**0.4 — Reference implementation:** executable conformance tests and a minimal implementation.

**0.5 — Multi-agent cognition:** communication, shared contexts, authority, negotiation and collective agency.

**0.6 — Research:** experimental learning architectures, baselines, benchmarks and empirical evaluation.

**1.0 — Stable specification:** independently implementable, versioned contracts and demonstrated interoperability.

## 12. Scope and limitations
RCF is a proposed conceptual and engineering framework. It does not establish that reality is entirely relational, that Jungian functions are neurobiologically discrete, or that simulated valuations entail subjective experience. Its practical merit depends on explanatory precision, implementation simplicity, and measurable performance against alternatives.
