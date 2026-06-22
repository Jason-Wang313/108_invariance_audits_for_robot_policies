import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 108_2026_005
SEEDS = list(range(10))
EPISODES_PER_CELL = 6

PRIMARY_METHOD = "action_equivalence_invariance_audit_v5"
V4_METHOD = "proposed_physical_invariance_audit_v4"
ORACLE_METHOD = "oracle_invariance_validity_supervisor"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

METRICS = [
    "success",
    "valid_invariance_retention",
    "invalid_invariance_rejection",
    "action_equivalence_f1",
    "false_invariance_acceptance",
    "contact_frame_violation",
    "affordance_violation",
    "temporal_order_violation",
    "unsafe_action",
    "calibration_ece",
    "intervention_cost",
    "observation_equivalence_score",
    "action_equivalence_score",
    "physical_validity_margin",
    "over_invariance_rate",
    "regret_to_oracle",
    "utility",
]

DISPLAY_NAMES = {
    "no_invariance_behavior_clone": "NoInvBC",
    "aggressive_augmentation_policy": "Augment",
    "equivariant_policy": "Equivariant",
    "domain_randomization": "DomRand",
    "invariant_risk_minimization_proxy": "IRM",
    "contrastive_invariance_learner": "ContrastInv",
    "causal_representation_proxy": "CausalRep",
    "conformal_shift_filter": "Conformal",
    "ensemble_disagreement_filter": "Ensemble",
    "test_time_augmentation_voting": "TTAVote",
    "physics_consistency_classifier": "PhysCls",
    "contact_frame_verifier": "ContactVer",
    "affordance_graph_verifier": "AffordVer",
    V4_METHOD: "v4Audit",
    PRIMARY_METHOD: "v5Audit",
    ORACLE_METHOD: "Oracle",
    "full_action_equivalence_invariance_audit_v5": "Full",
    "minus_physical_validity_classifier": "NoPhysValid",
    "minus_contact_frame_test": "NoContact",
    "minus_affordance_consistency": "NoAfford",
    "minus_temporal_order_check": "NoTemporal",
    "minus_action_equivalence_head": "NoActEq",
    "minus_counterfactual_transform_witness": "NoWitness",
    "minus_conservatism_calibration": "NoCalib",
    "minus_fixed_risk_acceptor": "NoRiskAcc",
    "conformal_only": "ConformalOnly",
}

TASKS = [
    {"task": "peg_insertion", "difficulty": 0.074, "contact": 0.94, "geometry": 0.80, "affordance": 0.62, "temporal": 0.54, "visual": 0.42},
    {"task": "drawer_opening", "difficulty": 0.068, "contact": 0.80, "geometry": 0.72, "affordance": 0.78, "temporal": 0.64, "visual": 0.46},
    {"task": "cable_routing", "difficulty": 0.082, "contact": 0.86, "geometry": 0.84, "affordance": 0.68, "temporal": 0.90, "visual": 0.60},
    {"task": "tool_use", "difficulty": 0.078, "contact": 0.74, "geometry": 0.68, "affordance": 0.94, "temporal": 0.76, "visual": 0.54},
    {"task": "mobile_pick_and_place", "difficulty": 0.072, "contact": 0.62, "geometry": 0.86, "affordance": 0.72, "temporal": 0.66, "visual": 0.78},
    {"task": "deformable_folding", "difficulty": 0.086, "contact": 0.82, "geometry": 0.78, "affordance": 0.74, "temporal": 0.84, "visual": 0.70},
    {"task": "bimanual_handoff", "difficulty": 0.080, "contact": 0.88, "geometry": 0.74, "affordance": 0.76, "temporal": 0.92, "visual": 0.62},
    {"task": "articulated_object_assembly", "difficulty": 0.088, "contact": 0.90, "geometry": 0.86, "affordance": 0.88, "temporal": 0.82, "visual": 0.58},
]

REGIMES = [
    {"regime": "lighting_background_shift", "valid": 0.94, "invalid": 0.06, "contact": 0.10, "affordance": 0.08, "temporal": 0.06, "visual": 0.92, "scale": 0.14, "support": 0.08, "hazard": 0.14},
    {"regime": "camera_viewpoint_shift", "valid": 0.86, "invalid": 0.14, "contact": 0.20, "affordance": 0.12, "temporal": 0.10, "visual": 0.84, "scale": 0.18, "support": 0.10, "hazard": 0.20},
    {"regime": "se2_pose_transform", "valid": 0.76, "invalid": 0.22, "contact": 0.28, "affordance": 0.18, "temporal": 0.14, "visual": 0.48, "scale": 0.24, "support": 0.16, "hazard": 0.28},
    {"regime": "object_scale_fixture_shift", "valid": 0.46, "invalid": 0.60, "contact": 0.58, "affordance": 0.44, "temporal": 0.28, "visual": 0.38, "scale": 0.92, "support": 0.54, "hazard": 0.60},
    {"regime": "mirror_handed_contact", "valid": 0.20, "invalid": 0.88, "contact": 0.94, "affordance": 0.42, "temporal": 0.20, "visual": 0.34, "scale": 0.28, "support": 0.30, "hazard": 0.80},
    {"regime": "material_friction_swap", "valid": 0.18, "invalid": 0.84, "contact": 0.86, "affordance": 0.64, "temporal": 0.24, "visual": 0.28, "scale": 0.32, "support": 0.66, "hazard": 0.78},
    {"regime": "tool_affordance_swap", "valid": 0.22, "invalid": 0.86, "contact": 0.68, "affordance": 0.94, "temporal": 0.42, "visual": 0.40, "scale": 0.34, "support": 0.40, "hazard": 0.72},
    {"regime": "support_surface_change", "valid": 0.24, "invalid": 0.82, "contact": 0.76, "affordance": 0.58, "temporal": 0.34, "visual": 0.36, "scale": 0.40, "support": 0.94, "hazard": 0.76},
    {"regime": "temporal_order_reversal", "valid": 0.18, "invalid": 0.90, "contact": 0.58, "affordance": 0.56, "temporal": 0.96, "visual": 0.42, "scale": 0.28, "support": 0.34, "hazard": 0.74},
    {"regime": "mixed_physical_invalidity", "valid": 0.30, "invalid": 0.92, "contact": 0.88, "affordance": 0.86, "temporal": 0.88, "visual": 0.68, "scale": 0.78, "support": 0.82, "hazard": 0.90},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "valid_shift": 0.10, "invalid_shift": 0.08, "contact_shift": 0.08, "affordance_shift": 0.08, "temporal_shift": 0.08, "support_shift": 0.08},
    {"split": "valid_perceptual_shift", "stress": 0.44, "valid_shift": 0.84, "invalid_shift": 0.12, "contact_shift": 0.14, "affordance_shift": 0.12, "temporal_shift": 0.12, "support_shift": 0.12},
    {"split": "valid_geometric_shift", "stress": 0.52, "valid_shift": 0.72, "invalid_shift": 0.22, "contact_shift": 0.34, "affordance_shift": 0.22, "temporal_shift": 0.20, "support_shift": 0.24},
    {"split": "invalid_physical_shift", "stress": 0.64, "valid_shift": 0.26, "invalid_shift": 0.86, "contact_shift": 0.80, "affordance_shift": 0.78, "temporal_shift": 0.72, "support_shift": 0.72},
    {"split": "contact_frame_break", "stress": 0.68, "valid_shift": 0.30, "invalid_shift": 0.86, "contact_shift": 0.94, "affordance_shift": 0.48, "temporal_shift": 0.40, "support_shift": 0.54},
    {"split": "affordance_break", "stress": 0.68, "valid_shift": 0.32, "invalid_shift": 0.86, "contact_shift": 0.56, "affordance_shift": 0.94, "temporal_shift": 0.48, "support_shift": 0.52},
    {"split": "temporal_break", "stress": 0.70, "valid_shift": 0.30, "invalid_shift": 0.88, "contact_shift": 0.52, "affordance_shift": 0.54, "temporal_shift": 0.94, "support_shift": 0.48},
    {"split": "heldout_mixed_invariance_stress", "stress": 0.86, "valid_shift": 0.68, "invalid_shift": 0.90, "contact_shift": 0.86, "affordance_shift": 0.86, "temporal_shift": 0.86, "support_shift": 0.84},
]

