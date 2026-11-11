# Agent instructions

You are working in a repository that has paperkit installed. Read this before
touching any paper text, figure, or number.

## Order of authority

1. What the user says in this conversation.
2. `.paperkit/memory/guidelines.md`, the house rules.
3. `paper/venue.md`, the target venue's norms for this paper.
4. Everything else, including your own instincts about how papers are written.

Where 2 and 3 disagree, the guidelines win on integrity and the venue wins
on form. Say out loud when you hit such a conflict rather than quietly picking.

## Hard rules

- **Do not invent terminology.** The guidelines have a vocabulary section.
  One term per concept. If a concept has no term yet, propose one and ask.
  Do not synonym-swap to make a sentence read better.
- **Do not write prose that is not backed by a claim row.** Every paragraph of
  the paper maps to a claim in `paper/claims.md`. If you want to assert
  something not in that file, add the claim first, with its evidence and
  status, and say you did.
- **Never promote a number's status.** A modelled number is modelled in the
  abstract too. Measured, modelled and estimated are different words and they
  stay attached to the number wherever it appears.
- **Never invent a number.** If a figure or table does not exist yet, write the
  claim and leave the number as `TBD`. Do not produce a plausible value.
- **Name every shortcut.** Simulator conveniences, privileged signals the real
  system would not have, excluded runs, hand-tuned configurations. These go in
  the paper, not just in your reply.
- **Do not write draft prose unless asked.** Structure, claims, outlines,
  figure plans and reviews are the default deliverable. Full paragraphs are a
  separate request.

## Starting work

If the `pk` command is available, run `pk status` first. It reports which
phases are done, the claim counts by status, the blockers and the next phase.
Do not treat its output as a substitute for reading the artifacts it names.

If `paper/venue.md` does not exist, run `/paper-venue` first. Everything
downstream depends on it, and guessing the venue produces a paper shaped for
no one.

If the user asks for something that skips a phase, do the work, then say which
artifact is now stale and offer to refresh it. Do not silently proceed on a
claims file that no longer matches the draft.

## Reporting

When you finish a phase, say what changed in the artifact, what is still `TBD`,
and what the next phase is. Do not summarize the paper back to the user; they
wrote it.

## Writing and editing

When asked to draft or revise prose, read
`.paperkit/memory/architecture-writing.md` and `paper/voice.md` if present.
Apply this guidance to the first draft too. It explains how to develop a
specific architecture argument, preserve the author's voice, and retain
technical precision. Writing samples supply style, not facts for this paper.

Use `/paper-edit` for an existing draft's optional audit/revision loop. An audit
does not edit the manuscript; a rewrite request authorizes the scoped edits.
Preserve an original baseline and check the revision with `pk edit-check`,
then manually inspect meaning, qualifiers and comparisons. The check's PASS
is not proof of scientific equivalence. Claim changes are proposed explicitly.

Record author-supplied style corrections in `paper/voice.md` so later sections
follow them. Keep the venue's current AI-use and disclosure policy in
`paper/venue.md`; an editing pass does not waive it.

## Maintaining the kit itself

Keep shared writing guidance in `.paperkit/memory/`, annotated reading
references in `.paperkit/references/`, phase instructions in `skills/`, and
project-specific choices in `paper/`; avoid duplicating rules. Each exemplar
needs a verified publication record, inspected version and passages, and a
specific writing lesson. Keep external examples distinct from author samples.
An optional editing loop must not become a submission blocker. Editorial
patterns produce warnings, not automatic rewrites or AI-authorship judgments.
When adding a skill or resource, verify install/upgrade delivery to Claude and
Codex and inclusion in the built wheel. Run the CLI tests and meaningful
preservation-check regressions. Retain attribution for adapted instructions.
