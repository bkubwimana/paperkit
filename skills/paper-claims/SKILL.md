---
name: "paper-claims"
description: "Build or update paper/claims.md: every assertion the paper makes, with its evidence, status (measured, modelled, estimated, unsupported, cited) and named shortcuts. Prose is written from this file."
argument-hint: "Optional: draft file, section, or new results to fold in"
compatibility: "Requires paperkit structure and paper/venue.md"
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

1. Run `.paperkit/scripts/bash/check-prerequisites.sh --phase claims` and parse
   its JSON. Stop on error.

2. Read the guidelines and `paper/venue.md`.

3. Gather sources in this order: the user's input, any existing draft, the
   paper repository's `data/` directory and its README, any existing
   `paper/claims.md`.

4. Extract every assertion. Split compound sentences into one claim each. A
   claim is one falsifiable sentence.

5. For each claim, find its evidence **by opening it**. A path that does not
   exist is not evidence. A data file whose numbers do not match the claim is
   not evidence for that claim. Record the mismatch.

6. Assign status strictly by the guidelines' definitions. When in doubt
   between two statuses, pick the weaker one and say why.

7. For every claim involving time, throughput, energy or memory, fill the
   configuration table: device, engine and version, format. If any is unknown,
   the claim is not reproducible yet; record it as an open question.

8. Record shortcuts for every claim. "None" is an answer you must be able to
   defend.

9. Write or update `paper/claims.md` from the template. Keep the cut and
   deferred table; never silently drop a row.

## Rules

- Never invent a number. Missing numbers are `TBD`.
- Never upgrade a status because the claim reads better stronger.
- Headline claims with status E or U are listed in the report as blockers.

## Report

Counts by status, the headline claims that are blockers, any evidence that did
not match its claim, and that the next phase is `/paper-outline`.
