# ICLR Main Gate

Paper: 108 invariance_audits_for_robot_policies

Previous v3 decision: KILL_ARCHIVE

v4 gate verdict: STRONG_REVISE

Evidence digest: physical-invariance audit benchmark with 5 tasks, 7 regimes, 5 splits, 9 methods, 7 seeds, 84 episodes/group.

Gate outcomes:

- success gate: pass, proposed beats strongest non-oracle by `0.073` success.
- diagnostic gate: pass, invalid-invariance rejection improves by `0.144`.
- safety gate: pass, contact violation, unsafe action, and intervention cost fall relative to strongest non-oracle.
- pairwise gate: pass, proposed wins 7/7 paired seeds against strongest non-oracle.
- ablation gate: pass, full model beats the best removed component by `0.030`.
- external-validation gate: fail, no real robot or independent high-fidelity benchmark.

The only honest main-conference-safe decision is STRONG_REVISE: the mechanism is worth developing, but the paper is not yet submission-ready.