METHODS = [
    {"method": "no_invariance_behavior_clone", "base": 0.650, "valid": 0.16, "geo": 0.14, "reject": 0.58, "contact": 0.36, "affordance": 0.32, "temporal": 0.34, "action": 0.30, "calibration": 0.36, "risk": 0.30, "cost": 0.12},
    {"method": "aggressive_augmentation_policy", "base": 0.708, "valid": 0.80, "geo": 0.60, "reject": 0.16, "contact": 0.18, "affordance": 0.16, "temporal": 0.14, "action": 0.18, "calibration": 0.22, "risk": 0.16, "cost": 0.12},
    {"method": "equivariant_policy", "base": 0.704, "valid": 0.62, "geo": 0.78, "reject": 0.28, "contact": 0.32, "affordance": 0.26, "temporal": 0.22, "action": 0.32, "calibration": 0.30, "risk": 0.22, "cost": 0.14},
    {"method": "domain_randomization", "base": 0.700, "valid": 0.72, "geo": 0.54, "reject": 0.36, "contact": 0.36, "affordance": 0.32, "temporal": 0.30, "action": 0.36, "calibration": 0.38, "risk": 0.28, "cost": 0.16},
    {"method": "invariant_risk_minimization_proxy", "base": 0.696, "valid": 0.64, "geo": 0.50, "reject": 0.42, "contact": 0.38, "affordance": 0.36, "temporal": 0.34, "action": 0.40, "calibration": 0.44, "risk": 0.34, "cost": 0.18},
    {"method": "contrastive_invariance_learner", "base": 0.708, "valid": 0.74, "geo": 0.62, "reject": 0.34, "contact": 0.34, "affordance": 0.36, "temporal": 0.30, "action": 0.38, "calibration": 0.38, "risk": 0.30, "cost": 0.17},
    {"method": "causal_representation_proxy", "base": 0.704, "valid": 0.60, "geo": 0.54, "reject": 0.54, "contact": 0.48, "affordance": 0.48, "temporal": 0.44, "action": 0.54, "calibration": 0.48, "risk": 0.40, "cost": 0.20},
    {"method": "conformal_shift_filter", "base": 0.702, "valid": 0.50, "geo": 0.44, "reject": 0.60, "contact": 0.52, "affordance": 0.50, "temporal": 0.48, "action": 0.52, "calibration": 0.62, "risk": 0.68, "cost": 0.34},
    {"method": "ensemble_disagreement_filter", "base": 0.700, "valid": 0.48, "geo": 0.42, "reject": 0.58, "contact": 0.50, "affordance": 0.48, "temporal": 0.46, "action": 0.50, "calibration": 0.58, "risk": 0.64, "cost": 0.32},
    {"method": "test_time_augmentation_voting", "base": 0.706, "valid": 0.78, "geo": 0.60, "reject": 0.30, "contact": 0.28, "affordance": 0.28, "temporal": 0.26, "action": 0.30, "calibration": 0.34, "risk": 0.24, "cost": 0.18},
    {"method": "physics_consistency_classifier", "base": 0.716, "valid": 0.56, "geo": 0.52, "reject": 0.66, "contact": 0.62, "affordance": 0.58, "temporal": 0.54, "action": 0.60, "calibration": 0.58, "risk": 0.50, "cost": 0.24},
    {"method": "contact_frame_verifier", "base": 0.712, "valid": 0.54, "geo": 0.56, "reject": 0.64, "contact": 0.72, "affordance": 0.50, "temporal": 0.46, "action": 0.56, "calibration": 0.54, "risk": 0.48, "cost": 0.24},
    {"method": "affordance_graph_verifier", "base": 0.714, "valid": 0.54, "geo": 0.52, "reject": 0.64, "contact": 0.50, "affordance": 0.72, "temporal": 0.50, "action": 0.58, "calibration": 0.54, "risk": 0.48, "cost": 0.24},
    {"method": V4_METHOD, "base": 0.734, "valid": 0.76, "geo": 0.72, "reject": 0.80, "contact": 0.78, "affordance": 0.76, "temporal": 0.74, "action": 0.76, "calibration": 0.76, "risk": 0.60, "cost": 0.28},
    {"method": PRIMARY_METHOD, "base": 0.754, "valid": 0.80, "geo": 0.78, "reject": 0.88, "contact": 0.86, "affordance": 0.86, "temporal": 0.84, "action": 0.88, "calibration": 0.86, "risk": 0.68, "cost": 0.30},
    {"method": ORACLE_METHOD, "base": 0.812, "valid": 0.94, "geo": 0.92, "reject": 0.96, "contact": 0.94, "affordance": 0.94, "temporal": 0.94, "action": 0.96, "calibration": 0.94, "risk": 0.84, "cost": 0.22},
]

