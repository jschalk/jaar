*This summary is authored by AI 5-26-2026.*


## Chapter 03 — `ch03_contact`
**"A Contact, A Group, and A Membership — the first core philosophical definitions in keg"**

**Prompt used to build this** *(from `ch03_ref.json`)*:
> "Defines a contact, and its group memberships. Groups will be produced from memberships."

**Summary of previous relevant chapters:**
- From `ch00_py`: `get_0_if_None`, `get_1_if_None`, `get_None_if_nan` for safe null handling.
- From `ch02_allot`: `allot_scale` and `default_grain_num_if_None` — used directly to distribute a contact's creditor/debtor pool proportionally across its group memberships. The semantic types `GrainNum`, `PoolNum`, `WeightNum` are re-exported through `ch03_semantic_types.py`.

**What this chapter does:**
This is where `keg`'s philosophical content starts. The author's ref note calls these *"keg's first core philosophical definitions."* The chapter defines the social actors of the system and how they relate to one another through credit and debt.

**`ContactUnit`** is the fundamental social actor — a named individual. Each contact carries:
- `contact_cred_lumen` and `contact_debt_lumen`: how much credit and debt the surrounding system assigns to this contact.
- `memberships`: a dictionary of `MemberShip` objects, each linking the contact to a `GroupTitle`.
- Calculated fields like `fund_give`, `fund_take`, `fund_agenda_give`, `fund_agenda_take`, and their ratios — populated later by the "thinkout" process in higher chapters.

**`MemberShip`** links a contact to a group with its own `group_cred_lumen` and `group_debt_lumen` weights. When a contact's `credor_pool` or `debtor_pool` is set, `allot_scale` (from `ch02`) distributes that pool proportionally across all of the contact's memberships.

**`GroupUnit`** is derived from memberships rather than declared directly. It aggregates the memberships of multiple contactunits and, using `allot_scale`, distributes its `fund_give` and `fund_take` values back down to individual members. This give/take accounting is the core mechanism by which the system tracks flows of obligation and resource.

**`AwardUnit`**, **`AwardHeir`**, and **`AwardLine`** form a parallel hierarchy representing explicit awards of `give_force` and `take_force` to groups — used later assign relevance to specific groups.

The semantic types introduced here (`ContactName`, `GroupTitle`, `GroupMark`, `NameTerm`, `FundNum`, `RespectNum`) are inherited by all subsequent chapters via `ch03_semantic_types.py`. The `GroupMark` (defaulting to `";"`) is the separator character that distinguishes a group title from a contact name — a contact name cannot contain it, while a group title can.

