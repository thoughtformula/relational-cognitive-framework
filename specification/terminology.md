# Common terminology and contracts

## Normative language

MUST and MUST NOT identify requirements; SHOULD identifies a recommended default with documented exceptions; MAY identifies an option. Tables specify required fields unless marked optional. Records are JSON objects; strings are Unicode; arrays are ordered unless a field is described as a set. Null is not equivalent to an omitted field or an unknown value unless explicitly specified.

## Core types

| Type | Contract |
|---|---|
| `Id` | Nonempty case-sensitive, opaque string unique within an exchange namespace; stable across renames and revisions |
| `Ref` | The exact `id` of another record; references MUST resolve in the bundle or a declared external registry |
| `Instant` | UTC timestamp in `YYYY-MM-DDTHH:MM:SS[.fraction]Z`, with valid calendar values |
| `Interval` | Object `{start: Instant or null, end: Instant or null}`; start inclusive, end exclusive; null means unbounded; if both bounds known, start MUST precede end |
| `JsonValue` | JSON-compatible null, boolean, finite number, string, array, or object; no duplicate keys or nonfinite numbers |
| `Confidence` | Tagged object `kind: unknown`, `kind: ordinal, value: low/medium/high`, or `kind: probability, value: number in [0,1], calibration: string` |

Probability requires an explicit calibration or model description; ordinal levels do not imply probabilities. Unknown confidence is explicit. Neither confidence, consensus, nor model coherence establishes truth.

## Record envelope

Every record MUST have `id: Id` and `type: string` as defined by its domain. Records are immutable once accepted; a correction or revision creates a new record and, where applicable, a `supersedes` reference of the same type. An exchange bundle MUST NOT contain two records with the same ID, including identical duplicates. Domain types distinguish identity records from assertions, evaluations, and events. References do not confer permission to read or mutate their targets.

Record-specific fields determine time semantics:

- `valid_during`: the interval to which a statement or association applies; omission means no temporal scope was specified, not that it is timeless.
- `observed_at`: when an observation was acquired; omitted if unknown.
- `recorded_at`: when a record became available to the recording agent/system.
- `occurred_at`: when an event occurred, if known.

The original source's event time MUST NOT be silently replaced with the receiving agent's recording time. When both acquisition and recording times are known, recording MUST NOT precede acquisition. Delayed reports and historical observations are allowed. Supersession changes which record is current, not what historically existed.

## Scope and interoperability

`environment_id` references an environment that defines the context of a record. Identity is global within a bundle; the same entity may participate in multiple environments. A reference can be valid without its target being visible to every agent. A proposition about an unverified external referent MAY use an opaque symbol rather than asserting existence.

Extensions MUST use namespaced keys of the form `x-<namespace>-<name>` and MUST NOT alter the meaning of a required field. An implementation MUST declare supported domain types and version. No automatic conversion between norms, claims, permissions, and world state is implied.
