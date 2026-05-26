# ch15_moment — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 15 — `ch15_moment`**
**"MomentUnit — the full coordination hub: a shared time system, person histories, fund ledger, and multi-pipeline listening orchestrator"**

---

## 2. Prompt Used to Build This

From `ch15_ref.json`:
> "A MomentUnit is a Moment system with the basic requirements: common system of time, contact transactions ledger, etc. Importantly a Moment system must know the state of a person's personunit at any time in the past."

Ontology note:
> "Defines MomentUnits: common time tech, ledger, ContactNames, history of PersonUnits."

---

## 3. Summary of Previous Relevant Chapters

Ch15 is the first true integration chapter — it imports from every prior chapter simultaneously:

- **ch00_py**: File I/O, path creation, directory management.
- **ch02_allot**: `default_grain_num_if_None` for grain initialization.
- **ch08_person_logic**: `PersonUnit`, `personunit_shop` — the core object managed by the moment.
- **ch10_person_lesson**: `LassoUnit`, `lassounit_shop`, `LessonFileHandler`, `open_gut_file`, `save_gut_file` — lesson/gut file management.
- **ch11_person_listen**: `create_listen_basis`, `listen_to_agendas_create_init_job_from_guts`, `listen_to_debtors_roll_jobs_into_job`, `open_job_file`, `save_job_file`, `save_duty_person`, `create_treasury_db_file` — the full listening pipeline.
- **ch12_bud**: `BudUnit`, `PersonBudHistory`, `TranBook`, `TranUnit`, `cellunit_shop`, `cellunit_save_to_dir` — the budget and transaction system.
- **ch14_time**: `EpochUnit`, `add_epoch_planunit`, `epochunit_shop` — the calendar system embedded in each person's gut.

`ch15_semantic_types.py` re-exports the full accumulated type chain with no additions — it is the most complete semantic accumulation point so far.

---

## 4. Summary of What This Chapter Does

`ch15_moment` defines `MomentUnit` — the top-level coordination object for a single keg community. A moment represents a shared context (identified by `moment_rope`) within which multiple persons interact, share beliefs, exchange funds, and track time together.

**`MomentUnit` fields:**
- `moment_rope` — the rope address that scopes this moment (e.g. `";TexasMusic;"`).
- `moment_mstr_dir` — the root directory where all moment data is persisted.
- `epoch` — the shared `EpochUnit` (calendar system) all persons in this moment use.
- `personbudhistorys` — a dictionary of `PersonBudHistory` per person, tracking all scheduled fund distributions.
- `paybook` — a `TranBook` recording all financial transactions within the moment.
- `offi_times` — the set of official time points at which distributions have been processed.
- Grain parameters (`fund_grain`, `respect_grain`, `mana_grain`) — shared resolution settings applied when creating new persons.

**The seven pipelines** (documented in the class docstring):
1. `lessons → gut` — apply incoming lesson atoms to a person's core belief file.
2. `gut → dutys` — from a person's gut, derive duty files for each healer they reference.
3. `duty → vision` — from duty files, produce vision files (a healer's synthesized view).
4. `vision → job` — from vision files, produce the job file (what a person will actually do).
5. `gut → job` (direct) — skip vision, build job directly from guts.
6. `gut → vision → job` — full pipeline through visions.
7. `lessons → job` — end-to-end pipeline.

**Key orchestration methods:**
- `create_gut_file_if_none(person_name)` — bootstraps a new person into the moment with an empty gut file.
- `create_init_job_from_guts(person_name)` — loads the person's gut, creates a listen basis, runs the initial job-from-guts listen pass, and saves the job file.
- `rotate_job(person_name)` — loads the current job, runs `thinkout()`, then re-listens to all debtors' job files to produce an updated job. Called repeatedly to converge the community's collective understanding.
- `generate_all_jobs()` — runs the full job-generation cycle for all persons: first creates initial jobs from guts, then rotates `job_listen_rotations` times to let the listening converge.
- `add_epoch_to_guts()` — injects the shared epoch (calendar) plan into all persons' gut files, ensuring everyone operates on the same time system.

`MomentUnit` is the highest-level object in keg's operational stack — it is where individual belief systems (ch08), change tracking (ch09–ch10), listening (ch11), fund flows (ch12–ch13), and time (ch14) all come together into a running community simulation.
