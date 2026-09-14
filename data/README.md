# Dodgers data notes

These two course-provided CSV files contain historical Los Angeles Dodgers player-season records. Treat them as the supplied assignment data; do not describe them as an official MLB export unless you separately verify their original source.

Do not edit either source CSV. Create cleaned or summarized DataFrames in `analysis.py`, and export any derived submission file under a new name.

## Grain and coverage

| File | Grain | Rows | Columns | Years |
|---|---|---:|---:|---:|
| `09-LAD_batting.csv` | one batter-season record | 2,758 | 31 | 1958–2023 |
| `09-LAD_pitching.csv` | one pitcher-season record | 1,253 | 37 | 1958–2023 |

A player can appear in multiple years. Therefore, counting rows is not the same as counting unique people across the full dataset.

## Useful batting fields

- `Year`, `Name`, `Position`
- `Games_Played`, `Plate_Appearances`, `At_Bats`
- `Hits`, `Doubles`, `Triples`, `Home_Runs`
- `Walks`, `Strikeouts`, `Stolen_Bases`
- `Batting_Average`, `On_Base_Percentage`, `Slugging_Percentage`

When combining players, calculate batting average from the totals:

```python
combined_ba = total_hits / total_at_bats
```

Do not take the unweighted mean of player batting averages.

One possible readable batting-role mapping is:

```python
{
    "C": "Catcher",
    "1B": "Infield",
    "2B": "Infield",
    "3B": "Infield",
    "SS": "Infield",
    "IF": "Infield",
    "MI": "Infield",
    "CI": "Infield",
    "LF": "Outfield",
    "CF": "Outfield",
    "RF": "Outfield",
    "OF": "Outfield",
    "DH": "Flex / other",
    "UT": "Flex / other",
    "P": "Flex / other",
}
```

Inspect the actual values before deciding whether this mapping fits your question.

## Useful pitching fields

- `Year`, `Name`, `Position`
- `Games_Played`, `Games_Started`, `Wins`, `Losses`, `Saves`
- `Innings_Pitched`, `Hits_Allowed`, `Runs_Allowed`, `Walks`, `Strikeouts`
- `Earned_Run_Average`, `Walks_Hits_Per_Inning_Pitched`

In the full pitching file, `Position` is missing for 592 of 1,253 rows. Preserve that information instead of silently dropping those rows. For this exercise, use:

```python
{
    "SP": "Starting pitcher",
    "RP": "Relief pitcher",
    "CL": "Closer",
}
```

After `.map()`, label missing or unfamiliar values as `Unclassified` in a new column. Reconcile the new group counts with the original filtered row count.

## Important innings-pitched warning

Baseball innings are written in outs, not ordinary tenths. A value displayed as `131.2` means 131 complete innings plus two outs. Do not sum or average `Innings_Pitched` as an ordinary decimal unless you first convert it correctly.
