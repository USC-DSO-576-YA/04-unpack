# AGENTS.md — WorldStage repository rules

This is a student-driven DSO-576 repository. Before acting, read `README.md`,
`agent.md`, and any task file the student names. When the student asks for
tutoring, read `tutor.md` and follow it.

## Non-negotiable rules

1. State a short plan before making changes and wait for the student to approve
   it.
2. Touch only files named by the approved task. Show the exact diff afterward.
3. Treat every CSV in the repository root as read-only source data. Never
   hand-edit, “repair,” or regenerate one unless the instructor explicitly asks.
4. Every reported number must be computed from the committed CSVs. Never invent
   a value, carry over a number from the 20-row concept sample, or hide an
   unknown by filling it without a documented rule.
5. Name the grain of each intermediate DataFrame. A successful run is not proof
   that the result answers the business question.
6. Preserve raw fields beside cleaned fields. Unknown aliases remain missing;
   do not guess a country, region, price, rating, or attendance value.
7. `tour_review.md` is the student's graded interpretation. Do not draft, fill,
   rewrite, or complete it. Ask questions that help the student produce their
   own explanation.

## Environment and scope

- Use the locked environment with `uv run python ...`.
- pandas and matplotlib are the only project dependencies.
- Analysis outputs belong in the repository root unless the approved request
  says otherwise.
- Keep credentials, personal information, and unrelated files out of prompts,
  reports, and commits. All supplied concert data is fictional.

## Tutoring boundary

For a direct concept question, explain with a new two-to-five-row example. Do
not reveal the large dataset's final regional ranking or fill the student's
review. Ask for a prediction before running a course specimen or checking an
answer.

