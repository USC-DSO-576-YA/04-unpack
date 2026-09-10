# WorldStage analysis brief

You are the analyst supporting WorldStage's regional strategy team. The team is
deciding where to add concert dates next year. They need a regional comparison
they can audit, plus a clear record of how the messy partner export was cleaned.

Read these files before doing anything:

- `notes/data_dictionary.md`
- `notes/vocabulary.md`
- `worldstage_shows.csv`
- `worldstage_shows_raw.csv`
- `country_aliases.csv`

First give me a short plan. Name the input and output grain for both the clean
analysis and the raw-data cleaning. Do not write code until I approve the plan.

After approval, create exactly these five files:

1. `worldstage_analysis.py` — one readable script with named steps for both
   parts of the request.
2. `regional_summary.csv` — one row per region, sorted by total tickets sold
   from largest to smallest.
3. `sell_through_by_region.png` — an honest horizontal bar chart made from the
   regional summary.
4. `cleaning_audit.csv` — one row per audit measure, with columns `measure`,
   `value`, and `meaning`.
5. `worldstage_cleaned.csv` — the cleaned raw export, preserving every raw
   column beside its cleaned counterpart.

Do not edit any supplied file. Do not write `tour_review.md` and do not make the
final expansion recommendation for me.

## Part 1 — group, aggregate, and plot the clean data

Load `worldstage_shows.csv` and work on a copy.

At the one-row-per-show grain, create:

- `sell_through = tickets_sold / capacity`
- `revenue = tickets_sold * ticket_price`

Then use one named `.groupby(...).agg(...)` pipeline to produce one row per
region with exactly these columns:

- `region`
- `total_tickets` — sum of `tickets_sold`
- `avg_sell_through` — mean of `sell_through`
- `shows` — number of show rows
- `rated_shows` — number of nonmissing `fan_rating` values
- `countries` — number of distinct nonmissing countries
- `avg_rating` — mean of nonmissing `fan_rating`
- `total_revenue` — sum of `revenue`

Sort by `total_tickets`, largest first. Round `avg_sell_through` to four decimal
places and `avg_rating` to two. Save the exact table to
`regional_summary.csv`.

Make a horizontal bar chart of `avg_sell_through` by region, sorted from lowest
to highest so the largest bar appears at the top. Format the x-axis as a
percentage, use the title `Average concert sell-through by region`, label both
axes, remove the legend, and save it as `sell_through_by_region.png`.

## Part 2 — clean the raw partner export without hiding uncertainty

Load `worldstage_shows_raw.csv` and work on a copy. Apply only the rules in
`notes/data_dictionary.md`.

- Preserve all raw columns.
- Create `country_key` by stripping whitespace, lowercasing, removing literal
  periods, and replacing hyphens with spaces.
- Build approved country and region lookup dictionaries from
  `country_aliases.csv`; create `country` and `region` with `.map()`. Leave
  unrecognized values missing.
- Create `event_type` by stripping whitespace, lowercasing, replacing hyphens
  with spaces, applying only the approved whole-value replacements, and using
  title case for display.
- Create `status` by stripping whitespace, lowercasing, and applying only the
  approved whole-value replacements.
- Clean `ticket_price_raw`: strip whitespace, lowercase, remove literal `$` and
  ` USD`, convert `FREE` to the text `0`, convert blank text to `pd.NA`, then use
  `pd.to_numeric(..., errors="coerce")` to create `ticket_price`.
- Record missing counts before filling anything.
- Fill missing `marketing_spend` with zero only because the data dictionary
  defines blank that way. Leave missing `fan_rating`, `country`, and
  `ticket_price` missing.
- Create `attendance_ready` by dropping rows missing `tickets_sold`.
- Create `revenue_ready` from `attendance_ready` by dropping rows missing
  `ticket_price`.

Save the complete cleaned working table to `worldstage_cleaned.csv`. The audit
file must include at least:

- raw rows;
- completed, cancelled, and postponed rows after status cleaning;
- missing country, event type, ticket price, marketing spend, fan rating, and
  tickets sold before any allowed fill;
- rows in `attendance_ready`;
- rows in `revenue_ready`;
- rows with a nonmissing fan rating.

## Checks to report before stopping

Run the finished script with `uv run python worldstage_analysis.py`, then report:

- the files created;
- the input and output grain of the regional summary;
- the row counts of all three supplied datasets and both fit-for-purpose raw
  tables;
- whether any raw country value was guessed rather than mapped;
- whether the chart and CSV use the same `avg_sell_through` values;
- the exact checks you ran and anything you did not verify.

