# ch98_linter — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 98 — `ch98_linter`**
**"Linter — AST-based style enforcement, chapter-move tooling, and line counting for the keg repository"**

---

## 2. Prompt Used to Build This

From `ch98_ref.json`:
> "Linter for repo."

Ontology note:
> "All chapters get checked for following style rules."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `is_camel_case`, `uppercase_in_str` from `dict_toolbox`; `create_path`, `get_dir_filenames`, `open_file` from `file_toolbox` — file traversal and string utilities.
- **ch01_keyword**: `get_example_strs_config` — the linter validates that example strings in test files match the registered example string configurations.
- **ch97_docs_builder**: `get_chapter_desc_prefix`, `get_chapter_descs`, `get_func_names_and_class_bases_from_file` — chapter directory discovery and AST-based function name extraction are reused from ch97.

`ch98_semantic_types.py` re-exports through ch22 with no additions.

---

## 4. Summary of What This Chapter Does

`ch98_linter` enforces keg's coding conventions across the repository. Because it needs to import from ch97 (which imports from nearly all chapters), it is positioned at 98 — only ch99 is later in the inductive chain.

**`style.py`** — the core linter:

- `filename_style_is_correct(filename)` — enforces two rules: no uppercase characters in `.py` or `.json` filenames; no Python files ending in `s.py` (plural module names are disallowed).
- `get_filenames_with_wrong_style(filenames)` — returns the set of violating filenames.
- An `ast.NodeVisitor` subclass traverses each Python file's AST, checking:
  - Function names must be `snake_case` (no camelCase via `is_camel_case`).
  - Import statements must not import from chapters higher than the current chapter's number (enforcing the inductive import rule: a chapter may only import from earlier chapters).
  - Functions must have docstrings if they exceed a minimum line count threshold.
  - Class names must be `PascalCase`.
- `get_func_names_and_class_bases_from_file` from ch97 is used to cross-check declared class hierarchies against style expectations.

**`line_counter.py`** — counts lines of code per chapter and per file, used to track codebase growth and identify chapters with unusually large files.

**`ch_move1.py`** / **`ch_move_many.py`** / **`chapter_move_tool.py`** — utilities for renumbering chapters. When a chapter needs to be renumbered (e.g. inserting a new chapter between existing ones), these tools:
  - Update all import statements across the entire `src/` tree that reference the old chapter number.
  - Rename the chapter directory itself.
  - Update `_ref/chXX_ref.json` chapter number fields.
  - Update test file paths and any hardcoded chapter references.
  `ch_move_many` extends this to batch-renumber a range of chapters simultaneously.

**`paths_change.py`** — finds and replaces path strings across the repo when directory structures change.

**`create_notebook.py`** — generates Jupyter notebook scaffolding for a chapter's test suite, enabling interactive exploration of chapter functionality.

The linter's placement at 98 means it can validate the import-ordering rule across the entire codebase — it has the highest chapter number of any functional chapter, and can therefore check that nothing in chapters 0–97 imports from chapters higher than themselves.
