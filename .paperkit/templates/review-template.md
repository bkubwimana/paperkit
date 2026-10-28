# Review: [PAPER_SHORT_TITLE]

Reviewed: [DATE] | Draft: [commit or version] | Venue: [VENUE]

Written as the venue's toughest plausible reviewer. Findings first, verdict
last. No praise section; strengths are listed only where a reviewer would cite
them in the decision.

## Verdict a reviewer would give

[Score on the venue's scale if known, one-line justification.]

## Findings

Ranked, most damaging first. Each finding names where in the draft it bites
and which claim it threatens.

| # | Severity | Finding | Location | Claim threatened | Fix |
| --- | --- | --- | --- | --- | --- |
| 1 | [reject / major / minor] | | [section, figure] | [H-id] | [what would resolve it] |

## Rubric

Answer each. A "no" becomes a finding above.

The evidence, baseline and reproducibility questions follow the categories of
the SIGPLAN Empirical Evaluation Checklist. The benchmarking questions are
Heiser's systems benchmarking crimes. Cite the category in a finding so the
author can look up the community's own wording.

### Contribution

- [ ] Is the contribution new, and does related work engage the closest prior art?
- [ ] Do the title, abstract and contributions promise exactly what is delivered?
- [ ] Is the design conclusion supported, or is it the measurement restated?

### Evidence

- [ ] Does every headline claim map to a figure or table with status M, D or C?
- [ ] Is every modelled number labelled as modelled wherever it appears?
- [ ] Is any number promoted from estimated or modelled by omission?
- [ ] Are models and simulators validated against measurement, with error stated?

### Baselines and fairness

- [ ] Is the baseline the strongest reasonable one, at a current version, tuned?
- [ ] If a stronger baseline exists and was not run, does the paper say why?
- [ ] Are ablations distinguished from baselines?

### Honesty

- [ ] Is every shortcut named where its result appears?
- [ ] Does any result depend on a signal the deployed system would not have?
- [ ] Are excluded runs reported with counts and reasons?

### Generality

- [ ] Does the result hold across the sensitivity range of its key assumptions?
- [ ] Is generality claimed from one workload, one device or one configuration?

### Data analysis and presentation (SIGPLAN)

- [ ] Enough trials per condition, and is the count stated?
- [ ] Is variability shown: a distribution, interval or stated spread, not a bare point?
- [ ] Are ratios plotted and summarized correctly, with absolute values available?
- [ ] Do axes start at zero where the comparison depends on magnitude?
- [ ] Is the precision of reported numbers no finer than the measurement supports?

### Benchmarking crimes (Heiser)

- [ ] Is a subset of a benchmark suite used without saying which and why?
- [ ] Does a micro-benchmark stand in for whole-system performance?
- [ ] Are only relative numbers given, with no absolute baseline values?
- [ ] Is an arithmetic mean taken over normalized ratios, where a geometric mean belongs?
- [ ] Is a throughput change reported without the resource cost (CPU, memory, energy) that produced it?
- [ ] Is a model calibrated and validated on the same data?
- [ ] Is the system compared only against itself, or against an untuned competitor?

### Reproducibility

- [ ] Does every performance number carry device, engine and format?
- [ ] Could a competent reader rebuild the main experiment from the methodology?

### Form

- [ ] Within page limit, in required format, anonymized if required?
- [ ] Terminology matches the guidelines' vocabulary throughout?
