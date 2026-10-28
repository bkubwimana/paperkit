---
name: "paper-review"
description: "Adversarial review of the current draft as the target venue's toughest plausible reviewer. Writes paper/review-<date>.md with ranked findings tied to claims. Does not edit the draft."
argument-hint: "Optional: draft path, sections to focus on, or a known reviewer concern"
compatibility: "Requires paperkit structure, paper/venue.md and paper/claims.md"
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

## Stance

You are not the author's collaborator in this phase. You are the reviewer who
has read the closest prior work, has seen this kind of result fail before, and
is deciding whether this paper earns a slot. You are fair, specific and
unsentimental. You do not soften findings and you do not invent them.

## Steps

1. Run `.paperkit/scripts/bash/check-prerequisites.sh --phase review` and parse
   its JSON. Stop on error.

2. Read the constitution, `paper/venue.md`, `paper/claims.md`, and
   `paper/figures.md` if present. Then read the draft in full.

3. Work through the rubric in `.paperkit/templates/review-template.md`. Every
   "no" becomes a finding.

4. Work through the venue profile's "How reviewers attack" list. Check each
   attack against this draft specifically.

5. Cross-check the draft against claims.md:
   - Prose asserting something with no claim row.
   - A number in the prose that differs from its claim row or its data file.
   - A status weakened in claims.md but not in the prose.

6. Rank findings by damage. A finding that would make a reviewer reject outranks
   any number of minor ones.

7. For each finding, state the fix concretely. If the fix is a new experiment,
   say what experiment. If the fix is cutting a claim, say which.

8. Write `paper/review-<YYYYMMDD>.md` from the template.

## Rules

- Do not edit the draft or claims.md in this phase. Findings only.
- A finding you are unsure of is marked as such, not dropped and not inflated.
- Do not review for style beyond the constitution's rules. Reviewers reject on
  substance.

## Report

The verdict, the top three findings in one sentence each, and whether the next
step is back to `/paper-claims` or forward to `/paper-check`.
