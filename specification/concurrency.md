# RCF 0.3 — Concurrency and partial ordering

Concurrent agents may observe stale snapshots, propose incompatible actions, or report independently acquired evidence. RCF does not assume a single clock or a globally ordered world outside a modeled environment authority.

## 1. Happens-before, not wall-clock order

`ordering_edge` declares **program order** (within one execution stream), **dependency** (data/control prerequisite), **serialization** (authority-established commit order), or **communication** (message transfer). An edge asserts that one operation/event happens before another under its declared basis; it does not by itself prove physical causation. Edges form a directed acyclic graph. Independent events remain incomparable even if timestamps differ, since clocks may be unsynchronized.

For a serializable environment with revision `r`, let `Apply(q, W_r)` be an atomic application or rejection at that environment's serialization boundary. Two effectful requests derived from the same snapshot MUST NOT both be assumed valid against `W_r` if the first materially changes the second's preconditions. The service MUST detect and reject/revalidate the stale second request; it MAY serialize both only when effects commute and all constraints remain satisfied.

## 2. Conflict and reconciliation

A conflict is *material* when applying one operation can change the validity or outcome of another. Overlapping targets alone are insufficient to prove conflict (e.g., two independent reads). Different targets do not prove independence where shared resources, quotas, or permissions are affected.

A runtime claiming the concurrency profile MUST:

- Check preconditions and grant validity at an authoritative execution boundary, not only during deliberation.
- Record a transition's result separately from the original request, including rejection or uncertainty.
- Prevent a `rejected` request from generating **authoritative result states** attributed to that request.
- Preserve each agent's own observations and beliefs rather than silently replacing them with global state.
- Prevent duplicate non-idempotent application where an idempotency contract promises exactly-once *effects*; absent such a contract, report uncertainty and reconcile instead of asserting exactly-once delivery.
- Explicitly distinguish observed order, serialized order, and inferred causal relationships.

A client re-planning after a rejected stale request MUST build a new context and new request; a historic decision cannot simply be relabeled with current state.

## 3. Interleaving example

At 09:10, Alice and Bob both read soil snapshot `S0`. Alice requests watering `A`, Bob requests watering `B`, and both proposals appear legal under their respective local views. The environment first applies `A` and emits `S1`. When processing `B`, the environment discovers that its expected snapshot `S0` is stale; it rejects `B` or revalidates the action under updated constraints, rather than applying it on faith. Neither agent's previously sincere belief becomes fraudulent or automatically correct.

## 4. Scheduling and fairness

Scheduling policies MAY prioritize deadlines, resource cost, fairness, or human authority. An implementation MUST declare which guarantees it actually provides. FIFO submission order does not imply execution order; timestamps do not confer authority; starvation-freedom and conflict serializability require independent justification. A processor may leave an uncertain transition `unknown` rather than fabricate a total order.

**Out of scope:** vector-clock wire format, distributed consensus, two-phase commit, fault-tolerant leader election, and a default scheduler. 0.4 can implement one bounded scheduling strategy without making it universal.
