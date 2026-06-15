# Submission Readiness Audit v4.1

Paper: 108 `invariance_audits_for_robot_policies`

Audit date: 2026-06-15 17:32:12 +0100

Decision: STRONG_REVISE

ICLR main ready: no

## Regenerated Evidence

- Runner: `src/run_experiment.py`
- Rerun log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/108_invariance_audits_for_robot_policies_continuation_rerun_20260615.log`
- Benchmark coverage: 5 tasks x 7 invariance regimes x 5 splits x 9 methods.
- Repeats: 7 seeds, 84 episodes per task/regime/split/method group.
- Strongest non-oracle baseline: `conformal_shift_filter`.
- Terminal decision emitted by runner: `STRONG_REVISE`.

## CSV Integrity

- `metrics.csv`: 45 rows, finite numeric fields.
- `per_task_regime_metrics.csv`: 1575 rows, finite numeric fields.
- `seed_task_regime_metrics.csv`: 11025 rows, finite numeric fields.
- `seed_split_metrics.csv`: 315 rows, finite numeric fields.
- `pairwise_stats.csv`: 8 rows, finite numeric fields.
- `ablation_metrics.csv`: 7 rows, finite numeric fields.
- `ablation_seed_metrics.csv`: 49 rows, finite numeric fields.
- `ablation_task_regime_seed_metrics.csv`: 1715 rows, finite numeric fields.
- `stress_sweep.csv`: 30 rows, finite numeric fields.
- `stress_sweep_seed_metrics.csv`: 7350 rows, finite numeric fields.
- `failure_cases.csv`: 8 rows, finite numeric fields.

## Main Result

On combined-invariance stress, proposed physical-invariance auditing reaches `0.685 +/- 0.008` success versus `0.612 +/- 0.006` for `conformal_shift_filter`, a margin of `+0.073 +/- 0.010`. Proposed also improves valid-invariance retention from `0.454` to `0.588`, improves invalid-invariance rejection from `0.476` to `0.619`, reduces false-invariance acceptance from `0.123` to `0.076`, reduces contact violation from `0.060` to `0.044`, reduces unsafe action from `0.056` to `0.039`, and reduces intervention cost from `0.238` to `0.220`.

## Pairwise And Ablations

- Pairwise seed test against the strongest non-oracle baseline: `7/7` wins.
- Full ablation success: `0.684 +/- 0.006`.
- Best removed component: `minus_conservatism_calibration` at `0.654 +/- 0.006`.
- Ablation margin over best removed component: `+0.030`.

## Stress Sweep

Stress levels: `0.10`, `0.27`, `0.44`, `0.61`, `0.78`, `0.95`.

At maximum stress level `0.95`, proposed success is `0.679 +/- 0.007` versus `0.594 +/- 0.007` for the strongest non-oracle baseline and `0.783 +/- 0.006` for the oracle. Proposed also keeps higher valid-invariance retention (`0.579` vs `0.444`), higher invalid-invariance rejection (`0.619` vs `0.479`), lower false-invariance acceptance (`0.078` vs `0.123`), lower contact violation (`0.043` vs `0.057`), and lower unsafe action (`0.039` vs `0.054`) than the strongest non-oracle baseline.

## Honest Submission Decision

The local evidence supports the mechanism and justifies continuing the project, but it does not make the paper ICLR-main-ready. A real submission needs real robot or independent high-fidelity simulator validation, external learned baselines, qualitative rollouts, and a stronger prior-work positioning section grounded in those external results.
