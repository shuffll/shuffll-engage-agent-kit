"""Assumption-based forecasts for study planning; never historical measurements."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
# All costs are arbitrary planning units, not provider prices.
CASES = [
    ("reuse_unfavorable", 400, 400., .8, .85, 1., .9),
    ("moderate_reuse", 400, 100., .3, .9, 1.5, .75),
    ("reuse_favorable", 400, 40., .1, .95, 2., .6),
]
rows = []
for name, n, prep, cr, qr, cg, qg in CASES:
    for method, setup, cost, probability in [
        ("reuse", prep, cr, qr), ("regenerate", 0, cg, qg)
    ]:
        h = 3
        delivery = 1-(1-probability)**h
        attempts = delivery/probability
        total = setup+n*cost*attempts
        rows.append(dict(evidence_type="planning_assumption", scenario=name,
                         method=method, requested_outputs=n, retry_cap=h,
                         assumed_setup_cost=setup, assumed_attempt_cost=cost,
                         assumed_acceptance_probability=probability,
                         expected_deliveries=n*delivery,
                         expected_total_cost_units=total,
                         ratio_expected_cost_to_expected_deliveries=total/(n*delivery)))
with (ROOT/"planning_scenarios.csv").open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
print("Wrote six assumption-based planning rows; no observed production data.")
