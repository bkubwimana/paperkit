---
name: "paper-check"
description: "Mechanical pre-submission gate. Checks page count, format, anonymity, claim evidence, number consistency, figure status, banned terms and placeholders. Writes paper/submission-check.md with pass or fail per item."
argument-hint: "Optional: path to the built PDF and build log"
compatibility: "Requires paperkit structure and all earlier paper artifacts"
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

1. Run `.paperkit/scripts/bash/check-prerequisites.sh --phase check` and parse
   its JSON. Stop on error.

2. Build the paper if a build command is known and a fresh PDF is not given.
   Capture the build log.

3. Run `.paperkit/scripts/bash/scan-text.sh` over the paper source. It reports
   placeholders and banned vocabulary with file and line.

4. Work through every item in
   `.paperkit/templates/submission-check-template.md`:
   - Page count: count the way the CFP counts, from `paper/venue.md`.
   - Anonymity: search source and PDF metadata for names, affiliations,
     acknowledgment text and identifying URLs.
   - Claims: every evidence path in claims.md must exist.
   - Numbers: for each number in the prose that has a claim row, compare it to
     the data file. Report every mismatch with both values.
   - Figures: all final, all referenced, all with data files.
   - References and labels: read the build log for undefined references.

5. Write `paper/submission-check.md` from the template. Every item is PASS,
   FAIL or N/A with a reason.

## Rules

- This phase does not fix anything. It reports.
- An item you could not check is FAIL with the reason, not N/A.

## Report

PASS or FAIL overall, and the failing items in one line each.
