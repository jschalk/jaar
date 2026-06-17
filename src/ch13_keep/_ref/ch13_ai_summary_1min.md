# ch13_keep — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 13 — `ch13_keep`**
**"RiverCycle and RiverRun — simulating how effectively a healer earns credit by caring for their community"**

---

## 2. Prompt Used to Build This

From `ch13_ref.json`:
> "Builds a simulation that describes how much credit a healer has earned."

Ontology note:
> "Challenging Ch, describes how effective a healer so does not take is."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `get_0_if_None`, `get_empty_dict_if_None` for safe initialization.
- **ch02_allot**: `allot_scale`, `default_grain_num_if_None`, `validate_pool_num` — the core mechanism by which `mana` (care credit) is distributed across contacts in each river cycle.
- **ch08_person_logic**: `PersonUnit` — `get_patientledger` and `get_doctorledger` extract credit/debt lumen dictionaries directly from a person's contacts.
- **ch12_bud**: `TimeNum`, `SparkInt` — imported via ch13's semantic types, tying the river simulation to the time/transaction layer.

New semantic type introduced in `ch13_semantic_types.py`:
- `ManaNum` (a `float`) — represents a unit of care credit ("mana"), the currency of the river cycle simulation. Distinct from `FundNum` to semantically separate the healer-care economy from the general fund economy.

---

## 4. Summary of What This Chapter Does

`ch13_keep` implements keg's **healer accountability simulation** — a mechanism for evaluating how much care credit a healer has genuinely earned through their keep (their designated responsibility zone).

The metaphor is a river: mana flows from healers to patients and circulates through the community across multiple cycles, accumulating to form a picture of who has given and received care.

**`get_patientledger(person)`** — extracts a ledger of `contact_name → contact_cred_lumen` for all contacts with positive credit lumen. These are the people the person cares about (their "patients").

**`get_doctorledger(person)`** — extracts `contact_name → contact_debt_lumen` for contacts with positive debt lumen. These are the people who owe care to this person (their "doctors").

**`RiverBook`** — a single person's mana distribution record within one cycle. Given a patient ledger and a total `book_point_amount`, it uses `allot_scale` to distribute the mana proportionally across patients.

**`RiverCycle`** — one full cycle of the river simulation for a healer. It holds `keep_patientledgers` (the patient ledgers of all persons in the healer's keep) and iterates through them, creating a `RiverBook` for each, then aggregates via `create_cylceledger()` — a merged ledger summing all care flows across all river books in the cycle. This cycle ledger becomes the input mana distribution for the next cycle.

**`riverrun.py`** (not read in full) orchestrates multiple `RiverCycle`s in sequence — running the river through N cycles to reach a static distribution. The convergence of the cycle ledger across runs indicates how much each person in the keep has earned relative to their declared responsibilities.

The river metaphor directly operationalizes the Levinasian ethic: a healer's credit is not self-declared but emerges from actual cycles of caring — how much mana flows through them toward others over time.
