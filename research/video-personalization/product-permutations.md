# Many Products, One Video Template: A Framework for Controlled Video Personalization

**Isaac Gili**  
Founder, Shuffll  
20 October 2026

**Working research draft, version 0.1.** This document defines a proposed method and evaluation protocol. It is not an arXiv submission, a peer-reviewed publication, or a report of completed performance experiments. Existing component checks are identified separately from proposed capabilities.

## Abstract

Producing many product-specific videos raises a systems question: which parts of a video must change for each product, and which can be reused without compromising correctness? We describe a template-oriented framework that separates a fixed video asset from replaceable product, artwork, text, and offer slots. A proposed variant manifest records the selected assets, compatibility constraints, timing, and rendering configuration. This enables explicit enumeration of valid combinations and provides a basis for reproducibility and cost accounting. The research hypothesis is that preparation shared across variants can reduce the marginal cost of personalization while preserving approved product and brand assets. We specify comparisons against ordinary template rendering, manual editing, and regeneration of each variant. The current evidence establishes selected template substitution and compositing components; it does not establish a complete permutation engine, visual quality, cost savings, or commercial outcomes.

## 1. Problem and scope

A video campaign can vary several independent-looking dimensions: the featured product, product artwork, message, offer, language, and destination. Multiplying the available options gives an upper bound on the number of outputs. However, business rules, layout limits, and narrative dependencies often make some combinations invalid. A useful system should represent these restrictions before spending resources on rendering.

Here, a template means a timeline with explicit replacement slots and a specified compositing procedure. The base video may be recorded or generated. In the generated-video case, the preparation stage must first produce a reusable base. Its generation cost, rejected attempts, and any manual cleanup remain part of total cost. The method does not assume that arbitrary products can be inserted convincingly into arbitrary footage.

We distinguish product presentation in an authored graphical slot from photorealistic replacement of an object within a scene. The first can be evaluated using approved assets and fixed layouts. The second additionally requires geometry, visibility, and lighting treatment. A result obtained on the first task cannot substantiate a claim about the second.

## 2. Relationship to prior work

NextAds separates personalized creative generation from creative integration and presents task-specific benchmarks [1]. Our proposed study focuses on a different systems boundary: reuse of an approved base and controlled, auditable variation of its slots. Whether this boundary supports a distinct contribution must be established through broader comparison and experiments.

VideoDirectorGPT uses a structured video plan to guide multi-scene generation [2]. It motivates making temporal and scene constraints explicit, but does not by itself demonstrate the product permutation workflow described here. VBench evaluates video generation along multiple quality dimensions [3]; a personalization study also needs assignment correctness, valid-combination coverage, and cost accounting.

Virtual product placement already has substantial prior work. Bhargavi, Sindwani, and Gholami describe automated two-dimensional placement with tracking and occlusion handling in a constrained video setting [4]. Consequently, neither asset substitution nor compositing alone is presented here as a new invention.

## 3. Proposed representation

Represent a template as T = (B, S, K, R), where B identifies the immutable base media, S is the set of typed replacement slots, K is a set of compatibility constraints, and R specifies the rendering environment. Each slot records its role, time interval, geometry or attachment reference, supported asset types, and layout limits.

A variant assignment v selects one permitted value for each applicable slot. If slot i has n_i options, the unconstrained combination count is the product of the n_i values. The valid set is V = {v: every constraint in K accepts v}. This definition covers combinations and ordered slot assignments; it does not imply that all choices are interchangeable mathematical permutations.

For illustration only, ten products, four artwork options, and three offers yield at most 120 assignments. That arithmetic is not an observed rendering result. The actual valid count depends on which artwork and offers may accompany which products.

The proposed manifest includes content hashes for the base and replacement assets, template revision, selected values, constraint revision, frame rate, output dimensions, font identifiers, and renderer configuration. A deterministic serialization of this manifest can identify a render request. A shared request identifier is not proof that independently rendered outputs are identical.

## 4. Proposed execution method

First, prepare and inspect the reusable base and author its slots. Record the preparation time and all unsuccessful preparation attempts. Second, validate the asset catalog and evaluate compatibility rules. Third, enumerate the valid assignments in a stable order and produce one manifest per assignment.

Fourth, apply only the manifest's selected substitutions to a fresh template instance. Do not mutate a shared template across concurrent variants. Fifth, render the selected graphical layers and composite them onto the base using explicit timing and layer order. Sixth, validate the resulting media and record output hashes, timing, resources, failures, and retry history.

Caching is a proposed optimization, not a property established by the component audit. A cache key must include every dependency that can affect the rendered layer, including fonts, layout dimensions, timing, and renderer version. Reuse across products is valid only when those dependencies are unchanged. Distinct product assets must not collide merely because they use the same slot name.

This decomposition offers a testable engineering hypothesis: an expensive preparation step may be shared across many outputs while a smaller rendering step remains per variant. The study must determine whether that sharing actually saves resources relative to a competent existing template renderer.