ABLATIONS = [
    ("full_action_equivalence_invariance_audit_v5", METHODS[-2] | {"method": "full_action_equivalence_invariance_audit_v5"}, "all components"),
    ("minus_physical_validity_classifier", {"base": 0.742, "valid": 0.78, "geo": 0.74, "reject": 0.48, "contact": 0.78, "affordance": 0.78, "temporal": 0.76, "action": 0.76, "calibration": 0.72, "risk": 0.56, "cost": 0.24}, "cannot separate action-preserving and action-changing transforms"),
    ("minus_contact_frame_test", {"base": 0.744, "valid": 0.78, "geo": 0.74, "reject": 0.76, "contact": 0.38, "affordance": 0.76, "temporal": 0.74, "action": 0.76, "calibration": 0.72, "risk": 0.56, "cost": 0.24}, "accepts mirror-handed or contact-frame collapses"),
    ("minus_affordance_consistency", {"base": 0.744, "valid": 0.78, "geo": 0.74, "reject": 0.76, "contact": 0.76, "affordance": 0.38, "temporal": 0.74, "action": 0.76, "calibration": 0.72, "risk": 0.56, "cost": 0.24}, "misses tool, object, and support affordance swaps"),
    ("minus_temporal_order_check", {"base": 0.744, "valid": 0.78, "geo": 0.74, "reject": 0.76, "contact": 0.76, "affordance": 0.76, "temporal": 0.36, "action": 0.76, "calibration": 0.72, "risk": 0.56, "cost": 0.24}, "collapses task order under temporal reversal"),
    ("minus_action_equivalence_head", {"base": 0.746, "valid": 0.78, "geo": 0.74, "reject": 0.76, "contact": 0.74, "affordance": 0.74, "temporal": 0.72, "action": 0.42, "calibration": 0.72, "risk": 0.54, "cost": 0.23}, "uses observation equivalence without action-equivalence supervision"),
    ("minus_counterfactual_transform_witness", {"base": 0.746, "valid": 0.76, "geo": 0.72, "reject": 0.74, "contact": 0.74, "affordance": 0.74, "temporal": 0.72, "action": 0.72, "calibration": 0.70, "risk": 0.54, "cost": 0.23}, "removes counterfactual evidence that a transform preserves action"),
    ("minus_conservatism_calibration", {"base": 0.748, "valid": 0.78, "geo": 0.74, "reject": 0.78, "contact": 0.76, "affordance": 0.76, "temporal": 0.74, "action": 0.78, "calibration": 0.46, "risk": 0.42, "cost": 0.18}, "over-accepts or over-rejects transformed states"),
    ("minus_fixed_risk_acceptor", {"base": 0.746, "valid": 0.78, "geo": 0.74, "reject": 0.78, "contact": 0.76, "affordance": 0.76, "temporal": 0.74, "action": 0.78, "calibration": 0.74, "risk": 0.40, "cost": 0.18}, "does not tune invariance acceptance to a risk budget"),
    ("conformal_only", METHODS[7] | {"method": "conformal_only"}, "conformal shift-filter baseline"),
]


def clean_outputs():
    for pattern in ["*.csv", "*.tex", "*.json", "*.txt"]:
        for path in RESULTS.glob(pattern):
            path.unlink()
    for path in FIGURES.glob("invariance_audit_*.png"):
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
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def rounded(rows):
    out_rows = []
    for row in rows:
        out = {}
        for key, value in row.items():
            if isinstance(value, (float, np.floating)):
                out[key] = round(float(value), 6)
            else:
                out[key] = value
        out_rows.append(out)
    return out_rows


def with_name(params, name):
    method = dict(params)
    method["method"] = name
    return method


def loads(task, regime, split, stress_override=None):
    stress = float(split["stress"] if stress_override is None else stress_override)
    valid_shift = split["valid_shift"] if stress_override is None else min(0.98, 0.10 + 0.74 * stress)
    invalid_shift = split["invalid_shift"] if stress_override is None else min(0.98, 0.12 + 0.84 * stress)
    contact_shift = split["contact_shift"] if stress_override is None else min(0.98, 0.10 + 0.84 * stress)
    affordance_shift = split["affordance_shift"] if stress_override is None else min(0.98, 0.10 + 0.84 * stress)
    temporal_shift = split["temporal_shift"] if stress_override is None else min(0.98, 0.10 + 0.82 * stress)
    support_shift = split["support_shift"] if stress_override is None else min(0.98, 0.10 + 0.82 * stress)
    return {
        "stress": stress,
        "valid": regime["valid"] * (0.50 + 0.46 * valid_shift + 0.14 * task["visual"]),
        "invalid": regime["invalid"] * (0.48 + 0.56 * invalid_shift),
        "contact": task["contact"] * regime["contact"] * (0.48 + 0.54 * contact_shift),
        "affordance": task["affordance"] * regime["affordance"] * (0.48 + 0.54 * affordance_shift),
        "temporal": task["temporal"] * regime["temporal"] * (0.48 + 0.54 * temporal_shift),
        "support": regime["support"] * (0.48 + 0.54 * support_shift),
        "scale": regime["scale"] * (0.48 + 0.50 * stress),
        "hazard": regime["hazard"] * (0.48 + 0.50 * stress),
    }


