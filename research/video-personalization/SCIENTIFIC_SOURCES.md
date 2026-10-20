# Scientific sources and provenance

Isaac Gili, Shuffll · v0.2 · sources checked 20 October 2026

This registry records what each source supports. It is a targeted related-work review, not an exhaustive novelty search. The linked manuscripts cite the relevant works by number. General statistical and control techniques are attributed rather than claimed as inventions.

| Primary source | Role in the manuscripts | Claim boundary |
|---|---|---|
| [Build Systems à la Carte](https://www.microsoft.com/en-us/research/publication/build-systems-la-carte/) | Dependency scheduling and rebuilding perspective | Does not validate this video compiler |
| [NextAds](https://arxiv.org/abs/2603.02137) | Personalized video-ad generation and integration | No claim that personalization is new |
| [VideoDirectorGPT](https://arxiv.org/abs/2309.15091) | Structured planning for multi-scene video | Planning is established prior work |
| [Zero-shot virtual product placement](https://www.amazon.science/publications/zero-shot-virtual-product-placement-in-videos) | Placement, tracking, occlusion-aware integration | Compositing is not a novel invention here |
| [Porter and Duff](https://keithp.com/~keithp/porterduff/p253-porter.pdf) | Alpha-compositing algebra | Error-budget application is distinct from the algebra itself |
| [Motion vectorization and transformation](https://arxiv.org/abs/2309.14642) | Editable motion-graphics representations | No novelty claim for vector animation |
| [LiveSVG](https://arxiv.org/abs/2605.30174) | Generated video as guidance for SVG animation | No performance comparison has been run |
| [SAM 2](https://arxiv.org/abs/2408.00714) | Candidate segmentation component | Not proof of certified attachment masks |
| [CoTracker3](https://arxiv.org/abs/2410.11831) | Candidate point-tracking component | Not proof of placement correctness |
| [VBench](https://arxiv.org/abs/2311.17982) | Multidimensional video evaluation | Scores do not alone certify accepted-output risk |
| [VBench-2.0](https://arxiv.org/abs/2503.21755) | Intrinsic-faithfulness evaluation | Not a campaign QC calibration result |
| [VideoScore](https://arxiv.org/abs/2406.15252) | Learned human-feedback proxy | A proxy is not the reference label by default |
| [Learn then Test](https://arxiv.org/abs/2110.01052) | Risk calibration and multiple-testing framing | Statistical foundations are prior work |
| [Conformal Risk Control](https://arxiv.org/abs/2208.02814) | Broader risk-control context | Different guarantees should not be conflated |
| [NIST exact binomial limits](https://itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbici.htm) | Exact-binomial confidence-limit construction | Requires matching sampling assumptions |
| [Confidence sequences](https://arxiv.org/abs/1810.08240) | Time-uniform alternative to repeated fixed-sample testing | Not implemented by the finite-sample reference code |
| [Mora](https://arxiv.org/abs/2403.13248) | Multi-agent video generation | "Agentic video" is not itself a new contribution |
| [RouteLLM](https://arxiv.org/abs/2406.18665) | Quality-cost model routing | Does not validate video-repair abilities |
| [ReAct](https://arxiv.org/abs/2210.03629) | Reasoning and tool action | A reasoning trace is not calibrated uncertainty |
| [Nilim and El Ghaoui](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2004/4236.html) | Robust MDP foundation | Rectangular robust control is established |

## Original evidence in this release

The synthetic reference computations and their inputs are available in `experiments/`. They were executed during manuscript preparation. Their output is evidence about the specified constructed environments only.

The 400-variant, four-week campaign description is Isaac Gili's recollection in this authoring conversation on 20 October 2026. Its QC loop reportedly used failure assessment and assessed model abilities. It is not independently audited and supplies no measured acceptance or cost result.

A read-only connected Engage Creator DEV catalog observation returned 12 configured video and 7 image entries on the same date. Local implementation inspection identified routing and voice interfaces. Neither the catalog nor code inspection establishes historical usage or measured ability.

Earlier v0.1 component checks comprised 58 helper checks and four editor checks. They establish selected component behavior only and are not counted as empirical video experiments in v0.2.

## Submission policy

[arXiv moderation policy](https://info.arxiv.org/help/moderation/index.html) describes scholarly-content moderation, overlap concerns, and responsibility for AI-assisted submissions. [Endorsement guidance](https://info.arxiv.org/help/endorsement.html) describes applicable submission eligibility. Moderation is not peer review. A theoretical contribution can be scholarly without a video benchmark, but length and mathematical formatting do not establish originality or acceptance.

## Reuse and disclosure

The text is original synthesis with source attribution. No paper's prose, figure, dataset, or implementation is copied into the research package. AI assistance was used and is disclosed in each manuscript. Author verification of novelty, proofs, sources, and contribution credit remains necessary.
