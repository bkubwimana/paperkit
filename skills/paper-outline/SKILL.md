---
name: "paper-outline"
description: "Build paper/outline.md: the venue's section spine for this paper, with each section's purpose, the claims it carries, its figures and a page budget that sums within the limit."
argument-hint: "Optional: sections to restructure or a new page limit"
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

## Steps

1. Run `.paperkit/scripts/bash/check-prerequisites.sh --phase outline` and
   parse its JSON. Stop on error.

2. Read the guidelines, `paper/venue.md` and `paper/claims.md`.

3. Start from the spine in `paper/venue.md`. Do not import a spine from another
   venue or from habit.

4. Assign every headline claim to exactly one section where it is established.
   It may be referenced elsewhere. Assign supporting claims to the sections
   that need them.

5. Any section with no claims assigned must justify itself as setup for a later
   claim, or be cut.

6. Budget pages per section. If the sum exceeds the limit, resolve it by
   proposing which claims to cut or move to supplementary material. Do not
   resolve it by assuming tighter formatting.

7. In the introduction notes, map each numbered contribution to an H-id.

8. Write or update `paper/outline.md` from the template.

## Report

The budget margin, any claims not assigned to a section, any section with no
claims, and that the next phase is `/paper-figures`.
