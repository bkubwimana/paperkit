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

### Writing that sounds like the researcher

PaperKit targets computer architecture and systems papers. When you ask for
prose, the agent reads the shared
[architecture writing guide](.paperkit/memory/architecture-writing.md): start
from the bottleneck, connect the mechanism to the observation, explain the
comparison, and keep its costs and limits visible. The guidance applies to
the first draft as well as revisions.

Use `/paper-edit main.tex` to revise an existing draft, or
`/paper-edit audit main.tex` for findings without manuscript edits. This is an
optional loop before substantive review; the six required phases stay the same.
It audits the scoped text, revises it when requested, and writes a change and
preservation report under `paper/edit-<timestamp>.md`. Clear passages can stay
as written. It preserves technical terms, qualifications, and scientific content.

Supply a writing sample with the request, for example:

```text
/paper-edit main.tex, introduction only; match my voice from prior-paper.tex
```

The agent records sourced observations and your corrections in `paper/voice.md`
using the bundled template. Future writing reads that profile. Without samples,
it uses architecture defaults. Samples never supply facts for the current paper.

Each edited source file gets an original snapshot under `paper/edit-baselines/`.
The mechanical check is also available directly, outside a PaperKit project:

```bash
pk edit-check before.tex after.tex --term "decision latency" --json
```

It compares occurrences of numbers, common quantities, citation/reference keys,
labels, common TeX math forms, input paths, selected qualifiers, and explicit
terms. Exit codes: 0 means these inventories match, 1 means REVIEW for detected
differences, and 2 means an input error. A PASS does not establish scientific
equivalence: the editor must inspect the diff for changed meaning, swapped
comparisons, negation, and scope. It does not expand TeX macros or included files;
run it separately for every edited source. Markdown supports the textual checks;
TeX-specific math and citation extraction is only applied to `.tex` files.

`pk scan` also flags common generic or promotional phrases as editorial
warnings. A warning is a contextual suggestion, never an AI-authorship test or
an automatic submission failure. Technical words and punctuation are not banned
to make prose "human". Verified venue AI-use and disclosure rules still apply.

The paper guidelines at `.paperkit/memory/guidelines.md` govern all six and the
editing loop. They hold the rules that do not change between papers: research integrity,
terminology, prose, figures. Edit them per project; do not let an agent edit
them without being asked.

The evaluation principles follow the community's own documents rather than
inventing new ones: the SIGPLAN Empirical Evaluation Guidelines, SIGARCH's
checklist manifesto for empirical evaluation, and Heiser's systems
benchmarking crimes. The review rubric uses their categories.

### Learn from recent architecture papers

The bundled [annotated reading guide](.paperkit/references/architecture-exemplars.md)
covers five papers from 2023-2026: Splitwise for motivation-to-design reasoning,
DynamoLLM for constrained optimization and tradeoffs, uPIMulator for simulator
validation, TPU v4 for system design explanations, and CounterPoint for careful
inference from measurements. Each entry links the paper, names the version and
sections to read, and suggests a concrete writing technique.

The writing guide and `/paper-edit` route agents to relevant passages when
helpful. Agents record what they consulted and applied. These are selected
writing exemplars, not a current performance ranking or a guarantee of human
authorship. Your claims, evidence, and voice still determine what gets written.

For example:

```text
/paper-edit main.tex, motivation only; use Splitwise as an argument example,
keep my voice and all scientific claims, and report which passages you read.
```

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
`.paperkit/`, the six phase commands and `/paper-edit` for your agent, a `paper/`
directory for the artifacts, and a pointer in `AGENTS.md` (and `CLAUDE.md` for Claude Code)
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
| `pk edit-check BEFORE AFTER [--term TERM] [--json]` | Compare protected content before/after a prose edit; manually review meaning |
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

### Attribution

The optional editorial workflow adapts the audit/rewrite/report, preservation,
and author-voice ideas from
[academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer).
The architecture guidance and fact-preserving examples are tailored to PaperKit.
See [.paperkit/THIRD_PARTY_NOTICES.md](.paperkit/THIRD_PARTY_NOTICES.md) for the
pinned upstream version and MIT notice. PaperKit's own license remains BSD-3-Clause.
