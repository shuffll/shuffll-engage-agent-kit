# Deterministic Vector-Art Attachment in Generated Video: A Reusable Compositing Framework

**Isaac Gili**  
Founder, Shuffll  
20 October 2026

**Working research draft, version 0.1.** This document defines a proposed attachment method and evaluation protocol. It is not an arXiv submission, a peer-reviewed publication, or a report of completed performance experiments. Surface tracking and cost improvements remain unvalidated.

## Abstract

Generated video and exact brand artwork impose different requirements. A video generator creates the moving scene, while approved logos, labels, illustrations, and text may need to retain their source identity across many variants. We describe a framework that separates scene preparation from artwork rendering and compositing. A proposed attachment record stores timing, transforms, visibility, and optional scene-dependent appearance parameters. Once prepared, the record can be reused with compatible vector assets. We distinguish screen-space graphics, authored motion, planar attachment, and nonrigid attachment because they have different requirements and failure modes. This draft documents relevant existing Lottie and video-compositing components and specifies an evaluation of repeatability, placement stability, artwork fidelity, and amortized cost. It does not claim a new tracking algorithm, automatic attachment to arbitrary generated scenes, or measured savings.

## 1. Motivation and scope

A personalized video may need to display a precise logo, a product label, a reward illustration, or a recipient-specific offer. A practical design question is whether these elements should be part of the generated scene or supplied as independently controlled artwork. Separating the artwork gives the application an explicit source asset and a specified rendering path. Its visual integration must still be evaluated.

The input to this task is a fixed base video, a vector artwork asset, and an attachment specification or preparation procedure. The output is a composited video. The base may originate from a generative model, but this draft treats it as immutable during variant rendering. Regenerating the background is a separate method with separate cost and identity-preservation behavior.

The proposed goal is consistent, reusable attachment with an auditable cost. Deterministic here refers to a specified processing contract under controlled inputs and environment. It does not mean that an automated tracker is always correct, or that fixing a generative seed guarantees identical encoded video on all hardware.

## 2. Related work and unresolved contribution

Zhang and colleagues convert motion graphics video into an SVG motion program and support transformations of the resulting editable representation [1]. Their work is relevant to recovering reusable motion and appearance structure. The present proposal instead starts with independent artwork and an attachment record for a fixed base video; this distinction needs experimental justification.

LiveSVG fits vector geometry to motion from a generated target video [2]. It is relevant to editable vector animation, but fitting new deformations can conflict with a requirement to preserve an approved mark's shape. A brand-art study should therefore declare which geometric transformations are permitted for each asset.

Bhargavi and colleagues investigate virtual product placement, including tracking, occlusion, and appearance integration in constrained footage [3]. This is direct prior work: attaching content to video surfaces is an established task. Our potential contribution must be narrower, such as a reusable attachment representation, a demonstrated preparation/rendering tradeoff, or an evaluation focused on exact brand assets.

## 3. Four attachment regimes

Screen-space attachment places graphics relative to the video frame. A lower-third or a corner logo belongs in this regime. Position, size, opacity, and timing can be authored explicitly without recovering scene geometry. This is the appropriate initial baseline for controlled overlays.

Authored motion allows artwork to follow a designed trajectory or animation. Its coordinates need not correspond to a physical surface. A Lottie animation over base footage can provide this behavior. It must not be described as automatic scene understanding merely because it moves.

Planar surface attachment makes artwork follow a sufficiently flat region such as a sign or package face. A time-varying projective transform can represent perspective, but the preparation process must estimate or author it and handle visibility. Nonrigid or three-dimensional attachment, including deforming fabric and turning objects, generally needs a richer representation and is outside the initial validated scope.

These regimes should be reported separately. Success on a fixed lower-third does not demonstrate success on a rotating bottle or an occluded package. A scene that violates a representation's assumptions should be rejected, corrected, or evaluated as an explicit failure.

## 4. Proposed attachment record

Define an attachment record A = (B, I, H, M, E, R). B identifies the immutable base video; I is the active frame interval; H stores transforms or authored motion; M stores visibility and occlusion masks when required; E stores optional appearance adjustments; and R identifies the rendering configuration. For a screen-space attachment, H may be a fixed transform and M a constant visibility field.

For a planar attachment at frame t, a source point p in artwork coordinates is mapped to an image point using a projective transform H_t, with homogeneous-coordinate normalization. The asset's viewport and mapping convention must be explicit. Masks and transforms must use the same frame timing and coordinate system.

Let G_t be the transformed rasterization of the vector artwork, alpha_t its effective coverage, and B_t the base frame. In a specified linear-light, premultiplied-alpha representation, the composited color is C_t = G_t + (1 - alpha_t) B_t. Occlusion modifies effective coverage before compositing. Implementations must declare color handling and alpha conventions; this equation is a standard compositing rule, not a novelty claim.

The record should distinguish source identity from rendered appearance. Perspective transforms, antialiasing, downsampling, and compression change pixels. Preserving the source SVG's content hash does not prove that small text remains legible or that a distorted logo remains acceptable in the final video.

## 5. Proposed preparation and rendering pipeline

Preparation first classifies the attachment regime and selects a compatible region or authored motion path. An operator, a vision model, or a combination may produce the initial transforms and masks. Their time and resource use belong to preparation cost. Human correction must be logged rather than hidden inside a supposedly automatic stage.

