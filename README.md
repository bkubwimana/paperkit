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

## Install the CLI

```bash
uv tool install git+https://github.com/bkubwimana/paperkit.git
```

This puts `pk` on your path, with `paperkit` as a long alias. The kit ships
inside the package, so `pk init` needs no network and always installs the
version that matches the CLI. Without uv, `pip install --user
git+https://github.com/bkubwimana/paperkit.git` works too.

## Set up a paper

```bash
pk init --here --venue isca
```

Or create a new directory with `pk init my-paper --venue isca`. This installs
`.paperkit/`, the six phase commands for your agent, a `paper/` directory for
the artifacts, and a pointer in `AGENTS.md` (and `CLAUDE.md` for Claude Code)
so the agent reads the kit's instructions first. An existing `AGENTS.md` keeps
its content and stays loaded.

Agents: `--ai claude` (default) installs commands into `.claude/skills/`;
`--ai codex` into `.agents/skills/`; `--ai claude,codex` both.

## Commands

| Command | What it does |
| --- | --- |
| `pk init [DIR] [--here] [--venue V] [--ai A]` | Set up paperkit in a paper repository |
| `pk status [--json]` | Phases done, claims by status, figure progress, deadline, blockers, next step |
| `pk scan [PATH]` | Flag placeholders and banned terms in the LaTeX source |
| `pk upgrade [--dry-run] [--force]` | Update the kit, keeping anything you edited |
| `pk venue list` / `info V` / `use V` | Browse venue profiles, set the project default |
| `pk agent list` / `add A` / `remove A` | Choose which agents get the phase commands |
| `pk check` | Confirm git, bash, Python, LaTeX, uv and agents are installed |
| `pk version [--json]` | CLI, install commit, Python, project kit version |
| `pk self check` / `self upgrade` | Compare with the latest on GitHub, upgrade with uv |
| `pk uninstall --yes` | Remove the kit; edited files and `paper/` are kept |

### How upgrades stay safe

Every file the kit installs is recorded with its SHA-256 in
`.paperkit/manifest.json`. On `pk upgrade`, a file that still matches its
record is replaced. A file you edited is kept, and the new version is written
beside it as `<file>.paperkit-new` for you to merge; `pk status` lists any that
are waiting. `--force` overwrites instead. Uninstall removes only unmodified
files. Projects set up with the old `bootstrap.sh` upgrade the same way, and a
`constitution.md` from before the rename becomes `guidelines.md` with your
edits intact.

## Maintaining it

The venue profiles hold community norms, which are durable, and hard numbers,
which are not. Page limits, deadline structure and anonymity rules change year
to year. Anything in a venue profile marked `VERIFY` must be checked against
the current call for papers before you rely on it. The rest is reasoning you
can trust between years.

When a reviewer teaches you something, add it to the guidelines or the venue
profile. That is the whole maintenance loop.
