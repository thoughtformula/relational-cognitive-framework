# 0.2 conformance scenarios

The [garden fixture](garden.json) is a self-contained illustrative exchange. Domain predicates are interpreted as follows: `soil_dry(soil)` means the soil is below 15% moisture in the specified interval; `soil_moisture_at_least_percent(soil, threshold)` means moisture meets or exceeds the threshold. The scenario assumes the steward is authorized to decide watering limits and has approved a two-litre intervention; an actual consumer must establish that authority independently. Fixture timestamps are UTC and illustrative.

## Expected interpretations

1. The soil entity retains its identity across both snapshots. Its past state is not overwritten by the second snapshot.
2. The stewardship relationship is n-ary; the gardeners occupy the same role but refer to different entities.
3. The positive and negative dry propositions are opposites at matching scope. Alice and Bob may disagree without mutating the world state.
4. Alice suspends her belief after contradictory evidence, then accepts it after another measurement. The original evidence and both prior beliefs remain in the bundle. No probability is invented for an ordinal or unknown confidence.
5. The opposing valuations use different values and holders; resolving the conflict does not erase disagreement or make water conservation worthless.
6. The capability and grant are distinct. Approval occurs before execution, targets match the grant, and execution is completed before verification. The measurement supports the goal condition in the specified interval. Authority is a scenario assumption, not inferred from `permission` alone.
7. The cognitive operation records a mixed orientation and produces ordinary domain records, not privileged truths.

## Negative cases

Each row describes an independent modification of the fixture. A validator or relevant domain consumer must reject or report the resulting violation; errors involving authority or external state may require external verification rather than structural rejection alone.

| Case | Modification | Expected result |
|---|---|---|
| Identity | Duplicate `soil` ID | Invalid, even if data matches |
| Reference | Change relationship participant to nonexistent ID | Invalid unresolved reference |
| Relationship | Repeat same participant and role | Invalid duplicate participation |
| Temporal | Set `soil-before` end before its start | Invalid interval |
| Temporal | Record `reading` before its acquisition | Invalid chronology |
| Scope | Change `not-dry` to a later, disjoint interval | Valid record; no same-time contradiction |
| Source | Make `support` depend on itself | Invalid cyclic justification |
| Revision | Make `alice-belief-2` supersede Bob's belief | Invalid cross-agent revision |
| Evidence | Change `counter` proposition to `not-dry` without changing the referencing beliefs | Invalid evidence scope for those beliefs |
| Confidence | Set ordinal value to `0.9` | Invalid confidence type |
| Valuation | Replace hard constraint handling with a scalar penalty | Nonconforming behavior |
| Authority | Remove the grant from `water-action` or expire it before approval | Approval must be blocked or separately authorized; capability alone is insufficient |
| Outcome | Mark the goal achieved with no supporting observation | Nonconforming verified outcome |
| Cognitive operation | Add orientation `telepathy` without extension semantics | Invalid orientation |

## Deferred conformance

0.2 defines these expected semantics without prescribing the algorithms used to detect or resolve arbitrary domain contradictions, authorize an external authority, perform empirical tests, or schedule concurrent operations. These are future dynamics and reference implementation work, not implied by this fixture.
