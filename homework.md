# Module 4 homework — WorldStage code and review

## Objective

Write the important pandas operations yourself, then use the resulting tables
to make a defensible regional recommendation. Codex may coach and check an
attempt, but it may not write the homework code or review for you.

## What you submit

Submit both files through the course submission link:

- `worldstage_homework.py` — your completed code scaffold;
- `tour_review.md` — your evidence-based review in your own words.

Your instructor will announce the due date and submission location.

## Setup

Run:

```text
uv sync
uv run python check_homework.py
```

The first check should report unfinished tasks. That is expected.

## The ten code tasks

Complete the `TODO` blocks in `worldstage_homework.py` in order.

| Task | Code you write | Main vocabulary |
|---:|---|---|
| 1 | Add two show-level measures | `.copy()`, derived column, denominator |
| 2 | Collapse 480 shows to four region rows | `groupby`, named `.agg`, `sum`, `mean`, `size`, `count`, `nunique` |
| 3 | Normalize raw country text | `.str.strip`, `.str.lower`, `.str.replace` |
| 4 | Translate approved location keys | `.map()` and missing unknown keys |
| 5 | Standardize event and status labels | string methods and whole-value `.replace()` |
| 6 | Parse messy ticket prices | `pd.to_numeric(errors="coerce")` |
| 7 | Count missing values by field | `.isna().sum()` |
| 8 | Apply the one justified fill | `.fillna()` |
| 9 | Build analysis-specific row sets | `.notna()`, `.loc`, `.dropna()` |
| 10 | Plot the four-region comparison | sorting, horizontal bar chart, percentage units |

Most tasks require one to four statements. Do not replace the scaffold with an
agent-generated pipeline.

## Check and inspect

After every task, run:

```text
uv run python check_homework.py
```

The checker reports only task status and structural problems; it does not print
the regional winners. Once every task passes, the homework creates:

- `regional_summary.csv`;
- `sell_through_by_region.png`;
- `worldstage_cleaned.csv`;
- `cleaning_audit.csv`.

Inspect those four outputs, then complete `tour_review.md` without asking Codex
to draft the wording or recommendation.

## Final checklist

- No `TODO` or `NotImplementedError` remains.
- `uv run python check_homework.py` reports all checks passed.
- You can state the input and output grain for every grouped table.
- You can justify why `FREE` becomes zero but `TBD` remains missing.
- You can explain why attendance, revenue, and rating tables have different row
  counts.
- The code and review are yours, and both required filenames are unchanged.