The prepared record is validated for timing, transform degeneracy, clipping, missing masks, and excessive distortion. Accepted records are stored with content hashes and revisions. Replacing the base video invalidates the record unless compatibility is explicitly re-established.

For each artwork variant, validate the SVG viewport, permitted transformations, fonts, and referenced assets. Render using a pinned engine, rasterize at the required resolution, apply the stored transforms and visibility, and composite the result with the base. Rendered media is raster video even when the source artwork remains vector-based.

Proposed safeguards include disabling external resource fetching during rendering and resolving dependencies before the render begins. These are requirements for the proposed public implementation, not claims about every existing renderer. No generative model is required in the per-variant compositing stage once preparation is complete; this is an architectural choice to evaluate.

## 6. Existing components and observed checks

Inspection on 20 October 2026 found Shuffll components for dynamic Lottie values, SVG-backed animation rendering, alpha-capable intermediate media, timed animation segments, and video layer composition. The inspected composition path applies explicit overlay, scale, crop, position, and layer-order operations.

The template helper's three focused suites passed 58 checks. Two existing editor suites passed four additional checks: preservation of an audio stream when applying a visual overlay, propagation of preparation errors, rejection of a zero-duration animation, and rejection of invalid overlay media. The audio check confirms an audio stream and volume-analysis output in its fixture; it is not a test of exact waveform preservation or perceptual audio quality.

These 62 component checks do not establish frame-identical repeat renders, complete SVG fidelity, geometric tracking accuracy, scene occlusion handling, or an economic advantage. The audit did not establish an automatic planar or nonrigid attachment system. No production source is included in this document release.

## 7. Evaluation protocol

Prepare separate test groups for fixed overlays, authored motion, planar motion, and occlusion. Use generated base videos with documented model and generation settings for the target task, and retain all rejected preparation attempts. Synthetic scenes with known transforms can provide geometric ground truth, but results on them must be labeled separately from results on generated footage.

Use approved artwork spanning simple marks, thin strokes, small text, gradients, and intricate illustrations. Define asset-specific constraints, including minimum size and whether perspective distortion is allowed. Split development and evaluation by base scene so that similar artwork variants do not leak the same scene into both groups.

Compare a manually authored attachment, a fixed overlay, a conventional tracked compositor, and the proposed reusable attachment record. Include generative editing as an additional comparison where it supports the same request. A fixed overlay is a fair baseline only for requests it is intended to satisfy; it is not a substitute for a competent tracked-compositing baseline.

Measure screen-space or corner reprojection error, temporal drift, mask accuracy where ground truth exists, and asset legibility after final encoding. Assess perceived attachment quality using blinded reviewers. Measure render latency, preparation time, retries, memory use, and cost separately. Report results by regime and scene, including failures and uncertainty.

Test repeatability at the manifest, decoded-frame, and encoded-file levels. An output file can differ solely because of metadata while decoded frames match. Conversely, a stable manifest may still produce different pixels. State the tested operating system, renderer, fonts, codecs, hardware, and thread settings.

## 8. Amortization and ablations

Let P be attachment preparation cost, c_i the full cost of rendering artwork variant i, and N the number of accepted variants. Average cost is (P + sum_i c_i + failed-attempt cost) / N when N is positive. Any claim of lower cost requires comparison with the same task under a baseline that can also reuse authored motion or tracking.

Evaluate one variant and increasing variant counts to expose the preparation/rendering tradeoff. Remove transform reuse, mask reuse, and artwork raster caches in separate ablations. Change fonts, renderer versions, or the base video to verify that stale cached results are not silently reused. Report the storage and invalidation costs of saved records.

The hypothesized advantage is avoiding repeated preparation and per-variant scene regeneration. Its magnitude is unknown. A short clip with one output may not justify preparation, while a complex attachment may remain expensive regardless of how its artwork is stored.

## 9. Limitations, relationship to the companion paper, and disclosure

This is a method and evaluation draft. The proposed representation, cache contract, and surface-related extensions are not presented as a complete released implementation. Photorealistic lighting, reflections, deformation, and changing topology remain difficult cases outside the observed component evidence.

The companion product-permutation draft studies the valid set of outputs and the sharing of preparation across a catalog. This draft studies an attachment record and the fidelity of individual rendered variants. Shared implementation and data must be disclosed. If experiments do not support independent contributions, a combined paper is the appropriate outcome.

Isaac Gili is Founder of Shuffll. Shuffll has a commercial interest in video personalization. AI assistance was used for literature discovery, synthesis, and drafting. Human author review and verification are required before scholarly submission. This document release does not include customer material, production renderer source, a completed evaluation harness, or permission to use third-party artwork.

## References

[1] Sharon Zhang, Jiaju Ma, Jiajun Wu, Daniel Ritchie, and Maneesh Agrawala. 2023. Editing Motion Graphics Video via Motion Vectorization and Transformation. https://arxiv.org/abs/2309.14642

[2] Matan Levy, Ran Margolin, Bar Cavia, Dvir Samuel, Yael Pritch, Shmuel Peleg, Alex Rav Acha, Ariel Shamir, and Dani Lischinski. 2026. LiveSVG: Zero-Shot SVG Animation via Video Generation. https://arxiv.org/abs/2605.30174

[3] Divya Bhargavi, Karan Sindwani, and Sia Gholami. 2023. Zero-shot virtual product placement in videos. https://www.amazon.science/publications/zero-shot-virtual-product-placement-in-videos
