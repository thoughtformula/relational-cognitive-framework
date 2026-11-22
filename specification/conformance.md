# Exchange and conformance

## Exchange format

A bundle is a JSON object containing `rcf_version: "0.2.0"`, `namespace: string`, `records: Record[]`, and optional `external_refs: [{id: Id, type: string}]`. External declarations identify known referents, not their content or authorization. External IDs MUST be unique and MUST NOT collide with bundle records. Invariants requiring external data that cannot be inspected MUST be reported as unverified. For a self-contained bundle, all references resolve locally. Record order is not semantically significant.

The field tables in each domain are the normative shape contracts. Every field is required unless marked optional; unknown unnamespaced fields are invalid. A receiver MUST reject malformed JSON and unsupported record types, or report them as unsupported without treating them as validated. Receivers MUST validate required fields, primitive and enum types, reference targets, shared and domain-specific invariants, and semantic scope where defined. Validity of a record is not proof of the truth of a represented proposition.

## Conformance classes

- **Record producer** emits records matching the declared domain contracts and preserves provenance and scope.
- **Bundle validator** checks structural, cross-reference, temporal, and graph invariants. It MUST distinguish invalid, unsupported, and unverified data; it MUST NOT claim to have validated external authority or truth when it has not.
- **Domain consumer** preserves semantic distinctions and follows applicable domain invariants; it declares which domains and record types it supports.

An implementation can declare multiple classes. A transport, storage format, or programming language alone does not establish conformance. Execution and algorithmic conformance are deferred to 0.3 and executable reference tests to 0.4. The illustrative JSON and [scenario matrix](../examples/conformance.md) provide acceptance fixtures for this release.

## Versioning

0.x versions are experimental and may revise contracts. Producers MUST identify their version; consumers MUST NOT assume compatibility of a different version. Migration SHOULD preserve identity, provenance and historical records. No extension may redefine a standard field. Documentation-only additions that do not change semantics may be patch releases.
