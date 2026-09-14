# Module 4 — Build and Audit a Dodgers Dashboard

This repository contains the Module 4 homework. You will use Codex to build a
small Streamlit dashboard from the supplied Dodgers batting and pitching data,
then trace and verify the pandas work behind it.

## Wait for the Wednesday demonstration

The professor will demonstrate the workflow in class on Wednesday. You are not
expected to begin the homework before that demonstration. Use `homework.md`
after the professor introduces the assignment.

## Required architecture

The dashboard has two Python layers. Keep them separate throughout the work.

| File | Responsibility |
|---|---|
| `analysis.py` | Load the CSVs and perform every pandas operation: filtering, copying, cleaning, mapping, missing-value handling, grouping, aggregation, derived measures, sorting, and validation. |
| `app.py` | Create the Streamlit page shown in the browser: titles, explanatory text, controls, metrics, tables, charts, and warnings. It calls functions from `analysis.py`; it does not perform pandas transformations. |

Streamlit generates the browser page for you. You do not need to create a
separate HTML file.

## Files in this repository

| Path | Purpose |
|---|---|
| `data/09-LAD_batting.csv` | Historical Dodgers batting player-season records. |
| `data/09-LAD_pitching.csv` | Historical Dodgers pitching player-season records. |
| `data/README.md` | Grain, important fields, missingness, and baseball-specific cautions. |
| `analysis.py` | Starter data layer. Codex extends this file with pandas functions. |
| `app.py` | Starter Streamlit layer. Codex extends this file with the dashboard interface. |
| `homework.md` | Requirements and submission checklist. Use after Wednesday's demonstration. |
| `reflection.md` | The individual reflection you complete in your own words. |
| `check_structure.py` | Confirms the data files and two-file architecture remain intact. |
| `AGENTS.md` | Rules Codex must follow while working in this repository. |
| `tutor.md` | Optional guided pandas and dashboard review. |
| `demo/README.md` | Location for the professor's demonstration notes after class. |

## After the demonstration

Open this repository in VS Code and use the shared DSO 576 environment.

Mac:

```text
~/dso576/00-setup/.venv/bin/python -m streamlit run app.py
```

Windows PowerShell:

```text
~/dso576/00-setup/.venv/Scripts/python.exe -m streamlit run app.py
```

Run the architecture check with the same Python executable:

```text
python check_structure.py
```

If `python` does not refer to the shared course environment, use the full Mac or
Windows executable shown above before `check_structure.py`.

Students work locally and commit locally. Do not push work to the course
repository. Submit the ZIP artifact described in `homework.md` through
Brightspace.