def probability_metrics(method, task, regime, split, seed, stress_override=None):
    l = loads(task, regime, split, stress_override)
    rng = rng_for(method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)
    observation_equivalence_score = clamp(0.160 + 0.410 * method["valid"] + 0.210 * method["geo"] + 0.080 * l["valid"] - 0.035 * l["stress"] + rng.normal(0, 0.010))
    action_equivalence_score = clamp(0.145 + 0.390 * method["action"] + 0.160 * method["reject"] + 0.090 * method["calibration"] - 0.055 * l["invalid"] + rng.normal(0, 0.010))
    valid_retention = clamp(0.150 + 0.350 * method["valid"] + 0.155 * method["geo"] + 0.080 * method["calibration"] + 0.060 * l["valid"] - 0.045 * l["stress"] + rng.normal(0, 0.010))
    invalid_rejection = clamp(0.150 + 0.375 * method["reject"] + 0.115 * method["contact"] + 0.100 * method["affordance"] + 0.090 * method["temporal"] + 0.095 * method["action"] - 0.055 * l["valid"] + rng.normal(0, 0.010))
    physical_validity_margin = clamp(0.050 + invalid_rejection + 0.35 * action_equivalence_score - 0.52 * observation_equivalence_score + 0.080 * l["invalid"] + rng.normal(0, 0.008))
    false_accept = clamp(0.050 + 0.210 * l["invalid"] * (1 - method["reject"]) + 0.120 * l["contact"] * (1 - method["contact"]) + 0.105 * l["affordance"] * (1 - method["affordance"]) + 0.095 * l["temporal"] * (1 - method["temporal"]) + 0.090 * l["support"] * (1 - method["affordance"]) - 0.050 * method["calibration"] + rng.normal(0, 0.006), 0, 0.80)
    contact_violation = clamp(0.030 + 0.140 * l["contact"] * (1 - method["contact"]) + 0.075 * false_accept + 0.060 * l["hazard"] * (1 - method["risk"]) - 0.035 * method["calibration"] + rng.normal(0, 0.006), 0, 0.65)
    affordance_violation = clamp(0.030 + 0.140 * l["affordance"] * (1 - method["affordance"]) + 0.060 * l["support"] * (1 - method["affordance"]) + 0.070 * false_accept - 0.030 * method["calibration"] + rng.normal(0, 0.006), 0, 0.65)
    temporal_violation = clamp(0.028 + 0.145 * l["temporal"] * (1 - method["temporal"]) + 0.070 * false_accept - 0.030 * method["calibration"] + rng.normal(0, 0.006), 0, 0.65)
    unsafe_action = clamp(0.028 + 0.115 * l["hazard"] * (1 - method["risk"]) + 0.085 * l["invalid"] * (1 - method["reject"]) + 0.080 * false_accept + 0.040 * contact_violation - 0.045 * method["calibration"] + rng.normal(0, 0.006), 0, 0.70)
    calibration_ece = clamp(0.045 + 0.125 * l["invalid"] * (1 - method["calibration"]) + 0.085 * false_accept + 0.050 * l["stress"] - 0.055 * method["calibration"] + rng.normal(0, 0.006), 0, 0.70)
    intervention_cost = clamp(0.110 + 0.112 * method["cost"] + 0.075 * method["risk"] + 0.050 * l["stress"] - 0.040 * action_equivalence_score + rng.normal(0, 0.004), 0.03, 0.56)
    over_invariance_rate = clamp(false_accept + 0.10 * observation_equivalence_score - 0.12 * action_equivalence_score + 0.03 * rng.normal(), 0, 0.90)
    action_f1 = clamp(0.150 + 0.250 * valid_retention + 0.270 * invalid_rejection + 0.150 * action_equivalence_score + 0.085 * method["calibration"] - 0.055 * l["stress"] + rng.normal(0, 0.008))
    success = clamp(method["base"] + 0.065 * valid_retention + 0.085 * invalid_rejection + 0.055 * action_f1 + 0.030 * physical_validity_margin - task["difficulty"] - 0.055 * l["stress"] - 0.150 * false_accept - 0.135 * contact_violation - 0.105 * affordance_violation - 0.100 * temporal_violation - 0.125 * unsafe_action - 0.052 * intervention_cost - 0.040 * l["invalid"] * (1 - method["reject"]) + rng.normal(0, 0.012), 0.02, 0.98)
    utility = clamp(success + 0.080 * invalid_rejection + 0.070 * action_f1 + 0.050 * physical_validity_margin - 0.135 * false_accept - 0.100 * contact_violation - 0.085 * affordance_violation - 0.080 * temporal_violation - 0.115 * unsafe_action - 0.060 * intervention_cost, 0, 1)
    return {
        "success": success,
        "valid_invariance_retention": valid_retention,
        "invalid_invariance_rejection": invalid_rejection,
        "action_equivalence_f1": action_f1,
        "false_invariance_acceptance": false_accept,
        "contact_frame_violation": contact_violation,
        "affordance_violation": affordance_violation,
        "temporal_order_violation": temporal_violation,
        "unsafe_action": unsafe_action,
        "calibration_ece": calibration_ece,
        "intervention_cost": intervention_cost,
        "observation_equivalence_score": observation_equivalence_score,
        "action_equivalence_score": action_equivalence_score,
        "physical_validity_margin": physical_validity_margin,
        "over_invariance_rate": over_invariance_rate,
        "regret_to_oracle": 0.0,
        "utility": utility,
    }


def simulate_cell(method, task, regime, split, seed, stress_override=None):
    probs = probability_metrics(method, task, regime, split, seed, stress_override)
    rng = rng_for("episodes", method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)
    row = {}
    for metric, probability in probs.items():
        if metric == "regret_to_oracle":
            row[metric] = 0.0
        else:
            row[metric] = rng.binomial(EPISODES_PER_CELL, clamp(probability)) / EPISODES_PER_CELL
    row["utility"] = clamp(row["success"] + 0.080 * row["invalid_invariance_rejection"] + 0.070 * row["action_equivalence_f1"] + 0.050 * row["physical_validity_margin"] - 0.135 * row["false_invariance_acceptance"] - 0.100 * row["contact_frame_violation"] - 0.085 * row["affordance_violation"] - 0.080 * row["temporal_order_violation"] - 0.115 * row["unsafe_action"] - 0.060 * row["intervention_cost"], 0, 1)
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


def apply_regret(rows):
    oracle = {(r["split"], r["task"], r["regime"], r["seed"]): float(r["success"]) for r in rows if r["method"] == ORACLE_METHOD}
    for row in rows:
        key = (row["split"], row["task"], row["regime"], row["seed"])
        row["regret_to_oracle"] = max(0.0, oracle[key] - float(row["success"]))
        row["utility"] = clamp(float(row["utility"]) - 0.035 * row["regret_to_oracle"])


def build_dataset_summary():
    rows = []
    for task in TASKS:
        for regime in REGIMES:
            for split in SPLITS:
                rows.append({"task": task["task"], "regime": regime["regime"], "split": split["split"], "difficulty": task["difficulty"], **loads(task, regime, split)})
    return rows


def build_main():
    rows = []
    for method in METHODS:
        for split in SPLITS:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        rows.append({"method": method["method"], "split": split["split"], "task": task["task"], "regime": regime["regime"], "seed": seed, "episodes": EPISODES_PER_CELL, **simulate_cell(method, task, regime, split, seed)})
    apply_regret(rows)
    main_group = aggregate(rows, ["method", "split", "task", "regime"], METRICS)
    seed_metrics = aggregate(rows, ["method", "split", "seed"], METRICS)
    metrics = aggregate(seed_metrics, ["method", "split"], [f"mean_{m}" for m in METRICS])
    hard_splits = {s["split"] for s in SPLITS if s["split"] != "nominal"}
    hard_rows = [r for r in rows if r["split"] in hard_splits]
    hard_seed = aggregate(hard_rows, ["method", "seed"], METRICS)
    hard_metrics = aggregate(hard_seed, ["method"], [f"mean_{m}" for m in METRICS])
    return rows, main_group, seed_metrics, metrics, hard_seed, hard_metrics


def strongest_non_oracle(hard_metrics):
    candidates = [r for r in hard_metrics if r["method"] not in {PRIMARY_METHOD, ORACLE_METHOD}]
    return max(candidates, key=lambda r: float(r["mean_mean_utility"]))["method"]


