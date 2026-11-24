# RCF 0.3 — Dynamics and execution conformance

0.3 extends 0.2 record conformance with *behavioral* obligations. It is still a formal specification, not a complete reference runtime.

## Profiles

| Profile | Required behavior |
|---|---|
| `rcf-0.3-records` | Validate all 0.3 new record shapes, references, temporal order and cross-domain invariants, preserve 0.2 distinctions |
| `rcf-0.3-revision` | Additionally supply named revision policy, provenance-preserving history, conflict handling and explicit limitations |
| `rcf-0.3-dynamics` | Additionally validate action lifecycles, context freshness, applicable authorization, transition receipts, reconciliation and feedback |
| `rcf-0.3-concurrent` | Additionally enforce safe concurrent application or explicit rejection/revalidation and maintain acyclic partial-order evidence |

An implementer MUST name the profiles it supports; record-only parsing is not evidence of execution or multi-agent safety. A profile validator MUST distinguish `valid`, `invalid`, `unsupported`, and `unverified` findings. It MUST NOT assert externally granted authority, world truth, sensor calibration, or causal effectiveness from records alone.

## Exchange version and migration

A 0.3 exchange bundle uses `rcf_version: "0.3.0"`, an opaque `namespace`, and `records`. It MAY declare `external_refs` exactly as in 0.2. All 0.2 record types retain their 0.2 meanings; the new record types are defined by [dynamics](dynamics.md). The `rcf_version` string denotes the **format contract**, not the software implementation version. A 0.2 bundle is not invalid because 0.3 exists. Migrators MUST NOT alter observation origins, past decision inputs, or original action results to make historical records seem compliant with dynamics they never captured.

## Example acceptance

See [dynamics scenarios](../examples/dynamics-conformance.md) and [dynamics fixture](../examples/dynamics.json). A conforming consumer must not infer that any unverified grantor is actually authorized. The example's assumed steward authority is a **fixture premise**, not a structural property established by a `permission` record.

## Minimum test families

1. Valid: belief conflict → suspension → retest revision, with prior beliefs and counterevidence preserved.
2. Valid: selected deliberation → explicitly authorized request → receipt applied → observed outcome and feedback.
3. Valid: concurrent proposals against one snapshot, first applied, second rejected as stale.
4. Invalid: selected deliberation without an actual candidate action; or abstention with a selected action.
5. Invalid: `strategy_run` tied to another agent's context, completed before it started, or claiming a phantom output.
6. Invalid: effectful transition with mismatched agent/environment, or rejected receipt claiming result states caused by the rejected request.
7. Invalid: feedback `matches` based only on a prediction, no observation.
8. Invalid: ordering-edge cycle, self-edge, or unsupported endpoint type.
9. Nonconforming runtime: accepting stale writes or permission merely because a grant record exists.
10. Unverified (not automatically invalid): external grantor authority, transition issuer authenticity, real-world state and measurement independence when the bundle alone provides no decisive evidence.

The companion [checker](../tools/check_dynamics.py) verifies a bounded subset of structural/semantic fixture properties. Its passing result MUST NOT be advertised as independent certification, an authority audit, or a full behavioral implementation.
