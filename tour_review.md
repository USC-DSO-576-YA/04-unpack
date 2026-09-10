# WorldStage Regional Tour Review

**Analyst:** <!-- your name -->  
**Date:** <!-- today's date -->

> Write this review in your own words after you inspect the generated code,
> tables, audit file, and chart. Do not paste an agent's recommendation here.

## 1. What changed when the data was grouped?

**Input grain:** <!-- one row per what? -->

**Output grain:** <!-- one row per what? -->

**Where the grain changed:** <!-- name the exact operation -->

In two or three sentences, explain what information disappeared during the
aggregation and which columns survived because they were group keys or measures.

<!-- your explanation -->

## 2. Read the regional summary

Complete this table from `regional_summary.csv`.

| Question | Region | Evidence |
|---|---|---|
| Highest total tickets | | |
| Highest average sell-through | | |
| Highest total revenue | | |
| Highest average fan rating | | |
| Fewest rated shows | | |

Why can two different regions legitimately “win” total tickets and average
sell-through?

<!-- your explanation; name both metrics and their denominators -->

Explain the difference between `shows` and `rated_shows`. Point to one region's
numbers as evidence.

<!-- your explanation -->

## 3. Audit the chart

**Chart source table:** <!-- file and column -->

**Grain of each bar:** <!-- one bar per what? -->

**Units on the x-axis:** <!-- proportion or percentage? -->

State one comparison the chart supports and one claim it does not support.

<!-- your explanation -->

## 4. Explain the cleaning decisions

Use `cleaning_audit.csv`, `worldstage_cleaned.csv`, and the data dictionary.

| Field | Missing count before fill/drop | Decision | Why that decision is defensible |
|---|---:|---|---|
| `country` | | | |
| `event_type` | | | |
| `ticket_price` | | | |
| `marketing_spend` | | | |
| `fan_rating` | | | |
| `tickets_sold` | | | |

Choose one raw country alias and trace it through `country_key` to `country` and
`region`. Then choose one unrecognized country value and explain why the code
leaves it missing.

<!-- your trace -->

Why is `FREE` converted to zero while `TBD` is left missing?

<!-- your explanation -->

Why would `work.fillna(0)` be wrong for this dataset? Name at least two columns
whose missing values mean different things.

<!-- your explanation -->

## 5. Fit-for-purpose tables

| Table | Rows | What question it can support | What it excludes |
|---|---:|---|---|
| full cleaned working table | | | |
| `attendance_ready` | | | |
| `revenue_ready` | | | |
| rows with a fan rating | | | |

Explain why these tables do not need to have the same number of rows.

<!-- your explanation -->

## 6. Recommendation

Recommend one regional next step: add dates, investigate further, or hold the
current plan. Use at least two different measures, state one data-quality caveat,
and name one additional piece of evidence you would request before committing
money.

<!-- your recommendation -->