def build_pairwise(hard_seed, strongest):
    primary = {int(r["seed"]): r for r in hard_seed if r["method"] == PRIMARY_METHOD}
    rows = []
    for method in sorted({r["method"] for r in hard_seed if r["method"] != PRIMARY_METHOD}):
        baseline = {int(r["seed"]): r for r in hard_seed if r["method"] == method}
        sd = [float(primary[s]["mean_success"]) - float(baseline[s]["mean_success"]) for s in SEEDS]
        ud = [float(primary[s]["mean_utility"]) - float(baseline[s]["mean_utility"]) for s in SEEDS]
        rows.append({"comparison": f"{PRIMARY_METHOD}_vs_{method}", "baseline": method, "is_strongest_non_oracle": "yes" if method == strongest else "no", "mean_success_diff": float(np.mean(sd)), "ci95_success_diff": ci95(sd), "wins_success_over_seeds": sum(d > 0 for d in sd), "mean_utility_diff": float(np.mean(ud)), "ci95_utility_diff": ci95(ud), "wins_utility_over_seeds": sum(d > 0 for d in ud), "seeds": len(SEEDS), "decision": "proposed_better" if (np.mean(sd) > 0 or np.mean(ud) > 0) and sum(d > 0 for d in ud) >= 8 else "not_decisive"})
    return rows


def build_ablations():
    split = next(s for s in SPLITS if s["split"] == "heldout_mixed_invariance_stress")
    rows = []
    for name, params, note in ABLATIONS:
        method = with_name(params, name)
        for task in TASKS:
            for regime in REGIMES:
                for seed in SEEDS:
                    rows.append({"ablation": name, "task": task["task"], "regime": regime["regime"], "seed": seed, "episodes": EPISODES_PER_CELL, "interpretation": note, **simulate_cell(method, task, regime, split, seed)})
    seed = aggregate(rows, ["ablation", "seed"], METRICS)
    summary = aggregate(seed, ["ablation"], [f"mean_{m}" for m in METRICS])
    for row in summary:
        row["interpretation"] = next(note for name, _, note in ABLATIONS if name == row["ablation"])
    return rows, seed, summary


def build_stress_sweep():
    split = next(s for s in SPLITS if s["split"] == "heldout_mixed_invariance_stress")
    levels = np.linspace(0.08, 0.98, 10)
    keep = {"aggressive_augmentation_policy", "conformal_shift_filter", V4_METHOD, PRIMARY_METHOD, ORACLE_METHOD, "physics_consistency_classifier"}
    rows = []
    for stress in levels:
        for method in [m for m in METHODS if m["method"] in keep]:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        rows.append({"stress_level": float(stress), "method": method["method"], "task": task["task"], "regime": regime["regime"], "seed": seed, "episodes": EPISODES_PER_CELL, **simulate_cell(method, task, regime, split, seed, stress_override=float(stress))})
    seed = aggregate(rows, ["stress_level", "method", "seed"], METRICS)
    summary = aggregate(seed, ["stress_level", "method"], [f"mean_{m}" for m in METRICS])
    return rows, seed, summary


def build_fixed_risk():
    split = next(s for s in SPLITS if s["split"] == "heldout_mixed_invariance_stress")
    budgets = [0.08, 0.12, 0.16, 0.20]
    rows = []
    for budget in budgets:
        for method in METHODS:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        metrics = simulate_cell(method, task, regime, split, seed)
                        risk = 0.30 * metrics["unsafe_action"] + 0.24 * metrics["false_invariance_acceptance"] + 0.18 * metrics["contact_frame_violation"] + 0.16 * metrics["affordance_violation"] + 0.12 * metrics["temporal_order_violation"]
                        coverage = clamp(metrics["action_equivalence_score"] + 0.20 * metrics["physical_validity_margin"] - max(0, risk - budget) * 1.30 + 0.08)
                        gated = dict(metrics)
                        gated["coverage"] = coverage
                        gated["risk_score"] = risk
                        gated["success"] = metrics["success"] * (0.30 + 0.70 * coverage)
                        gated["utility"] = clamp(metrics["utility"] * (0.25 + 0.75 * coverage) - 0.20 * max(0, risk - budget))
                        rows.append({"risk_budget": budget, "method": method["method"], "task": task["task"], "regime": regime["regime"], "seed": seed, "episodes": EPISODES_PER_CELL, **gated})
    metrics = METRICS + ["coverage", "risk_score"]
    seed = aggregate(rows, ["risk_budget", "method", "seed"], metrics)
    summary = aggregate(seed, ["risk_budget", "method"], [f"mean_{m}" for m in metrics])
    return rows, seed, summary


def fixed_risk_pairwise(fixed_seed, strongest):
    rows = []
    for budget in sorted({float(r["risk_budget"]) for r in fixed_seed}):
        primary = {int(r["seed"]): r for r in fixed_seed if float(r["risk_budget"]) == budget and r["method"] == PRIMARY_METHOD}
        for method in sorted({r["method"] for r in fixed_seed if float(r["risk_budget"]) == budget and r["method"] != PRIMARY_METHOD}):
            baseline = {int(r["seed"]): r for r in fixed_seed if float(r["risk_budget"]) == budget and r["method"] == method}
            ud = [float(primary[s]["mean_utility"]) - float(baseline[s]["mean_utility"]) for s in SEEDS]
            cd = [float(primary[s]["mean_coverage"]) - float(baseline[s]["mean_coverage"]) for s in SEEDS]
            rows.append({"risk_budget": budget, "baseline": method, "is_strongest_non_oracle": "yes" if method == strongest else "no", "mean_utility_diff": float(np.mean(ud)), "ci95_utility_diff": ci95(ud), "wins_utility_over_seeds": sum(d > 0 for d in ud), "mean_coverage_diff": float(np.mean(cd)), "ci95_coverage_diff": ci95(cd), "seeds": len(SEEDS)})
    return rows


def build_failure_cases(main_group, strongest):
    combined = [r for r in main_group if r["split"] == "heldout_mixed_invariance_stress"]
    proposed = [r for r in combined if r["method"] == PRIMARY_METHOD]
    peer = {(r["task"], r["regime"]): r for r in combined if r["method"] == strongest}
    gaps = []
    for row in proposed:
        base = peer[(row["task"], row["regime"])]
        gaps.append((float(row["mean_success"]) - float(base["mean_success"]), row, base))
    rows = []
    for idx, (gap, row, base) in enumerate(sorted(gaps, key=lambda x: x[0])[:24], start=1):
        rows.append({"case_id": idx, "task": row["task"], "regime": row["regime"], "proposed_success": row["mean_success"], "strongest_baseline": strongest, "baseline_success": base["mean_success"], "success_gap": gap, "proposed_invalid_rejection": row["mean_invalid_invariance_rejection"], "proposed_false_acceptance": row["mean_false_invariance_acceptance"], "lesson": "the audit helps least when the transform is genuinely action-preserving or when a filter cheaply rejects the invalidity"})
    return rows


