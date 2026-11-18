# Figure captions for computer architecture papers

Use this guide when planning figures, drafting or editing captions, or reviewing
their clarity. The figure and caption together should let a reader identify
the question, understand the encoding, and interpret the supported result.
Exact measurements must remain available, but a caption need not narrate every
bar or repeat the evaluation paragraph.

This is PaperKit's synthesis of the guidance and examples below, checked on
2026-11-18. It is not a universal venue rule. Follow the target venue's verified
formatting requirements; do not import another journal's caption word limit.

## Write for the figure's job

- Open with a short purpose statement or a supported takeaway. A comparison
  plot can state a scoped trend; a system diagram can identify the mechanism
  and flow; a methodology figure can explain the setup. Do not force a speedup,
  a number, or a causal claim into every opening sentence.
- Explain the reading context that the graphic does not make clear: panel
  mapping, abbreviations, symbols, line styles, and what plotted marks represent.
  Use the agreed terms in `paper/claims.md`, including baseline and metric names.
- Preserve what bounds the comparison: measured versus simulated/modelled,
  baseline, normalization denominator, workload scope, and essential setup.
  Keep units and the direction of improvement clear. The figure/caption must
  carry the configuration required by the guidelines; detailed methods can
  live in the methodology section with an explicit pointer.
- State the aggregation, what error bars or shaded bands mean, and sample/run
  counts when needed to interpret uncertainty. Do not invent missing statistics.
  Say which panels a qualification applies to, especially when panels differ.
- Stop when the reader can interpret the figure. Longer panel explanations
  can be necessary. A short caption that hides a baseline, exception, or
  measurement boundary is worse than a longer precise one.

These choices combine the message-and-reading guidance in [Rougier et al.,
Rules 2 and 4](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003833)
with [IEEE's guidance on clear, self-explanatory figures and concise captions](https://proceedingsoftheieee.ieee.org/resources/guidelines-for-figures-and-tables/).
For uncertainty, [Nature's manuscript checklist, section 3](https://www.nature.com/documents/nature-manuscript-checklist-research.pdf)
also calls for defined error bars and sample counts. Its journal-specific
formatting limits are not PaperKit defaults.

## Decide which numbers belong

For each number, ask what interpretation would become ambiguous without it.

| Role of the number | Caption decision |
| --- | --- |
| Defines a normalization, threshold, sample count, or relevant configuration | Retain when needed to interpret the figure. |
| Quantifies the main supported takeaway | Include when the magnitude matters; retain its baseline, aggregation, scope, and evidence status. |
| Defines uncertainty or an important exception | Retain; concision must not hide variability, failures, or a losing case. |
| Repeats each bar, every workload, or several already-visible gains | Usually keep the exact values in readable labels, a table, or the main text and summarize the pattern in the caption. |
| Adds a second analysis or a speculative explanation | Put the supported analysis in the main text; flag an unsupported explanation. |

There is no quota of zero, one, or two numbers, and no generic sentence limit.
Do not round away meaningful differences, select only the largest gain, remove
a caveat to make room, or claim statistical significance from a visible gap.
If exact values matter, make them accessible in the paper; a reader should not
have to estimate them from bar heights. This placement principle follows
[Rougier et al., Rule 4](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003833).

## What published architecture captions illustrate

These are observations about particular figures, not claims that every caption
in a published paper is ideal. Read the figure with its caption and surrounding
text. Do not copy its wording, values, or findings into the current paper.

| Source and passages inspected | Useful choice |
| --- | --- |
| [Splitwise, ISCA 2024, arXiv v2](https://arxiv.org/html/2311.18677v2), Figure 3 and section III-A; Figure 5 and III-C | Short captions identify the distribution or comparison; nearby prose develops the numerical findings. This shows that a caption need not repeat every result. Check that your own figure still defines its terms and scope. |
| [uPIMulator study, HPCA 2024, arXiv v3](https://arxiv.org/html/2308.00846v3), Figures 5 and 6 | The captions explain utilization denominators and how runtime categories are assigned. Some numerical detail is doing necessary interpretive work rather than listing gains. |
| [CounterPoint, ASPLOS 2026, author proceedings PDF](https://www.anuragkhandelwal.com/papers/counterpoint.pdf), Figure 5 | A longer caption connects the panels, explains uncertainty and the approximation, and defines symbols. Cutting it to a slogan would lose information needed to read the figure. |

## A constructed example

The following values are invented only to demonstrate editing. Assume the
example plot already labels every bar with its exact value and identifies the
shared device, simulator, and workload configuration. Its verified claim is
that the proposed scheduler has lower simulated median execution time on the
three shown workloads. These are not results for a manuscript.

**Before:** Simulated execution time for workloads A, B, and C. The baseline
values are 1.0, 1.0, and 1.0; the proposed scheduler's values are 0.9, 0.8, and
0.7. Bars show medians normalized to the baseline; lower is better.

**After:** The proposed scheduler has lower simulated execution time on the
evaluated workloads. Bars show median execution time normalized to the baseline
(1.0); lower is better.

The revised caption keeps the evidence status and normalization. The exact
values remain in the labelled plot. If they were absent or unreadable there
and not stated elsewhere in the paper, this edit would need another location
for them or would need to retain them in the caption.

## Edit and verify without losing evidence

1. Open the figure, its caption, associated claim rows, and the data or source
   needed to check the caption. Inspect the rendered figure when labels or
   visual interpretation matter. Report unavailable material as unchecked.
2. Identify the purpose, essential context, and any repeated numerical detail.
   Keep a quantitative takeaway only if the claims and figure support it.
3. For an authorized caption edit, remove a repeated value only after verifying
   that the same result, baseline, scope, and precision remain available in
   readable figure labels, a table, or manuscript text. Record where. Relocate
   unique detail only within the authorized edit scope; otherwise propose the
   move. Do not discard a unique result or qualification to shorten a caption.
4. Keep the original baseline and run `pk edit-check` on each edited source.
   Removing repeated values can legitimately produce REVIEW. Keep that actual
   output and document each verified removal or relocation; never relabel it
   PASS, relax the checker, or add dummy numbers to satisfy token counts.
5. Manually verify terminology, number-to-result associations, metric boundaries,
   uncertainty, and the figure/caption pair. A matching token count alone cannot
   establish any of these. The report distinguishes resolved presentation
   changes from unresolved scientific issues.

The examples and editorial recommendations here are original annotations.
Linked papers and publishing guidance remain at their sources under their own
terms; no source figures or captions are reproduced.
