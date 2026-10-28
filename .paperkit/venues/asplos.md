# ASPLOS

Architectural Support for Programming Languages and Operating Systems. The
cross-layer venue: hardware, systems software and languages, and specifically
the places where they meet.

Anything marked `VERIFY` changes year to year.

## What the venue rewards

Work whose contribution is the **interaction between layers**. A hardware
mechanism that needs a runtime change to be usable. A system abstraction that
only pays off given a particular hardware property. A compiler technique
justified by a microarchitectural measurement.

The distinguishing test against ISCA: if you could remove the software side and
still have the paper, it is an ISCA paper. If you could remove the hardware
side, it is an OSDI or a PLDI paper. ASPLOS wants the ones where you cannot.

ASPLOS is more willing than ISCA to accept a **real implementation measured on
real hardware** in place of simulation, and more willing to accept a system
that is engineered rather than invented, provided the cross-layer insight is
genuine.

## Section spine

Close to ISCA, with two differences.

1. Introduction.
2. Background and motivation. The motivating measurement often spans layers:
   something the hardware does that the software cannot see, or the reverse.
3. **Design, split by layer.** State the interface between layers explicitly.
   Reviewers look for whether the split is principled or arbitrary.
4. Implementation. Taken more seriously here than at ISCA. Real line counts,
   real integration points, what had to change in the existing stack.
5. Methodology.
6. Evaluation, including the cost of the software side.
7. Related work, positioned across all the layers you touch, not just one.
8. Conclusion.

## Evaluation norms

- Real hardware is welcome and often preferred. Name the platform exactly.
- If you simulate, the same validation expectations as ISCA apply.
- **The software overhead is part of the result.** A hardware mechanism whose
  runtime support costs more than it saves has not been evaluated until that
  cost is measured.
- Comparison against the unmodified stack is the baseline. Comparison against a
  research prototype is an addition.
- Workloads should be ones the systems community recognizes, not only the
  architecture ones.

## How reviewers attack

1. The cross-layer claim is decorative. The paper is really single-layer with
   the other layer mentioned.
2. The interface between layers is drawn where it was convenient to implement,
   not where it belongs.
3. The software cost is unmeasured or measured separately from the benefit.
4. The implementation is a simulation described as an implementation.
5. Related work covers one community and misses the other.

## Hard constraints

- Page limit: `VERIFY`.
- Submission cycles: ASPLOS has used **multiple rounds per year** with revision
  outcomes. `VERIFY` the current structure and deadlines; it affects planning
  more than at single-deadline venues.
- Double-blind: `VERIFY`.
- Artifact evaluation: widely used here. `VERIFY` requirements.

## Fit test

- Does the contribution **require** both a hardware and a software side?
- Is the interface between them a design decision you defend, rather than an
  implementation detail?
- Is there a real implementation, or a credible path to one?