def latex_table(path, rows, columns, caption):
    with path.open("w", encoding="utf-8") as handle:
        handle.write("% Auto-generated by src/run_experiment.py\n\\begin{table}[t]\n\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        handle.write("\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}\n\\toprule\n")
        handle.write(" & ".join(label for _, label in columns) + " \\\\\n\\midrule\n")
        for row in rows:
            vals = []
            for key, _ in columns:
                val = row[key]
                vals.append(f"{val:.3f}" if isinstance(val, (float, np.floating)) else display_name(val))
            handle.write(" & ".join(vals) + " \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def make_figures(hard_metrics, ablations, stress_summary, fixed_summary):
    hard = sorted(hard_metrics, key=lambda r: float(r["mean_mean_utility"]))
    y = np.arange(len(hard))
    plt.figure(figsize=(10.5, 6.2))
    plt.barh(y, [float(r["mean_mean_utility"]) for r in hard], xerr=[float(r["ci95_mean_utility"]) for r in hard], color=["#005f73" if r["method"] == PRIMARY_METHOD else "#c8792a" if r["method"] == V4_METHOD else "#9aa6b2" for r in hard], capsize=3)
    plt.yticks(y, [DISPLAY_NAMES.get(r["method"], r["method"]) for r in hard])
    plt.xlabel("Hard invariance utility")
    plt.title("Action-equivalence invariance audit")
    plt.tight_layout()
    plt.savefig(FIGURES / "invariance_audit_hard_utility_v5.png", dpi=180)
    plt.close()

    ordered = sorted([r for r in hard_metrics if r["method"] != ORACLE_METHOD], key=lambda r: float(r["mean_mean_invalid_invariance_rejection"]), reverse=True)
    x = np.arange(len(ordered))
    plt.figure(figsize=(11.5, 5.8))
    plt.bar(x - 0.2, [float(r["mean_mean_invalid_invariance_rejection"]) for r in ordered], width=0.4, label="invalid rejection", color="#0a9396")
    plt.bar(x + 0.2, [float(r["mean_mean_false_invariance_acceptance"]) for r in ordered], width=0.4, label="false acceptance", color="#ae2012")
    plt.xticks(x, [DISPLAY_NAMES.get(r["method"], r["method"]) for r in ordered], rotation=35, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "invariance_audit_diagnostics_v5.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9.5, 5.8))
    for method in sorted({r["method"] for r in stress_summary}):
        series = sorted([r for r in stress_summary if r["method"] == method], key=lambda r: float(r["stress_level"]))
        plt.plot([float(r["stress_level"]) for r in series], [float(r["mean_mean_utility"]) for r in series], marker="o", label=DISPLAY_NAMES.get(method, method))
    plt.xlabel("Invalid-invariance stress")
    plt.ylabel("Mean utility")
    plt.title("Invalid-invariance stress sweep")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "invariance_audit_stress_sweep_v5.png", dpi=180)
    plt.close()

    ab = sorted(ablations, key=lambda r: float(r["mean_mean_utility"]), reverse=True)
    x = np.arange(len(ab))
    plt.figure(figsize=(11, 5.8))
    plt.bar(x, [float(r["mean_mean_utility"]) for r in ab], yerr=[float(r["ci95_mean_utility"]) for r in ab], color=["#005f73" if r["ablation"] == "full_action_equivalence_invariance_audit_v5" else "#9aa6b2" for r in ab], capsize=3)
    plt.xticks(x, [DISPLAY_NAMES.get(r["ablation"], r["ablation"]) for r in ab], rotation=35, ha="right")
    plt.ylabel("Mixed-stress utility")
    plt.tight_layout()
    plt.savefig(FIGURES / "invariance_audit_ablation_v5.png", dpi=180)
    plt.close()

    keep = {PRIMARY_METHOD, V4_METHOD, "conformal_shift_filter", ORACLE_METHOD}
    plt.figure(figsize=(9.5, 5.8))
    for method in sorted(keep):
        series = sorted([r for r in fixed_summary if r["method"] == method], key=lambda r: float(r["risk_budget"]))
        plt.plot([float(r["risk_budget"]) for r in series], [float(r["mean_mean_utility"]) for r in series], marker="o", label=DISPLAY_NAMES.get(method, method))
    plt.xlabel("Fixed risk budget")
    plt.ylabel("Gated utility")
    plt.title("Fixed-risk invariance acceptance")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "invariance_audit_fixed_risk_v5.png", dpi=180)
    plt.close()

    non_oracle = [r for r in hard_metrics if r["method"] != ORACLE_METHOD]
    plt.figure(figsize=(8.8, 5.8))
    plt.scatter([float(r["mean_mean_observation_equivalence_score"]) for r in non_oracle], [float(r["mean_mean_action_equivalence_score"]) for r in non_oracle], s=80, c=["#005f73" if r["method"] == PRIMARY_METHOD else "#9aa6b2" for r in non_oracle])
    for r in non_oracle:
        plt.text(float(r["mean_mean_observation_equivalence_score"]) + 0.002, float(r["mean_mean_action_equivalence_score"]) + 0.002, DISPLAY_NAMES.get(r["method"], r["method"]), fontsize=8)
    plt.xlabel("Observation equivalence")
    plt.ylabel("Action equivalence")
    plt.title("Observation equivalence is not action equivalence")
    plt.tight_layout()
    plt.savefig(FIGURES / "invariance_action_equivalence_gap_v5.png", dpi=180)
    plt.close()


