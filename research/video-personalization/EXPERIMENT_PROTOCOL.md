# Shared video-pipeline experiment protocol

Isaac Gili, Shuffll · WS-RESEARCH-01 · Protocol v0.2 · 20 October 2026

**Status: prospective protocol, not preregistered and not a completed video benchmark.** The accompanying finite numerical studies have been executed; this document specifies the empirical study still required. Freeze a timestamped revision before looking at its comparative results.

## 1. The question

At the same material-defect tolerance and resource budget, does failure-conditioned component repair improve successful delivery relative to bounded same-model retries and a competent fixed repair tree? Within the same study, measure the incremental effect of template reuse and exact vector compositing.

Avoid a single ablation in which generation model, assets, renderer, QC, retry cap, and budget all change. That design cannot attribute the outcome to any one contribution.

## 2. Retrospective evidence already reported

On 20 October 2026 Isaac Gili recalled:

- 400 variants.
- A four-week interval, with its meaning not yet verified.
- A QC feedback loop choosing the next action from the failure and model-ability assessments.
- A pipeline involving video, image, text, segmentation, TTS and STT model families.

This is **reported memory**. It establishes a case-study lead and the author's account of the workflow. It does not establish 400 successes, 400 independent cases, four weeks of compute time, acceptance rate, cost savings, the identities of the historical models, or causal superiority.

Recover request IDs, variant IDs, template families, timestamps, all attempts, provider revisions, failures, intervention choices, exports, review records, and cost receipts. Count cancellations and unknown outcomes explicitly. No remembered aggregate should be silently converted into a precise logged result.

## 3. System inventory

The connected Engage Creator DEV image/video catalog was read on 20 October 2026 and returned 12 video and 7 image entries. Its scope excludes other modalities. The current catalog is not a historical execution record.

Use a registry with these columns:

| Field | Meaning |
|---|---|
| action_id and version | Stable, immutable action definition |
| modality and task | Text, image, video, TTS, STT, object mask, shot segmentation, compositor |
| provider/model revision | Actual resolved endpoint version, not a display label alone |
| capabilities | First/last frame, duration, language, alpha, input limits, supported geometry |
| preconditions | Owned assets, input types, scene constraints, evidence requirements |
| changed_nodes | Artifact dependencies invalidated by the action |
| reservation_bound | Maximum permitted cost, retries, and concurrency |
| assessed_failure_family | Failures for which ability was measured |
| assessment_source | Dataset/split/version and raw outcome references |
| uncertainty | Interval or calibrated statement with assumptions |

A configured choice is not an assessed capability. A capability is not authorization to spend or publish. Do not interpret the synthetic routing intervals as provider measurements.

## 4. Prospective phases

**Phase A: deterministic challenge set.** Create original assets and controlled scenes with known transforms, timestamps, text, and masks. Inject wrong product assignments, stale fonts, timing offsets, mask leakage, missing audio, and altered logos. Measure detection and repair against exact reference data. This isolates deterministic behavior and requires no paid generative calls.

**Phase B: model ability assessment.** For each verified eligible model/action, randomize a balanced set of failure instances across allowed repairs. Measure resolution, collateral defects, cost, and latency. Group by failure family, language, motion regime, and campaign family. Sparse cells remain uncertain. Fit or choose the router only on this tuning partition.

**Phase C: frozen-policy calibration.** Freeze the generator, controller, retry cap, QC rules, judge versions, and candidate policies. Collect independent campaigns/episodes and apply the calibration method matching the sampling design. Preserve all failed and rejected attempts.

**Phase D: independent comparison.** Evaluate on held-out campaign families and a later-time or new-version split. Publish risk, coverage, and cost together, with cluster-aware uncertainty. Preserve the full failure taxonomy and worst-performing strata.

The four papers use distinct endpoints from these phases. The same campaign must not be counted as four independent replications.

## 5. Treatment arms and controlled interventions

