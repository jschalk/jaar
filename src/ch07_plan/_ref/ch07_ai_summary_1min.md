# ch07_plan — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 07 — `ch07_plan`**
**"PlanUnit — the most complex concept in keg, a hierarchical node carrying reasoning, funding, workforce, and pledge logic"**

---

## 2. Prompt Used to Build This

From `ch07_ref.json`:
> "Defines PlanUnits. Plans are complicated. A plan can have sub plans, define itself as a pledge, define Awardees, assigned Workforce, required Reasons, etc."

Ontology note:
> "PlanUnits are the most complicated concepts in Keg2. Plans are hierarchical with child plans and a parent plan (unless its a root). Data in a plan can be sourced from the Parent Plan (Heirs) or the Child Plan (Lines). Plans distribute funds to Awardees. There is a lot."

---

## 3. Summary of Previous Relevant Chapters

`ch07_plan` is the first chapter to draw on every prior chapter simultaneously:

- **ch00_py**: null-safe helpers (`get_0_if_None`, `get_1_if_None`, `get_empty_dict_if_None`, `get_False_if_None`, `get_positive_int`).
- **ch02_allot**: `allot_scale` and `default_grain_num_if_None` — used to distribute a plan's fund pool proportionally among its child plans (via their `poynt` weights) and to distribute award funds among `AwardUnit`s.
- **ch03_contact**: `AwardUnit`, `AwardHeir`, `AwardLine`, `GroupUnit` — the award system from ch03 is embedded into each `PlanUnit`. Groups receive fund flows via award structures.
- **ch04_workforce**: `WorkforceUnit`, `WorkforceHeir` — each plan can declare which groups/contactunits are responsible for carrying it out; these inherit down the tree.
- **ch05_rope**: `RopeTerm`, `create_rope`, `rebuild_rope`, `is_sub_rope`, `find_replace_rope_key_dict`, `all_ropes_between` — the plan tree is entirely organized by rope paths. Every plan has a `parent_rope` and a `plan_label`, and its full identity is its rope.
- **ch06_reason**: `ReasonUnit`, `ReasonHeir`, `FactUnit`, `FactHeir` — each plan can declare conditions (`reasonunits`) and local facts (`factunits`). These are evaluated to determine `plan_active`.

Ch07 also introduces `HealerUnit` (in `healer.py`) and `RangeUnit` (in `range_toolbox.py`) as supporting structures.

---

## 4. Summary of What This Chapter Does

`ch07_plan` defines `PlanUnit` — the central data structure of keg. A `PlanUnit` is a node in a tree of plans rooted at a single root. Each node can be:

- A **container** (`kids: dict[LabelTerm, PlanUnit]`) that groups sub-plans.
- A **pledge** (`pledge: True`) — a declared commitment that can be active or inactive.
- A **fact source** (`factunits`) — a local regulator of incoming facts.
- A **reason-gated plan** (`reasonunits`) — only active if its conditions are met.
- A **funded node** — receives a slice of the parent's fund pool proportional to its `poynt` weight, tracked via `fund_onset` and `fund_cease`.
- A **ranged plan** (`begin`, `close`, `addin`, `numor`, `denom`, `morph`) — can represent a numeric interval that can be inherited and morphed by children.
- A **problem** (`problem_bool`) with designated **healers** (`healerunit`) — plans that flag issues and point to responsible remediation plans.

**Key computed ("heir") attrs** that flow down from parent to child:
- `factheirs` — facts inherited and possibly narrowed by local `factunits`.
- `reasonheirs` — reasons inherited from parent and evaluated against `factheirs`.
- `workforceheir` — inherited workforce assignment.
- `awardheirs` / `awardlines` — fund flow directions inherited and accumulated from children.

**`PlanAttrHolder`** is a parameter-object pattern used to batch-set attrs on a `PlanUnit` without requiring positional arguments for every field — a clean API for the large number of settable properties.

The plan tree is the structural core of keg. Every subsequent chapter either populates this tree, tracks changes to it, or reads from it to produce outputs such as reports.