## 5. Evidence available in this version

An inspection of Shuffll's local components on 20 October 2026 found code for identifying template fields and substituting text, fill colors, numeric controls, image references, and related asset values. Separate rendering components describe SVG-backed Lottie rendering and transparent animation layers; the editor includes layer composition over base video.

Three existing helper suites were executed: token parsing, reference resolution, and dynamic template updates. They passed 15, 9, and 34 checks respectively, for 58 checks in total. These are engineering checks on selected component behavior, not a campaign benchmark or a measurement of rendered product fidelity.

The inspection did not establish a complete constrained permutation engine, reusable generative-video preparation, a production cache for the proposed manifests, or measured performance across product catalogs. Those capabilities are proposals in this draft. No customer results, scale claims, or percentage savings are reported.

## 6. Evaluation protocol

Use a declared collection of templates and product assets with permission to publish the necessary examples. Include multiple aspect ratios, short and long text, varied product silhouettes, and deliberately invalid product-offer combinations. Begin with a small pilot, then freeze the test set and rules before collecting the comparative results. Split development and evaluation by template or scene rather than by near-identical variants.

Compare four workflows: manual editing, an ordinary template compositor, the proposed shared-preparation workflow, and generation of each variant independently where technically applicable. Give the template baseline the same approved assets and comparable caching opportunities. Report any capability mismatch instead of treating a failed unsupported workflow as a zero-quality output.

The primary measurements are valid-assignment coverage, incorrect product or offer rate, rejected invalid assignments, human preparation minutes, end-to-end latency, compute consumption, storage, and total cost per accepted output. Separately assess legibility, visual seams, temporal consistency, and brand-asset fidelity. Use blinded human assessment for perceptual judgments, and disclose annotator instructions, sample sizes, and uncertainty.

Run ablations that remove shared preparation, remove caching, and remove pre-render constraint validation. Include cold and warm cache conditions, repeat renders, long text, missing fonts, and failed asset downloads. Count retries and rejected outputs in the cost and reliability denominators. Report all attempted outputs, not only successful showcase examples.

## 7. Cost model and reproducibility

Let P denote preparation cost, r the average variable cost of a render attempt, a_i the number of attempts for requested output i, and Q the number of accepted outputs. Then amortized cost is (P + sum_i a_i r + storage and delivery cost) / Q, provided Q is positive. Record heterogeneous attempt costs directly when a constant r would be misleading.

The expression explains why reuse might help; it does not prove a saving. A competing workflow may also amortize preparation. Report the preparation cost and marginal cost separately, with an observed crossover point only if the measurements support one.

Reproducibility has several levels: identical assignments, identical normalized manifests, identical decoded frames, and identical encoded files. Browser rendering, fonts, codecs, metadata, and hardware can affect the latter levels. The experiment should test and state exactly which level is achieved under a pinned environment.

## 8. Limitations and publication boundary

This draft provides a proposed representation, method, and evaluation design. It does not yet demonstrate a new algorithm or an empirical advantage. A stronger publication requires a reproducible implementation, substantive comparison with existing workflows, documented failures, and a precise account of the contribution beyond established template rendering.

The companion vector-art draft concerns attachment and rendering of an individual artwork variant. This paper concerns valid variant sets and shared preparation across them. If the eventual implementation and experiments do not establish independent contributions, the papers should be combined rather than presented as two substantially similar submissions.

## 9. Availability and disclosures

This release contains research text and evaluation plans. It does not release Shuffll's production renderer, proprietary application source, customer assets, or a completed benchmark harness. A future reproducibility release should identify the exact code revision, environment, asset permissions, and raw measurements supporting each conclusion.

Isaac Gili is Founder of Shuffll. Shuffll has a commercial interest in personalized video. AI assistance was used for literature discovery, synthesis, and drafting. References and technical claims require author review before scholarly submission; human authors retain responsibility for the final work.

## References

[1] Yiyan Xu, Ruoxuan Xia, Wuqiang Zheng, Fengbin Zhu, Wenjie Wang, and Fuli Feng. 2026. NextAds: Towards Next-generation Personalized Video Advertising. https://arxiv.org/abs/2603.02137

[2] Han Lin, Abhay Zala, Jaemin Cho, and Mohit Bansal. 2023; revised 2024. VideoDirectorGPT: Consistent Multi-scene Video Generation via LLM-Guided Planning. https://arxiv.org/abs/2309.15091

[3] Ziqi Huang et al. 2023. VBench: Comprehensive Benchmark Suite for Video Generative Models. https://arxiv.org/abs/2311.17982

[4] Divya Bhargavi, Karan Sindwani, and Sia Gholami. 2023. Zero-shot virtual product placement in videos. https://www.amazon.science/publications/zero-shot-virtual-product-placement-in-videos
