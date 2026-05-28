# ch05_rope — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 05 — `ch05_rope`**
**"Ropes and Knots — a path-based identity system for navigating a tree of concepts"**

---

## 2. Prompt Used to Build This

From `ch05_ref.json`:
> "Defines what a Rope is and required format for groups names and individual names."

Ontology note from the ref:
> "Ropes, Knots delineate reality into totalities using letters. From the nothing root all ropes ever branch out."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `is_path_valid` from `file_toolbox` is used to check whether a rope can map to a valid OS directory path.
- **ch02_allot**: `GrainNum`, `PoolNum`, `WeightNum` re-exported through `ch05_semantic_types.py`.
- **ch03_contact**: All of ch03's semantic types (`ContactName`, `GroupTitle`, `GroupMark`, `NameTerm`, `BreakTerm`, `FundNum`, `RespectNum`, etc.) are re-exported, making ch05 the new semantic type accumulation point for all downstream chapters.

Ch05 introduces no new numeric types, only new string-based structural types.

---

## 4. Summary of What This Chapter Does

`ch05_rope` defines the **address system** used throughout keg to identify any node in the plan tree. The core idea: reality is organized as a hierarchy of named nodes, and any node can be uniquely addressed by its path from the root — this path is called a `RopeTerm`.

**New semantic types introduced:**
- `KnotTerm` — the delimiter character that separates labels within a rope (defaults to `";"`). This directly parallels `GroupMark` from ch03, which used the same default separator to distinguish group names from contact names. In ch05 the concept is generalized into the tree-path domain.
- `LabelTerm` — a single node name; must not contain the `KnotTerm`.
- `RopeTerm` — a full path string composed of `LabelTerm`s joined by `KnotTerm`s, always beginning and ending with the knot (e.g. `";root;tasks;cooking;"`).
- `FirstLabel` — the top-level label in a rope, the root of a subtree.

**Key functions in `rope.py`:**
- `create_rope(parent_rope, tail_label, knot)` — constructs a new rope by appending a label to an existing rope.
- `get_all_rope_labels(rope, knot)` — splits a rope into its constituent labels.
- `get_parent_rope(rope)` / `get_tail_label(rope)` — navigate up and down the tree.
- `get_ancestor_ropes(rope)` — returns the full list of ancestor paths from root to the given rope.
- `is_sub_rope(ref_rope, sub_rope)` / `is_heir_rope(src, heir)` — test hierarchical containment relationships.
- `rebuild_rope(subj_rope, old_rope, new_rope)` / `replace_knot(rope, old_knot, new_knot)` — support structural refactoring of the tree.
- `get_unique_short_ropes(ropes_set, knot)` — produces the shortest unambiguous label suffix for each rope in a set (useful for display).
- `rope_is_valid_dir_path(rope, knot)` — checks if a rope can be mapped to a valid OS file path, enabling the file-system-backed persistence used in later chapters.

The rope system is the backbone of every subsequent chapter. Every `PlanUnit`, every `ReasonUnit`, every `FactUnit` is identified by a `RopeTerm`. The tree structure of plans is navigated entirely through rope operations.
