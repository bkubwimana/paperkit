# Paper Constitution

House rules for agent-assisted paper writing. These hold across papers and
venues. The venue profile adds form on top; it never relaxes anything here.

Version: 1.0.0 | Ratified: 2026-10-28 | Owner: bkubwimana

## Core Principles

### I. Evidence before prose (NON-NEGOTIABLE)

Every claim in the paper exists as a row in `paper/claims.md` before it exists
as a sentence. Each row names the evidence that backs it and the status of that
evidence. A claim with no evidence is written down as unsupported, not written
around.

The abstract and introduction are held to this more strictly than the rest of
the paper, not less. They are where unsupported claims survive review.

### II. Status travels with the number

Three statuses, and they are not interchangeable.

- **Measured**: produced by running the real thing on real hardware, with the
  run recorded and the artifact kept.
- **Modelled**: produced by a fitted model, simulator or analytical expression.
  The model's inputs and its validation against measurement are stated.
- **Estimated**: a reasoned guess. Says so, in the text, every time.

A modelled number stays modelled in the abstract. Promotion by omission is the
most common way an honest paper becomes a dishonest one.

### III. Name the shortcut

Anything that makes the result easier than reality gets named in the paper, in
the section where the result appears, not only in an appendix.

This includes simulator conveniences, privileged signals the deployed system
would not have, objects placed to be reachable, runs excluded after the fact,
configurations tuned per workload, and any oracle standing in for a component
that does not exist yet.

If naming the shortcut weakens the claim, the claim was too strong.

### IV. The baseline is the strongest reasonable one

A baseline chosen because it is easy to beat invalidates the paper even when
every number in it is correct. Where a stronger baseline exists and was not
run, the paper says so and says why.

Ablations compare against your own system with one thing removed. They are not
baselines and do not substitute for one.

### V. Every performance number carries its configuration

No throughput, latency or energy number appears without the triple that makes
it reproducible: device, engine, format. Driver and version pins live in the
evidence record, and the paper points at it.

"Fast on a GPU" is not a result. "N milliseconds on this part, this runtime,
this precision" is.

### VI. One term per concept

The vocabulary section below is binding. A term is defined once, on first use,
and never traded for a synonym because a sentence reads better. If the paper
needs a concept with no term, the term is proposed and agreed before it is used.

### VII. Scope is a promise

The paper delivers exactly what the title, abstract and contributions list
promise. Work that is interesting but outside that promise goes in the
follow-on paper and is not hinted at as though it were done.

## Vocabulary

Write for computer systems and architecture readers. Use the vocabulary of that
literature so a reviewer parses every term on first read.

### Banned terms

These were decided, with reasons. Do not reintroduce them.

| Never write | Write instead | Why |
| --- | --- | --- |
| arm, treatment (for an experimental condition) | condition, sharing configuration, design point | Clinical-trial and bandit jargon; means nothing to systems readers |
| cohort (for a set of tasks) | task set | Same |
| service law, device law, service model | performance model | A fitted timing model of a device is a performance model |
| campaign (for the recorded run set) | workload recording | Names what it is: the source of demand traces |
| robot battery (for electronics energy) | electronics energy, or the named subsystem | The boundary is the compute and communication subsystem, not the robot |
| bandwidth, unqualified | memory bandwidth, or network bandwidth | GB/s and Mb/s are different quantities; never leave the reader to guess |

"Arm" for a robot manipulator is the noun for the hardware and is fine.

### Experiment vocabulary

| Term | Meaning |
| --- | --- |
| workload | the demand placed on the system |
| condition | one pairing of settings that is run |
| sharing configuration | how agents exchange context: withheld, share-all, agentic, native-information |
| device setting | latency multiplier, model, placement |
| sweep | a series of conditions varying one setting |
| design point | one point in the configuration space |
| configuration space | the full set of settings considered |

### Timing terms

Each term has a boundary. State it on first use and never cross it.

| Term | Boundary |
| --- | --- |
| inference time | prefill plus decode for one call; excludes queueing, network and dispatch |
| decision latency | capture to command availability; includes queueing and communication |
| capture-to-action latency | decision latency plus dispatch and the control tick |

### Context exchange terms

| Term | Meaning |
| --- | --- |
| context exchange | the overall process of sharing task-relevant context between agents |
| message | one transmitted unit, with content and metadata |
| information | what the content conveys; used for relevance, novelty, value |
| local context | the representation an agent maintains and uses for decisions |
| report | a message describing an observation or an action outcome, and nothing else |

**Receiving is not admitting.** A message received has not entered local
context. Use "admitted into local context" for consumption. The pipeline stages
transmit, receive, admit and use are charged separately and named separately.

## Metrics

Every metric the paper reports is defined in a metrics subsection before its
first number, with five things stated.

- **Unit.**
- **Aggregation.** Median over what, per what.
- **Boundary.** What is inside the measurement and what is excluded.
- **Source.** Measured from which counter or log, or modelled from what.
- **Failure handling.** What happens to failed or timed-out samples.

The system boundary itself is stated once and named exclusions are listed.
Memory traffic is measured from hardware counters where they exist, not
inferred from a model that is then used to validate itself.

## Naming hardware and systems

- In the paper, name the **architecture family**: "Hopper GPU", "Blackwell GPU",
  "Orin-class SoC". Never the marketing part number until the part itself has
  been measured and the part is what the claim is about.
- In READMEs, configs, evidence files and code identifiers, use the **exact
  part**. Precision belongs where it can be checked, generality where it can be
  misread.
- A part whose driver reports no marketing name, or whose board number marks a
  sample revision, is named by family only. Do not infer a product name from a
  PCI identifier.
- Project and system names in public text are the agreed public names. Internal
  or former names do not appear.

## Prose

- Present tense for what the paper does. Past tense for what was run.
- Active voice. The system does things; things are not done to it by nobody.
- No adjectives that cannot be measured. Drop "significant", "dramatic",
  "novel", "efficient" unless a number follows in the same sentence.
- Define every metric before its first number. Units on every quantity.
- Contributions are falsifiable statements, not activities. "We show X" beats
  "We explore X".
- A sentence containing two numbers that are not being compared should be two
  sentences, or a table.

## Figures

- **Medians only.** Do not mix medians and means in one figure or across
  figures that will be read together. State the dispersion measure in the
  caption and use the same one everywhere.
- **No arrows** as decoration in diagrams. If an arrow carries meaning, it is
  in the legend. No arrow styling packages.
- **No font-size overrides** inside a figure that has no grid to align to.
  Consistent type across the figure set.
- Caption states the takeaway, not a description of the axes. The reader should
  get the point from the caption alone.
- Every figure must survive greyscale printing and reduction to column width.
- Axes labelled with units. Log axes marked as log. Truncated axes marked.

## Data and evidence

- Generated data that the paper plots lives in the paper repository under
  `data/`, with a README recording how each file was produced.
- Heavy raw logs stay in the code repository and are referenced from that
  README, never copied into the paper repository.
- Every figure names the data file it was built from.
- A number that appears in the text and in a data file must match. The check is
  mechanical and belongs in `/paper-check`.
- Results produced before a source change are not mixed with results produced
  after it. Pins are recorded; changed pins mean a new result set.

## Governance

This file supersedes an agent's defaults and its sense of what papers usually
look like. An agent may propose amendments; it does not make them unasked.

Amendments record what changed and why, usually a reviewer comment or a mistake
that reached a draft. Version is MAJOR.MINOR.PATCH: MAJOR for a principle
removed or reversed, MINOR for a principle or binding term added, PATCH for
wording.
