# Computer architecture writing exemplars

Selected papers from 2023-2026, with bibliographic details and the reading
passages below checked on 2026-11-10. These are examples of useful writing
choices, not a ranking of today's fastest systems or a claim about whether
their authors used AI. The annotations are PaperKit's editorial judgments.

## Choose a paper for the writing problem

| What needs work | Start with | Look for |
| --- | --- | --- |
| Motivation that justifies a mechanism | [Splitwise](#splitwise-isca-2024) | Workload observations carried into design decisions |
| Evaluation of competing objectives | [DynamoLLM](#dynamollm-hpca-2025) | Energy objective, latency constraints, and costs of adaptation |
| Simulator credibility and limitations | [uPIMulator](#upimulator-hpca-2024) | Validation against hardware and explicit model boundaries |
| A system design with several contributions | [TPU v4](#tpu-v4-isca-2023) | Deployment constraints that explain architectural choices |
| Claims from indirect or noisy measurements | [CounterPoint](#counterpoint-asplos-2026) | Observations, assumptions, and alternative explanations |

Choose one or two relevant passages for the current section. Reading the whole
catalog is not a prerequisite for drafting, editing, or submission.

## Splitwise (ISCA 2024)

Pratyush Patel et al., *Splitwise: Efficient Generative LLM Inference Using
Phase Splitting*. [Publication record](https://www.microsoft.com/en-us/research/publication/splitwise-efficient-generative-llm-inference-using-phase-splitting/)
and [DOI](https://doi.org/10.1109/ISCA59077.2024.00019).

**Read:** [arXiv v2, 2024-05-20](https://arxiv.org/html/2311.18677v2),
sections III-C/D/G, the opening of IV, IV-B/C, and V-A/B.
Section references here refer to this version.

**Writing lesson:** The characterization gives the reader a reason for
separating inference phases before the design introduces machine pools and
schedulers. The scheduling explanation points back to the relevant batching
observations. KV-cache transfer gets its own overhead discussion. The
methodology distinguishes the hardware implementation from cluster simulation.

**Apply:** Check whether each proposed mechanism in your design has a motivating
observation and whether its added work is explained. State which conclusions
come from hardware and which come from simulation. These observations concern
the paper's workloads and hardware; they are not universal premises for your
LLM system.

## DynamoLLM (HPCA 2025)

Jovan Stojkovic et al., *DynamoLLM: Designing LLM Inference Clusters for
Performance and Energy Efficiency*.
[Publication record](https://www.microsoft.com/en-us/research/publication/dynamollm-designing-llm-inference-clusters-for-performance-and-energy-efficiency/)
and [DOI](https://doi.org/10.1109/HPCA61900.2025.00102).

**Read:** [Author-hosted proceedings PDF](https://iacoma.cs.uiuc.edu/iacoma-papers/hpca25_2.pdf),
opening of IV and IV-A, then V-A/B. This is the HPCA 2025 version,
checked on the date above; section references do not refer to the earlier preprint.

**Writing lesson:** The design names the energy objective and performance
constraints before explaining the controllers. Evaluation separates energy,
latency, and power, with baselines that isolate different control choices.
It also reports the tradeoff between median and tail latency instead of
reducing the outcome to a single favorable number.

**Apply:** Write the objective, constraint, comparator, and measurement boundary
before the headline gain. Explain a tradeoff when your evidence shows one.
An energy reduction does not by itself establish a latency improvement or a
carbon reduction; those claims need their own evidence and assumptions.

## uPIMulator (HPCA 2024)

Bongjoon Hyun et al., *Pathfinding Future PIM Architectures by Demystifying a
Commercial PIM Technology*. uPIMulator is the simulator introduced in this paper.
[Publication record and DOI](https://doi.org/10.1109/HPCA57654.2024.00029).

**Read:** [arXiv v3, 2024-03-07](https://arxiv.org/html/2308.00846v3),
sections III-C and VI-A/B. Section references here refer to this version.

**Writing lesson:** Validation separates a single DPU from multiple DPUs so the
communication model's effect on accuracy is visible. The authors disclose
benchmark modifications and report absolute error alongside correlation.
The limitations identify missing power/area modeling and the simplified
communication model, rather than offering a generic future-work sentence.

**Apply:** State what your simulator was validated against, where it is less
accurate, and which conclusions those limits affect. A strong correlation is
not a substitute for reporting error. Do not describe a simulated design
exploration as a demonstrated hardware result.

## TPU v4 (ISCA 2023)

Norman P. Jouppi et al., *TPU v4: An Optically Reconfigurable Supercomputer for
Machine Learning with Hardware Support for Embeddings: Industrial Product*.
ISCA 2023 Industry Track. [Publication record and DOI](https://doi.org/10.1145/3579371.3589350).

**Read:** [arXiv v3, 2023-04-20](https://arxiv.org/pdf/2304.01433v3),
sections 1, 2.1-2.3, and 7.3-7.6. Section references here refer to this version.

**Writing lesson:** Deployment constraints explain the interconnect choices.
The discussion anticipates reader questions about comparison fairness,
alternative networks, and power. It distinguishes measured effects from
possible explanations and makes the assumptions behind a datacenter carbon
comparison visible.

**Apply:** Explain why a design choice follows from your constraints, then answer
the strongest comparison question your evidence supports. Keep chip, system,
and datacenter boundaries explicit. This is a retrospective on an earlier
deployment; its historical comparisons do not establish current leadership.

## CounterPoint (ASPLOS 2026)

Nick Lindsay et al., *CounterPoint: Using Hardware Event Counters to Refute and
Refine Microarchitectural Assumptions*.
[Author publication page](https://www.anuragkhandelwal.com/papers/counterpoint/)
and [DOI](https://doi.org/10.1145/3779212.3790145).

**Read:** [Author-hosted proceedings PDF](https://www.anuragkhandelwal.com/papers/counterpoint.pdf),
sections 4 and 5. This is the ASPLOS 2026 proceedings version,
checked on the date above.

**Writing lesson:** The method treats noisy observations separately from the
models being tested. A worked example shows how a violated constraint motivates
a model revision. The text explains that multiple models can remain consistent
with the data, and makes stronger inferences conditional on covering the
relevant feature space.

**Apply:** Separate what you observed, the assumptions used to interpret it,
and the explanations still possible. Preserve conditions when shortening a
conclusion. Consistency with measurements is not by itself proof that one
proposed internal mechanism is the uniquely correct explanation.

## Use the examples without importing their science or voice

1. Identify the writing problem in the requested section and the claim IDs
   supporting its content. Choose an entry for that problem, not just a matching
   topic or a prestigious venue.
2. Open the relevant source passages before making new observations about their
   writing. Record the URL, version or access date, and sections actually read.
   If access fails, say so; use these annotations as guidance without claiming
   to have read the source. This does not block supported writing work.
3. Describe the technique in your own words and apply it only where it helps the
   current argument. Do not copy distinctive wording or make every paragraph
   follow the exemplar's structure. The author's explicit preferences and the
   venue's requirements still govern the prose.
4. External papers are not samples of this author's voice. Keep their lessons
   separate from author observations in `paper/voice.md`. Add a preference there
   only if the author explicitly adopts it, recording that instruction.
5. Examples supply no facts, results, terminology, novelty claims, or automatic
   citations for the manuscript. A paper used as scientific evidence must go
   through the normal claim-and-source verification in `/paper-claims`.
6. In an edit report, record the selected passage, writing technique, and where
   it was applied. For a new draft, include this briefly in the delivery notes.
   Run the normal preservation checks for edits and review meaning manually.

For example, a note might say: "Splitwise v2, IV-C: explain the transfer cost
introduced by the mechanism. Applied to the design paragraph supported by
claim C7; no Splitwise result or phrase imported." Use actual claim IDs and
observations from the current work; this is a format example only.

## Maintaining this collection

Add an entry only after checking the publication record and reading the
passages that support its writing lesson. Record venue/year, a primary-source
link, an accessible full-text link, version or access date, and precise reading
locations. Recheck those locations when changing versions. Prefer a small set
of complementary lessons over a long bibliography.

This file contains original annotations and links. Papers remain at their
publishers' or authors' sites under their own terms; their prose, figures, and
PDFs are not bundled with PaperKit.
