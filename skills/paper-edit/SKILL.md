---
name: paper-edit
description: Audit or edit an existing computer architecture or systems paper for clear argument, natural author voice, and precise technical prose while preserving its claims and evidence. Use for rewriting, polishing, or humanizing a draft section.
metadata:
  author: paperkit
---

## Scope

Use the user's requested draft and sections. An audit request produces findings
only; an edit/rewrite request (or `/paper-edit` with a draft path) authorizes
prose edits in that scope. Keep the existing section and paragraph structure
unless restructuring was requested. This is an optional writing loop, not a
prerequisite for the six paper phases. It does not optimize detector scores or
replace the venue's disclosure requirements.

## Ground the edit

1. Run `.paperkit/scripts/bash/check-prerequisites.sh --phase edit` and parse
   its JSON. Read the guidelines, `paper/venue.md`, `paper/claims.md`, and
   `.paperkit/memory/architecture-writing.md`. Read the draft and the context
   needed to interpret the requested section.
2. Read `paper/voice.md` if present. When the author provides samples or voice
   corrections, create or update this profile from
   `.paperkit/templates/voice-template.md`, preserving explicit preferences
   and attributing observations. No samples means architecture defaults;
   it is not a reason to stop. Samples are stylistic references, not evidence.
3. Map assertions to claim rows and open the evidence needed to check a proposed
   change. If a required artifact is missing, report it. If the section contains
   an unsupported assertion, flag that assertion; other supported prose can
   still be edited. Never fill a gap with a plausible result.
   Read the claims file's Terminology section and follow the guidelines'
   terminology checks, including their fallback for older claims files.
4. When a writing problem would benefit from an example, consult
   `.paperkit/references/architecture-exemplars.md`. Select one or two relevant
   passages and follow its reading and reporting steps. Keep external examples
   separate from the author's voice samples. Their writing techniques may guide
   the edit; their scientific claims do not supply evidence for this paper.
5. For captions, read `.paperkit/memory/figure-captions.md` and inspect the
   associated figures and evidence. Audit purpose, essential context, and
   repeated numerical detail; do not force a number into every caption.

## Audit, revise, verify

- Audit for reasoning and flow first: a buried bottleneck, unclear referents,
  a mechanism unexplained, or a comparison detached from its configuration.
  Then examine generic openings, promotional phrasing, repetitive transitions,
  noun-heavy sentences, and needless repetition. Use the guide's section roles
  and examples. Leave clear passages alone.
- For audit mode, write the findings and stop without editing the manuscript.
  For edit mode, save each original file under
  `paper/edit-baselines/<unique-run-id>/<relative-source-path>` before editing.
  Keep these snapshots outside the manuscript build; never overwrite a prior
  run's baseline. Do not use the revised file as its own baseline.
- Revise with the author's rhythm and the paper's agreed terms. Keep meaningful
  hedges, passive voice, and long sentences when they improve precision. Do not
  add personality, synonym-swap hardware terms, impose punctuation bans, or
  introduce technical claims to make a paragraph sound more specific.
- Preserve numbers, units, symbols, equations, citations, labels, evidence
  status, comparator identity, aggregation, scope, and substantive coverage.
  Report proposed changes to scientific meaning or claim strength separately;
  do not silently edit claims.md to justify them.
  For caption edits, use the caption guide's verification and reporting rules
  for removing repeated values or relocating detail within the authorized
  scope. Preserve the information and keep the checker's actual REVIEW result.
- Run `pk edit-check BASELINE.tex EDITED.tex` for **each** edited source file.
  If `pk` is unavailable, run `python -m paperkit edit-check` from the CLI's
  environment. Use repeated `--term "..."` for the section's agreed technical
  terms and relevant recorded short forms. Keep the actual output and source
  hashes in the report. Resolve every REVIEW result or report it as unresolved;
  do not label a skipped check PASS.
- Manually inspect the diff even after PASS. Check which number belongs to which
  result, units and boundaries, negation, qualifier placement, conditions, and
  observation versus causal interpretation. The checker compares a limited
  inventory; it cannot establish scientific equivalence or expand TeX macros.
- Check technical names and meanings against the terminology record in the
  requested scope, including any captions or labels inspected. Report the
  location, conflicting usage, agreed term, and meaning affected. Matching
  `--term` counts cannot detect all aliases or a term used for two concepts.

## Deliver

Write `paper/edit-<YYYYMMDD-HHMMSS>.md` using
`.paperkit/templates/edit-report-template.md`, choosing another suffix if that
path already exists. Include the scoped changes, claim-related open issues,
voice choices, and real mechanical and manual verification results. In audit
mode the preservation table is N/A because no manuscript was edited.

If text changed after an earlier review or submission check, name those reports
as stale and refresh them when requested; their verdict does not validate the
new draft. Report the edited files and unresolved issues concisely. Recommend
`/paper-claims` for scientific changes and `/paper-review` for a supported
revision ready for substantive review.
