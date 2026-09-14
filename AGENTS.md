# Dodgers dashboard agent instructions

Help the student build, run, inspect, and revise the Module 4 Dodgers dashboard.
The assignment intentionally allows agent-written application code. The student
is responsible for tracing the code, verifying results, identifying limitations,
and writing `reflection.md` in their own words.

## Non-negotiable two-file architecture

Keep the data work and the browser interface in different Python files.
`analysis.py` is the DataFrame file; `app.py` is the file that creates the
Streamlit browser page (the generated HTML interface). They must remain two
different `.py` files.

### `analysis.py` owns every DataFrame operation

All pandas work belongs in `analysis.py`, including:

- reading the two CSV files;
- `.copy()`, filtering, `.loc`, and `.query()`;
- `.str` operations, `.map()`, `.isna()`, `.notna()`, `.fillna()`, and
  `pd.to_numeric()`;
- `groupby`, named `.agg()`, `size`, `count`, `nunique`, `sum`, `mean`, `min`,
  `max`, and `median`;
- derived columns, rates, sorting, and validation checks;
- preparation of complete tables that are ready for display or plotting.

`analysis.py` must not import Streamlit, call `st.*`, create page layout, or
contain browser/HTML presentation code.

### `app.py` owns the Streamlit page

All dashboard and browser/HTML presentation work belongs in `app.py`, including:

- `st.set_page_config`, titles, captions, and explanatory text;
- selectors, checkboxes, tabs, columns, metrics, tables, charts, and warnings;
- calling functions imported from `analysis.py`;
- displaying the already-prepared values and tables returned by those functions.

`app.py` must not import pandas and must not contain DataFrame cleaning,
filtering, `groupby`, aggregation, mapping, missing-value handling, derived
business calculations, or sorting. If the interface needs a new value or table,
add a function to `analysis.py` and call it from `app.py`.

Never collapse the two layers into one file. Never duplicate the same
transformation in both files. When reviewing a change, explicitly state which
layer it belongs to and why.

## Data and analysis rules

- Treat `data/09-LAD_batting.csv` and `data/09-LAD_pitching.csv` as read-only.
- Preserve raw columns. Create a `.copy()` before adding or changing columns.
- State the input and output grain before implementing a grouped table.
- Use the documented role mappings. Do not infer a missing baseball position.
- Keep missing positions visible as `Unclassified` only in a separate reporting
  column when the task requires all rows to remain represented.
- Check that grouped row counts reconcile to the intended filtered population.
- Do not average player batting averages to calculate a combined batting
  average. Use total hits divided by total at-bats.
- Do not sum `Innings_Pitched` as ordinary decimals. Values such as `131.2`
  follow baseball notation and mean 131 innings plus two outs.
- Prefer familiar pandas and simple native Streamlit charts. Add a new package
  only if the student explicitly asks and the course environment lacks the
  needed capability.

## How to work with the student

Before editing, give a short plan that names the files you will change and the
grain of each requested summary. Make small, readable changes. Run the relevant
functions, run `check_structure.py`, and start the Streamlit app long enough to
confirm it loads without an exception.

Explain unfamiliar syntax with a small example when asked. Help the student
trace their actual code and compare displayed results with source rows. Point
out unsupported claims, unclear denominators, silent row loss, and misleading
plots.

Do not write or edit `reflection.md` for the student. You may ask questions,
identify missing evidence, and comment on the student's draft, but the final
reflection and interpretation must remain the student's own work.
