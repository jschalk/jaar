# ch08_person_logic — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 08 — `ch08_person_logic`**
**"PersonUnit — a complete belief system: one person's plan tree, contacts, and the thinkout engine that brings it all to life"**

---

## 2. Prompt Used to Build This

From `ch08_ref.json`:
> "A person is a personunit, made of contacts and plans. All plans are connected to the planroot, which is given all the funds in a personunit."

Ontology note:
> "A PersonUnit is a single planroot and Contacts. thinkout awards fund debts and creds to Contacts and defines the PersonUnit's agenda."

---

## 3. Summary of Previous Relevant Chapters

Ch08 is the first full integration chapter — it imports from every prior chapter:

- **ch00_py**: null-safe helpers, dict/file utilities.
- **ch02_allot**: `allot_scale`, `valid_allotment_ratio`, `validate_pool_num` — the fund pool and respect pools are allotted across contacts using these tools.
- **ch03_contact**: `ContactUnit`, `contactunit_shop`, `GroupUnit`, `groupunit_shop`, `membership_shop`, `AwardUnit` — contacts and groups are first-class members of `PersonUnit`.
- **ch04_workforce**: `WorkforceUnit` — plans within the person carry workforce assignments.
- **ch05_rope**: All rope navigation functions — `create_rope`, `get_ancestor_ropes`, `get_parent_rope`, `get_forefather_ropes`, `is_sub_rope`, etc. — used to traverse and manage the plan tree.
- **ch06_reason**: `FactUnit`, `ReasonUnit` — facts and reasons are set on plans within the person.
- **ch07_plan**: `PlanUnit`, `PlanAttrHolder`, `planunit_shop` — the plan tree is the core data structure of the person. The `PersonUnit.planroot` is a `PlanUnit`.

A new semantic type is introduced in `ch08_semantic_types.py`: `PersonName` (a `NameTerm`) and `ManaGrain` (a float subtype for mana grain sizing).

---

## 4. Summary of What This Chapter Does

`ch08_person_logic` defines `PersonUnit` — the top-level object representing a single participant in the keg system. A person is the union of:

- **`planroot`**: A single `PlanUnit` that is the root of the entire plan tree. All fund flows begin here.
- **`contacts`**: A dictionary of `ContactUnit`s representing the people this person relates to.
- **Grain and pool parameters**: `fund_pool`, `fund_grain`, `respect_grain`, `mana_grain`, `credor_respect`, `debtor_respect` — the numeric resolution and scale of the person's economy.

**The `thinkout()` method** is the computational core of `PersonUnit`. It is a multi-phase engine that resolves the entire person's state:

1. **Clear and rebuild the plan dict** — flattens the plan tree into a `_plan_dict` keyed by rope.
2. **Set range attrs** — evaluates numeric range inheritance for ranged plans.
3. **Set contact/group respect ledgers** — builds credit and debit ledgers across contacts and groups.
4. **Clear fund attrs** — resets all fund tracking fields.
5. **Set factheirs, workforceheirs, awardheirs** — propagates inherited attrs down the plan tree.
6. **Iterative plan-active loop** — repeatedly traverses the plan tree setting `plan_active` for each plan based on its reasons and facts, until no more changes occur (the system reaches a `rational` stable state, or `max_tree_traverse` is reached).
7. **Set fund attrs** — distributes the `fund_pool` down the tree proportionally by `kar` weights using `allot_scale`, assigning each plan its `fund_onset` and `fund_cease`.
8. **Set contact/group fund flows** — propagates fund give/take from plan award structures back to contacts and groups.
9. **Set keep attrs** — identifies "keep" plans (healer-designated plans) for governance tracking.

**`get_agenda_dict()`** returns the subset of plans that are active pledges with a qualifying reason context — this is the person's current to-do list.

This chapter is the largest in the codebase (~1.4MB) and is the computational core of keg. All subsequent chapters either transform `PersonUnit` data or use it to produce outputs (reports, world coordination, other things to be defined).