| Comparison | Control | Treatment | What stays matched |
|---|---|---|---|
| Compiler reuse | Optimized standard compositor with caching | Complete dependency graph and evidence invalidation | Assets, compositor, output specification, QC |
| Vector attachment | Conventional tracked compositor | Same estimator plus uncertainty contract and selective repair | Tracker, masks, vector assets, quality threshold |
| QC | Fixed score threshold / bounded best-of-H | Frozen episode-level calibrated acceptance | Generator pool, budget, reference labels |
| Repair routing | Same-model retry and fixed expert repair tree | Nominal vs robust failure-conditioned routing | Tools, preconditions, QC, budget, reviewer access |

Include full regeneration as an additional end-to-end comparator only where it can satisfy the same creative request. Regenerating exact typography and retaining a fixed vector layer are different tasks if the acceptance requirements differ.

Randomize execution order within template/failure blocks. Log queue state, time, provider revision, and rate-limit incidents. Shared provider outages and all sibling variants stay in the same analysis cluster.

## 6. Units, endpoints, and labeling

The operational unit is a complete request episode including every attempt until delivery or abstention. The generalization unit is an independent campaign/template family. Frames, retries, and sibling variants are repeated observations, not independent experimental units.

Primary endpoints:

1. Material-defect risk among accepted outputs.
2. Delivery coverage among all eligible requests within budget and deadline.
3. Total cost per accepted output, reported with coverage and total spend.

Secondary endpoints: first-pass acceptance, exact product/offer correctness, OCR and speech correctness, attachment contour error, visibility leakage, temporal inconsistency, collateral defects, human review minutes, latency distribution, retries, and unknown outcomes.

Use blinded reference labels. Two reviewers label a common subset; report agreement and adjudication. VLM, OCR, STT, and signal scores are features, not automatic ground truth. Label "unresolved" separately. A policy's own critic should not be the sole evaluator of its success.

## 7. Analysis plan

Report intention-to-process denominators: every randomized eligible request remains in its assigned arm. Failed provider jobs, aborted attempts, and deadline misses remain in total cost and coverage. Disclose any exclusions with rules fixed before outcomes are viewed.

For paired continuous cost/latency outcomes, estimate within-campaign differences and bootstrap independent campaigns, preserving sibling observations. For certification, use the exact episode method only when its iid assumptions are defensible; otherwise use campaign endpoints or the bounded-cluster construction. A bootstrap interval is not automatically a finite-sample risk certificate.

Specify the number of candidate policies before calibration and correct for policy selection and any claimed subgroup/category guarantees. An overall guarantee does not imply every language or failure family is certified. Keep calibration and test data separate.

No effect size is assumed from the recollection. An initial pilot estimates paired campaign variance, not a claimed benefit. For planning only, a normal approximation suggests independent-pair count proportional to `(1.96 + 0.84)^2 * sd_difference^2 / target_difference^2` for a two-sided 5% test at approximately 80% power. Use a justified design-specific calculation after the pilot; clustered binary outcomes and multiple primary comparisons require different treatment.

## 8. Strong falsification conditions

- Reuse loses its benefit against the optimized template baseline.
- Quality passes only under the system's own judge and fails blinded human review.
- A risk claim vanishes when variants are clustered by shared template.
- Failure-aware routing has no advantage after equalizing tools, budget, or reviewer assistance.
- Robustness improves its chosen utility but harms the operationally required coverage.
- Cost savings disappear after failed jobs, preparation, review, and repairs are included.
- Improvements do not survive a held-out campaign family or model revision.

Publish these outcomes if observed. Do not search for a favorable subset and relabel it the primary analysis.

## 9. Data provenance and release

Every row has an `evidence_type`: `measured`, `reported_memory`, `synthetic_computation`, or `planning_assumption`. Measured rows require a source artifact/job/log reference. Do not join these types into an empirical results table without explicit stratification.

Use `experiments/measurement_template.csv` for future measurements; it deliberately contains headers only. An absent value means unknown, not zero. Retain private identifiers privately and release stable pseudonymous identifiers plus cleared artifacts where permitted.

The public synthetic code, results, and source manuscripts can be reproduced independently. Real-video comparison remains outstanding. arXiv moderation and novelty assessment cannot be guaranteed by length, equations, or formatting.
