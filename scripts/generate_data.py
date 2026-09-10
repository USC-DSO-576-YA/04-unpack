"""Generate the fictional WorldStage concert datasets.

The seed is fixed so every student receives identical files. Run this script
only when maintaining the repository; students should treat the generated CSVs
as read-only source data.
"""

from __future__ import annotations

import csv
import random
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RNG = random.Random(57604)

COUNTRIES = {
    "Asia": [
        ("Japan", "Tokyo"),
        ("South Korea", "Seoul"),
        ("Singapore", "Singapore"),
        ("Thailand", "Bangkok"),
        ("India", "Mumbai"),
    ],
    "Europe": [
        ("France", "Paris"),
        ("United Kingdom", "London"),
        ("Germany", "Berlin"),
        ("Spain", "Madrid"),
        ("Italy", "Milan"),
    ],
    "America": [
        ("United States", "Los Angeles"),
        ("Mexico", "Mexico City"),
        ("Brazil", "Sao Paulo"),
        ("Argentina", "Buenos Aires"),
        ("Colombia", "Bogota"),
    ],
    "Africa": [
        ("Nigeria", "Lagos"),
        ("South Africa", "Johannesburg"),
        ("Kenya", "Nairobi"),
        ("Egypt", "Cairo"),
        ("Ghana", "Accra"),
    ],
}

EVENTS = ["Arena Show", "Festival", "Club Show", "Stadium Show"]
BASE_CAPACITY = {
    "Arena Show": 12_000,
    "Festival": 22_000,
    "Club Show": 2_800,
    "Stadium Show": 42_000,
}
REGION_CAPACITY = {"Asia": 1.00, "Europe": 1.30, "America": 1.02, "Africa": 0.72}
REGION_SELL_THROUGH = {"Asia": 0.84, "Europe": 0.75, "America": 0.92, "Africa": 0.80}
REGION_PRICE = {"Asia": 82, "Europe": 102, "America": 74, "Africa": 54}
REGION_RATING = {"Asia": 4.55, "Europe": 4.38, "America": 4.68, "Africa": 4.48}

CONCEPT_ROWS = [
    ["S01", "Asia", "Japan", "Jan", 9000, 10000, 90, 4.8],
    ["S02", "Asia", "South Korea", "Feb", 8000, 10000, 80, 4.7],
    ["S03", "Europe", "France", "Jan", 7000, 10000, 100, 4.3],
    ["S04", "Europe", "United Kingdom", "Feb", 9000, 12000, 110, 4.4],
    ["S05", "Europe", "Germany", "Mar", 10000, 14000, 105, ""],
    ["S06", "America", "Brazil", "Jan", 9500, 10000, 70, 4.9],
    ["S07", "America", "Mexico", "Feb", 8500, 9000, 65, 4.8],
    ["S08", "Africa", "Nigeria", "Mar", 4800, 6000, 50, ""],
    ["S09", "Africa", "South Africa", "Mar", 5200, 6500, 55, 4.6],
    ["S10", "Europe", "France", "Mar", 8000, 10000, 85, 4.5],
    ["S11", "Asia", "Singapore", "Mar", 7500, 9000, 75, 4.6],
    ["S12", "Asia", "Thailand", "Apr", 8500, 10000, 88, ""],
    ["S13", "Asia", "India", "Apr", 9200, 11000, 82, 4.5],
    ["S14", "Europe", "Spain", "Apr", 11000, 15000, 95, 4.2],
    ["S15", "America", "Argentina", "Mar", 7800, 8500, 68, 4.7],
    ["S16", "America", "Chile", "Apr", 8800, 9500, 72, ""],
    ["S17", "America", "Colombia", "Apr", 9700, 10500, 75, 4.9],
    ["S18", "Africa", "Kenya", "Jan", 6100, 7500, 60, 4.5],
    ["S19", "Africa", "Egypt", "Feb", 5700, 7000, 58, 4.4],
    ["S20", "Africa", "Ghana", "Apr", 6300, 8000, 62, ""],
]

RAW_VARIANTS = {
    "United States": [" U.S. ", "USA", "United States", "united-states"],
    "United Kingdom": ["uk", "U.K.", "United Kingdom ", "great britain"],
    "South Korea": ["South Korea", "south-korea", "KOREA, SOUTH"],
}


def month_name(month: int) -> str:
    return date(2026, month, 1).strftime("%b")


def clean_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    show_no = 1
    for region, locations in COUNTRIES.items():
        for country_no, (country, city) in enumerate(locations):
            for month in range(1, 13):
                for repeat in range(2):
                    event = EVENTS[(show_no + country_no + repeat) % len(EVENTS)]
                    capacity_factor = RNG.uniform(0.88, 1.12)
                    capacity = int(
                        round(
                            BASE_CAPACITY[event]
                            * REGION_CAPACITY[region]
                            * capacity_factor
                            / 100
                        )
                        * 100
                    )
                    season = 0.035 if month in {5, 6, 7, 8} else -0.01
                    event_shift = {
                        "Club Show": 0.04,
                        "Arena Show": 0.02,
                        "Festival": -0.01,
                        "Stadium Show": -0.04,
                    }[event]
                    rate = REGION_SELL_THROUGH[region] + season + event_shift
                    rate += RNG.gauss(0, 0.045)
                    rate = min(0.995, max(0.52, rate))
                    tickets = min(capacity, int(round(capacity * rate / 10) * 10))

                    event_price = {
                        "Club Show": -12,
                        "Arena Show": 8,
                        "Festival": 0,
                        "Stadium Show": 18,
                    }[event]
                    price = max(20, int(round(REGION_PRICE[region] + event_price + RNG.randint(-6, 6))))
                    spend = 0 if RNG.random() < 0.18 else int(round(capacity * RNG.uniform(0.45, 1.05)))
                    rating_value = REGION_RATING[region] + (rate - REGION_SELL_THROUGH[region]) * 1.4
                    rating_value += RNG.gauss(0, 0.16)
                    rating = "" if RNG.random() < 0.14 else round(min(5.0, max(3.3, rating_value)), 1)

                    rows.append(
                        {
                            "show_id": f"WS{show_no:04d}",
                            "show_date": date(2026, month, 4 + repeat * 14 + country_no).isoformat(),
                            "month": month_name(month),
                            "region": region,
                            "country": country,
                            "city": city,
                            "event_type": event,
                            "capacity": capacity,
                            "tickets_sold": tickets,
                            "ticket_price": price,
                            "marketing_spend": spend,
                            "fan_rating": rating,
                        }
                    )
                    show_no += 1
    assert len(rows) == 480
    return rows


