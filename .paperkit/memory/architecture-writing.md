# Writing for computer architecture readers

Use this guide when asked to draft or edit prose. The guidelines and verified
venue constraints still govern the work. The goal is writing that sounds like
the researcher explaining a particular machine, experiment, and design choice.

## Learn the author's voice

Read `paper/voice.md` when present. If the author supplies writing samples,
record useful observations using `.paperkit/templates/voice-template.md`:
how they open sections, connect sentences, explain mechanisms, use "we", and
qualify results. Attribute each observation to a sample and section. Distinguish
observations from preferences the author explicitly chose. Existing preferences
win over an inferred habit. Update the profile when the author corrects an edit
so the next section benefits too.

Samples supply style, never results, citations, terminology, or novelty claims
for this paper. Do not copy distinctive sentences. With no samples, say that
you are using the architecture defaults below; do not pretend to know the
author's voice or make samples a prerequisite.

## Learn from published architecture papers

When a concrete writing problem would benefit from a published example, consult
the [annotated reading guide](../references/architecture-exemplars.md). Choose
one or two relevant passages and follow its source-reading and reporting steps.
Use the observed writing technique with this paper's own claims and evidence.
External exemplars do not establish the author's voice; only an explicit author
choice turns an external style lesson into a preference in `paper/voice.md`.

## Build an argument, not a list of polished sentences

- Start where this paper becomes specific: the resource constraint, failed
  assumption, workload behavior, or unresolved tradeoff. A broad field-history
  opener is useful only when it supplies context this audience needs.
- Connect observation to design choice to consequence. Distinguish the
  mechanism's intended effect from evidence that it caused the observed result.
  An ablation can support an explanation; a faster runtime alone cannot.
- Give each paragraph a job. Carry a known subject into the next sentence,
  then introduce the new fact. Name the referent of "this" when it could mean
  the policy, workload, result, or whole system.
- Let reasoning supply transitions: explain why a limitation motivates the
  next design choice. Repeated "Moreover" and "Furthermore" cannot supply that
  missing connection. If the connection is unsupported, flag the gap.
- Keep useful detail and necessary qualifications. Compression that removes
  a simulator assumption or an exception makes the prose less accurate.

Vary sentence length with the reasoning. A short sentence can state the
consequence; a longer one can express a necessary condition or comparison.
Split a sentence when its clauses do different jobs. Do not force a word limit,
identical paragraph lengths, a three-item list, or the same rhetorical template
onto every paragraph. Preserve paragraph and section boundaries in a local
edit unless restructuring was requested.

## Make the machine and the comparison concrete

- Name the component and its action: the scheduler delays an issue, the
  directory tracks sharers, the controller prioritizes a request. Replace
  abstract noun chains with an actor and a verb when it clarifies the mechanism.
- Preserve distinctions such as throughput versus latency, memory versus
  network bandwidth, capacity versus traffic, energy versus power, and a
  speedup versus a percentage latency reduction. Never substitute one to vary
  the wording. Preserve the defined aggregation and measurement boundary.
- Explain a design choice's cost or applicability when the claims support it:
  metadata, critical path, area, contention, sensitivity, or a losing workload.
  Do not invent a tradeoff to complete a pleasing narrative.
- Keep configurations, comparator names, workload subsets, qualifiers, and
  evidence pointers beside the result they bound. Do not turn "up to" into
  an average, a median into a mean, a simulated result into a hardware result,
  or a workload-specific gain into general superiority.
- Use the paper's agreed technical names consistently. Synonym variety is
  harmful when "request", "transaction", and "access" refer to different things.

## Match the section's purpose

| Section | Writing task |
| --- | --- |
| Abstract | State the problem, specific insight, mechanism, and supported result within its scope. Keep the result's evidence status and comparator. |
| Introduction | Establish the bottleneck and why existing choices leave it unresolved; connect the insight to the design and claim-backed contributions. |
| Background | Supply only the concepts needed to understand the new argument; explain unfamiliar terms before using them. |
| Motivation | Show the observation that makes the design necessary. Separate observations from hypotheses about their cause. |
| Design | Explain what happens, why each choice follows, and its supported costs and limits. Preserve ordering and correctness conditions. |
| Methodology | State what was run and how. Reproducibility details are content, even when they interrupt a smooth sentence. |
| Evaluation | Establish the scoped result, explain what supports its interpretation, and discuss sensitivity and counterexamples. |
| Related work | Explain the closest relevant distinction and cite it. Preserve every citation; propose citation changes separately. |
| Caption | State the supported takeaway with the necessary configuration, units, aggregation, and uncertainty. |

