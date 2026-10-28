# MICRO and HPCA

The other two core architecture venues. Expectations overlap heavily with ISCA;
read `isca.md` first and treat this file as the delta.

Anything marked `VERIFY` changes year to year.

## MICRO

International Symposium on Microarchitecture.

**Focus.** The inside of the machine. Pipelines, prediction, caches and the
memory hierarchy, accelerator microarchitecture, the mechanisms rather than the
system around them.

**Temperament.** Historically the most willing of the three to take a
speculative or unconventional idea with a clean mechanism, where the evaluation
shows promise rather than deployment readiness. This is a tendency, not a rule,
and it does not lower the evaluation bar.

**Delta from ISCA.**
- Mechanism detail is expected to go deeper. A block diagram without a critical
  path discussion is thin here.
- Simulation at microarchitectural detail is the norm; a high-level model needs
  a stronger justification.
- Novelty of the mechanism matters relatively more, breadth of the evaluation
  relatively less.

## HPCA

International Symposium on High-Performance Computer Architecture.

**Focus.** Architecture that could plausibly be built, with performance as the
organizing concern. Historically friendlier to industry work, to real systems,
and to results measured on shipping hardware.

**Temperament.** Implementability is a virtue, not a limitation. A paper whose
idea is modest but demonstrably practical does better here than at MICRO.

**Delta from ISCA.**
- Real-hardware measurement carries more weight relative to simulation.
- Cost and complexity arguments are first-class. A design that is cheap to add
  to an existing pipeline is making a real claim.
- Industrial relevance can be stated plainly rather than implied.

## Choosing between the three

| If the contribution is | Target |
| --- | --- |
| A general architectural principle with broad evidence | ISCA |
| A specific mechanism with deep microarchitectural detail | MICRO |
| A practical, implementable design justified on cost and performance | HPCA |
| A hardware and software co-design where neither side stands alone | ASPLOS |
| A systems result on real ML workloads and real hardware | MLSys |

These are tendencies. All four accept papers that look like the others.

## Hard constraints

- Page limits, blind policy, format and cycle structure: `VERIFY` for each
  venue separately. They do not match each other and they move.
- Both run artifact evaluation. `VERIFY` current requirements.
