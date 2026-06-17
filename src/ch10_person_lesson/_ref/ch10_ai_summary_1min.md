# ch10_person_lesson — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 10 — `ch10_person_lesson`**
**"LessonUnit and PersonDelta — packaging PersonAtoms into named, ordered change sets that express what was learned"**

---

## 2. Prompt Used to Build This

From `ch10_ref.json`:
> "Tools for the creation and organization of lessons, which are collections of personunit atoms for building complex personunits."

Ontology note:
> "Any PersonUnit change implies something has been learned. The LessonUnit that was learned is made of AtomUnits."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: File I/O (`create_path`, `open_json`, `save_json`, `get_json_filename`) used by `lesson_filehandler.py` to persist lessons to disk.
- **ch03_contact**: `ContactUnit`, `MemberShip` — compared field-by-field in `PersonDelta` when generating contact-level atoms.
- **ch05_rope**: `RopeTerm` — used as keys in nested `PersonDelta` structures, particularly for plan-level atom tracking.
- **ch06_reason**: `FactUnit`, `ReasonUnit` — compared in `PersonDelta` when generating reason and fact atoms.
- **ch07_plan**: `PlanUnit` — compared plan-by-plan in `PersonDelta.add_personatoms_plans`.
- **ch08_person_logic**: `PersonUnit`, `personunit_shop` — the before/after objects that `PersonDelta` diffs.
- **ch09_person_atom**: `PersonAtom`, `personatom_shop`, `modify_person_with_personatom`, `jvalues_different`, `sift_personatom` — the atom building blocks that `PersonDelta` organizes and applies.

New semantic types introduced in `ch10_semantic_types.py`:
- `FaceName` (a `NameTerm`) — identifies the source of outside data, the external "face" from which a lesson arrives.
- `MomentRope` (a `RopeTerm`) — the rope address of a Moment, the temporal/contextual location where lessons accumulate.

---

## 4. Summary of What This Chapter Does

`ch10_person_lesson` builds two layered abstractions on top of ch09's atoms: the **delta** (a structured collection of atoms) and the **lesson** (a delta attributed to a face and moment).

**`PersonDelta`** is the workhorse. It holds a nested dictionary of `PersonAtom`s organized by `crud_str → dimen → jkeys`. Its key capabilities:

- `add_all_different_personatoms(before_person, after_person)` — the diff engine. It calls `thinkout()` on both persons, then walks contacts and plans field-by-field, generating INSERT/UPDATE/DELETE atoms for every difference found. This is a complete, schema-aware diff of two `PersonUnit` states.
- `get_sorted_personatoms()` — returns atoms in the correct application order (respecting `atom_order` so that e.g. a plan exists before its reasons are inserted).
- `get_atom_edited_person(before_person)` — applies the delta to a copy of a person, producing the after state.
- `get_minimal_persondelta(delta, person)` — filters a delta to only atoms that would actually change the focus person, eliminating no-ops.

**`LessonUnit`** wraps a `PersonDelta` with provenance metadata:
- `spark_face` (`FaceName`) — who the lesson came from.
- `moment_rope` (`MomentRope`) — where in the temporal/moment structure this lesson belongs.
- `person_name` — whose belief system is being updated.
- `spark_num` — the ordinal position of this lesson within a moment's sequence.
- `lesson_id` / `delta_start` — for sequencing and resuming lesson application.

**`LassoUnit`** (in `lasso.py`) is a small path-construction helper that converts a `MomentRope` into an OS directory path — bridging the rope addressing system to the file system layout used for persisting lesson and gut files.

**`legible.py`** (not read in full) provides human-understandable representations of deltas and atoms for debugging and reporting.

Together, ch10 establishes the full change-tracking and persistence layer: any transformation of a `PersonUnit` can be expressed as a named, ordered, file-backed `LessonUnit` attributed to a specific face and moment.
