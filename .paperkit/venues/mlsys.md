# MLSys

Conference on Machine Learning and Systems. Systems work whose workload is
machine learning: training, serving, compilation, data pipelines, hardware for
ML, and the interaction between model behaviour and system behaviour.

Anything marked `VERIFY` changes year to year.

## What the venue rewards

**End-to-end improvement on real ML workloads, measured on real hardware.** The
community cares whether the system makes something people actually run faster,
cheaper or possible, and whether the result holds at realistic scale.

Two things MLSys takes seriously that architecture venues treat as secondary:

- **Model quality is part of the result.** A serving speedup that changes the
  output distribution, or a training speedup that changes final accuracy, has
  to report that change. "Same accuracy" is a claim with evidence, not a default.
- **The workload must be current.** Last generation's model or a toy-sized one
  weakens the paper even when the system idea is sound.

## Section spine

1. Introduction, with the headline end-to-end number.
2. Background on the workload. What the model does and why the system
   bottleneck exists for it.
3. Motivation, usually a profile showing where time, memory or energy goes.
4. System design.
5. Implementation. Which framework it is built on, what was changed.
6. Evaluation. End-to-end first, then breakdown, then scaling, then quality.
7. Related work.
8. Conclusion.

## Evaluation norms

- **Real hardware is the default.** Simulation needs a reason.
- **Report the serving or training configuration completely**: model, precision
  and quantization format, batch size, sequence lengths, parallelism, engine
  and version. Small changes to any of these move results by large factors.
- **Latency is a distribution.** Report median and tail, and say which tail.
  A mean latency for a serving system is close to meaningless.
- **Throughput under a latency target** (goodput) is often the honest metric
  for serving. Peak throughput with an unbounded tail is not.
- **Baselines are the production-grade systems people actually deploy**, at
  their current version, tuned. Comparing against an untuned or outdated
  version of a fast-moving engine is the common failure here.
- Scaling results state how many devices and how they are connected.

## How reviewers attack

1. The baseline engine is an old version, or untuned, or misconfigured.
2. Quality impact of an optimization is unreported or measured on a weak proxy.
3. The workload is outdated or too small to show the claimed bottleneck.
4. Latency reported as a mean, or tail behaviour hidden.
5. The speedup comes from a configuration difference, not the contribution.
6. Results do not transfer: one model, one device, one batch size.

## Hard constraints

- Page limit, format, blind policy, artifact expectations: `VERIFY`.
- Reproducibility is weighted heavily. Plan to release code and configs.

## Fit test

- Is the workload a real, current ML workload?
- Is the main result end-to-end on real hardware?
- Is the model quality impact measured and reported?
- If the contribution is mainly about the hardware, would ISCA or ASPLOS be the
  more natural home?