def raw_country(country: str, row_no: int) -> str:
    if row_no % 173 == 0:
        return ""
    if row_no % 113 == 0:
        return "Atlantis"
    if country in RAW_VARIANTS:
        return RAW_VARIANTS[country][row_no % len(RAW_VARIANTS[country])]
    variants = [country, country.upper(), f" {country} ", country.lower().replace(" ", "-")]
    return variants[row_no % len(variants)]


def raw_event(event: str, row_no: int) -> str:
    if row_no % 89 == 0:
        return ""
    variants = {
        "Arena Show": ["Arena-Show", "arena show ", "ARENA SHOW"],
        "Festival": ["FESTIVAL", "festival-show", " Festival "],
        "Club Show": ["Club", "club-show", "CLUB SHOW "],
        "Stadium Show": ["Stadium-Show", "stadium show ", "STADIUM"],
    }
    return variants[event][row_no % len(variants[event])]


def raw_status(status: str, row_no: int) -> str:
    variants = {
        "completed": [" COMPLETE ", "completed", "Complete", "Completed "],
        "cancelled": ["CANCELLED", "cancelled ", "Canceled"],
        "postponed": ["POSTPONED", " postponed", "Postponed "],
    }
    return variants[status][row_no % len(variants[status])]


def raw_price(price: int, status: str, row_no: int) -> str:
    if status == "completed" and row_no % 37 == 0:
        return "FREE"
    if row_no % 29 == 0:
        return "TBD"
    if row_no % 41 == 0:
        return ""
    variants = [f"${price}", f"{price} USD", str(price), f" {price} "]
    return variants[row_no % len(variants)]


def messy_rows(base_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row_no in range(1, 601):
        base = dict(base_rows[(row_no * 7) % len(base_rows)])
        roll = row_no % 20
        status = "completed" if roll < 16 else ("cancelled" if roll < 18 else "postponed")
        country = str(base["country"])
        event = str(base["event_type"])
        price = int(base["ticket_price"])

        tickets: object = base["tickets_sold"]
        if status == "cancelled":
            tickets = 0
        elif status == "postponed" or row_no % 47 == 0:
            tickets = ""

        marketing: object = base["marketing_spend"]
        if row_no % 5 == 0:
            marketing = ""

        rating: object = base["fan_rating"]
        if status != "completed" or row_no % 4 == 0:
            rating = ""

        rows.append(
            {
                "show_id": f"RAW{row_no:04d}",
                "show_date": base["show_date"],
                "country_raw": raw_country(country, row_no),
                "event_type_raw": raw_event(event, row_no),
                "status_raw": raw_status(status, row_no),
                "capacity": base["capacity"],
                "tickets_sold": tickets,
                "ticket_price_raw": raw_price(price, status, row_no),
                "marketing_spend": marketing,
                "fan_rating": rating,
            }
        )
    assert len(rows) == 600
    return rows


def normalized_key(value: str) -> str:
    return value.strip().lower().replace(".", "").replace("-", " ")


def alias_rows() -> list[dict[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for region, locations in COUNTRIES.items():
        for country, _ in locations:
            variants = RAW_VARIANTS.get(
                country,
                [country, country.upper(), f" {country} ", country.lower().replace(" ", "-")],
            )
            for variant in variants:
                result[normalized_key(variant)] = (country, region)
    return [
        {"country_key": key, "country": country, "region": region}
        for key, (country, region) in sorted(result.items())
    ]


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    clean = clean_rows()
    raw = messy_rows(clean)

    with (ROOT / "concept_shows.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "show_id",
                "region",
                "country",
                "month",
                "tickets_sold",
                "capacity",
                "ticket_price",
                "fan_rating",
            ]
        )
        writer.writerows(CONCEPT_ROWS)

    write_csv(
        ROOT / "worldstage_shows.csv",
        clean,
        [
            "show_id",
            "show_date",
            "month",
            "region",
            "country",
            "city",
            "event_type",
            "capacity",
            "tickets_sold",
            "ticket_price",
            "marketing_spend",
            "fan_rating",
        ],
    )
    write_csv(
        ROOT / "worldstage_shows_raw.csv",
        raw,
        [
            "show_id",
            "show_date",
            "country_raw",
            "event_type_raw",
            "status_raw",
            "capacity",
            "tickets_sold",
            "ticket_price_raw",
            "marketing_spend",
            "fan_rating",
        ],
    )
    write_csv(
        ROOT / "country_aliases.csv",
        alias_rows(),
        ["country_key", "country", "region"],
    )

    print(f"concept_shows.csv: {len(CONCEPT_ROWS)} rows")
    print(f"worldstage_shows.csv: {len(clean)} rows")
    print(f"worldstage_shows_raw.csv: {len(raw)} rows")
    print(f"country_aliases.csv: {len(alias_rows())} rows")


if __name__ == "__main__":
    main()