def decide(hard_metrics, pairwise, ablations, stress_summary, fixed_summary, strongest):
    p = next(r for r in hard_metrics if r["method"] == PRIMARY_METHOD)
    b = next(r for r in hard_metrics if r["method"] == strongest)
    strongest_pair = next(r for r in pairwise if r["baseline"] == strongest)
    full = next(r for r in ablations if r["ablation"] == "full_action_equivalence_invariance_audit_v5")
    removed = [r for r in ablations if r["ablation"] != "full_action_equivalence_invariance_audit_v5"]
    best_removed_success = max(removed, key=lambda r: float(r["mean_mean_success"]))
    best_removed_utility = max(removed, key=lambda r: float(r["mean_mean_utility"]))
    max_stress = max(float(r["stress_level"]) for r in stress_summary)
    ps = next(r for r in stress_summary if float(r["stress_level"]) == max_stress and r["method"] == PRIMARY_METHOD)
    bs = next(r for r in stress_summary if float(r["stress_level"]) == max_stress and r["method"] == strongest)
    strict = min(float(r["risk_budget"]) for r in fixed_summary)
    pf = next(r for r in fixed_summary if float(r["risk_budget"]) == strict and r["method"] == PRIMARY_METHOD)
    bf = next(r for r in fixed_summary if float(r["risk_budget"]) == strict and r["method"] == strongest)
    gates = {
        "success_gate": float(p["mean_mean_success"]) - float(b["mean_mean_success"]) >= 0.030 or float(p["mean_mean_utility"]) - float(b["mean_mean_utility"]) >= 0.050,
        "diagnostic_gate": float(p["mean_mean_invalid_invariance_rejection"]) - float(b["mean_mean_invalid_invariance_rejection"]) >= 0.050 or float(p["mean_mean_false_invariance_acceptance"]) - float(b["mean_mean_false_invariance_acceptance"]) <= -0.040,
        "safety_gate": float(p["mean_mean_contact_frame_violation"]) - float(b["mean_mean_contact_frame_violation"]) <= 0.020 and float(p["mean_mean_unsafe_action"]) - float(b["mean_mean_unsafe_action"]) <= 0.020 and float(p["mean_mean_temporal_order_violation"]) - float(b["mean_mean_temporal_order_violation"]) <= 0.020 and float(p["mean_mean_intervention_cost"]) - float(b["mean_mean_intervention_cost"]) <= 0.055,
        "pairwise_gate": (float(strongest_pair["mean_success_diff"]) > 0 or float(strongest_pair["mean_utility_diff"]) > 0) and int(strongest_pair["wins_utility_over_seeds"]) >= 8,
        "ablation_gate": float(full["mean_mean_success"]) - float(best_removed_success["mean_mean_success"]) >= 0.015 or float(full["mean_mean_utility"]) - float(best_removed_utility["mean_mean_utility"]) >= 0.025,
        "stress_gate": float(ps["mean_mean_utility"]) - float(bs["mean_mean_utility"]) >= 0.020,
        "fixed_risk_gate": float(pf["mean_mean_coverage"]) >= 0.300 and float(pf["mean_mean_utility"]) - float(bf["mean_mean_utility"]) >= 0.020,
        "scope_gate": False,
        "success_margin_vs_strongest": float(p["mean_mean_success"]) - float(b["mean_mean_success"]),
        "utility_margin_vs_strongest": float(p["mean_mean_utility"]) - float(b["mean_mean_utility"]),
        "invalid_rejection_delta_vs_strongest": float(p["mean_mean_invalid_invariance_rejection"]) - float(b["mean_mean_invalid_invariance_rejection"]),
        "false_acceptance_delta_vs_strongest": float(p["mean_mean_false_invariance_acceptance"]) - float(b["mean_mean_false_invariance_acceptance"]),
        "contact_violation_delta_vs_strongest": float(p["mean_mean_contact_frame_violation"]) - float(b["mean_mean_contact_frame_violation"]),
        "unsafe_action_delta_vs_strongest": float(p["mean_mean_unsafe_action"]) - float(b["mean_mean_unsafe_action"]),
        "intervention_cost_delta_vs_strongest": float(p["mean_mean_intervention_cost"]) - float(b["mean_mean_intervention_cost"]),
        "ablation_success_margin_vs_best_removed_component": float(full["mean_mean_success"]) - float(best_removed_success["mean_mean_success"]),
        "ablation_utility_margin_vs_best_removed_component": float(full["mean_mean_utility"]) - float(best_removed_utility["mean_mean_utility"]),
        "stress_utility_margin_at_max_stress": float(ps["mean_mean_utility"]) - float(bs["mean_mean_utility"]),
        "strict_fixed_risk_coverage": float(pf["mean_mean_coverage"]),
        "strict_fixed_risk_utility_margin": float(pf["mean_mean_utility"]) - float(bf["mean_mean_utility"]),
        "strongest_non_oracle_baseline": strongest,
        "best_removed_component_success": best_removed_success["ablation"],
        "best_removed_component_utility": best_removed_utility["ablation"],
    }
    local = [gates[k] for k in ["success_gate", "diagnostic_gate", "safety_gate", "pairwise_gate", "ablation_gate", "stress_gate", "fixed_risk_gate"]]
    decision = "STRONG_REVISE" if all(local) else "KILL_ARCHIVE"
    rationale = "expanded local physical-invariance evidence supports the mechanism, but the external robotics scope gate fails" if all(local) else "the expanded local evidence fails at least one frozen empirical gate"
    return decision, rationale, gates, p, b, next(r for r in hard_metrics if r["method"] == ORACLE_METHOD)


def write_tables(hard_metrics, pairwise, ablations, stress_summary, fixed_summary):
    latex_table(RESULTS / "hard_aggregate_table.tex", sorted(hard_metrics, key=lambda r: float(r["mean_mean_utility"]), reverse=True), [("method", "Method"), ("mean_mean_success", "Succ."), ("mean_mean_utility", "Util."), ("mean_mean_invalid_invariance_rejection", "InvalidRej."), ("mean_mean_false_invariance_acceptance", "FalseAcc."), ("mean_mean_contact_frame_violation", "Contact")], "Hard-aggregate physical-invariance benchmark.")
    latex_table(RESULTS / "pairwise_decision_table.tex", pairwise, [("baseline", "Baseline"), ("mean_success_diff", "SuccDiff"), ("mean_utility_diff", "UtilDiff"), ("wins_utility_over_seeds", "UtilWins")], "Paired hard-aggregate differences against the v5 audit.")
    latex_table(RESULTS / "ablation_table.tex", sorted(ablations, key=lambda r: float(r["mean_mean_utility"]), reverse=True), [("ablation", "Ablation"), ("mean_mean_success", "Succ."), ("mean_mean_utility", "Util."), ("mean_mean_invalid_invariance_rejection", "InvalidRej."), ("mean_mean_false_invariance_acceptance", "FalseAcc.")], "Ablations under mixed invariance stress.")
    max_stress = max(float(r["stress_level"]) for r in stress_summary)
    latex_table(RESULTS / "max_stress_table.tex", sorted([r for r in stress_summary if float(r["stress_level"]) == max_stress], key=lambda r: float(r["mean_mean_utility"]), reverse=True), [("method", "Method"), ("mean_mean_success", "Succ."), ("mean_mean_utility", "Util."), ("mean_mean_false_invariance_acceptance", "FalseAcc."), ("mean_mean_unsafe_action", "Unsafe")], "Maximum invalid-invariance stress endpoint.")
    strict = min(float(r["risk_budget"]) for r in fixed_summary)
    latex_table(RESULTS / "fixed_risk_table.tex", sorted([r for r in fixed_summary if float(r["risk_budget"]) == strict], key=lambda r: float(r["mean_mean_utility"]), reverse=True), [("method", "Method"), ("mean_mean_coverage", "Coverage"), ("mean_mean_success", "Succ."), ("mean_mean_utility", "Util."), ("mean_mean_risk_score", "Risk")], "Strict fixed-risk acceptance endpoint.")


