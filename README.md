# 108 Invariance Audits for Robot Policies

Submission-hardening version: v5 expanded rebuild

Terminal decision: STRONG_REVISE for an ICLR-main-target paper, not ready-to-submit.

Canonical PDF: `C:/Users/wangz/Downloads/108.pdf`

Public GitHub: `https://github.com/Jason-Wang313/108_invariance_audits_for_robot_policies`

## What Changed

Paper 108 was rebuilt from the short v4.1 diagnostic into a 25-page ICLR-style v5 artifact. The core claim is narrow: robot-policy invariances must be audited for physical action equivalence because lighting or viewpoint shifts can preserve the correct action while mirror-handed contact, material/friction swaps, tool-affordance swaps, support-surface changes, and temporal-order reversals can invalidate it.

The rebuild expands the frozen local benchmark to 8 task families, 10 transformation regimes, 8 splits, 16 methods, 10 seeds, and 6 episodes per cell. It writes all CSVs, tables, figures, `summary.json`, and the manuscript from source.

## Frozen Evidence

The proposed `action_equivalence_invariance_audit_v5` reaches:

- hard success: `0.7860` versus `0.7379` for the strongest non-oracle baseline `proposed_physical_invariance_audit_v4`
- hard utility: `0.8785` versus `0.8211`
- invalid-invariance rejection: `0.8067` versus `0.7361`
- false-invariance acceptance: `0.0390` versus `0.0650`
- contact-frame violation: `0.0189` versus `0.0307`
- unsafe action: `0.0157` versus `0.0313`
- strict fixed-risk coverage: `0.8707`

All local empirical gates pass: success, diagnostic, safety, pairwise, ablation, stress, and fixed-risk. The scope gate fails because this repository still lacks real robot validation, an accepted high-fidelity benchmark, external benchmark split, calibrated deployment logs, trained checkpoints, and rollout videos.

## Row Counts

- main cells: `102400`
- main group rows: `10240`
- seed metric rows: `1280`
- stress cells: `48000`
- fixed-risk cells: `51200`
- ablation cells: `8000`
- failure cases: `24`

## Reproduce

```powershell
python src\run_experiment.py
python scripts\generate_manuscript.py
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
cd ..
Copy-Item -LiteralPath .\paper\main.pdf -Destination "$env:USERPROFILE\Downloads\108.pdf" -Force
python scripts\validate_submission_artifacts.py
```

Validated final PDF SHA256:

`BDBD2E84747B74FFB8C0C70B22F7B04D88C6E855AA155D49E799984D4B582EA4`

The validator enforces row counts, finite CSV values, local gate status, explicit scope failure, bright boxed citation settings, 25+ pages, hash equality between `paper/main.pdf` and `Downloads/108.pdf`, and absence of numbered PDFs on the visible Desktop or repo roots.
