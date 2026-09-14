"""Streamlit presentation layer for the Module 4 Dodgers dashboard.

This file owns only the browser interface and display. Every DataFrame operation
must be implemented in analysis.py and called from here.
"""

import streamlit as st

from analysis import source_inventory


st.set_page_config(page_title="Dodgers dashboard", layout="wide")
st.title("Dodgers dashboard")
st.caption("Module 4 starter")

inventory = source_inventory()
left, middle, right = st.columns(3)
left.metric("Batting rows", f"{inventory['batting_rows']:,}")
middle.metric("Pitching rows", f"{inventory['pitching_rows']:,}")
right.metric(
    "Seasons",
    f"{inventory['first_year']}–{inventory['last_year']}",
)

st.info(
    "The data files loaded successfully. After Wednesday's demonstration, "
    "follow homework.md and use Codex to build the analysis and dashboard."
)

# After the demonstration, add Streamlit controls and display calls here. Do not
# filter, clean, group, aggregate, sort, or calculate DataFrame values in app.py.
