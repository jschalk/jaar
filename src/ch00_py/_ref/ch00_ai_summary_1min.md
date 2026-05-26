*This summary is authored by AI 5-26-2026.*

---

## Chapter 00 — `ch00_py`
**"Standard Python Toolbox — the foundation everything else is built on"**

**Prompt used to build this** *(from `ch00_ref.json`)*:
> "Create some standard tools for files, python dictionaries, databases, and other basic programming objects."

**Summary of previous relevant chapters:**
None. This is chapter zero — the base of the inductive stack. It imports only from the Python standard library and a small set of third-party packages (`compact_json`, `pathlib`, `shutil`, etc.). Nothing in `keg` precedes it.

**What this chapter does:**
`ch00_py` provides purely utilitarian helper functions used throughout every subsequent chapter. It has no domain logic and no philosophical content — the author's own ref note says *"there is nothing philosophically interesting here."* It is organized into four toolboxes:

- `dict_toolbox.py` — safe null-handling helpers (`get_0_if_None`, `get_empty_dict_if_None`), nested dict operations (get, set, delete by key path), JSON serialization, CSV-to-dict conversion, and normalization utilities.
- `file_toolbox.py` — OS-level path construction (`create_path`), directory creation/deletion/copying, file open/save, JSON file read/write, and path validity checks.
- `csv_toolbox.py` — CSV reading with type coercion, CSV-to-SQLite bridging.
- `plotly_toolbox.py` — minimal Plotly charting wrappers.

The chapter establishes the project's coding style: highly defensive null handling, consistent type aliasing, and thin wrappers around standard library calls with explicit, readable names.

