*This summary is authored by AI 5-26-2026.*

## Chapter 02 — `ch02_allot`
**"Allotment Engine — defines how a finite pool of value is divided across a weighted ledger"**

**Prompt used to build this** *(from `ch02_ref.json`)*:
> "Defines tools for allotment of a large number (called a pool) to a ledger (a list of things with a weighted value to represent their importance)."

**Summary of previous relevant chapters:**
Imports from `ch00_py` only — `dict_toolbox` for null-safe helpers (`get_0_if_None`, `get_1_if_None`) and `file_toolbox` for `create_path`, `open_json`, `save_json`. It does not use `ch01_keyword`. This chapter introduces its own semantic type aliases in `ch02_semantic_types.py` (`GrainNum`, `PoolNum`, `WeightNum`) which are thin subclasses of `float` used to make function signatures self-describing.

**What this chapter does:**
`ch02_allot` solves the problem of fairly distributing a discrete pool of value (e.g. a budget, a time allocation, a resource pool) across a set of competing claims that have relative weights. The author's ref note says plainly: *"When things have to be divided, such as currency, this defines how."*

Three semantic types anchor the logic:
- `PoolNum` — the total amount to distribute.
- `WeightNum` — the unnormalized relative importance of each ledger entry.
- `GrainNum` — the smallest indivisible unit (like a cent in currency).

The core function `allot_scale(ledger, scale_number, grain_unit)` takes a weighted dictionary, a total to distribute, and a grain size, and returns a new dictionary where each key receives a share proportional to its weight — guaranteed to sum exactly to `scale_number` with no floating-point remainder. A careful residual-distribution algorithm handles the rounding leftover by assigning extra grain units to the highest-weighted entries first.

`allot_nested_scale` extends this to hierarchical ledgers stored as directory trees of JSON files, recursively allotting a parent's share down to its children up to a configurable depth. This foreshadows the tree-structured plan logic that appears in later chapters.

