# Reproducible finite experiments

Isaac Gili, Shuffll · version 0.2

The experiment runner requires Python 3.10+ and the standard library. It uses no network access, provider accounts, customer media, or production code.

```text
python experiments/run_experiments.py
python experiments/planning_scenarios.py
```

Optional figure regeneration uses `python experiments/plot_results.py` with Matplotlib installed. The figures were built with Matplotlib 3.11.2; this dependency is not needed for the five computational studies.

The first command writes five constructed computational studies and their raw CSVs. The second writes separate assumption-based forecasts. The first must not be described as a real-video benchmark; the second must not be described as observed evidence.

| Study | What is actually executed | Important exclusion |
|---|---|---|
| E1 | Two finite constraint enumerators, symbolic dependency caching, stale-font counterexample | No video rendering or measured cost |
| E2 | Analytic RGB compositing on a spatial grid, bound checks, discontinuous-edge example | No SVG engine, tracker, codec, or perception study |
| E3 | Binomial inversion, exact sampling-distribution enumeration, sample requirements | No video labels or real QC certificate |
| E4 | Finite robust dynamic program, independent policy evaluator, exhaustive sequence oracle | No LLM agent or assessed provider abilities |
| E5 | Failure-conditioned intervention matrix, 64-policy oracle, diagnosis-shift counterexample | No learned diagnosis, real-media repair, or calibrated capability matrix |

`results.json` records all parameters and outcomes. `measurement_template.csv` contains no fabricated rows; fill it only from traceable measurement records. Floating-point results may differ in the last digits across platforms. Check numerical tolerances rather than asserting portable byte equality.

The algorithms are transparent reference calculations, not a production scheduler, renderer, statistical service, or provider SDK. The mathematical methods are credited in the manuscripts.
