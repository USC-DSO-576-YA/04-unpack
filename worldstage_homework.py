"""Module 4 homework scaffold: complete the ten TODO tasks yourself."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import pandas as pd


ROOT = Path(__file__).resolve().parent


def add_show_metrics(shows: pd.DataFrame) -> pd.DataFrame:
    """Task 1: return a copy with show-level sell_through and revenue."""
    work = shows.copy()

    # TODO 1: Write the two column-assignment statements described above.
    raise NotImplementedError("Complete Task 1")

    return work


def summarize_regions(shows: pd.DataFrame) -> pd.DataFrame:
    """Task 2: return the required one-row-per-region summary."""
    # Required columns, in order:
    # region, total_tickets, avg_sell_through, shows, rated_shows,
    # countries, avg_rating, total_revenue
    # Use one named groupby(...).agg(...) pipeline. Then round the two average
    # columns and sort total_tickets from largest to smallest.

    # TODO 2: Replace this exception with your aggregation, rounding, and sort.
    raise NotImplementedError("Complete Task 2")


def normalize_country_keys(values: pd.Series) -> pd.Series:
    """Task 3: normalize country text into approved lookup keys."""
    # Strip outside spaces, lowercase, remove literal periods, and replace
    # hyphens with spaces. Return a Series; do not fill blanks or unknowns.

    # TODO 3: Replace this exception with one string-method chain.
    raise NotImplementedError("Complete Task 3")


def map_locations(raw: pd.DataFrame, aliases: pd.DataFrame) -> pd.DataFrame:
    """Task 4: preserve raw fields and add country_key, country, and region."""
    work = raw.copy()
    work["country_key"] = normalize_country_keys(work["country_raw"])

    country_lookup = aliases.set_index("country_key")["country"].to_dict()
    region_lookup = aliases.set_index("country_key")["region"].to_dict()

    # TODO 4: Add country and region with two Series.map(...) assignments.
    raise NotImplementedError("Complete Task 4")

    return work


def clean_labels(work: pd.DataFrame) -> pd.DataFrame:
    """Task 5: add standardized event_type and status columns."""
    result = work.copy()
    event_replacements = {
        "club": "club show",
        "stadium": "stadium show",
        "festival show": "festival",
    }
    status_replacements = {"complete": "completed", "canceled": "cancelled"}

    # TODO 5: Normalize the two raw Series and apply only the dictionaries
    # above. Event labels should use title case; status labels stay lowercase.
    raise NotImplementedError("Complete Task 5")

    return result


def parse_ticket_prices(work: pd.DataFrame) -> pd.DataFrame:
    """Task 6: add numeric ticket_price without changing ticket_price_raw."""
    result = work.copy()

    # TODO 6: Clean ticket_price_raw according to the data dictionary, then use
    # pd.to_numeric(..., errors="coerce"). FREE is known zero; TBD is unknown.
    raise NotImplementedError("Complete Task 6")

    return result


def missing_counts_before_fill(work: pd.DataFrame) -> pd.Series:
    """Task 7: count missing values in the six audited fields."""
    audit_columns = [
        "country",
        "event_type",
        "ticket_price",
        "marketing_spend",
        "fan_rating",
        "tickets_sold",
    ]

    # TODO 7: Return one Series indexed by audit_columns.
    raise NotImplementedError("Complete Task 7")


def apply_missing_rule(work: pd.DataFrame) -> pd.DataFrame:
    """Task 8: apply only the documented marketing-spend fill."""
    result = work.copy()

    # TODO 8: Fill missing marketing_spend with zero in one assignment.
    # Do not fill any other column.
    raise NotImplementedError("Complete Task 8")

    return result


def make_analysis_tables(
    work: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Task 9: return attendance-, revenue-, and rating-ready tables."""
    # attendance_ready requires tickets_sold.
    # revenue_ready is a subset of attendance_ready and also requires price.
    # rating_ready requires fan_rating, regardless of the other two measures.

    # TODO 9: Create all three independent copies, then return them in the
    # order named above. Use .loc with .notna() at least once and
    # .dropna(subset=[...]) at least once.
    raise NotImplementedError("Complete Task 9")


def make_sell_through_chart(summary: pd.DataFrame, output_path: Path) -> None:
    """Task 10: save the required four-region horizontal bar chart."""
    # Sort avg_sell_through from lowest to highest for a horizontal bar chart.
    # Use percentage tick labels, label both axes, remove the legend, and title
    # it "Average concert sell-through by region".

    # TODO 10: Replace this exception with the plotting statements and save the
    # figure to output_path at dpi=150 with bbox_inches="tight". Close it after.
    raise NotImplementedError("Complete Task 10")


def build_cleaning_audit(
    before_fill: pd.DataFrame,
    missing_counts: pd.Series,
    attendance_ready: pd.DataFrame,
    revenue_ready: pd.DataFrame,
    rating_ready: pd.DataFrame,
) -> pd.DataFrame:
    """Assemble already-computed checks; this helper is not a TODO task."""
    statuses = before_fill["status"].value_counts(dropna=False)
    rows = [
        ("raw_rows", len(before_fill), "all planned concert records"),
        ("completed_rows", statuses.get("completed", 0), "cleaned status"),
        ("cancelled_rows", statuses.get("cancelled", 0), "cleaned status"),
        ("postponed_rows", statuses.get("postponed", 0), "cleaned status"),
    ]
    rows.extend(
        (
            f"missing_{column}_before_fill",
            int(value),
            "missing before any allowed fill",
        )
        for column, value in missing_counts.items()
    )
    rows.extend(
        [
            ("attendance_ready_rows", len(attendance_ready), "tickets known"),
            (
                "revenue_ready_rows",
                len(revenue_ready),
                "tickets and price known",
            ),
            ("rating_ready_rows", len(rating_ready), "fan rating known"),
        ]
    )
    return pd.DataFrame(rows, columns=["measure", "value", "meaning"])


def main() -> None:
    clean = pd.read_csv(ROOT / "worldstage_shows.csv")
    raw = pd.read_csv(ROOT / "worldstage_shows_raw.csv")
    aliases = pd.read_csv(ROOT / "country_aliases.csv")

    shows_with_metrics = add_show_metrics(clean)
    summary = summarize_regions(shows_with_metrics)
    summary.to_csv(ROOT / "regional_summary.csv", index=False)
    make_sell_through_chart(summary, ROOT / "sell_through_by_region.png")

    cleaned = map_locations(raw, aliases)
    cleaned = clean_labels(cleaned)
    cleaned = parse_ticket_prices(cleaned)
    missing_counts = missing_counts_before_fill(cleaned)
    before_fill = cleaned.copy()
    cleaned = apply_missing_rule(cleaned)
    attendance_ready, revenue_ready, rating_ready = make_analysis_tables(cleaned)

    cleaned.to_csv(ROOT / "worldstage_cleaned.csv", index=False)
    audit = build_cleaning_audit(
        before_fill,
        missing_counts,
        attendance_ready,
        revenue_ready,
        rating_ready,
    )
    audit.to_csv(ROOT / "cleaning_audit.csv", index=False)

    print("Homework pipeline completed. Now run: uv run python check_homework.py")


if __name__ == "__main__":
    main()
