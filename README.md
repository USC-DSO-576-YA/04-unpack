# WorldStage — Regional Tour Review

**WorldStage** promotes concerts across Asia, Europe, America, and Africa. The
company is deciding where to add shows next year. A single “best region” answer
is not enough: ticket volume, sell-through, revenue, ratings, country coverage,
and missing data can point in different directions.

You are the analyst reviewing the evidence. Monday's work turns hundreds of
show rows into one decision row per region. Wednesday's work cleans a messy
multi-platform export without quietly turning unknown values into zeros.

This is the DSO-576 Module 4 repo.

## What's in this repo

| File | What it is |
|---|---|
| `concept_shows.csv` | The exact 20 fictional shows used on the Module 4 Concepts pages. Use it to reproduce the small examples. |
| `worldstage_shows.csv` | The larger clean dataset: 480 completed concerts, one row per show, across 20 countries and 12 months. Use it for `groupby`, named aggregations, sorting, and plots. |
| `worldstage_shows_raw.csv` | A 600-row raw partner export with inconsistent country, event, status, and price text plus meaningful missing values. Use it for Wednesday's cleaning work. |
| `country_aliases.csv` | WorldStage's approved country and region lookup. Values absent from this file stay missing; do not guess. |
| `notes/data_dictionary.md` | Column meanings and the business rules for `FREE`, blanks, `TBD`, ratings, and marketing spend. Read this before cleaning. |
| `notes/vocabulary.md` | The Module 4 pandas vocabulary, organized by Monday and Wednesday. |
| `homework.md` | The assignment, ten code tasks, required outputs, and submission checklist. |
| `worldstage_homework.py` | The protected code scaffold. You complete its ten short pandas tasks. |
| `check_homework.py` | A read-only structural checker that reports task status without printing the answers. |
| `analysis-prompt.md` | A bounded request that makes Codex review an attempt without supplying code. |
| `tour_review.md` | Your evidence-based review template, written in your own words. |
| `agent.md` | How you should work with Codex in this repo. |
| `AGENTS.md` | Repository rules Codex reads automatically. |
| `tutor.md` | Instructions that turn your agent into a Module 4 pandas tutor. |
| `scripts/generate_data.py` | Reproducible generator for the fictional datasets. Maintainer tool; students do not run or edit it. |

## The decision

WorldStage can add a limited number of dates next year. The strategy lead wants
a regional summary and one honest chart, followed by an analyst's review of the
data-quality choices behind them.

The analysis must answer:

- Which region leads in total tickets sold?
- Which region leads in average sell-through relative to capacity?
- How many shows, rated shows, and distinct countries support each result?
- Do revenue and fan ratings tell the same story?
- Which raw rows become unusable for attendance or revenue analysis, and why?

Do not choose a region from one metric alone. The point is to name the grain,
the denominator, and the missing-data decisions behind every comparison.

## Start here

Open a terminal in this folder and install the locked environment:

```text
uv sync
```

Run the starter checker:

```text
uv run python check_homework.py
```

It should report Tasks 1–10 as unfinished. Read `homework.md`, complete one
small `TODO` at a time in `worldstage_homework.py`, and rerun the checker after
each attempt.

If you need coaching, open Codex in this folder and enter:

```text
/plan Execute @analysis-prompt.md
```

Codex may explain a concept or check your attempt, but `AGENTS.md` prohibits it
from editing the homework, giving you paste-ready code, printing the final
regional winners, or writing `tour_review.md`.

For quiz practice, start a separate conversation and say:

```text
Read tutor.md and tutor me.
```

## The two class sessions

### Monday — group and compare

Use `concept_shows.csv` first, then scale the same reasoning to
`worldstage_shows.csv`:

1. State the input grain: one row per completed concert.
2. Derive `sell_through` and `revenue` at the show grain.
3. Use `groupby(...).agg(...)` to create one row per region.
4. Compare `sum`, `mean`, `size`, `count`, and `nunique`.
5. Sort the summary and choose a plot that matches the business question.

### Wednesday — clean before grouping

Use `worldstage_shows_raw.csv` and the rules in the data dictionary:

1. Preserve raw columns and work on a `.copy()`.
2. Normalize text with `.str` operations.
3. Use `.map()` only with the approved country lookup.
4. Inspect missing values with `.isna()` and `.notna()`.
5. Use `.fillna()` only when the business meaning supports a real replacement.
6. Use `pd.to_numeric(..., errors="coerce")` for messy numeric text.
7. Create separate fit-for-purpose attendance, revenue, and rating tables.

## Working here

The datasets are fictional, committed, and read-only. Do not hand-edit them.
If you want to test an idea, create a small scratch DataFrame in a new file.

You work locally and commit locally. Nothing is submitted through GitHub. Keep
both `worldstage_homework.py` and `tour_review.md` in your own words and upload
the required files through the course submission channel named by your
instructor.
