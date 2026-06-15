# 108 Invariance Audits for Robot Policies

Submission-hardening version: v4

Terminal decision: STRONG_REVISE for an ICLR-main-target paper, not ready-to-submit.

This rebuild replaces the v3 archive with a paper-specific physical-invariance audit benchmark. The central claim is narrow: robot-policy invariances must be audited for physical validity, because lighting or viewpoint changes can preserve the correct action while mirror-handed contact, friction swaps, tool-affordance swaps, or temporal-order reversals can erase necessary distinctions.

The local evidence supports the mechanism. On combined invariance stress, `proposed_physical_invariance_audit` reaches `0.685 +/- 0.008` success versus `0.612 +/- 0.006` for the strongest non-oracle baseline, `conformal_shift_filter`. Invalid-invariance rejection improves from `0.476` to `0.619`; false-invariance acceptance falls from `0.123` to `0.076`; contact violation falls from `0.060` to `0.044`; and paired seed comparisons favor the proposed method in 7/7 seeds.

The honest limitation is still material: this is a local executable diagnostic benchmark, not real robot or independently validated high-fidelity simulator evidence. The paper should be revised with external robot validation before main-track submission.

## Reproduce Evidence

```powershell
python src\run_experiment.py
```

Generated artifacts:

- `results/metrics.csv`
- `results/pairwise_stats.csv`
- `results/ablation_metrics.csv`
- `results/stress_sweep.csv`
- `results/failure_cases.csv`
- `figures/invariance_audit_*.png`
- `paper/main.tex`

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/108.pdf`
