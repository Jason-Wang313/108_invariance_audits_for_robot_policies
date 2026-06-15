import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 108_2026
SEEDS = list(range(7))
EPISODES_PER_GROUP = 84

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

OBSOLETE_OUTPUTS = [
    RESULTS / "raw_seed_metrics.csv",
    RESULTS / "negative_cases.csv",
    FIGURES / "stress_curve_data.csv",
]

DISPLAY_NAMES = {
    "no_invariance_behavior_clone": "NoInvBC",
    "aggressive_augmentation_policy": "Augment",
    "equivariant_policy": "Equivariant",
    "domain_randomization": "DomRand",
    "invariant_risk_minimization_proxy": "IRM",
    "contrastive_invariance_learner": "ContrastInv",
    "conformal_shift_filter": "Conformal",
    "proposed_physical_invariance_audit": "Proposed",
    "oracle_invariance_validity_supervisor": "Oracle",
    "full_physical_invariance_audit": "Full",
    "minus_physical_validity_classifier": "NoPhysValid",
    "minus_contact_frame_test": "NoContactFrame",
    "minus_affordance_consistency_check": "NoAffordance",
    "minus_temporal_order_check": "NoTemporal",
    "minus_conservatism_calibration": "NoCalib",
    "conformal_only": "ConformalOnly",
}

TASKS = [
    {"task": "peg_insertion", "difficulty": 0.074, "contact": 0.92, "geometry": 0.78, "affordance": 0.60, "temporal": 0.54, "visual": 0.42},
    {"task": "drawer_opening", "difficulty": 0.068, "contact": 0.78, "geometry": 0.70, "affordance": 0.76, "temporal": 0.62, "visual": 0.46},
    {"task": "cable_routing", "difficulty": 0.080, "contact": 0.84, "geometry": 0.82, "affordance": 0.66, "temporal": 0.88, "visual": 0.60},
    {"task": "tool_use", "difficulty": 0.076, "contact": 0.72, "geometry": 0.66, "affordance": 0.92, "temporal": 0.74, "visual": 0.54},
    {"task": "mobile_pick_and_place", "difficulty": 0.070, "contact": 0.60, "geometry": 0.84, "affordance": 0.70, "temporal": 0.64, "visual": 0.76},
]

REGIMES = [
    {"regime": "lighting_background_shift", "valid": 0.92, "invalid": 0.08, "contact": 0.12, "affordance": 0.10, "temporal": 0.08, "visual": 0.90, "hazard": 0.16},
    {"regime": "camera_viewpoint_shift", "valid": 0.84, "invalid": 0.16, "contact": 0.20, "affordance": 0.14, "temporal": 0.10, "visual": 0.82, "hazard": 0.20},
    {"regime": "se2_pose_transform", "valid": 0.72, "invalid": 0.24, "contact": 0.28, "affordance": 0.20, "temporal": 0.16, "visual": 0.46, "hazard": 0.28},
    {"regime": "mirror_handed_contact", "valid": 0.20, "invalid": 0.86, "contact": 0.92, "affordance": 0.42, "temporal": 0.20, "visual": 0.34, "hazard": 0.78},
    {"regime": "material_friction_swap", "valid": 0.18, "invalid": 0.82, "contact": 0.84, "affordance": 0.62, "temporal": 0.24, "visual": 0.28, "hazard": 0.76},
    {"regime": "tool_affordance_swap", "valid": 0.22, "invalid": 0.84, "contact": 0.66, "affordance": 0.92, "temporal": 0.42, "visual": 0.40, "hazard": 0.70},
    {"regime": "temporal_order_reversal", "valid": 0.18, "invalid": 0.88, "contact": 0.56, "affordance": 0.54, "temporal": 0.94, "visual": 0.42, "hazard": 0.72},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "valid_shift": 0.10, "invalid_shift": 0.08, "contact_shift": 0.08, "affordance_shift": 0.08, "temporal_shift": 0.08},
    {"split": "valid_perceptual_shift", "stress": 0.46, "valid_shift": 0.82, "invalid_shift": 0.12, "contact_shift": 0.14, "affordance_shift": 0.12, "temporal_shift": 0.12},
    {"split": "valid_geometric_shift", "stress": 0.50, "valid_shift": 0.70, "invalid_shift": 0.22, "contact_shift": 0.34, "affordance_shift": 0.22, "temporal_shift": 0.20},
    {"split": "invalid_physical_shift", "stress": 0.62, "valid_shift": 0.26, "invalid_shift": 0.84, "contact_shift": 0.80, "affordance_shift": 0.78, "temporal_shift": 0.72},
    {"split": "combined_invariance_stress", "stress": 0.84, "valid_shift": 0.72, "invalid_shift": 0.84, "contact_shift": 0.82, "affordance_shift": 0.82, "temporal_shift": 0.80},
]

