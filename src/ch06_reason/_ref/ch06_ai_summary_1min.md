# ch06_reason — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 06 — `ch06_reason`**
**"Reasons and Facts — the logic engine that decides whether a Reason is active"**

---

## 2. Prompt Used to Build This

From `ch06_ref.json`:
> "Describes what a reason and a fact is; if the reasons match the facts, the Reason.reason_active = True"

Ontology note:
> "ReasonUnits mated to FactUnits produce justifications. If a task must be justified the Reasons and Facts must match."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `get_empty_dict_if_None` for safe initialization of cases dictionaries.
- **ch05_rope**: `RopeTerm`, `KnotTerm`, `default_knot_if_None`, `is_heir_rope`, `rebuild_rope`, `replace_knot`, `find_replace_rope_key_dict` — all rope operations are central here. Both `FactUnit` and `ReasonUnit` use `RopeTerm` as their identity keys (`fact_context`, `reason_context`). The `is_in_lineage` check in `CaseUnit` uses `is_heir_rope` to test whether a fact's state rope is an ancestor or descendant of the case's required state rope.
- **ch02_allot**, **ch03_contact** semantic types are re-exported through `ch06_semantic_types.py`. Two new float subtypes are introduced: `ReasonNum` and `FactNum`.

---

## 4. Summary of What This Chapter Does

`ch06_reason` implements the **conditional activation logic** of keg — the mechanism by which a node object declares what conditions must be true for it to be considered active.

**`FactUnit` / `FactHeir` / `FactCore`**
A `FactUnit` is a statement about the world: it says that a context (identified by a `RopeTerm` called `fact_context`) is currently in a particular state (`fact_state`), optionally within a numeric range (`fact_lower` to `fact_upper`). Facts are supplied externally to the person and flow down a tree as `FactHeir` objects. A `FactHeir` can be further narrowed by child `FactUnit` moldations as it propagates.

**`CaseUnit`**
A `CaseUnit` is a single condition within a reason. It specifies:
- `reason_state`: the rope state that must be active for this case to pass.
- Optionally `reason_lower` / `reason_upper`: a numeric range the fact must be within.
- Optionally `reason_divisor`: enables **cyclic/modular reasoning** — the fact value is taken modulo the divisor before comparing to the range. This allows conditions like "every 7 rotations of the earth" or "every quarter."

`CaseUnit.set_case_active(factheir)` evaluates whether the supplied fact satisfies this case's condition, setting both `case_active` and `case_task` (whether the case indicates there is still work remaining within the range).

**`CaseActiveFinder`**
A helper dataclass that handles the complex modular arithmetic for cyclic range checks. It computes remainders of fact bounds against the divisor and tests multiple overlap scenarios to determine whether the cyclic condition is currently satisfied.

**`ReasonUnit` / `ReasonHeir`**
A `ReasonUnit` groups one or more `CaseUnit`s under a shared `reason_context` rope. It can also carry `active_requisite` — a boolean that, if set, requires the *parent node's active state* to match before this reason counts. `ReasonHeir.set_reason_active(factheirs)` evaluates all cases against the current fact set and sets `reason_active = True` if any case passes (or if `active_requisite` is satisfied). It also computes `reason_task` to indicate whether the node is not yet fully complete within the fact's range.

This chapter delivers the core inference engine: given a set of real-world facts and a set of declared conditions, it determines what is currently true and what still needs to be done.
