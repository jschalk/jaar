# keg2

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

keg2 is a desktop app that takes what matters to someone else — captured as idea files — and brings those ideas into your daily world. It updates your agenda, your KPIs, and your own ideas so you can act on them and share them with others.

Repository: https://github.com/jschalk/keg

---

## Requirements

- **Python 3.10+** — [download here](https://www.python.org/downloads/)

---

## Installation

1. Install Python 3.10 or newer from the link above
2. Open Command Prompt and run:

```
pip install keg2
```

If you have installed keg2 before and want to ensure you have the latest version:

```
pip uninstall keg2
pip install --no-cache keg2
```

---

## Starting the app

Once installed, start the app at any time by running:

```
keg2_app
```

The app window will open and you are ready to go.

![App demo](demo.gif)

---

## First-time setup

When the app opens for the first time, fill in the following fields:

| Field | What to enter |
|---|---|
| **Me** | Your name |
| **You** | The name of the person whose ideas you are bringing in |
| **Ideas Dir** | The folder where their idea files (Excel) are stored |
| **Bricks Dir** | The folder where your building blocks are stored |
| **Worlds Dir** | The folder where your worlds live |
| **World Name** | The name of the world you are currently working in |
| **Agendas Dir** | The folder where your daily agendas will be saved |

The app remembers these settings the next time you open it, so you only need to fill them in once.

---

## Daily use

1. Run `keg2_app` to open the app
2. Confirm your settings look correct
3. Click **Create Agendas for Today** to pull in the latest ideas and update your agenda, KPIs, and idea files
4. Your agendas folder will open automatically when the run finishes

---

## Idea file format

The pipeline will only process Excel files that follow the correct **idea type** format. Idea types mirror the **brick type** formats documented in `src/docs`.

If you are not sure how to structure an idea file, the app includes built-in examples for every supported idea type. Below the **Create Agendas for Today** button there is a scrollable table — each row names an idea type. Click any row and the app copies a ready-made example file directly into your Ideas directory. Open that file, fill it in with real content, and it will be picked up on the next run.

The brick type format specifications are in `src/docs` if you need to understand the full structure in more detail.

---

## Punch viewer

The punch viewer shows a summary of activity for a given person and time period. Use the **Person** and **Moment** dropdowns to select what you want to see. You can **Copy** the result to your clipboard or **Print** it using the buttons at the top of the viewer.

---

## How keg works

### The philosophy behind listening

keg is built on the philosophy of Emmanuel Levinas (1906-1995), as expressed in his book *Totality and Infinity: An Essay on Exteriority* (translated by Lingis, 1969), and taught by Jules Simon PhD, Philosopher at The University of Texas at El Paso (UTEP).

The central idea is that real listening is painful. To truly listen is to not know what is going to be said — to take in the suffering of the Other, bring it into yourself, and be changed by it in ways you could not have predicted. Levinas describes the failure to listen as a form of murder. keg is an attempt to make that kind of listening practical and measurable.

### Moments

For Levinas, all of reality is born from the face-to-face encounter. The Other's face tells me of its suffering, and that suffering becomes mine. I then make a **Moment** — a decision to change who I am in response. The Moment cuts the infinite into the finite and becomes the foundation for a world.

A Moment can create a new world or change a current one. Each person can only make one Moment at a time, so a world built from multiple Moments implies each came from a different person at a different time. keg indexes time by `spark_num`, always an integer — a discrete, indivisible unit of time.

Every piece of data in keg requires three fields: `spark_num`, `spark_face`, and a rope — either `moment_rope` or `plan_rope`.

### Excel sheets as declarations

Needs and ideas are expressed as Excel sheets. These range in complexity from a simple five-column single-row file to sheets with 10+ columns that include configuration options. Each row is translated into the internal data set. Even a single-row sheet like the example below is enough for keg to process.

**Example input — fizz0.xlsx, sheet "br00000_buzz"**

| spark_num | spark_face | moment_rope | person_name | contact_name | tran_time | amount |
|---|---|---|---|---|---|---|
| 77 | Emmanuel | OxboxDean | Emmanuel | Dean | 891 | 7000 |

keg reads this and creates a Moment called "OxboxDean" containing Emmanuel and Dean, with a single transaction of 7000 from Emmanuel to Dean.

**Resulting metric**

| moment_rope | person_name | moment_fund_amount | moment_fund_rank | moment_pledges |
|---|---|---|---|---|
| OxboxDean | Emmanuel | -7000 | 2 | 0 |
| OxboxDean | Dean | 7000 | 1 | 0 |

**Output idea — emmanuel_idea.xlsx, sheet "br00000"**

| spark_num | spark_face | moment_rope | person_name | contact_name | tran_time | amount |
|---|---|---|---|---|---|---|
| 77 | Emmanuel | OxboxDean | Emmanuel | Dean | 891 | 7000 |

### Agendas

Each contact's agenda in the community is built from two sources: the agendas of others they are listening to, and their own independent agenda. Each agenda is saved as a JSON file and can include pledges to act and pledges of existence.

### Data structure

The internal data model is built around the following object hierarchy:

- PersonUnit
- PersonUnit → ContactUnit
- PersonUnit → GroupUnit
- PersonUnit → PlanUnit
- PersonUnit → PlanUnit → AwardUnit / AwardLine / AwardHeir
- PersonUnit → PlanUnit → Reason → CaseUnit / CaseHeir
- PersonUnit → PlanUnit → FactUnit / FactHeir

### Development

keg was built using Test-Driven Development. Every feature has a corresponding test. This is mostly a one-man project — Femi has significantly helped.
pip deployment has been a challenge. Hopefully __init__.py file creation gets rid of failed file reference errors. 
---

## Acknowledgements

Jules Simon PhD — Philosopher at UTEP, whose teaching of Levinas in 2014 is still being worked through.

Femi — for significant contributions to the project.

---

## License

MIT