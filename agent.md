# Working with Codex in this repo

Codex reads `AGENTS.md` automatically. This page is the student's short guide
to using the agent deliberately rather than accepting a polished-looking result.

## For the WorldStage analysis

Start with:

```text
/plan Execute @analysis-prompt.md
```

Before approving the plan, check that it says all of the following:

- the clean table begins at one row per show and ends at one row per region;
- `sell_through` is tickets sold divided by capacity;
- `size`, `count`, and `nunique` are used for different questions;
- the raw data is copied and raw columns are preserved;
- each missing-value decision comes from `notes/data_dictionary.md`;
- the agent will create only the files named in the prompt.

After the run, enter `/diff`. Read the generated code in named steps. For each
step, ask: What rows exist? What does one row mean? Which columns were created?
What values became missing? What did the next operation remove or collapse?

## Useful follow-up requests

These are good requests because they expose reasoning without asking Codex to
write your review:

```text
Show me the row count and grain after each named step, but do not recommend a region.
```

```text
Audit whether the chart uses the same summary and units as the printed table.
```

```text
List every cleaning decision and point to the exact data-dictionary rule that supports it.
```

```text
Give me a three-row invented example showing why size and count can differ.
```

## What not to delegate

Do not ask the agent to write `tour_review.md`, choose your final recommendation,
or turn missing values into convenient numbers. The value of this module is your
ability to explain what the pipeline computed, at what grain, from which rows,
and with which assumptions.

For practice rather than assignment work, say: *“Read tutor.md and tutor me.”*

