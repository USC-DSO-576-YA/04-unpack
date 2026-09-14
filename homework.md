# Module 4 homework — Build and audit a Dodgers dashboard

Begin this assignment **after Wednesday's in-class demonstration**. You are not expected to know the dashboard workflow before that demonstration.

## Your goal

Use Codex to help you build a small Streamlit dashboard from the supplied Dodgers batting and pitching data. Your job is not only to produce a working page. You must also trace the generated pandas work, verify the displayed results, and revise anything that is misleading.

## Required architecture

Keep the two responsibilities separate throughout the assignment:

- `analysis.py` loads, cleans, maps, groups, sorts, and validates DataFrames.
- `app.py` creates the Streamlit interface and displays results returned by `analysis.py`.

Do not put pandas transformations in `app.py`, and do not put Streamlit code in `analysis.py`. Streamlit creates the browser page for you; you do not need a separate HTML file.

## A useful first prompt for Codex

> Read `AGENTS.md`, `homework.md`, and `data/README.md`. Before editing, state the grain of each dataset and propose a two-file plan. Build a simple Streamlit Dodgers dashboard. Put every pandas operation in `analysis.py` and only Streamlit interface code in `app.py`. Let the user select a year. Include a batting summary, a pitching-position quality audit, two plots, and a visible limitation. Preserve the supplied CSV files, use mappings, verify grouped row counts, run `check_structure.py`, and start the app.

You may revise this prompt. Do not ask Codex to write your reflection.

## Dashboard requirements

Your dashboard must include all of the following:

1. A year selector that changes the displayed results.
2. The number of batting rows and pitching rows for the selected year.
3. A batting-role summary created with `groupby` and named aggregation. Show:
   - number of player-season rows,
   - total at-bats (`AB`),
   - total hits (`H`),
   - total home runs (`HR`), and
   - combined batting average, calculated as total hits divided by total at-bats.
4. A pitching-position quality check showing both the number and percentage of rows with missing `Position`.
5. A new readable pitching-role column made with `.map()`:
   - `SP` → `Starting pitcher`
   - `RP` → `Relief pitcher`
   - `CL` → `Closer`
   - missing or unmapped values → `Unclassified`
6. A check that the pitching-role group counts add back to the selected year's pitching row count.
7. Two plots that answer different questions, with clear labels and units.
8. One visible limitation or caution about the data.

Treat `Innings_Pitched` carefully. Baseball notation such as `131.2` means 131 innings plus two outs, not 131.2 ordinary decimal innings. Converting and totaling it correctly is optional; do not sum it naively.

## Trace, verify, revise

Before submitting:

1. Trace one grouped result from source rows to the value shown in the app.
2. Independently verify one displayed number with a small pandas calculation.
3. Check whether each plot matches the question, grain, and units.
4. Run `python check_structure.py` and fix every reported failure.
5. Ask Codex for one targeted revision based on a problem you found.

## What to submit on Brightspace

Submit one file named `module4_submission.zip` containing:

- `analysis.py`
- `app.py`
- your completed `reflection.md`
- `dashboard.png`, a screenshot of the running dashboard
- one summary CSV created by your analysis

Do **not** include the supplied source CSV files in your ZIP. Work locally and do not push to the shared course repository.

## Final checklist

- The dashboard runs without an exception.
- Changing the year changes the results.
- `analysis.py` contains the DataFrame work.
- `app.py` contains the Streamlit display work.
- Missing and unmapped positions remain visible as `Unclassified`.
- Group counts reconcile with the filtered source rows.
- Combined batting average uses `sum(H) / sum(AB)`.
- Plot titles, axes, and units are understandable.
- The reflection is written in your own words.
