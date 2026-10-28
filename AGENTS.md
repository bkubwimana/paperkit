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
