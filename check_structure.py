"""Check the Module 4 starter's data files and two-file architecture."""

from __future__ import annotations

import ast
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent

DATASETS = {
    "09-LAD_batting.csv": {
        "rows": 2758,
        "columns": 31,
        "required": {"Year", "Position", "Name", "At_Bats", "Hits", "Home_Runs"},
    },
    "09-LAD_pitching.csv": {
        "rows": 1253,
        "columns": 37,
        "required": {
            "Year",
            "Position",
            "Name",
            "Games_Played",
            "Strikeouts",
            "Innings_Pitched",
        },
    },
}

FORBIDDEN_IN_APP = (
    "import pandas",
    "from pandas",
    "pd.",
    ".groupby(",
    ".agg(",
    ".fillna(",
    ".dropna(",
    ".map(",
    ".query(",
    ".sort_values(",
    ".str.",
)


def import_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def check_csv(name: str, expected: dict[str, object]) -> list[str]:
    errors: list[str] = []
    path = ROOT / "data" / name
    if not path.exists():
        return [f"missing data/{name}"]

    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        row_count = sum(1 for _ in reader)

    required = expected["required"]
    missing = sorted(required - set(header))
    if row_count != expected["rows"]:
        errors.append(f"data/{name}: expected {expected['rows']} rows, found {row_count}")
    if len(header) != expected["columns"]:
        errors.append(
            f"data/{name}: expected {expected['columns']} columns, found {len(header)}"
        )
    if missing:
        errors.append(f"data/{name}: missing required columns {missing}")
    return errors


def main() -> int:
    errors: list[str] = []

    for name, expected in DATASETS.items():
        errors.extend(check_csv(name, expected))

    analysis_path = ROOT / "analysis.py"
    app_path = ROOT / "app.py"

    if not analysis_path.exists():
        errors.append("missing analysis.py")
    else:
        analysis_imports = import_roots(analysis_path)
        analysis_text = analysis_path.read_text(encoding="utf-8")
        if "pandas" not in analysis_imports:
            errors.append("analysis.py must import pandas")
        if "streamlit" in analysis_imports or "st." in analysis_text:
            errors.append("analysis.py must not contain Streamlit code")

    if not app_path.exists():
        errors.append("missing app.py")
    else:
        app_imports = import_roots(app_path)
        app_text = app_path.read_text(encoding="utf-8")
        app_text_lower = app_text.lower()
        if "streamlit" not in app_imports:
            errors.append("app.py must import Streamlit")
        for token in FORBIDDEN_IN_APP:
            if token.lower() in app_text_lower:
                errors.append(f"app.py contains DataFrame work: {token}")

    if errors:
        print("STRUCTURE CHECK FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: both supplied Dodgers datasets have the expected shape and columns")
    print("PASS: pandas work is isolated in analysis.py")
    print("PASS: Streamlit display work is isolated in app.py")
    print("Starter note: dashboard analysis is intentionally incomplete until Wednesday's demo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