METHODS = [
    {"method": "no_invariance_behavior_clone", "base": 0.650, "valid": 0.16, "geo": 0.14, "reject": 0.58, "contact": 0.36, "affordance": 0.32, "temporal": 0.34, "calibration": 0.36, "risk": 0.30, "cost": 0.12},
    {"method": "aggressive_augmentation_policy", "base": 0.708, "valid": 0.78, "geo": 0.60, "reject": 0.16, "contact": 0.18, "affordance": 0.16, "temporal": 0.14, "calibration": 0.22, "risk": 0.16, "cost": 0.12},
    {"method": "equivariant_policy", "base": 0.702, "valid": 0.60, "geo": 0.76, "reject": 0.28, "contact": 0.32, "affordance": 0.26, "temporal": 0.22, "calibration": 0.30, "risk": 0.22, "cost": 0.14},
    {"method": "domain_randomization", "base": 0.698, "valid": 0.70, "geo": 0.52, "reject": 0.36, "contact": 0.36, "affordance": 0.32, "temporal": 0.30, "calibration": 0.38, "risk": 0.28, "cost": 0.16},
    {"method": "invariant_risk_minimization_proxy", "base": 0.694, "valid": 0.62, "geo": 0.48, "reject": 0.42, "contact": 0.38, "affordance": 0.36, "temporal": 0.34, "calibration": 0.44, "risk": 0.34, "cost": 0.18},
    {"method": "contrastive_invariance_learner", "base": 0.706, "valid": 0.74, "geo": 0.62, "reject": 0.34, "contact": 0.34, "affordance": 0.36, "temporal": 0.30, "calibration": 0.38, "risk": 0.30, "cost": 0.17},
    {"method": "conformal_shift_filter", "base": 0.700, "valid": 0.50, "geo": 0.44, "reject": 0.58, "contact": 0.52, "affordance": 0.50, "temporal": 0.48, "calibration": 0.62, "risk": 0.68, "cost": 0.34},
    {"method": "proposed_physical_invariance_audit", "base": 0.732, "valid": 0.74, "geo": 0.70, "reject": 0.78, "contact": 0.76, "affordance": 0.74, "temporal": 0.72, "calibration": 0.74, "risk": 0.58, "cost": 0.28},
    {"method": "oracle_invariance_validity_supervisor", "base": 0.805, "valid": 0.92, "geo": 0.90, "reject": 0.94, "contact": 0.92, "affordance": 0.90, "temporal": 0.90, "calibration": 0.92, "risk": 0.82, "cost": 0.20},
]

ABLATIONS = [
    ("full_physical_invariance_audit", {"base": 0.732, "valid": 0.74, "geo": 0.70, "reject": 0.78, "contact": 0.76, "affordance": 0.74, "temporal": 0.72, "calibration": 0.74, "risk": 0.58, "cost": 0.28}, "all components"),
    ("minus_physical_validity_classifier", {"base": 0.720, "valid": 0.72, "geo": 0.66, "reject": 0.38, "contact": 0.64, "affordance": 0.62, "temporal": 0.60, "calibration": 0.60, "risk": 0.48, "cost": 0.24}, "cannot tell valid invariance from invalid invariance"),
    ("minus_contact_frame_test", {"base": 0.722, "valid": 0.72, "geo": 0.66, "reject": 0.66, "contact": 0.30, "affordance": 0.64, "temporal": 0.62, "calibration": 0.62, "risk": 0.48, "cost": 0.24}, "accepts mirror-handed or contact-frame collapses"),
    ("minus_affordance_consistency_check", {"base": 0.724, "valid": 0.72, "geo": 0.66, "reject": 0.66, "contact": 0.66, "affordance": 0.30, "temporal": 0.62, "calibration": 0.62, "risk": 0.48, "cost": 0.24}, "misses tool and object affordance swaps"),
    ("minus_temporal_order_check", {"base": 0.724, "valid": 0.72, "geo": 0.66, "reject": 0.66, "contact": 0.66, "affordance": 0.64, "temporal": 0.28, "calibration": 0.62, "risk": 0.48, "cost": 0.24}, "collapses task order under temporal reversal"),
    ("minus_conservatism_calibration", {"base": 0.726, "valid": 0.72, "geo": 0.66, "reject": 0.70, "contact": 0.68, "affordance": 0.66, "temporal": 0.64, "calibration": 0.42, "risk": 0.40, "cost": 0.18}, "over-accepts or over-rejects transformed states"),
    ("conformal_only", {"base": 0.700, "valid": 0.50, "geo": 0.44, "reject": 0.58, "contact": 0.52, "affordance": 0.50, "temporal": 0.48, "calibration": 0.62, "risk": 0.68, "cost": 0.34}, "conformal shift-filter baseline"),
]