The target venue determines the actual section spine. This table does not add
missing sections or make an unverified assertion about a venue's requirements.

## Remove generic prose without flattening scholarship

Prefer a direct statement to "it is worth noting that". Replace "extensive
experiments" with the actual scope only when that scope is already supplied by
the claims and evidence. Explain what is new rather than repeatedly declaring
it "novel". Cut praise such as "groundbreaking" when it adds no scientific
content. Do not treat individual words as evidence of AI authorship.

Keep legitimate passive voice when the actor is irrelevant, first-person "we"
when it fits the author, and technical words such as "pipeline", "out-of-order",
and "speculation" in their domain meaning. Punctuation, including an em dash,
is a choice rather than an authorship test. Keep a long sentence when its
structure makes a precise relationship easier to follow.

Keep "suggests", "may", and "is consistent with" when uncertainty is real.
"Proves" is appropriate for a supplied proof, not an empirical speedup.
"Demonstrates" is not intrinsically wrong. A numerical difference alone does
not establish statistical significance. Flag a missing test or overclaim;
never manufacture a p-value, confidence interval, experiment, or figure number.

## Edit within an evidence boundary

An editorial pass preserves numbers, units, equations, symbols, citations,
labels, terminology, evidence status, and substantive coverage. Do not add a
specific result to make a vague sentence convincing. Record the missing support
against its claim ID. A change to scientific meaning, scope, or claim strength
belongs in the report as a proposed claim change, not a silent style fix.

Use `/paper-edit` for an existing draft's audit and revision. Use
`pk edit-check BEFORE.tex AFTER.tex` for each edited source file, then manually
review the diff: matching tokens cannot prove that a number still belongs to
the same baseline or that a negation survived. When drafting from claims,
read this guide first and apply the same reasoning and voice choices.

## Examples: identical facts, clearer architecture prose

These are constructed examples, not results to copy into a manuscript. Every
factual detail in an "after" is present in its "before".

**Before:** In recent years, cache management has attracted increasing
attention. Our policy uses reuse distance to select victims in the LLC.

**After:** Our LLC policy uses reuse distance to select victims.

**Before:** It is worth noting that our modelled median decision latency is
8 ms on the Orin-class SoC with TensorRT FP16, compared with 10 ms for the FIFO
baseline under the same configuration (Figure~\ref{fig:latency}). This excludes
dispatch and the control tick.

**After:** With TensorRT FP16 on the Orin-class SoC, our modelled median decision
latency is 8 ms, compared with 10 ms for the FIFO baseline under the same
configuration (Figure~\ref{fig:latency}). This excludes dispatch and the control
tick.

**Before:** Furthermore, the controller delays prefetches when the request
queue is full. Moreover, demand requests retain priority.

**After:** The controller delays prefetches when the request queue is full.
Demand requests retain priority.

**Before:** The usefulness of increasing issue width is limited by front-end
supply in this workload. The front end delivers 3 instructions per cycle, and
the core can issue 6. Our design adds a decoded-instruction buffer to reduce
repeated decode work. Whether decode is the cause of the supply limit remains
untested.

**After:** In this workload, the front end delivers 3 instructions per cycle
to a core that can issue 6. This supply limit bounds the benefit of increasing
issue width. Our design adds a decoded-instruction buffer to reduce repeated
decode work. We have not yet tested whether decode causes the supply limit.

**Leave unchanged:** These simulated results suggest that queue contention
limits throughput for this workload; they do not establish the cause.

**Flag instead of filling in:** "Our policy significantly outperforms prior
work." Identify the claim and ask for its comparator, metric, scope, and
statistical support. Do not replace it with an invented quantified result.

## Provenance

Adapted from the audit/rewrite/report, scholarly-preservation, and author-voice
ideas in AIScientists-Dev/academic-humanizer, version 0.3.3, commit
`94b88b23703bed7df507acae7d6d5876209a0cdf`. The examples and architecture-specific
guidance here are new. Attribution and the upstream MIT notice are in
`.paperkit/THIRD_PARTY_NOTICES.md`.
