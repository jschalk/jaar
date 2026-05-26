*This summary is authored by AI.*


## Chapter 04 — `ch04_workforce`
**"Workforce and Labor — assigning who is responsible for tasks"**

**Prompt used to build this** *(from `ch04_ref.json`)*:
> "Introduces Workforce concept: How tasks are assigned."

**Summary of previous relevant chapters:**
- From `ch00_py`: `get_empty_dict_if_None`, `get_False_if_None` for safe initialization.
- From `ch03_contact`: `ContactName`, `GroupTitle`, `GroupUnit` — workforce assignment is expressed entirely in terms of the group and contact structures defined in ch03. `ch04_semantic_types.py` simply re-exports all of ch03's semantic types wholesale, adding nothing new of its own.

**What this chapter does:**
`ch04_workforce` is a focused, relatively small chapter that introduces the concept of *labor* — which groups or contacts are designated as responsible for carrying out a task.

**`LaborUnit`** is a simple dataclass pairing a `GroupTitle` with an optional `solo` boolean flag. When `solo=True`, the labor is restricted to a single contact rather than any member of the group.

**`WorkforceUnit`** is a container of `LaborUnit` objects — essentially a named set of groups/contacts that are eligible to perform a task. It supports add, delete, and existence checks for individual labor entries.

**`LaborHeir`** and **`WorkforceHeir`** are the "inherited" counterparts used when a task inherits workforce constraints from a parent task in the plan tree. `WorkforceHeir.set_labors()` implements the inheritance logic: if the parent has no workforce defined, the child's own workforce is used; if the child has no workforce, the parent's is inherited; if both have workforce definitions, the parent's takes precedence and the child's is only added if not already present. `WorkforceHeir.get_person_name_is_workforce_bool()` then checks whether a specific contact (by `ContactName`) is a member of any of the heir's labor groups, determining if that person is eligible to carry out the task.

This chapter establishes the workforce inheritance pattern that will be applied recursively across the plan tree in later chapters.
