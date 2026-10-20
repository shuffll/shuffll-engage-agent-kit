# Shuffll research working drafts

**Isaac Gili, Founder of Shuffll**  
Version 0.1 - 20 October 2026

These working drafts investigate reusable video personalization and vector-art compositing. They are published for discussion and development. Neither has been submitted to arXiv or peer reviewed. They contain proposed methods, component observations, and evaluation protocols; they do not report completed comparative performance experiments.

| Working draft | Research question |
|---|---|
| [Many Products, One Video Template](product-permutations.md) · [PDF](shuffll-product-permutations-working-draft.pdf) | How can valid product, artwork, and offer combinations share preparation while preserving correctness? |
| [Deterministic Vector-Art Attachment in Generated Video](vector-art-attachment.md) · [PDF](shuffll-vector-art-attachment-working-draft.pdf) | How can prepared attachment instructions be reused while preserving approved artwork and controlling render cost? |

## Current evidence

The product draft documents 58 passing checks from three existing template-helper suites. The attachment draft also documents four passing editor checks. These observations support selected component behavior. They do not validate a complete public implementation, surface tracking, pixel-identical video, lower cost, or product-scale results.

## Next research milestone

Implement the proposed public evaluation harness, select cleared test assets, freeze baselines and metrics, and collect reproducible comparative measurements. Publish the code revision, raw measurements, failure cases, and environment before making performance claims. The drafts describe proposed capabilities separately from inspected components.

## Scope of this release

This directory releases documents. It does not contain Shuffll production renderer source, customer data, a completed benchmark implementation, or third-party artwork. The repository's package license does not grant rights to those excluded materials or access to Shuffll services. Any eventual scholarly submission requires author review, confirmed contributor credit, and the applicable arXiv submission requirements.

AI assistance was used for literature discovery, synthesis, and drafting. Shuffll has a commercial interest in this work. Related work is cited within each draft; no academic priority or empirical superiority is claimed by this release.

[Shuffll Engage](https://engage.shuffll.com) · [API documentation](https://api-docs.shuffll.com/engage)
