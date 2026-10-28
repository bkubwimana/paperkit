# paperkit

Conference grounding for agent-assisted paper writing. Pull it into a paper
repository so an agent works from the target venue's norms and your own house
rules instead of inventing its own.

Built on the same idea as [Spec Kit](https://github.com/github/spec-kit): the
rules are not a document you hope gets read. They are phases that produce
checked artifacts, and later phases refuse to run until the earlier ones exist.

## Why it exists

An agent asked to "write the evaluation section" will produce something that
reads like a paper and is wrong in the ways reviewers punish. It invents
terminology, picks a convenient baseline, states a claim no figure supports,
and mixes measured with modelled numbers. None of that is visible in the prose.

paperkit makes those failures structural rather than stylistic. Every sentence
of prose traces to a claim. Every claim traces to evidence with a stated
status. An agent that cannot find the evidence has to say so instead of writing
around the gap.

## The flow

| Phase | Command | Produces |
| --- | --- | --- |
| 1 | `/paper-venue` | `paper/venue.md`, the target venue's spine and hard constraints |
| 2 | `/paper-claims` | `paper/claims.md`, every claim with its evidence and status |
| 3 | `/paper-outline` | `paper/outline.md`, section spine with budgets and claim assignments |
| 4 | `/paper-figures` | `paper/figures.md`, one row per figure with takeaway and data source |
| 5 | `/paper-review` | `paper/review-<date>.md`, an adversarial reviewer pass |
| 6 | `/paper-check` | `paper/submission-check.md`, the mechanical pre-submission gate |

Phases 2 through 4 are a loop, not a line. A review finding usually sends you
back to claims.

The paper guidelines at `.paperkit/memory/guidelines.md` govern all six. They
hold the rules that do not change between papers: research integrity,
terminology, prose, figures. Edit them per project; do not let an agent edit
them without being asked.

The evaluation principles follow the community's own documents rather than
inventing new ones: the SIGPLAN Empirical Evaluation Guidelines, SIGARCH's
checklist manifesto for empirical evaluation, and Heiser's systems
benchmarking crimes. The review rubric uses their categories.

## Install into a paper repository

```bash
git clone git@github.com:bkubwimana/paperkit.git /tmp/paperkit
/tmp/paperkit/bootstrap.sh /path/to/paper-repo
```

The bootstrap copies `.paperkit/` and the skills into the target repository and
creates `paper/`. Re-running it upgrades the kit in place and never overwrites
`.paperkit/memory/guidelines.md` or anything under `paper/`.

To track upstream instead of copying:

```bash
git submodule add git@github.com:bkubwimana/paperkit.git .paperkit-upstream
```

## Maintaining it

The venue profiles hold community norms, which are durable, and hard numbers,
which are not. Page limits, deadline structure and anonymity rules change year
to year. Anything in a venue profile marked `VERIFY` must be checked against
the current call for papers before you rely on it. The rest is reasoning you
can trust between years.

When a reviewer teaches you something, add it to the guidelines or the venue
profile. That is the whole maintenance loop.
