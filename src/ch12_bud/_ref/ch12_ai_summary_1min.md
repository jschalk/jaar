# ch12_bud — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 12 — `ch12_bud`**
**"BudUnit and TranBook — time-stamped fund distributions and the transaction ledger that records them"**

---

## 2. Prompt Used to Build This

From `ch12_ref.json`:
> "Defines a budget and the tools necessary to create one. Budgets are created when a personunit is given funds that must be distributed."

Ontology note:
> "Defines Budget that distribute funds."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: Nested dict utilities (`get_from_nested_dict`, `set_in_nested_dict`, `del_in_nested_dict`, `exists_in_nested_dict`, `create_csv`) — used to manage the three-level nested structure of `TranBook.tranunits` (`person_name → contact_name → tran_time → amount`).
- **ch02_allot**: `default_pool_num()` — provides the default `quota` value for a `BudUnit`.
- **ch10_person_lesson**: `MomentRope` — `TranBook` is scoped to a moment rope, tying transactions to a specific temporal/contextual location.

New semantic types introduced in `ch12_semantic_types.py`:
- `TimeNum` (an `int`) — represents an instant on the time number line (absolute minutes from a zero-minute).
- `SparkInt` (an `int`) — describes the ordinal position of a data ingestion event (a "spark").

---

## 4. Summary of What This Chapter Does

`ch12_bud` introduces the **time dimension** to keg's fund-flow system. Where ch03 defined how funds are distributed across contacts within a single `PersonUnit` evaluation, ch12 defines how those distributions are recorded as time-stamped transactions and aggregated across time.

**`TranUnit`** is the atomic fund record: a transfer of `amount` (`FundNum`) from a source person (`src`) to a destination contact (`dst`) at a specific `tran_time` (`TimeNum`). It is keg's equivalent of a double-entry ledger line.

**`TranBook`** aggregates `TranUnit`s into a three-level nested dictionary: `person_name → contact_name → tran_time → amount`. It tracks a `moment_rope` scope and provides:
- `add_tranunit` — validates against blocked times and a maximum time ceiling before inserting.
- `get_person_contacts_net` — calculates the net fund position for each `(person_name, contact_name)` pair across all recorded transactions.
- `get_tran_times` — retrieves all distinct transaction times.
- Export to nested dicts and CSV for reporting.

**`BudUnit`** is a scheduled distribution event: at a given `bud_time`, a `quota` of funds is to be distributed. The `celldepth` parameter (default 2) controls how many layers of the listening hierarchy participate in distributing that quota. `calc_magnitude()` verifies that the net of `bud_contact_nets` (positive credits and negative debits) sums to zero — enforcing conservation of funds.

**`PersonBudHistory`** is a person's full history of `BudUnit`s keyed by `bud_time`. It tracks summary statistics: total quota committed, net contact balances, and time range.

**`cell_main.py`** and **`weighted_facts_tool.py`** (not read in full) implement the cell-based distribution logic — the mechanism by which a `BudUnit`'s quota is recursively divided among listening participants up to `celldepth` levels deep, weighted by the contact cred/debt lumen values established in ch03.

Ch12 is the first chapter to introduce `TimeNum` as a first-class type, setting up the time numbers for later.