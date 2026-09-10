# WorldStage data dictionary

All records and organizations in this repository are fictional.

## The three show files

### `concept_shows.csv`

The exact 20-row table used in the Module 4 Concepts pages. One row represents
one completed concert. It is deliberately small enough to trace by hand.

### `worldstage_shows.csv`

The larger analysis-ready extract. It contains 480 completed concerts: 120 per
region, five countries per region, and dates from January through December
2026. One row represents one completed concert.

Blank `fan_rating` means the show did not receive enough survey responses for a
rating. It is not a rating of zero.

### `worldstage_shows_raw.csv`

A 600-row staging export assembled from venue, promoter, and ticketing-system
files. One row represents one planned concert record. It includes completed,
cancelled, and postponed records. Raw text is intentionally inconsistent.

## Column definitions

| Column | Meaning |
|---|---|
| `show_id` | Unique fictional show record. |
| `show_date` | Scheduled calendar date in `YYYY-MM-DD` form. |
| `month` | Three-letter month label in the clean file. |
| `region` | Approved reporting region: Asia, Europe, America, or Africa. |
| `country` | Approved display country. |
| `city` | Host city in the clean file. |
| `country_raw` | Country text exactly as supplied by a source platform. |
| `event_type` | Approved display event type. |
| `event_type_raw` | Event type exactly as supplied. |
| `status_raw` | Status exactly as supplied. |
| `capacity` | Sellable venue capacity for the show. |
| `tickets_sold` | Tickets recorded as sold. A blank means attendance evidence is unavailable. |
| `ticket_price` | Numeric average ticket price in US dollars. |
| `ticket_price_raw` | Price text exactly as supplied. |
| `marketing_spend` | Paid media spend in US dollars. |
| `fan_rating` | Average post-show survey rating on a 1–5 scale. |

## Approved cleaning rules

These rules are business definitions, not convenient guesses.

### Countries and regions

Normalize `country_raw` by stripping surrounding spaces, lowercasing, removing
literal periods, and replacing hyphens with spaces. Then map the resulting key
through `country_aliases.csv`.

If the key is absent from the lookup, both cleaned `country` and `region` remain
missing. Do not infer a location from a city, price, event type, or neighboring
row.

### Event type

After text normalization, these are the only approved whole-value replacements:

| Normalized raw value | Approved value before title case |
|---|---|
| `club` | `club show` |
| `stadium` | `stadium show` |
| `festival show` | `festival` |

Any other normalized value stays as written. A blank remains missing.

### Status

After stripping and lowercasing:

- `complete` becomes `completed`;
- `canceled` becomes `cancelled`;
- `completed`, `cancelled`, and `postponed` remain themselves.

Do not treat cancelled or postponed shows as completed.

### Ticket price

- `$95`, `95 USD`, `95`, and surrounding-space variants all mean numeric 95.
- `FREE` is a known price of 0.
- `TBD`, blank text, and any other unparseable value mean unknown price and
  become missing through `pd.to_numeric(..., errors="coerce")`.
- Unknown price is not zero.

### Missing values

- Blank `marketing_spend` means no paid campaign was purchased. Fill it with 0.
- Blank `fan_rating` means no usable survey rating. Leave it missing.
- Blank `tickets_sold` means attendance evidence is unavailable. Leave it
  missing and exclude the row only from tables that require attendance.
- Blank or unrecognized country means the location is unresolved. Leave it
  missing.
- Blank or `TBD` ticket price means price is unknown. Leave it missing and
  exclude the row only from revenue work.

Never run `df.fillna(0)` on the entire DataFrame. Missingness has a different
meaning in each column.

## Metric definitions

- **Sell-through** — `tickets_sold / capacity`. The denominator is the sellable
  capacity of that show.
- **Revenue** — `tickets_sold * ticket_price`. This is modeled ticket revenue,
  not profit and not cash received after fees or refunds.
- **Total tickets** — sum of show-level `tickets_sold` within the group.
- **Average sell-through** — mean of the show-level sell-through values. Every
  show receives equal weight; this is not the same as total tickets divided by
  total capacity.
- **Shows** — number of rows, including rows with a missing rating.
- **Rated shows** — number of nonmissing `fan_rating` values.
- **Countries** — number of distinct nonmissing approved countries.
- **Average rating** — mean across nonmissing ratings only.

