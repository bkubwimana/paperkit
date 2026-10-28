---
name: "paper-figures"
description: "Build paper/figures.md: one row per figure and table with its takeaway, claims, data file and build script, and check each against the guidelines' figure rules."
argument-hint: "Optional: figure IDs to check or a figures directory to scan"
compatibility: "Requires paperkit structure and paper/claims.md"
metadata:
  author: "paperkit"
user-invocable: true
disable-model-invocation: false
---

## User Input

```text
$ARGUMENTS
```

Consider the user input before proceeding.

## Steps

1. Run `.paperkit/scripts/bash/check-prerequisites.sh --phase figures` and
   parse its JSON. Stop on error.

2. Read the guidelines' figure, data and naming sections, plus
   `paper/claims.md` and `paper/outline.md` if present.

3. Inventory existing figures in the paper repository and the figures the
   outline calls for.

4. For each figure, write the takeaway as the caption's first sentence. If you
   cannot state a takeaway, the figure has no claim and is flagged for cutting.

5. Map each figure to the claims it supports and to the data file it is built
   from. Open the data file. Confirm it exists and that the README records how
   it was produced.

6. Run the rule checklist for every figure. For existing figures, check the
   source (plotting script, TikZ, pgfplots) rather than guessing from the
   rendered image where possible.

7. Write or update `paper/figures.md` from the template.

## Rules

- Do not change a figure's data to make it fit a takeaway. Change the takeaway.
- Do not restyle figures unasked. Report rule violations; fix them only when
  the user asks.

## Report

Figures by status, rule violations by figure, figures with no claim, claims
with no figure where one is expected, and that the next phase is
`/paper-review`.
