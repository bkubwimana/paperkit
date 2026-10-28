---
name: "paper-venue"
description: "Pick the target venue for a paper, verify its hard constraints against the current call for papers, and write paper/venue.md. Run this first; every other paper phase depends on it."
argument-hint: "Venue and year, e.g. ISCA 2027, plus the paper's one-line contribution"
compatibility: "Requires paperkit structure with .paperkit/ directory"
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

1. Run `.paperkit/scripts/bash/check-prerequisites.sh --phase venue` from the
   repository root and parse its JSON. Stop on error.

2. Read `.paperkit/memory/constitution.md` in full.

3. Identify the venue from the input. Load the matching profile from
   `.paperkit/venues/`. If no profile exists, say so, copy
   `.paperkit/venues/_template.md` to a new profile, and fill it from the
   current call for papers. Ask before committing a new profile.

4. Run the profile's **fit test** against the paper's contribution as the user
   described it. If two or more answers are no, stop and report which venue the
   comparison table points to instead. Do not proceed on a poor fit without the
   user confirming.

5. Find the current call for papers. Fill every row of the hard-constraints
   table from the CFP itself. If you cannot reach the CFP, mark each row
   `UNVERIFIED` with the reason. Never fill a constraint from the profile's
   historical note.

6. Adapt the profile's spine to this paper. Note dropped or added sections.

7. From the profile's reviewer attack list, select the ones that apply to this
   paper and state what currently defends against each, or that nothing does.

8. Write `paper/venue.md` from `.paperkit/templates/venue-template.md`. If it
   already exists, show the diff and ask before overwriting.

## Report

State the venue, the fit result, any `UNVERIFIED` constraints, the reviewer
risks with no defence yet, and that the next phase is `/paper-claims`.
