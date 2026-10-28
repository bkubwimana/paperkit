# ISCA

International Symposium on Computer Architecture. With MICRO and HPCA, one of
the three core architecture venues; ASPLOS sits alongside them and leans
cross-layer.

Anything marked `VERIFY` changes year to year. Check the current call for
papers before relying on it.

## What the venue rewards

An architectural insight that is **new**, **general**, and **demonstrated
quantitatively**. The bar is not "we built a system that works". It is "we
found something about how machines should be built, and here is the evidence".

Papers that land usually have a shape like this: a measurement shows an
accepted assumption is wrong or a bottleneck is somewhere unexpected; a design
follows from that specific finding; the evaluation isolates the design's effect
from everything else.

Papers that fail usually have a design in search of a motivation, or an
evaluation that cannot separate the contribution from the platform.

## Section spine

1. **Introduction.** Problem, the specific observation that motivates it, what
   you did, what you found, numbered contributions. The key quantitative result
   appears here, with its status.
2. **Background.** Only what the reader needs to follow the design. Not a
   tutorial. If a reader of this venue knows it, cut it.
3. **Motivation or characterization.** A measurement study that establishes the
   problem is real and that existing approaches do not solve it. In strong
   papers this section is where the contribution actually lives.
4. **Design.** The mechanism. What it does, why each piece is necessary,
   what it costs. Include the cases where it does not apply.
5. **Methodology.** Platform, simulator and its validation, benchmarks,
   baselines, what is measured and how. Enough for a competent reader to
   rebuild the experiment.
6. **Evaluation.** Main result, then breakdown by component, then sensitivity
   to the key assumptions, then overheads.
7. **Related work.** Positioned against, not listed. Each entry says what it
   does and why it does not solve this problem.
8. **Conclusion.** Short.

Motivation before design is close to mandatory here. A design section that
arrives before the reader believes the problem is the most common structural
rejection.

## Evaluation norms

- **The simulator must be named and validated.** Common choices are gem5,
  Sniper, Accel-Sim, Ramulator and DRAMSim for memory, CACTI for area and
  energy. Validation against real hardware or against published silicon numbers
  is expected, and its error is reported.
- **Area, power and timing overheads are reported** for any hardware proposal.
  A synthesis result names the technology node and the tool flow. An
  area number without a node is not a number.
- **Sensitivity studies** for every assumption the result leans on. If the
  benefit disappears at a different cache size, bandwidth or batch size, the
  paper says where the crossover is.
- **Benchmarks the community recognizes.** A workload you built yourself is
  acceptable as an addition, rarely as the whole evaluation, and it must be
  released.
- **Speedup, energy and area** are the familiar trio. A paper that improves one
  while quietly costing another is caught in review.
- Artifact evaluation exists and badged artifacts help. `VERIFY` whether it is
  required or optional for the cycle you are targeting.

## How reviewers attack

In rough order of how often these sink a paper.

1. The baseline is weak or ill-specified.
2. The simulator is unvalidated, or validated on something unrelated to the
   claim.
3. Overheads are missing, understated, or measured in a configuration other
   than the one that produced the benefit.
4. The result is real but the explanation of why is asserted, not shown.
5. The idea is a known one with a new name. Related work does not engage with
   the closest prior art.
6. Generality is claimed from a single workload or a single configuration.
7. The motivating measurement does not actually motivate the design that
   follows.

## Hard constraints

- Page limit: `VERIFY` against the current CFP. Historically around eleven
  pages of text with references excluded, but this has moved.
- Double-blind: `VERIFY`. Assume yes and write accordingly; de-anonymizing a
  submission is unrecoverable.
- Format: ACM `sigconf` or the venue's own class, `VERIFY` the required version.
- Submission cycles: `VERIFY`. Several architecture venues have moved to
  multiple rounds with revision decisions.

## Fit test

Before targeting ISCA, answer these. If two or more are no, consider ASPLOS,
MLSys or an embedded venue instead.

- Does the contribution say something about **how machines should be built**,
  rather than how to use an existing one well?
- Is there a **measurement that surprises** someone who knows this area?
- Can the benefit be **isolated** from the platform it was measured on?
- Would the finding still matter if the specific part it was measured on were
  replaced by its successor?
