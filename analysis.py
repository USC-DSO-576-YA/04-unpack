"""Pandas data layer for the Module 4 Dodgers dashboard.

All DataFrame loading, cleaning, filtering, grouping, derived metrics, sorting,
and validation belong in this file. Do not import Streamlit here.
"""

from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).parent / "data"
BATTING_PATH = DATA_DIR / "09-LAD_batting.csv"
PITCHING_PATH = DATA_DIR / "09-LAD_pitching.csv"


def load_batting() -> pd.DataFrame:
    """Return an unchanged copy of the supplied batting data."""
    return pd.read_csv(BATTING_PATH)


def load_pitching() -> pd.DataFrame:
    """Return an unchanged copy of the supplied pitching data."""
    return pd.read_csv(PITCHING_PATH)


def source_inventory() -> dict[str, int]:
    """Return starter checks that the Streamlit layer may display."""
    batting = load_batting()
    pitching = load_pitching()
    return {
        "batting_rows": len(batting),
        "pitching_rows": len(pitching),
        "first_year": int(min(batting["Year"].min(), pitching["Year"].min())),
        "last_year": int(max(batting["Year"].max(), pitching["Year"].max())),
    }


# After Wednesday's demonstration, ask Codex to add the dashboard's filtering,
# role mapping, missing-value audit, grouped summaries, derived measures, sorting,
# and validation functions below. Keep every DataFrame operation in this file.
