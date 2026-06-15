# Final Audit

1. Chosen thesis: robot-policy invariances must be audited for physical validity before deployment.
2. ICLR-main decision: STRONG_REVISE.
3. Submission-hardening version: v4.
4. Evidence: 5 tasks x 7 invariance regimes x 5 splits x 9 methods, 7 seeds, 84 episodes/group.
5. Strongest non-oracle baseline: `conformal_shift_filter`.
6. Main result: proposed combined-invariance success `0.685 +/- 0.008` vs strongest non-oracle `0.612 +/- 0.006`.
7. Diagnostic result: invalid-invariance rejection `0.619` vs `0.476`; false-invariance acceptance `0.076` vs `0.123`.
8. Safety result: contact violation `0.044` vs `0.060`; unsafe action `0.039` vs `0.055`; intervention cost `0.220` vs `0.238`.
9. Ablation result: full model `0.684 +/- 0.006`; best removed component `minus_conservatism_calibration` at `0.654 +/- 0.006`.
10. Pairwise result: proposed beats the strongest non-oracle baseline in 7/7 seeds with `0.073 +/- 0.010` mean success difference.
11. Claim-validity status: mechanism supported locally; not submission-ready without external robot/high-fidelity validation.
12. Exact Downloads PDF path: `C:/Users/wangz/Downloads/108.pdf`.
13. GitHub URL: https://github.com/Jason-Wang313/108_invariance_audits_for_robot_policies
14. Confirmation: no visible Desktop copy was requested or made.
