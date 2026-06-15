# Reproducibility Checklist

## What Reproduces

- [x] `python src/run_experiment.py`
- [x] `python -m py_compile src/run_experiment.py`
- [x] `results/seed_task_regime_metrics.csv`
- [x] `results/per_task_regime_metrics.csv`
- [x] `results/seed_split_metrics.csv`
- [x] `results/metrics.csv`
- [x] `results/pairwise_stats.csv`
- [x] `results/ablation_metrics.csv`
- [x] `results/stress_sweep.csv`
- [x] `results/failure_cases.csv`
- [x] `figures/invariance_audit_combined_success.png`
- [x] `figures/invariance_audit_diagnostics.png`
- [x] `figures/invariance_audit_stress_sweep.png`
- [x] `figures/invariance_audit_ablation.png`
- [x] `figures/invariance_audit_contact_regret.png`
- [x] `paper/main.tex`
- [x] Canonical PDF: `C:/Users/wangz/Downloads/108.pdf`

## What Does Not Yet Reproduce

- [ ] Real robot results.
- [ ] Independent high-fidelity benchmark runs.
- [ ] Trained learned policy checkpoints.
- [ ] External robot-system baselines.

This is reproducible as a local evidence rebuild and strong-revise paper scaffold, not as a final ICLR-main empirical robotics submission.