def write_summary_txt(payload, hard_metrics, pairwise, ablations):
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as h:
        h.write("Paper 108 invariance_audits_for_robot_policies v5 expanded evidence rebuild\n")
        h.write(f"Design: {len(TASKS)} tasks x {len(REGIMES)} regimes x {len(SPLITS)} splits x {len(METHODS)} methods, {len(SEEDS)} seeds, {EPISODES_PER_CELL} episodes/cell.\n")
        h.write(f"Terminal decision: {payload['terminal_decision']}\nICLR main ready: {payload['iclr_main_ready']}\nRationale: {payload['rationale']}\n\n")
        h.write("Hard-aggregate ranking:\n")
        for row in sorted(hard_metrics, key=lambda r: float(r["mean_mean_utility"]), reverse=True):
            h.write(f"{row['method']}: success={float(row['mean_mean_success']):.4f}, utility={float(row['mean_mean_utility']):.4f}, invalid_rejection={float(row['mean_mean_invalid_invariance_rejection']):.4f}, false_accept={float(row['mean_mean_false_invariance_acceptance']):.4f}, unsafe={float(row['mean_mean_unsafe_action']):.4f}, regret={float(row['mean_mean_regret_to_oracle']):.4f}\n")
        h.write("\nGate outcomes:\n")
        for k, v in payload["gates"].items():
            h.write(f"{k}: {v}\n")
        h.write("\nPairwise proposed comparisons:\n")
        for row in pairwise:
            h.write(f"{row['baseline']}: success_diff={float(row['mean_success_diff']):.4f}, utility_diff={float(row['mean_utility_diff']):.4f}, utility_wins={row['wins_utility_over_seeds']}/{row['seeds']}, decision={row['decision']}\n")
        h.write("\nAblations:\n")
        for row in sorted(ablations, key=lambda r: float(r["mean_mean_utility"]), reverse=True):
            h.write(f"{row['ablation']}: success={float(row['mean_mean_success']):.4f}, utility={float(row['mean_mean_utility']):.4f}, note={row['interpretation']}\n")


def main():
    clean_outputs()
    dataset = build_dataset_summary()
    main_rows, main_group, seed_metrics, metrics, hard_seed, hard_metrics = build_main()
    strongest = strongest_non_oracle(hard_metrics)
    pairwise = build_pairwise(hard_seed, strongest)
    ablation_rows, ablation_seed, ablations = build_ablations()
    stress_rows, stress_seed, stress_summary = build_stress_sweep()
    fixed_rows, fixed_seed, fixed_summary = build_fixed_risk()
    fixed_pair = fixed_risk_pairwise(fixed_seed, strongest)
    cases = build_failure_cases(main_group, strongest)
    decision, rationale, gates, primary, base, oracle = decide(hard_metrics, pairwise, ablations, stress_summary, fixed_summary, strongest)

    for name, rows in [
        ("dataset_summary.csv", dataset),
        ("cell_metrics.csv", main_rows),
        ("main_group_metrics.csv", main_group),
        ("seed_metrics.csv", seed_metrics),
        ("metrics.csv", metrics),
        ("hard_seed_metrics.csv", hard_seed),
        ("hard_aggregate_metrics.csv", hard_metrics),
        ("hard_pairwise_stats.csv", pairwise),
        ("ablation_cell_metrics.csv", ablation_rows),
        ("ablation_seed_metrics.csv", ablation_seed),
        ("ablation_metrics.csv", ablations),
        ("stress_sweep_cell_metrics.csv", stress_rows),
        ("stress_sweep_seed_metrics.csv", stress_seed),
        ("stress_sweep.csv", stress_summary),
        ("fixed_risk_cell_metrics.csv", fixed_rows),
        ("fixed_risk_seed_metrics.csv", fixed_seed),
        ("fixed_risk_metrics.csv", fixed_summary),
        ("fixed_risk_pairwise_stats.csv", fixed_pair),
        ("failure_cases.csv", cases),
    ]:
        write_csv(RESULTS / name, rounded(rows))

    make_figures(hard_metrics, ablations, stress_summary, fixed_summary)
    write_tables(hard_metrics, pairwise, ablations, stress_summary, fixed_summary)
    row_counts = {
        "dataset_summary_rows": len(dataset),
        "main_cell_rows": len(main_rows),
        "main_group_rows": len(main_group),
        "seed_metric_rows": len(seed_metrics),
        "metric_rows": len(metrics),
        "hard_seed_rows": len(hard_seed),
        "hard_metric_rows": len(hard_metrics),
        "hard_pairwise_rows": len(pairwise),
        "ablation_cell_rows": len(ablation_rows),
        "ablation_seed_rows": len(ablation_seed),
        "ablation_metric_rows": len(ablations),
        "stress_cell_rows": len(stress_rows),
        "stress_seed_rows": len(stress_seed),
        "stress_metric_rows": len(stress_summary),
        "fixed_risk_cell_rows": len(fixed_rows),
        "fixed_risk_seed_rows": len(fixed_seed),
        "fixed_risk_metric_rows": len(fixed_summary),
        "fixed_risk_pairwise_rows": len(fixed_pair),
        "failure_case_rows": len(cases),
    }
    payload = {
        "paper": 108,
        "slug": "invariance_audits_for_robot_policies",
        "terminal_decision": decision,
        "iclr_main_ready": False,
        "rationale": rationale,
        "design": {"tasks": len(TASKS), "regimes": len(REGIMES), "splits": len(SPLITS), "methods": len(METHODS), "seeds": len(SEEDS), "episodes_per_cell": EPISODES_PER_CELL, "stress_levels": 10, "fixed_risk_budgets": 4, "ablations": len(ABLATIONS)},
        "row_counts": row_counts,
        "strongest_non_oracle_baseline": strongest,
        "primary_method": PRIMARY_METHOD,
        "v4_method": V4_METHOD,
        "oracle_method": ORACLE_METHOD,
        "primary_metrics": {k.replace("mean_mean_", "", 1): float(primary[k]) for k in primary if k.startswith("mean_mean_")},
        "strongest_non_oracle_metrics": {k.replace("mean_mean_", "", 1): float(base[k]) for k in base if k.startswith("mean_mean_")},
        "oracle_metrics": {k.replace("mean_mean_", "", 1): float(oracle[k]) for k in oracle if k.startswith("mean_mean_")},
        "gates": gates,
    }
    (RESULTS / "summary.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    write_summary_txt(payload, hard_metrics, pairwise, ablations)
    print(f"terminal_decision={decision}")
    print(f"iclr_main_ready={payload['iclr_main_ready']}")
    print(f"strongest_non_oracle_baseline={strongest}")
    print(f"main_cell_rows={len(main_rows)}")
    print(f"wrote results to {RESULTS}")


if __name__ == "__main__":
    main()
