# Submission Version Log

## v1 - Generated Draft

- Original continuation-batch generated paper and toy single-seed experiment.

## v2 - Submission Hardening

- Added hostile reviewer attack log and response docs.
- Added multi-seed synthetic diagnostics.
- Terminal decision: WORKSHOP_ONLY.

## v3 - ICLR Main Gate Archive

- Applied stricter ICLR-main-conference standard.
- Determined that missing real-robot/high-fidelity evidence, template-generated experiments, and unresolved novelty threats were not recoverable from local artifacts.
- Terminal decision: KILL_ARCHIVE.

## v4 - Paper-Specific Evidence Rebuild

- Replaced the shared template script with a physical-invariance audit benchmark.
- Added 5 tasks, 7 invariance regimes, 5 splits, 9 methods, 7 seeds, and 84 episodes/group.
- Added success, valid-invariance retention, invalid-invariance rejection, task-equivalence F1, false-invariance acceptance, contact violation, unsafe action, calibration ECE, intervention cost, regret, paired tests, ablations, stress sweeps, failure cases, figures, and LaTeX tables.
- Rewrote docs and manuscript around the actual evidence.
- Terminal decision: STRONG_REVISE.

## v4.1 - Continuation Submission Audit

- Added `docs/paper108_iclr_submission_execution_plan_20260615.md`.
- Reran `src/run_experiment.py` from source with the full benchmark and logged the run at `logs/108_invariance_audits_for_robot_policies_continuation_rerun_20260615.log`.
- Verified expected CSV coverage and finite numeric outputs.
- Reconfirmed the strongest non-oracle baseline as `conformal_shift_filter`.
- Preserved the narrow claim that robot-policy invariances need physical-validity auditing, not that invariance learning is generally bad.
- Added terminal audit docs and rebuilt the numbered Downloads PDF.
- Terminal decision: STRONG_REVISE; ICLR main ready: no.
