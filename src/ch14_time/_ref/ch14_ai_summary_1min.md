# ch14_time — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 14 — `ch14_time`**
**"Epoch and Calendar — mapping arbitrary human time structures onto the absolute TimeNum line using plan trees"**

---

## 2. Prompt Used to Build This

From `ch14_ref.json`:
> "Allows arbitrary calendars to be defined for each personunit with minimal configuration."

Ontology note:
> "Keg's ontological structure of time: absolute day minutes length, c400_cycle, variable months, weeks, hours."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `create_path`, `open_json` — used to load `c400_constants.json`, the Gregorian calendar constants file.
- **ch05_rope**: `create_rope`, `get_first_label_from_rope`, `is_sub_rope` — epoch plan trees are organized and navigated using rope paths.
- **ch06_reason**: `CaseUnit`, `FactUnit`, `ReasonUnit` — `epoch_reason.py` generates reason/case structures on a person's plan tree to express time-based conditions (e.g. "active during Monday 8am–10am").
- **ch07_plan**: `PlanUnit`, `planunit_shop`, `all_plans_between`, `get_rangeunit_from_lineage_of_plans` — the epoch calendar is built as a tree of `PlanUnit`s with `denom` and `morph` attributes that encode calendar arithmetic.
- **ch08_person_logic**: `PersonUnit`, `add_frame_to_personunit`, `person_planunit_exists`, `person_planunit_get_obj` — epoch plans are inserted into a person's plan tree and queried.
- **ch12_bud**: `TimeNum` — the absolute integer minute value that the epoch system converts to and from human calendar positions.
- **ch13_keep**: `ManaNum` — re-exported through ch14's semantic types, accumulating the full type chain.

New semantic type: `EpochLabel` (a `LabelTerm`) — identifies a specific epoch unit (e.g. `"hr"`, `"day"`, `"week"`, `"month"`, `"year"`).

---

## 4. Summary of What This Chapter Does

`ch14_time` solves a fundamental problem: keg's reasoning engine operates on abstract numeric ranges (`fact_lower`, `fact_upper`, `reason_lower`, `reason_upper`) but humans think in calendars. This chapter bridges the two.

**The C400 system.** Time in keg is measured in absolute minutes from an epoch. The Gregorian calendar repeats exactly every 400 years (a "c400 cycle" of 210,379,680 minutes). `c400_constants.json` encodes the precise minute-lengths of leap years, non-leap centuries, 4-year cycles, and individual years. These constants are loaded into `C400Constants` and used to build standard `PlanUnit`s with `denom` and `morph` attributes that perform the modular calendar arithmetic.

**Epoch plan trees.** A calendar is represented as a hierarchy of `PlanUnit`s (e.g. `c400_leap → c100 → yr4_leap → year → month → week → day → hour`) where each node's `denom` encodes the number of minutes in that unit relative to its parent's cycle. The `morph=True` flag instructs the plan tree to inherit and transform parent numeric ranges — enabling a `TimeNum` value to be correctly positioned within any calendar level by propagating the range arithmetic down the tree.

**`epoch_reason.py`** provides functions that take a human-readable time specification (e.g. "Monday, 8am to 10am, weekly") and translate it into `ReasonUnit`/`CaseUnit` structures on a specific plan in the person's tree, using modular arithmetic against the day/week denominators. This is how a person declares "this pledge is active every Monday morning" — expressed as a case with a `reason_divisor` equal to the week length in minutes.

**`epoch_main.py`** provides helpers like `get_day_rope`, `get_week_rope`, `get_year_rope` — pre-built rope paths for standard calendar nodes — and `stan_c400_leap_planunit()` etc. — factory functions for the standard Gregorian plan units.

**`calendar_markdown.py`** generates human-readable calendar output from a person's plan tree for display and reporting.

In summary, ch14 makes keg's belief system time-aware: a person's plan tree can now express not just what they want to accomplish, but *when* — using any calendar structure they choose, mapped faithfully onto the absolute `TimeNum` line.
