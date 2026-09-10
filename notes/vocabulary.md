# Module 4 vocabulary

## Monday — group, aggregate, and plot

- **grain** — what one row represents; say “one row per ___.”
- **group key** — the column whose values define the groups.
- **`groupby()`** — splits rows by the group key; an aggregation then combines
  each group.
- **aggregation** — a rule that reduces many values to a summary value.
- **named aggregation / `.agg()`** — creates several clearly named summary
  columns in one grouped result.
- **`sum`** — adds nonmissing values.
- **`mean`** — averages nonmissing values.
- **`size`** — counts every row in a group.
- **`count`** — counts nonmissing values in a specific column.
- **`nunique`** — counts distinct nonmissing values.
- **`as_index=False`** — keeps the group key as an ordinary column.
- **derived column** — a column computed from existing columns, such as
  `tickets_sold / capacity`.
- **`sort_values()`** — reorders rows by values; it does not remove rows.
- **bar chart** — compares one number across categories.
- **line chart** — follows a number across ordered time.
- **scatter plot** — compares two numeric variables.
- **axis, unit, and title** — the chart labels that define what the picture
  actually claims.

## Wednesday — standardize text and handle missingness

- **raw column** — a field preserved exactly as supplied.
- **cleaned column** — a new standardized field derived from raw data.
- **`.copy()`** — creates an independent DataFrame before cleaning.
- **`.str.strip()`** — removes spaces at the beginning and end of each string.
- **`.str.lower()`** — lowercases each string for consistent comparison.
- **`.str.title()`** — capitalizes words for display.
- **`.str.replace(..., regex=False)`** — replaces literal text inside every
  string.
- **`.str.contains(..., na=False)`** — checks for a pattern and treats missing
  text as False for that Boolean question.
- **Series `.replace()`** — replaces whole values, not text inside values.
- **`.map(lookup)`** — translates each Series value through an approved mapping;
  an unknown key becomes missing.
- **missing value / `NaN` / `pd.NA`** — unavailable or unknown data, whose
  meaning depends on the column.
- **`.isna()`** — True where a value is missing.
- **`.notna()`** — True where a value is present.
- **`.fillna(value)`** — replaces missing values only when a documented meaning
  justifies the replacement.
- **`.dropna(subset=[...])`** — removes rows missing fields required for one
  named analysis.
- **`pd.to_numeric(..., errors="coerce")`** — parses numeric text and turns
  unparseable values into missing values.
- **`value_counts(dropna=False)`** — counts categories while keeping missing
  values visible during an audit.
- **fit-for-purpose table** — a table whose rows are usable for one stated
  question; attendance, revenue, and rating work may require different rows.
- **data dictionary** — the authority for what columns and missing values mean.

## Cumulative vocabulary still in use

DataFrame, Series, index, column selection, Boolean mask, `.loc`, `.iloc`,
`.head()`, `.shape`, `.columns`, `.dtypes`, `.reset_index()`, `.sort_values()`,
`.copy()`, function, parameter, return value, type hint, `len`, `min`, `max`,
and denominator.

