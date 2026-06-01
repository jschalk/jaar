*This summary is authored by AI 5-26-2026.*

## Chapter 01 — `ch01_keyword`
**"Keyword Glossary Engine — gives every chapter a shared controlled vocabulary"**

**Prompt used to build this** *(from `ch01_ref.json`)*:
> "Create Keyword Enum classes for use in testing files."

**Summary of previous relevant chapters:**
Imports directly from `ch00_py` — specifically `file_toolbox` for `create_path`, `open_json`, and `save_file`. It relies on `ch00`'s file I/O to read two source JSON configs (`keywords_src.json` and `example_strs.json`) that define the full vocabulary of the project.

**What this chapter does:**
`ch01_keyword` is the project's glossary engine. It reads a master list of keyword strings (stored in `ch99_glossary/keywords_src.json`) where each keyword is tagged with a `valid_ch` field indicating which chapters it belongs to. From this, the chapter dynamically generates Python `Enum` classes — one per chapter — so that every chapter has a type-safe, auto-documented set of domain terms available for use in tests and code.

Key mechanics:
- `chapter_desc_main.py` scans the `src/` directory using `ch00`'s `get_level1_dirs` to discover all chapter folders and extract their numbers.
- `keyword_class_builder.py` parses the `valid_ch` range syntax (e.g. `"3:"` means "all chapters from 3 onwards"), builds cumulative keyword sets per chapter, and generates `Enum` class source code strings like `C03Keywords`, `C07Keywords`, etc.
- It also produces a human-understandable `keywords_by_chapter.md` markdown file listing which keywords are introduced in each chapter.

The effect is that all later chapters can reference domain terms as strongly-typed enum values rather than raw strings, making the codebase self-documenting and testable at the vocabulary level.

