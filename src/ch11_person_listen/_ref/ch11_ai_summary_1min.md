# ch11_person_listen — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 11 — `ch11_person_listen`**
**"Listening — how one PersonUnit takes in another's agenda and facts, implementing keg's core Levinasian ethic in code"**

---

## 2. Prompt Used to Build This

From `ch11_ref.json`:
> "These tools describe how one personunit listens to another."

Ontology note:
> "To truly listen one must consider the other's perspective. This chapter contains tools that do just that. The listener takes the speaker's PersonUnit, changes the person_name to their own and takes the agenda into their own PersonUnit."

---

## 3. Summary of Previous Relevant Chapters

- **ch02_allot**: `allot_scale` — used in `generate_ingest_list` to distribute the listener's `debtor_respect` pool across the speaker's agenda plans proportionally by their `kar` weights.
- **ch05_rope**: `get_ancestor_ropes`, `get_first_label_from_rope` — used when ingesting plans to create any missing ancestor plans in the listener's tree.
- **ch07_plan**: `PlanUnit` — the unit of exchange between speaker and listener.
- **ch08_person_logic**: `PersonUnit`, `ContactUnit` — the listener and speaker objects. `create_empty_person_from_person` and `create_listen_basis` (in `basis_person.py`) create clean shells of a person preserving grain/pool parameters.
- **ch10_person_lesson**: `LassoUnit`, `lassounit_shop`, `LessonFileHandler`, `open_gut_file` — used to load speaker gut files from disk when running the full multi-speaker listening pipeline.

`ch11_semantic_types.py` is a pass-through re-export with no new types.

---

## 4. Summary of What This Chapter Does

This is the philosophical center of keg, implemented as code. The `listen_to_speaker_agenda` function embodies the Levinasian concept that genuine listening means taking the other person's perspective seriously and incorporating it into your own understanding.

**`get_perspective_person(speaker, listener_person_name)`** (from `keep_tool.py`) — creates a version of the speaker's `PersonUnit` re-evaluated from the listener's perspective. Facts on the speaker's plan root are reset so the listener can independently assess which of the speaker's pledges are currently active from their own vantage point.

**`listen_to_speaker_agenda(listener, speaker)`** — the core function:
1. Checks the listener has the speaker as a contact (a prerequisite — you can only listen to someone you've acknowledged).
2. Gets the perspective person.
3. If the speaker's belief system is irrational (didn't converge), marks the full speaker `contact_debt_lumen` as `irrational_contact_debt_lumen` — the listener notes the speaker couldn't provide a coherent agenda.
4. If the speaker has no agenda items, marks the debt as `inallocable_contact_debt_lumen`.
5. Otherwise, generates the agenda, scales each plan's `kar` by `allot_scale` against the listener's `debtor_respect`, and ingests each plan into the listener's tree via `_ingest_single_planunit`.

**`listen_to_speaker_fact(listener, speaker)`** — fills in missing facts in the listener's plan tree by borrowing matching facts from the speaker. This allows the listener to become aware of real-world state they couldn't observe themselves.

**`listen_to_agendas_create_init_job_from_guts`** and **`listen_to_agendas_jobs_into_job`** — orchestrate multi-speaker listening pipelines: for each contact in the listener's debtor roll, load that contact's gut (or job) file and call `listen_to_speaker_agenda`. The distinction between "gut" (a person's own belief system) and "job" (a person's synthesized listening output) is introduced here.

**`create_listen_basis`** (in `basis_person.py`) — creates a fresh `PersonUnit` shell that carries over the grain/pool parameters and contact list from the gut, but with a blank plan tree and reset listen-tracking fields — the starting state for each new listening cycle.

The `irrational` and `inallocable` debt tracking from ch03's `ContactUnit` is here put to use: failed listening is not silently dropped, it is accounted for, maintaining the integrity of the credit/debit ledger.
