# ch09_person_atom — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 09 — `ch09_person_atom`**
**"PersonAtom — the irreducible unit of change for a PersonUnit, enabling versioning and delta-based updates"**

---

## 2. Prompt Used to Build This

From `ch09_ref.json`:
> "Defines PersonAtoms: Irreducible units of change for a PersonUnit."

Ontology note:
> "Any difference between PersonUnits can be expressed as AtomUnits."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `get_empty_dict_if_None` for safe dict initialization.
- **ch03_contact**: `contactunit_shop`, `awardunit_shop` — atom execution reconstructs or modifies contacts and awards.
- **ch05_rope**: `create_rope`, `get_parent_rope`, `get_tail_label` — rope operations reconstruct plan paths from atom key arguments.
- **ch06_reason**: `factunit_shop` — fact atoms reconstruct fact objects.
- **ch07_plan**: `planunit_shop` — plan atoms reconstruct plan nodes.
- **ch08_person_logic**: `PersonUnit` is the object that atoms are applied to. `person_attr_exists` and `person_get_obj` (from `person_tool.py`) are used during atom execution to check and retrieve the current state before applying a change.

Ch09's `ch09_semantic_types.py` re-exports types from ch03, ch05, ch06 with no additions of its own — it is a pass-through semantic layer.

---

## 4. Summary of What This Chapter Does

`ch09_person_atom` defines `PersonAtom` — a minimal, self-describing record of a single create, update, or delete operation on a `PersonUnit`. The concept is analogous to a database transaction log entry or a git commit diff at the finest granularity.

**`PersonAtom` structure:**
- `dimen` — the "dimension" or table being modified. Valid dimensions (defined in `atom_config.json`) include: `personunit`, `person_contactunit`, `person_contact_membership`, `person_planunit`, `person_plan_awardunit`, `person_plan_factunit`, `person_plan_reasonunit`, `person_plan_reason_caseunit`, `person_plan_healerunit`, `person_plan_laborunit`.
- `crud_str` — one of `"INSERT"`, `"UPDATE"`, `"DELETE"`.
- `jkeys` — the primary key fields that identify the target object (e.g. `plan_rope` for a plan, `contact_name` for a contact).
- `jvalues` — the attribute fields being set or changed.
- `atom_order` — an integer determining the correct application order (e.g. a plan must exist before its reasons can be inserted).

**Validation:** `is_valid()` checks that `crud_str` is legal, `jkeys` matches the schema for the given `dimen`, and `jvalues` is a subset of the allowed value fields.

**`modify_person_with_personatom(person, atom)`** is the execution function. It dispatches by `dimen` to the appropriate low-level modification function (e.g. `_modify_person_insert_planunit`, `_modify_person_delete_contactunit`), which directly calls the relevant `PersonUnit` setter methods.

**`jvalues_different(dimen, x_obj, y_obj)`** compares two objects of a given dimension to determine what atom(s) would need to be generated to transform one into the other — the basis for diff-generation between two `PersonUnit` states.

Together, `PersonAtom`s form a complete, ordered, reversible description of any transformation between two `PersonUnit` states. This chapter is the foundation for future chapters that use PersonAtoms to communicate indivisible data.
