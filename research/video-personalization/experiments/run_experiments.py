"""Reproducible synthetic experiments. No provider APIs, customer data, or prices.

Python >=3.10, standard library only. Run from any directory:
    python experiments/run_experiments.py
Writes deterministic results and CSVs beside this file. These are computational
experiments on constructed systems, not measurements of Shuffll or video models.
"""
from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHECKS = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    CHECKS.append(name)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def write_csv(name, rows):
    with (ROOT / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def variant_experiment():
    # p=product, a=artwork, o=offer, l=locale, w=layout.
    domains = [range(8), range(3), range(4), range(3), range(2)]

    def valid(v):
        p, a, o, l, w = v
        return ((a == p % 2 or a == 2)
                and (o == 0 or (p + o) % 3 != 0)
                and (l != 2 or o in (0, 2))
                and not (l == 2 and w == 0))

    exhaustive = [v for v in itertools.product(*domains) if valid(v)]
    # Independent nested construction with early constraint pruning.
    pruned = []
    for p in range(8):
        for a in (p % 2, 2):
            for o in range(4):
                if o and (p + o) % 3 == 0:
                    continue
                for l in range(3):
                    if l == 2 and o not in (0, 2):
                        continue
                    for w in range(2):
                        if l == 2 and w == 0:
                            continue
                        pruned.append((p, a, o, l, w))
    check("E1 exact constrained enumeration agrees", set(pruned) == set(exhaustive))
    check("E1 no duplicate assignments", len(pruned) == len(set(pruned)))
    art = {(p, a) for p, a, o, l, w in exhaustive}
    text = {(p, o, l, w) for p, a, o, l, w in exhaustive}
    rows = []
    for name, base_count, art_count, text_count in [
        ("no_reuse", len(exhaustive), len(exhaustive), len(exhaustive)),
        ("base_only", 1, len(exhaustive), len(exhaustive)),
        ("dependency_reuse", 1, len(art), len(text)),
    ]:
        rows.append(dict(policy=name, valid_outputs=len(exhaustive),
                         base_evaluations=base_count, art_evaluations=art_count,
                         text_evaluations=text_count,
                         composite_evaluations=len(exhaustive),
                         assumed_cost_units=round(40*base_count+2*art_count+
                                                  text_count+.3*len(exhaustive), 8)))
    # Reference rendering is a symbolic pure computation, not a video encoder.
    def render(v, font):
        p, a, o, l, w = v
        return ("base-v1", ("art", p, a), ("text", p, o, l, w, font), v)

    cache = {}
    for v in exhaustive:
        for font in ("font-v1", "font-v2"):
            key = digest({"variant": v, "font": font, "renderer": "symbolic-v1"})
            cache.setdefault(key, render(v, font))
            check("E1 complete-key output matches oracle", cache[key] == render(v, font))
    bad_key_collisions = sum(render(v, "font-v1") != render(v, "font-v2")
                             for v in exhaustive)
    check("E1 omitted-font counterexample affects every output",
          bad_key_collisions == len(exhaustive))
    write_csv("variant_results.csv", rows)
    return dict(evidence_type="synthetic_computation", raw_assignments=576,
                valid_assignments=len(exhaustive), unique_art=len(art),
                unique_text=len(text), omitted_font_stale_outputs=bad_key_collisions,
                rows=rows)


def geometry_experiment():
    # Analytic continuous RGB foreground; no tracker/SVG engine is evaluated.
    def foreground(x, y):
        return (.5+.5*math.sin(8*x), .5+.5*math.cos(6*y), .25+.5*x)

    def compose(x, y, eps, matte):
        f = foreground(x+eps, y)
        b = (.15, .25, .35)
        return tuple(matte*f[c]+(1-matte)*b[c] for c in range(3))

    rows = []
    for eps in (0, .002, .01, .04):
        errors, outputs = [], []
        for i in range(65):
            for j in range(65):
                x, y = .1+.8*i/64, .1+.8*j/64
                exact = compose(x, y, 0, .7)
                approximate = compose(x, y, eps, .72)
                errors.extend(abs(a-b) for a, b in zip(exact, approximate))
                outputs.append(approximate)
        bound = 4*eps+.02  # max x derivative of each RGB component <= 4
        check("E2 smooth-field error bound", max(errors) <= bound+1e-12)
        repeated = [compose(.1+.8*i/64, .1+.8*j/64, eps, .72)
                    for i in range(65) for j in range(65)]
        check("E2 same-process numerical repeatability", digest(outputs) == digest(repeated))
        rows.append(dict(displacement=eps, opacity_error=.02,
                         maximum_channel_error=max(errors),
                         mean_channel_error=sum(errors)/len(errors),
                         proven_upper_bound=bound, same_process_hash_equal=True))
    # A step edge is not Lipschitz: arbitrarily small motion gives unit error.
    def step(x):
        return float(x >= .5)
    counterexample = abs(step(.5-.0005)-step(.5-.0005+.001))
    check("E2 discontinuous-edge counterexample", counterexample == 1)
    write_csv("geometry_results.csv", rows)
    return dict(evidence_type="synthetic_computation", points_per_case=65*65,
                rows=rows, discontinuous_edge_error=counterexample,
                evaluated_svg_renderer=False, evaluated_video_tracker=False)


def binomial_cdf(k, n, p):
    if k < 0:
        return 0.0
    if k >= n or p == 0:
        return 1.0
    if p == 1:
        return 0.0
    terms = [math.lgamma(n+1)-math.lgamma(i+1)-math.lgamma(n-i+1)
             + i*math.log(p)+(n-i)*math.log1p(-p) for i in range(k+1)]
    m = max(terms)
    return min(1.0, math.exp(m)*sum(math.exp(t-m) for t in terms))


def cp_upper(k, n, delta):
    if n == 0 or k == n:
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(65):
        mid = (lo+hi)/2
        if binomial_cdf(k, n, mid) > delta:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2


def qc_experiment():
    rows = []
    for m in (1, 10, 100):
        n_min = math.ceil(math.log(.05/m)/math.log(1-.02))
        for n in (50, 100, 200, 500):
            upper = cp_upper(0, n, .05/m)
            check("E3 CP zero-error closed form",
                  abs(upper-(1-(.05/m)**(1/n))) < 1e-10)
            rows.append(dict(candidate_policies=m, accepted_episodes=n,
                             observed_errors=0, upper_error_rate=upper,
                             target=.02, certifies=upper <= .02,
                             zero_error_minimum_n=n_min))
    coverage = []
    # Exact enumeration of the binomial sampling distribution, not Monte Carlo.
    for n in (10, 30, 100):
        bounds = [cp_upper(k, n, .05) for k in range(n+1)]
        for p in (.01, .02, .05, .1, .3, .7):
            probability = sum(math.comb(n, k)*p**k*(1-p)**(n-k)
                              for k in range(n+1) if bounds[k] < p)
            check("E3 exact undercoverage <= delta", probability <= .05+1e-10)
            coverage.append(dict(n=n, true_error_rate=p,
                                 exact_undercoverage_probability=probability))
    check("E3 no-data bound is vacuous", cp_upper(0, 0, .05) == 1)
    check("E3 all-error bound is one", cp_upper(10, 10, .05) == 1)
    write_csv("qc_results.csv", rows)
    write_csv("qc_coverage_results.csv", coverage)
    return dict(evidence_type="synthetic_computation", rows=rows,
                exact_coverage_cases=coverage,
                independent_policy_search_false_pass_example=1-.95**20,
                predicted_video_performance=False)


# Synthetic repair action probability intervals, not named provider abilities.
# Each action generates/repairs a candidate and applies a verifier.
ACTIONS = {
    "cheap_quick": dict(cost=1, g=(.55, .85), s=(.9, .98), f=(.08, .15)),
    "cheap_strict": dict(cost=2, g=(.55, .85), s=(.7, .9), f=(.005, .02)),
    "strong_quick": dict(cost=3, g=(.8, .95), s=(.9, .98), f=(.08, .15)),
    "strong_strict": dict(cost=4, g=(.8, .95), s=(.7, .9), f=(.005, .02)),
}
ALPHA = .03
PENALTY = 10
COST_WEIGHT = .02


def probabilities(g, s, f):
    good, bad = g*s, (1-g)*f
    return good, bad, 1-good-bad


def corners(a):
    return list(itertools.product(a["g"], a["s"], a["f"]))


def risk_bound(a):
    g, s, f = a["g"][0], a["s"][0], a["f"][1]
    good, bad, _ = probabilities(g, s, f)
    return bad/(good+bad)


def make_policy(robust, shield):
    @lru_cache(None)
    def value(budget, horizon):
        if horizon == 0:
            return 0., "stop"
        candidates = [(0., "stop")]
        for name, a in ACTIONS.items():
            if a["cost"] > budget or (shield and risk_bound(a) > ALPHA):
                continue
            future, _ = value(budget-a["cost"], horizon-1)
            parameter_sets = corners(a) if robust else [
                tuple(sum(a[key])/2 for key in ("g", "s", "f"))]
            values = []
            for params in parameter_sets:
                good, bad, retry = probabilities(*params)
                values.append(good-PENALTY*bad-COST_WEIGHT*a["cost"]+retry*future)
            candidates.append((min(values), name))
        return max(candidates, key=lambda item: item[0])

    return lambda b, h: value(b, h)[1], value


def evaluate(policy, budget, horizon, mode):
    if horizon == 0:
        return (0., 0., 0.)
    name = policy(budget, horizon)
    if name == "stop":
        return (0., 0., 0.)
    a = ACTIONS[name]
    check("E4 hard budget invariant", a["cost"] <= budget)
    future = evaluate(policy, budget-a["cost"], horizon-1, mode)
    if mode == "nominal":
        params = tuple(sum(a[key])/2 for key in ("g", "s", "f"))
    else:
        # Rectangular adversary minimizes the stated penalized utility.
        params = min(corners(a), key=lambda p:
                     probabilities(*p)[0]-PENALTY*probabilities(*p)[1]
                     + probabilities(*p)[2]*(future[0]-PENALTY*future[1]-
                                              COST_WEIGHT*future[2]))
    good, bad, retry = probabilities(*params)
    return good+retry*future[0], bad+retry*future[1], a["cost"]+retry*future[2]


def routing_experiment():
    nominal, nominal_value = make_policy(False, False)
    robust, robust_value = make_policy(True, True)
    policies = {
        "fixed_cheap_quick": lambda b, h: "cheap_quick" if b >= 1 else "stop",
        "fixed_strong_strict": lambda b, h: "strong_strict" if b >= 4 else "stop",
        "nominal_dp": nominal,
        "robust_shielded_dp": robust,
    }
    rows = []
    for policy_name, policy in policies.items():
        for mode in ("nominal", "adversarial"):
            good, bad, cost = evaluate(policy, 6, 3, mode)
            rows.append(dict(policy=policy_name, environment=mode,
                             initial_action=policy(6, 3), good_delivery_probability=good,
                             bad_delivery_probability=bad,
                             accepted_defect_fraction=bad/(good+bad) if good+bad else 0,
                             expected_cost_units=cost,
                             utility=good-PENALTY*bad-COST_WEIGHT*cost))
            if policy_name == "robust_shielded_dp":
                check("E4 shielded accepted-defect guarantee", bad/(good+bad) <= ALPHA)
    exact = evaluate(robust, 6, 3, "adversarial")
    check("E4 robust recursion agrees with independent policy evaluation",
          abs(robust_value(6, 3)[0]-
              (exact[0]-PENALTY*exact[1]-COST_WEIGHT*exact[2])) < 1e-12)
    # In this reject-only constructed state space every deterministic policy
    # reduces to a finite action sequence. Enumerate them independently.
    sequences = []
    for length in range(4):
        for seq in itertools.product(ACTIONS, repeat=length):
            if sum(ACTIONS[x]["cost"] for x in seq) <= 6 and all(
                    risk_bound(ACTIONS[x]) <= ALPHA for x in seq):
                v = 0.
                for x in reversed(seq):
                    a = ACTIONS[x]
                    v = min(g-PENALTY*b-COST_WEIGHT*a["cost"]+r*v
                            for g, b, r in map(lambda p: probabilities(*p), corners(a)))
                sequences.append(v)
    check("E4 robust DP matches exhaustive sequence oracle",
          abs(max(sequences)-robust_value(6, 3)[0]) < 1e-12)
    states = []
    for b in range(7):
        for h in range(1, 4):
            a = robust(b, h)
            if a != "stop":
                check("E4 reachable/unreachable state shield",
                      risk_bound(ACTIONS[a]) <= ALPHA and ACTIONS[a]["cost"] <= b)
            states.append(dict(budget=b, attempts_left=h, action=a,
                               robust_value=robust_value(b, h)[0]))
    write_csv("routing_results.csv", rows)
    write_csv("routing_policy.csv", states)
    return dict(evidence_type="synthetic_computation", assumptions=ACTIONS,
                horizon=3, hard_budget=6, accepted_defect_limit=ALPHA,
                defect_penalty=PENALTY, cost_weight=COST_WEIGHT, rows=rows,
                enumerated_feasible_sequences=len(sequences),
                evaluated_actual_model_routing=False)


def failure_conditioning_experiment():
    # Uniform latent failure class, symmetric diagnostic confusion.
    # Success includes avoiding an independently assumed collateral defect.
    actions = {
        "regenerate": {"cost": 4, "resolve": [.85, .65, .45], "collateral": .04},
        "repair_motion": {"cost": 3, "resolve": [.88, .15, .05], "collateral": .03},
        "repair_artwork": {"cost": 1, "resolve": [.05, .97, .02], "collateral": .005},
        "repair_speech": {"cost": 1, "resolve": [.03, .02, .96], "collateral": .01},
    }
    labels = ["motion", "artwork", "speech"]

    def quality(action, observed, accuracy):
        a = actions[action]
        posterior = [accuracy if i == observed else (1-accuracy)/2 for i in range(3)]
        return sum(p*r for p, r in zip(posterior, a["resolve"]))*(1-a["collateral"])

    def local_utility(action, observed, accuracy):
        return quality(action, observed, accuracy)-.06*actions[action]["cost"]

    global_action = max(actions, key=lambda a:
                        sum(local_utility(a, j, .85) for j in range(3))/3)
    nominal = tuple(max(actions, key=lambda a: local_utility(a, j, .85))
                    for j in range(3))
    robust = tuple(max(actions, key=lambda a:
                       min(local_utility(a, j, q) for q in (.6, .9)))
                   for j in range(3))
    def objective(mapping, robust_mode):
        return sum(min(local_utility(a, j, q) for q in
                       ((.6, .9) if robust_mode else (.85,)))
                   for j, a in enumerate(mapping))/3
    for mode, mapping in [(False, nominal), (True, robust)]:
        oracle = max(objective(candidate, mode)
                     for candidate in itertools.product(actions, repeat=3))
        check("E5 diagnosis policy matches exhaustive 64-policy oracle",
              abs(objective(mapping, mode)-oracle) < 1e-12)
    rows = []
    policies = {"global_fixed": (global_action,)*3,
                "nominal_diagnosis": nominal, "robust_diagnosis": robust}
    for name, mapping in policies.items():
        for q in (.4, .6, .85, .95):
            good = sum(quality(a, j, q) for j, a in enumerate(mapping))/3
            cost = sum(actions[a]["cost"] for a in mapping)/3
            rows.append(dict(policy=name, actual_diagnosis_accuracy=q,
                             good_after_one_action=good, mean_cost_units=cost,
                             utility=good-.06*cost))
    write_csv("failure_conditioning_results.csv", rows)
    return dict(evidence_type="synthetic_computation", labels=labels,
                actions=actions, policies=policies, rows=rows,
                diagnostic_nominal=.85, diagnostic_uncertainty=[.6, .9],
                provider_measurements=False)


def main():
    results = dict(schema_version=1, experiment_version="0.2",
                   evidence_type="synthetic_computation",
                   warning="Constructed environments; not production/video-model results.",
                   variants=variant_experiment(), geometry=geometry_experiment(),
                   qc=qc_experiment(), routing=routing_experiment(),
                   failure_conditioning=failure_conditioning_experiment())
    results["verification"] = dict(assertions_passed=len(CHECKS),
                                   unique_checks=sorted(set(CHECKS)))
    (ROOT / "results.json").write_text(json.dumps(results, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
