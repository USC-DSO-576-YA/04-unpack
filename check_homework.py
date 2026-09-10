"""Structural checker for Module 4; it intentionally does not print answers."""

from __future__ import annotations

import ast
from pathlib import Path
import subprocess
import sys

import pandas as pd


ROOT = Path(__file__).resolve().parent
HOMEWORK = ROOT / "worldstage_homework.py"


def unfinished_tasks() -> list[int]:
    tree = ast.parse(HOMEWORK.read_text(encoding="utf-8"))
    unfinished: list[int] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Raise) or node.exc is None:
            continue
        if not isinstance(node.exc, ast.Call) or not node.exc.args:
            continue
        message = node.exc.args[0]
        if isinstance(message, ast.Constant) and isinstance(message.value, str):
            if message.value.startswith("Complete Task "):
                unfinished.append(int(message.value.removeprefix("Complete Task ")))
    return sorted(unfinished)


def require(condition: bool, task: int, message: str) -> None:
    if not condition:
        raise AssertionError(f"Task {task}: {message}")


def check_outputs() -> None:
    import worldstage_homework as homework

    clean = pd.read_csv(ROOT / "worldstage_shows.csv")
    raw = pd.read_csv(ROOT / "worldstage_shows_raw.csv")
    aliases = pd.read_csv(ROOT / "country_aliases.csv")
    summary = pd.read_csv(ROOT / "regional_summary.csv")
    cleaned = pd.read_csv(ROOT / "worldstage_cleaned.csv")
    audit = pd.read_csv(ROOT / "cleaning_audit.csv")

    metrics = homework.add_show_metrics(clean)
    require(
        {"sell_through", "revenue"}.issubset(metrics.columns),
        1,
        "both derived columns are required",
    )
    expected_sell_through = clean["tickets_sold"] / clean["capacity"]
    expected_revenue = clean["tickets_sold"] * clean["ticket_price"]
    require(
        metrics["sell_through"].equals(expected_sell_through),
        1,
        "sell_through values differ from the defined ratio",
    )
    require(
        metrics["revenue"].equals(expected_revenue),
        1,
        "revenue values differ from the defined product",
    )

    required_summary = [
        "region",
        "total_tickets",
        "avg_sell_through",
        "shows",
        "rated_shows",
        "countries",
        "avg_rating",
        "total_revenue",
    ]
    require(
        list(summary.columns) == required_summary,
        2,
        "summary columns or order differ",
    )
    require(len(summary) == 4, 2, "summary must contain one row per region")
    require(
        set(summary["region"]) == {"Asia", "Europe", "America", "Africa"},
        2,
        "region groups differ",
    )
    require(
        summary["total_tickets"].is_monotonic_decreasing,
        2,
        "total_tickets is not sorted descending",
    )
    require(
        summary["shows"].sum() == len(clean),
        2,
        "show counts do not cover the clean data",
    )
    require(
        summary["total_tickets"].sum() == clean["tickets_sold"].sum(),
        2,
        "ticket totals changed during grouping",
    )
    require(
        summary["rated_shows"].sum() == clean["fan_rating"].count(),
        2,
        "rated-show counts are inconsistent",
    )
    require(
        summary["countries"].sum() == clean["country"].nunique(),
        2,
        "country counts are inconsistent",
    )
    for row in summary.itertuples(index=False):
        region_rows = metrics.loc[metrics["region"].eq(row.region)]
        require(
            row.total_tickets == region_rows["tickets_sold"].sum(),
            2,
            "a regional ticket total is incorrect",
        )
        require(
            row.avg_sell_through == round(region_rows["sell_through"].mean(), 4),
            2,
            "a regional sell-through average is incorrect",
        )
        require(
            row.total_revenue == region_rows["revenue"].sum(),
            2,
            "a regional revenue total is incorrect",
        )

    specimen = pd.Series([" U.S. ", "south-korea", "U.K.", pd.NA], dtype="string")
    expected_keys = pd.Series(["us", "south korea", "uk", pd.NA], dtype="string")
    require(
        homework.normalize_country_keys(specimen).equals(expected_keys),
        3,
        "country-key normalization differs on the checker specimen",
    )

    require(len(cleaned) == len(raw), 4, "cleaning must preserve all raw rows")
    require(set(raw.columns).issubset(cleaned.columns), 4, "a raw column was removed")
    require(
        {"country_key", "country", "region"}.issubset(cleaned.columns),
        4,
        "location columns are missing",
    )
    unknown_mask = raw["country_raw"].eq("Atlantis")
    require(
        cleaned.loc[unknown_mask, ["country", "region"]].isna().all().all(),
        4,
        "an unknown country was guessed",
    )
    mapped = homework.map_locations(raw, aliases)
    country_lookup = aliases.set_index("country_key")["country"]
    region_lookup = aliases.set_index("country_key")["region"]
    require(
        mapped["country"].equals(mapped["country_key"].map(country_lookup)),
        4,
        "country values differ from the approved lookup",
    )
    require(
        mapped["region"].equals(mapped["country_key"].map(region_lookup)),
        4,
        "region values differ from the approved lookup",
    )

    require(
        {"event_type", "status"}.issubset(cleaned.columns),
        5,
        "clean label columns are missing",
    )
    require(
        set(cleaned["status"].dropna())
        == {"completed", "cancelled", "postponed"},
        5,
        "status labels are not standardized",
    )
    require(
        set(cleaned["event_type"].dropna())
        == {"Arena Show", "Festival", "Club Show", "Stadium Show"},
        5,
        "event labels are not standardized",
    )
    labels = homework.clean_labels(mapped)
    require(
        labels[["event_type", "status"]]
        .astype("string")
        .fillna("<missing>")
        .equals(
            cleaned[["event_type", "status"]]
            .astype("string")
            .fillna("<missing>")
        ),
        5,
        "saved labels differ from the Task 5 result",
    )

    require("ticket_price" in cleaned.columns, 6, "numeric ticket_price is missing")
    raw_price = raw["ticket_price_raw"].astype("string").str.strip().str.lower()
    free_mask = raw_price.eq("free")
    unknown_price = raw_price.isin(["", "tbd"])
    require(
        cleaned.loc[free_mask, "ticket_price"].eq(0).all(),
        6,
        "FREE must become known zero",
    )
    require(
        cleaned.loc[unknown_price, "ticket_price"].isna().all(),
        6,
        "blank and TBD prices must stay unknown",
    )
    prices = homework.parse_ticket_prices(labels)
    require(
        prices["ticket_price"]
        .astype("Float64")
        .equals(cleaned["ticket_price"].astype("Float64")),
        6,
        "saved prices differ from the Task 6 result",
    )

    expected_measures = {
        "raw_rows",
        "completed_rows",
        "cancelled_rows",
        "postponed_rows",
        "missing_country_before_fill",
        "missing_event_type_before_fill",
        "missing_ticket_price_before_fill",
        "missing_marketing_spend_before_fill",
        "missing_fan_rating_before_fill",
        "missing_tickets_sold_before_fill",
        "attendance_ready_rows",
        "revenue_ready_rows",
        "rating_ready_rows",
    }
    require(
        set(audit["measure"]) == expected_measures,
        7,
        "cleaning audit measures differ",
    )
    missing = homework.missing_counts_before_fill(prices)
    audit_values = audit.set_index("measure")["value"]
    for column, value in missing.items():
        require(
            audit_values[f"missing_{column}_before_fill"] == value,
            7,
            "a missing-value count is incorrect",
        )

    filled = homework.apply_missing_rule(prices)
    require(
        filled["marketing_spend"].notna().all(),
        8,
        "marketing_spend still contains missing values",
    )
    require(
        filled["fan_rating"].equals(prices["fan_rating"]),
        8,
        "fan-rating missingness was changed",
    )
    require(
        filled["tickets_sold"].equals(prices["tickets_sold"]),
        8,
        "attendance missingness was changed",
    )

    attendance, revenue, ratings = homework.make_analysis_tables(filled)
    attendance_rows = int(audit_values["attendance_ready_rows"])
    revenue_rows = int(audit_values["revenue_ready_rows"])
    rating_rows = int(audit_values["rating_ready_rows"])
    require(
        attendance_rows == len(attendance),
        9,
        "attendance-ready row count differs",
    )
    require(
        revenue_rows == len(revenue),
        9,
        "revenue-ready row count differs",
    )
    require(
        rating_rows == len(ratings),
        9,
        "rating-ready row count differs",
    )
    require(attendance["tickets_sold"].notna().all(), 9, "attendance table has unknown tickets")
    require(
        revenue[["tickets_sold", "ticket_price"]].notna().all().all(),
        9,
        "revenue table has an unknown required field",
    )
    require(ratings["fan_rating"].notna().all(), 9, "rating table has unknown ratings")

    chart = ROOT / "sell_through_by_region.png"
    require(
        chart.exists() and chart.stat().st_size > 5_000,
        10,
        "chart file is missing or empty",
    )


def main() -> None:
    unfinished = unfinished_tasks()
    if unfinished:
        joined = ", ".join(str(task) for task in unfinished)
        print(f"Unfinished tasks: {joined}")
        print(f"Start with Task {unfinished[0]}. The checker will not show its answer.")
        raise SystemExit(1)

    run = subprocess.run(
        [sys.executable, str(HOMEWORK)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if run.returncode != 0:
        print("The homework script stopped before structural checks could run.")
        print(run.stderr.strip() or run.stdout.strip())
        raise SystemExit(1)

    try:
        check_outputs()
    except AssertionError as error:
        print(error)
        print("Revise that task, then run the checker again.")
        raise SystemExit(1) from error

    print("All 10 code tasks passed the structural checks.")
    print("Inspect the four outputs and complete tour_review.md in your own words.")


if __name__ == "__main__":
    main()
