# Predicted values for study planning

Isaac Gili, Shuffll · 20 October 2026

**Every value in this file's companion CSV is assumption-based. None is a reconstructed result from the reported 400-variant campaign.** These are sensitivity scenarios, not a fitted predictive model or estimated provider prices.

Run `python experiments/planning_scenarios.py` to regenerate six rows in `experiments/planning_scenarios.csv`.

We use 400 requested outputs to align the planning scale with the founder's recollection. The retry cap of three and every cost/acceptance parameter are invented planning inputs. Each attempt is assumed independent with constant cost and acceptance probability. Those assumptions are particularly doubtful when outputs share a base or a common failure.

| Scenario | Reuse preparation | Reuse attempt cost | Reuse acceptance | Regeneration attempt cost | Regeneration acceptance |
|---|---:|---:|---:|---:|---:|
| Reuse unfavorable | 400 | 0.8 | 0.85 | 1.0 | 0.90 |
| Moderate reuse | 100 | 0.3 | 0.90 | 1.5 | 0.75 |
| Reuse favorable | 40 | 0.1 | 0.95 | 2.0 | 0.60 |

Costs are arbitrary units. The unfavorable case intentionally permits reuse to lose. For attempt acceptance probability q and cap H, expected delivered count is `N * [1-(1-q)^H]`, and expected attempt count per request is `[1-(1-q)^H]/q`. The CSV reports a ratio of expected cost to expected deliveries, which is not generally the expectation of a finite-sample cost-per-delivery ratio.

Acceptance here is a planning event, not proof of actual quality. No defect-rate, QC calibration, or model superiority is predicted. Replace inputs only with documented measurements, preserve these original scenarios, and record every revision. Do not rename the predicted columns as observations.