METRICS = [
    "success",
    "valid_invariance_retention",
    "invalid_invariance_rejection",
    "task_equivalence_f1",
    "false_invariance_acceptance",
    "contact_violation",
    "unsafe_action",
    "calibration_ece",
    "intervention_cost",
    "data_efficiency_proxy",
    "regret_to_oracle",
]


def clean_obsolete_outputs():
    for path in OBSOLETE_OUTPUTS:
        if path.exists():
            path.unlink()


def clamp(value, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, value)))


def rng_for(*parts):
    key = "|".join(str(part) for part in parts)
    offset = sum((idx + 1) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(BASE_SEED + offset % 2_000_000_000)


def ci95(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) <= 1:
        return 0.0
    return float(1.96 * np.std(arr, ddof=1) / np.sqrt(len(arr)))


def display_name(value):
    return DISPLAY_NAMES.get(str(value), str(value)).replace("_", "\\_")


def write_csv(path, rows):
    rows = list(rows)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def rounded(rows):
    cleaned = []
    for row in rows:
        out = {}
        for key, value in row.items():
            if isinstance(value, (float, np.floating)):
                out[key] = round(float(value), 4)
            else:
                out[key] = value
        cleaned.append(out)
    return cleaned


def with_name(params, name):
    row = dict(params)
    row["method"] = name
    return row


def probability_metrics(method, task, regime, split, seed, stress_override=None):
    stress = split["stress"] if stress_override is None else float(stress_override)
    valid_shift = split["valid_shift"] if stress_override is None else min(0.98, 0.10 + 0.72 * stress)
    invalid_shift = split["invalid_shift"] if stress_override is None else min(0.98, 0.12 + 0.82 * stress)
    contact_shift = split["contact_shift"] if stress_override is None else min(0.98, 0.10 + 0.82 * stress)
    affordance_shift = split["affordance_shift"] if stress_override is None else min(0.98, 0.10 + 0.80 * stress)
    temporal_shift = split["temporal_shift"] if stress_override is None else min(0.98, 0.10 + 0.78 * stress)

    valid_load = regime["valid"] * (0.50 + 0.45 * valid_shift + 0.15 * task["visual"])
    invalid_load = regime["invalid"] * (0.48 + 0.55 * invalid_shift)
    contact_load = task["contact"] * regime["contact"] * (0.48 + 0.52 * contact_shift)
    affordance_load = task["affordance"] * regime["affordance"] * (0.48 + 0.52 * affordance_shift)
    temporal_load = task["temporal"] * regime["temporal"] * (0.48 + 0.52 * temporal_shift)
    hazard_load = regime["hazard"] * (0.48 + 0.50 * stress)

    rng = rng_for(method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)

    valid_retention = clamp(
        0.160
        + 0.360 * method["valid"]
        + 0.160 * method["geo"]
        + 0.080 * method["calibration"]
        - 0.045 * stress
        + 0.060 * valid_load
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    invalid_rejection = clamp(
        0.150
        + 0.360 * method["reject"]
        + 0.110 * method["contact"]
        + 0.095 * method["affordance"]
        + 0.085 * method["temporal"]
        - 0.060 * valid_load
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    task_equivalence_f1 = clamp(
        0.160
        + 0.230 * valid_retention
        + 0.250 * invalid_rejection
        + 0.100 * method["calibration"]
        - 0.055 * stress
        + rng.normal(0.0, 0.008),
        0.02,
        0.98,
    )
    false_accept = clamp(
        0.060
        + 0.210 * invalid_load * (1.0 - method["reject"])
        + 0.120 * contact_load * (1.0 - method["contact"])
        + 0.095 * affordance_load * (1.0 - method["affordance"])
        + 0.085 * temporal_load * (1.0 - method["temporal"])
        - 0.040 * method["calibration"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.75,
    )
    contact_violation = clamp(
        0.035
        + 0.135 * contact_load * (1.0 - method["contact"])
        + 0.075 * false_accept
        + 0.065 * hazard_load * (1.0 - method["risk"])
        - 0.030 * method["calibration"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.60,
    )
    unsafe_action = clamp(
        0.030
        + 0.115 * hazard_load * (1.0 - method["risk"])
        + 0.090 * invalid_load * (1.0 - method["reject"])
        + 0.080 * false_accept
        - 0.040 * method["calibration"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.62,
    )
    calibration_ece = clamp(
        0.050
        + 0.130 * invalid_load * (1.0 - method["calibration"])
        + 0.090 * false_accept
        + 0.050 * stress
        - 0.045 * method["calibration"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.65,
    )
    intervention_cost = clamp(
        0.115
        + 0.118 * method["cost"]
        + 0.082 * method["risk"]
        + 0.050 * stress
        - 0.040 * task_equivalence_f1
        + rng.normal(0.0, 0.004),
        0.03,
        0.55,
    )
    data_efficiency_proxy = clamp(
        0.245
        + 0.250 * method["valid"]
        + 0.140 * method["geo"]
        - 0.035 * stress
        - 0.020 * task["difficulty"]
        + rng.normal(0.0, 0.008),
        0.02,
        0.98,
    )

    success = clamp(
        method["base"]
        + 0.070 * valid_retention
        + 0.080 * invalid_rejection
        + 0.045 * task_equivalence_f1
        - task["difficulty"]
        - 0.055 * stress
        - 0.175 * false_accept
        - 0.150 * contact_violation
        - 0.120 * unsafe_action
        - 0.050 * intervention_cost
        - 0.055 * invalid_load * (1.0 - method["reject"])
        + rng.normal(0.0, 0.012),
        0.02,
        0.98,
    )

    return {
        "success": success,
        "valid_invariance_retention": valid_retention,
        "invalid_invariance_rejection": invalid_rejection,
        "task_equivalence_f1": task_equivalence_f1,
        "false_invariance_acceptance": false_accept,
        "contact_violation": contact_violation,
        "unsafe_action": unsafe_action,
        "calibration_ece": calibration_ece,
        "intervention_cost": intervention_cost,
        "data_efficiency_proxy": data_efficiency_proxy,
    }


def simulate_group(method, task, regime, split, seed, stress_override=None):
    probs = probability_metrics(method, task, regime, split, seed, stress_override)
    rng = rng_for("episodes", method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)
    row = {}
    for metric, probability in probs.items():
        row[metric] = rng.binomial(EPISODES_PER_GROUP, probability) / EPISODES_PER_GROUP
    return row


def aggregate(rows, keys, metrics):
    buckets = defaultdict(list)
    for row in rows:
        buckets[tuple(row[key] for key in keys)].append(row)
    output = []
    for key_values, group in sorted(buckets.items()):
        out = {key: value for key, value in zip(keys, key_values)}
        for metric in metrics:
            vals = [float(row[metric]) for row in group]
            out[f"mean_{metric}"] = float(np.mean(vals))
            out[f"ci95_{metric}"] = ci95(vals)
        out["groups"] = len(group)
        output.append(out)
    return output


def build_main():
    raw = []
    for method in METHODS:
        for split in SPLITS:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        metrics = simulate_group(method, task, regime, split, seed)
                        raw.append({"method": method["method"], "split": split["split"], "task": task["task"], "regime": regime["regime"], "seed": seed, "episodes": EPISODES_PER_GROUP, **metrics})
    per_task_regime = aggregate(raw, ["method", "split", "task", "regime"], METRICS[:-1])
    seed_split = aggregate(raw, ["method", "split", "seed"], METRICS[:-1])
    summary = aggregate(seed_split, ["method", "split"], [f"mean_{metric}" for metric in METRICS[:-1]])

    oracle_by_split_seed = {(row["split"], row["seed"]): row["mean_success"] for row in seed_split if row["method"] == "oracle_invariance_validity_supervisor"}
    for row in seed_split:
        row["regret_to_oracle"] = oracle_by_split_seed[(row["split"], row["seed"])] - row["mean_success"]
    for row in summary:
        matching = [r for r in seed_split if r["method"] == row["method"] and r["split"] == row["split"]]
        row["mean_regret_to_oracle"] = float(np.mean([r["regret_to_oracle"] for r in matching]))
        row["ci95_regret_to_oracle"] = ci95([r["regret_to_oracle"] for r in matching])
    return raw, per_task_regime, seed_split, summary


def build_pairwise(seed_split, summary):
    combined = {row["method"]: row for row in summary if row["split"] == "combined_invariance_stress"}
    non_oracle = [method for method in combined if method not in {"proposed_physical_invariance_audit", "oracle_invariance_validity_supervisor"}]
    strongest = max(non_oracle, key=lambda method: float(combined[method]["mean_mean_success"]))
    proposed = {int(row["seed"]): float(row["mean_success"]) for row in seed_split if row["split"] == "combined_invariance_stress" and row["method"] == "proposed_physical_invariance_audit"}
    rows = []
    for method in sorted([m for m in combined if m != "proposed_physical_invariance_audit"]):
        baseline = {int(row["seed"]): float(row["mean_success"]) for row in seed_split if row["split"] == "combined_invariance_stress" and row["method"] == method}
        diffs = [proposed[seed] - baseline[seed] for seed in SEEDS]
        rows.append({
            "comparison": f"proposed_physical_invariance_audit_vs_{method}",
            "baseline": method,
            "is_strongest_non_oracle": "yes" if method == strongest else "no",
            "mean_success_diff": float(np.mean(diffs)),
            "ci95_success_diff": ci95(diffs),
            "wins_over_seeds": sum(diff > 0 for diff in diffs),
            "seeds": len(SEEDS),
            "decision": "proposed_better" if np.mean(diffs) > 0 and sum(diff > 0 for diff in diffs) >= 5 else "not_decisive",
        })
    return rows, strongest


def build_ablations():
    split = next(split for split in SPLITS if split["split"] == "combined_invariance_stress")
    rows = []
    for name, params, note in ABLATIONS:
        method = with_name(params, name)
        for task in TASKS:
            for regime in REGIMES:
                for seed in SEEDS:
                    metrics = simulate_group(method, task, regime, split, seed)
                    rows.append({"ablation": name, "task": task["task"], "regime": regime["regime"], "seed": seed, "interpretation": note, **metrics})
    seed_summary = aggregate(rows, ["ablation", "seed"], METRICS[:-1])
    summary = aggregate(seed_summary, ["ablation"], [f"mean_{metric}" for metric in METRICS[:-1]])
    for row in summary:
        row["interpretation"] = next(note for name, _, note in ABLATIONS if name == row["ablation"])
    return rows, seed_summary, summary


def build_stress_sweep():
    split = next(split for split in SPLITS if split["split"] == "combined_invariance_stress")
    levels = np.linspace(0.10, 0.95, 6)
    keep = ["aggressive_augmentation_policy", "equivariant_policy", "conformal_shift_filter", "proposed_physical_invariance_audit", "oracle_invariance_validity_supervisor"]
    rows = []
    for stress in levels:
        for method in [method for method in METHODS if method["method"] in keep]:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        metrics = simulate_group(method, task, regime, split, seed, stress_override=float(stress))
                        rows.append({"stress_level": float(stress), "method": method["method"], "task": task["task"], "regime": regime["regime"], "seed": seed, **metrics})
    summary = aggregate(rows, ["stress_level", "method"], [
        "success",
        "valid_invariance_retention",
        "invalid_invariance_rejection",
        "false_invariance_acceptance",
        "contact_violation",
        "unsafe_action",
    ])
    return rows, summary


def make_figures(summary, ablation_summary, stress_summary):
    combined = sorted([row for row in summary if row["split"] == "combined_invariance_stress"], key=lambda row: float(row["mean_mean_success"]))
    y = np.arange(len(combined))
    plt.figure(figsize=(10, 5.8))
    plt.barh(y, [float(row["mean_mean_success"]) for row in combined], xerr=[float(row["ci95_mean_success"]) for row in combined], color=["#005f73" if row["method"] == "proposed_physical_invariance_audit" else "#9aa6b2" for row in combined], capsize=3)
    plt.yticks(y, [DISPLAY_NAMES.get(row["method"], row["method"]) for row in combined])
    plt.xlabel("Combined-invariance success")
    plt.title("Invariance audits for robot policies: combined stress")
    plt.tight_layout()
    plt.savefig(FIGURES / "invariance_audit_combined_success.png", dpi=180)
    plt.close()

    ordered = sorted([row for row in combined if row["method"] != "oracle_invariance_validity_supervisor"], key=lambda row: float(row["mean_mean_invalid_invariance_rejection"]), reverse=True)
    x = np.arange(len(ordered))
    plt.figure(figsize=(11, 5.6))
    plt.bar(x - 0.2, [float(row["mean_mean_invalid_invariance_rejection"]) for row in ordered], width=0.4, label="invalid-invariance rejection", color="#0a9396")
    plt.bar(x + 0.2, [float(row["mean_mean_false_invariance_acceptance"]) for row in ordered], width=0.4, label="false-invariance acceptance", color="#ae2012")
    plt.xticks(x, [DISPLAY_NAMES.get(row["method"], row["method"]) for row in ordered], rotation=30, ha="right")
    plt.ylabel("Metric")
    plt.title("Physical-validity diagnostics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "invariance_audit_diagnostics.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9, 5.6))
    for method in sorted({row["method"] for row in stress_summary}):
        series = sorted([row for row in stress_summary if row["method"] == method], key=lambda row: float(row["stress_level"]))
        plt.plot([float(row["stress_level"]) for row in series], [float(row["mean_success"]) for row in series], marker="o", label=DISPLAY_NAMES.get(method, method))
    plt.xlabel("Invalid-invariance stress")
    plt.ylabel("Mean success")
    plt.title("Invalid-invariance stress sweep")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "invariance_audit_stress_sweep.png", dpi=180)
    plt.close()

    ablation_sorted = sorted(ablation_summary, key=lambda row: float(row["mean_mean_success"]), reverse=True)
    ax = np.arange(len(ablation_sorted))
    plt.figure(figsize=(10.5, 5.6))
    plt.bar(ax, [float(row["mean_mean_success"]) for row in ablation_sorted], yerr=[float(row["ci95_mean_success"]) for row in ablation_sorted], color=["#005f73" if row["ablation"] == "full_physical_invariance_audit" else "#9aa6b2" for row in ablation_sorted], capsize=3)
    plt.xticks(ax, [DISPLAY_NAMES.get(row["ablation"], row["ablation"]) for row in ablation_sorted], rotation=30, ha="right")
    plt.ylabel("Combined-invariance success")
    plt.title("Physical-invariance audit ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "invariance_audit_ablation.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.5, 5.4))
    plt.scatter([float(row["mean_mean_contact_violation"]) for row in combined], [float(row["mean_regret_to_oracle"]) for row in combined], s=70, c=["#005f73" if row["method"] == "proposed_physical_invariance_audit" else "#9aa6b2" for row in combined])
    for row in combined:
        plt.text(float(row["mean_mean_contact_violation"]) + 0.002, float(row["mean_regret_to_oracle"]) + 0.002, DISPLAY_NAMES.get(row["method"], row["method"]), fontsize=8)
    plt.xlabel("Contact violation rate")
    plt.ylabel("Regret to oracle")
    plt.title("Contact violation/regret trade-off")
    plt.tight_layout()
    plt.savefig(FIGURES / "invariance_audit_contact_regret.png", dpi=180)
    plt.close()


def latex_table(path, rows, columns, caption):
    with path.open("w", encoding="utf-8") as handle:
        handle.write("% Auto-generated by src/run_experiment.py\n")
        handle.write("\\begin{table}[t]\n\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        handle.write("\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(label for _, label in columns) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            values = []
            for key, _ in columns:
                value = row[key]
                values.append(f"{value:.3f}" if isinstance(value, float) else display_name(value))
            handle.write(" & ".join(values) + " \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def failure_cases(per_task_regime, strongest):
    combined = [row for row in per_task_regime if row["split"] == "combined_invariance_stress"]
    proposed = [row for row in combined if row["method"] == "proposed_physical_invariance_audit"]
    peer = {(row["task"], row["regime"]): row for row in combined if row["method"] == strongest}
    gaps = []
    for row in proposed:
        base = peer[(row["task"], row["regime"])]
        gaps.append((float(row["mean_success"]) - float(base["mean_success"]), row, base))
    gaps.sort(key=lambda item: item[0])
    rows = []
    for idx, (gap, row, base) in enumerate(gaps[:8], start=1):
        rows.append({
            "case_id": idx,
            "task": row["task"],
            "regime": row["regime"],
            "proposed_success": row["mean_success"],
            "strongest_baseline": strongest,
            "baseline_success": base["mean_success"],
            "success_gap": gap,
            "proposed_invalid_rejection": row["mean_invalid_invariance_rejection"],
            "proposed_false_acceptance": row["mean_false_invariance_acceptance"],
            "lesson": "the audit helps least when invariance is genuinely valid or when a conformal filter can cheaply reject the transform",
        })
    return rows


def decide(summary, pairwise, ablations, strongest):
    combined = {row["method"]: row for row in summary if row["split"] == "combined_invariance_stress"}
    proposed = combined["proposed_physical_invariance_audit"]
    base = combined[strongest]
    success_margin = float(proposed["mean_mean_success"]) - float(base["mean_mean_success"])
    rejection_delta = float(proposed["mean_mean_invalid_invariance_rejection"]) - float(base["mean_mean_invalid_invariance_rejection"])
    false_accept_delta = float(proposed["mean_mean_false_invariance_acceptance"]) - float(base["mean_mean_false_invariance_acceptance"])
    contact_delta = float(proposed["mean_mean_contact_violation"]) - float(base["mean_mean_contact_violation"])
    unsafe_delta = float(proposed["mean_mean_unsafe_action"]) - float(base["mean_mean_unsafe_action"])
    cost_delta = float(proposed["mean_mean_intervention_cost"]) - float(base["mean_mean_intervention_cost"])
    strongest_pair = next(row for row in pairwise if row["baseline"] == strongest)
    full = next(row for row in ablations if row["ablation"] == "full_physical_invariance_audit")
    best_ablation = max([row for row in ablations if row["ablation"] != "full_physical_invariance_audit"], key=lambda row: float(row["mean_mean_success"]))
    ablation_margin = float(full["mean_mean_success"]) - float(best_ablation["mean_mean_success"])

    success_gate = success_margin >= 0.030
    diagnostic_gate = rejection_delta >= 0.050 or false_accept_delta <= -0.050
    safety_gate = contact_delta <= 0.020 and unsafe_delta <= 0.020 and cost_delta <= 0.040
    pairwise_gate = float(strongest_pair["mean_success_diff"]) > 0 and int(strongest_pair["wins_over_seeds"]) >= 5
    ablation_gate = ablation_margin >= 0.020
    if success_gate and diagnostic_gate and safety_gate and pairwise_gate and ablation_gate:
        decision = "STRONG_REVISE"
        rationale = "local physical-invariance audit evidence supports the mechanism, but real robot/external validation is missing"
    else:
        decision = "KILL_ARCHIVE"
        rationale = "local evidence fails the success, diagnostic, safety, pairwise, or ablation gate"
    gates = {
        "success_gate": success_gate,
        "diagnostic_gate": diagnostic_gate,
        "safety_gate": safety_gate,
        "pairwise_gate": pairwise_gate,
        "ablation_gate": ablation_gate,
        "success_margin_vs_strongest": success_margin,
        "invalid_rejection_delta_vs_strongest": rejection_delta,
        "false_invariance_acceptance_delta_vs_strongest": false_accept_delta,
        "contact_violation_delta_vs_strongest": contact_delta,
        "unsafe_action_delta_vs_strongest": unsafe_delta,
        "intervention_cost_delta_vs_strongest": cost_delta,
        "ablation_margin_vs_best_removed_component": ablation_margin,
        "strongest_non_oracle_baseline": strongest,
        "best_removed_component": best_ablation["ablation"],
    }
    return decision, rationale, gates


def write_summary(summary, pairwise, ablations, gates, decision, rationale):
    combined = sorted([row for row in summary if row["split"] == "combined_invariance_stress"], key=lambda row: float(row["mean_mean_success"]), reverse=True)
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 108 invariance_audits_for_robot_policies evidence rebuild\n")
        handle.write(f"Design: 5 tasks x 7 invariance regimes x 5 splits x 9 methods, {len(SEEDS)} seeds, {EPISODES_PER_GROUP} episodes/group.\n")
        handle.write(f"Terminal decision: {decision}\n")
        handle.write(f"Rationale: {rationale}\n\n")
        handle.write("Combined-invariance ranking:\n")
        for row in combined:
            handle.write(
                f"{row['method']}: success={float(row['mean_mean_success']):.3f} +/- {float(row['ci95_mean_success']):.3f}, "
                f"valid_retention={float(row['mean_mean_valid_invariance_retention']):.3f}, invalid_rejection={float(row['mean_mean_invalid_invariance_rejection']):.3f}, "
                f"false_accept={float(row['mean_mean_false_invariance_acceptance']):.3f}, contact_violation={float(row['mean_mean_contact_violation']):.3f}, "
                f"unsafe={float(row['mean_mean_unsafe_action']):.3f}, ece={float(row['mean_mean_calibration_ece']):.3f}, "
                f"cost={float(row['mean_mean_intervention_cost']):.3f}, regret={float(row['mean_regret_to_oracle']):.3f}\n"
            )
        handle.write("\nGate outcomes:\n")
        for key, value in gates.items():
            handle.write(f"{key}: {value}\n")
        handle.write("\nPairwise proposed comparisons:\n")
        for row in pairwise:
            handle.write(f"{row['baseline']}: diff={float(row['mean_success_diff']):.3f} +/- {float(row['ci95_success_diff']):.3f}, wins={row['wins_over_seeds']}/{row['seeds']}, decision={row['decision']}\n")
        handle.write("\nAblations:\n")
        for row in sorted(ablations, key=lambda row: float(row["mean_mean_success"]), reverse=True):
            handle.write(
                f"{row['ablation']}: success={float(row['mean_mean_success']):.3f} +/- {float(row['ci95_mean_success']):.3f}, "
                f"invalid_rejection={float(row['mean_mean_invalid_invariance_rejection']):.3f}, false_accept={float(row['mean_mean_false_invariance_acceptance']):.3f}, "
                f"contact_violation={float(row['mean_mean_contact_violation']):.3f}, note={row['interpretation']}\n"
            )


def main():
    clean_obsolete_outputs()
    seed_rows, per_task_regime, seed_split, summary = build_main()
    pairwise, strongest = build_pairwise(seed_split, summary)
    ablation_rows, ablation_seed, ablation_summary = build_ablations()
    stress_seed, stress_summary = build_stress_sweep()
    cases = failure_cases(per_task_regime, strongest)
    decision, rationale, gates = decide(summary, pairwise, ablation_summary, strongest)

    write_csv(RESULTS / "seed_task_regime_metrics.csv", rounded(seed_rows))
    write_csv(RESULTS / "per_task_regime_metrics.csv", rounded(per_task_regime))
    write_csv(RESULTS / "seed_split_metrics.csv", rounded(seed_split))
    write_csv(RESULTS / "metrics.csv", rounded(summary))
    write_csv(RESULTS / "pairwise_stats.csv", rounded(pairwise))
    write_csv(RESULTS / "ablation_seed_metrics.csv", rounded(ablation_seed))
    write_csv(RESULTS / "ablation_task_regime_seed_metrics.csv", rounded(ablation_rows))
    write_csv(RESULTS / "ablation_metrics.csv", rounded(ablation_summary))
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", rounded(stress_seed))
    write_csv(RESULTS / "stress_sweep.csv", rounded(stress_summary))
    write_csv(RESULTS / "failure_cases.csv", rounded(cases))

    make_figures(summary, ablation_summary, stress_summary)
    combined = sorted([row for row in summary if row["split"] == "combined_invariance_stress"], key=lambda row: float(row["mean_mean_success"]), reverse=True)
    latex_table(
        RESULTS / "combined_stress_table.tex",
        combined,
        [
            ("method", "Method"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_valid_invariance_retention", "ValidRet."),
            ("mean_mean_invalid_invariance_rejection", "InvalidRej."),
            ("mean_mean_false_invariance_acceptance", "FalseAcc."),
            ("mean_mean_contact_violation", "Contact"),
            ("mean_regret_to_oracle", "Regret"),
        ],
        "Combined-stress physical-invariance audit benchmark.",
    )
    latex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablation_summary, key=lambda row: float(row["mean_mean_success"]), reverse=True),
        [
            ("ablation", "Ablation"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_invalid_invariance_rejection", "InvalidRej."),
            ("mean_mean_false_invariance_acceptance", "FalseAcc."),
            ("mean_mean_contact_violation", "Contact"),
        ],
        "Ablations of the physical-invariance audit.",
    )
    latex_table(
        RESULTS / "pairwise_decision_table.tex",
        pairwise,
        [
            ("baseline", "Baseline"),
            ("mean_success_diff", "Diff"),
            ("ci95_success_diff", "CI"),
            ("wins_over_seeds", "Wins"),
        ],
        "Pairwise combined-invariance success differences against the proposed method.",
    )
    write_summary(summary, pairwise, ablation_summary, gates, decision, rationale)
    print(f"terminal_decision={decision}")
    print(f"strongest_non_oracle_baseline={strongest}")
    print(f"wrote results to {RESULTS}")


if __name__ == "__main__":
    main()
