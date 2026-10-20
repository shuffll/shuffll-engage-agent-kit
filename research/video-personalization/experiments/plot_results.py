"""Optional figure reproduction. Requires matplotlib; studies use stdlib only."""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
FIGURES=ROOT.parent/"figures"
FIGURES.mkdir(exist_ok=True)
results=json.loads((ROOT/"results.json").read_text())
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10, "axes.spines.top":False,"axes.spines.right":False})

def plot_figures():
    fig, ax = plt.subplots(figsize=(7, 3))
    rows = results["variants"]["rows"]
    x = range(3)
    for offset, (key, title, color) in enumerate([
        ("base_evaluations", "Base", "#243b53"),
        ("art_evaluations", "Artwork", "#427f9c"),
        ("text_evaluations", "Text", "#8eb7c5")]):
        ax.bar([v+(offset-1)*.23 for v in x], [r[key] for r in rows],
               width=.23, label=title, color=color)
    ax.set_xticks(list(x), ["No reuse", "Base only", "Dependency reuse"])
    ax.set_ylabel("Stage evaluations")
    ax.set_title("Constructed catalogue: 218 valid outputs")
    ax.legend(frameon=False, ncol=3)
    fig.tight_layout()
    fig.savefig(FIGURES/"variant-work.png", dpi=180)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 3))
    rows = results["geometry"]["rows"]
    ax.plot([r["displacement"] for r in rows],
            [r["maximum_channel_error"] for r in rows], "o-", label="Measured analytic error")
    ax.plot([r["displacement"] for r in rows],
            [r["proven_upper_bound"] for r in rows], "s--", label="Conditional upper bound")
    ax.set(xlabel="Coordinate shift (normalized units)", ylabel="Maximum channel error",
           title="Synthetic smooth-field compositing; fixed matte error 0.02")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES/"attachment-error.png", dpi=180)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 3))
    ns = list(range(20, 601))
    for m in (1, 10, 100):
        ax.plot(ns, [100*(1-(.05/m)**(1/n)) for n in ns], label=f"{m} policies")
    ax.axhline(2, color="#9a463d", linestyle="--", label="2% target")
    ax.set(xlabel="Accepted independent episodes with zero errors",
           ylabel="Upper error limit (%)", ylim=(0, 12),
           title="Exact binomial planning calculation; 95% simultaneous confidence")
    ax.legend(frameon=False, ncol=2)
    fig.tight_layout()
    fig.savefig(FIGURES/"qc-sample-requirements.png", dpi=180)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 3))
    names = ["fixed_cheap_quick", "fixed_strong_strict", "nominal_dp", "robust_shielded_dp"]
    for off, (env, color) in enumerate([("nominal", "#427f9c"), ("adversarial", "#b57968")]):
        vals = [next(r["utility"] for r in results["routing"]["rows"]
                     if r["policy"] == n and r["environment"] == env) for n in names]
        ax.bar([i+(off-.5)*.35 for i in range(4)], vals, width=.35,
               label=env.title(), color=color)
    ax.set_xticks(range(4), ["Cheap/quick", "Strong/strict", "Nominal DP", "Robust + shield"])
    ax.axhline(0, color="#777777", linewidth=.7)
    ax.set(ylabel="Penalized utility (constructed units)",
           title="Synthetic routing: nominal benefit and robustness tradeoff")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES/"routing-tradeoff.png", dpi=180)
    plt.close(fig)

if __name__ == "__main__":
    plot_figures()
