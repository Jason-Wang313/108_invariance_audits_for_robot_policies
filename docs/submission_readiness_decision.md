# Submission Readiness Decision

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

The v4 rebuild provides a paper-specific local benchmark for physical invariance audits in robot policies, with strong synthetic baselines, ablations, paired seed comparisons, stress sweeps, failure cases, finite CSV artifacts, and generated figures/tables. The evidence supports the mechanism: on combined invariance stress, `proposed_physical_invariance_audit` reaches `0.685 +/- 0.008` success versus `0.612 +/- 0.006` for the strongest non-oracle baseline, `conformal_shift_filter`.

Diagnostic evidence also supports the mechanism. Invalid-invariance rejection improves from `0.476` to `0.619`; false-invariance acceptance falls from `0.123` to `0.076`; contact violation falls from `0.060` to `0.044`; unsafe action falls from `0.055` to `0.039`; and paired seed comparisons favor the proposed method over the strongest baseline in 7/7 seeds.

The honest terminal action is strong-revise, not submit. A submission-quality revival still requires real robot or independent high-fidelity simulator validation, implemented learned baselines, and external benchmark evidence.
