# Working with Codex in this repo

Codex reads `AGENTS.md` automatically. In this homework it is a coach and
checker, not the author of your code.

## The productive loop

1. Read one task in `worldstage_homework.py`.
2. Predict the output's type, columns, and grain.
3. Write the small missing piece yourself.
4. Run:

   ```text
   uv run python check_homework.py
   ```

5. If it fails, inspect the first failing task and revise your attempt.

When you want help, start Codex in this folder and enter:

```text
/plan Execute @analysis-prompt.md
```

The agent may run the checker, ask questions, explain vocabulary, or use a tiny
unrelated example. It may not edit `worldstage_homework.py`, provide a line you
can paste into a homework task, reveal the final regional ranking, or write
`tour_review.md`.

## Good requests

```text
My Task 2 result has the wrong grain. Ask me questions that help me locate why.
```

```text
Explain named aggregation with a three-row bookstore example. Do not use the homework columns.
```

```text
Check whether my attempted Task 6 line treats known zero and unknown price differently. Do not rewrite it.
```

```text
Run the checker and explain only the first failure category.
```

## Your responsibility

You must be able to explain every line you submit: what object enters, what
object returns, whether rows were filtered or collapsed, and what missing
values mean. A green checker is evidence that the pipeline works; it is not a
substitute for your explanation.
