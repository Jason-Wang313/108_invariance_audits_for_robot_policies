# Paper 108 Rebuild Plan: Invariance Audits for Robot Policies

Started: 2026-06-15 01:05:00 +0100

## Goal

Rebuild Paper 108 from a v3 archive into an honest ICLR-main-target evidence package if, and only if, the evidence supports it. The falsifiable claim is that robot-policy invariances must be audited for physical validity: some transformations preserve the correct action, while others erase distinctions that matter for contact, safety, affordance, or temporal order.

## Claimed Mechanism

The proposed method, `proposed_physical_invariance_audit`, separates:

- valid perceptual invariances such as lighting, mild viewpoint, background, and texture changes;
- valid geometric equivariances such as object-frame translation or rotation when the task symmetry truly holds;
- invalid invariances such as mirror-handed contact, reversed force direction, changed friction/material, tool-affordance swaps, support-surface changes, and temporal-order swaps;
- audit actions that decide whether to preserve, weaken, or reject an invariance before policy deployment.

It should preserve useful invariances while rejecting invariances that collapse physically necessary distinctions.

## Benchmark To Build

Create a RAM-light executable benchmark with aggregate metrics rather than full trajectory storage. The benchmark will cover:

- 5 task families: peg insertion, drawer opening, cable routing, tool use, and mobile pick-and-place.
- 7 invariance stress regimes: lighting/background shift, camera viewpoint shift, SE(2) pose transform, mirror-handed contact, material/friction swap, tool-affordance swap, and temporal-order reversal.
- 5 evaluation splits: nominal, valid-perceptual shift, valid-geometric shift, invalid-physical shift, and combined invariance stress.
- 9 methods: no-invariance behavior clone, aggressive augmentation policy, equivariant policy, domain randomization, invariant risk minimization proxy, contrastive invariance learner, conformal shift filter, proposed physical-invariance audit, and oracle invariance-validity supervisor.
- 7 random seeds with independent task/regime groups.
- 84 episodes per task/regime/split/method group.

## Evidence Requirements

The rebuild must produce:

- Task success, valid-invariance retention, invalid-invariance rejection, task-equivalence F1, false-invariance acceptance, contact violation, unsafe action, calibration ECE, intervention cost, data-efficiency proxy, and regret to oracle.
- Per-task/per-regime breakdowns.
- Pairwise seed-level tests against the strongest non-oracle baseline.
- Stress sweep over invalid-invariance intensity.
- Ablations for physical-validity classifier, contact-frame test, affordance-consistency check, temporal-order check, and conservatism calibration.
- Failure cases showing where augmentation or equivariance is sufficient, where the audit is too conservative, and where invalid invariance causes silent failure.
- Figures and LaTeX tables generated from CSVs.

## Terminal Gate

Mark `STRONG_REVISE` only if the proposed method:

- Beats the strongest non-oracle closed-loop baseline on combined invariance stress by at least 0.030 success.
- Improves invalid-invariance rejection by at least 0.050 or reduces false-invariance acceptance by at least 0.050.
- Does not buy success by increasing contact violations, unsafe actions, or intervention cost beyond the configured tolerance.
- Wins paired seed comparisons against the strongest non-oracle baseline in at least 5/7 seeds.
- Survives core ablations: removing physical-validity classification, contact-frame testing, affordance-consistency checking, temporal-order checking, or conservatism calibration must not match the full method.
- States clearly that real robot/external benchmark validation is still missing.

Otherwise mark `KILL_ARCHIVE` with evidence.

## Execution Steps

1. Replace the shared v3 probability script with a paper-specific physical-invariance audit benchmark.
2. Generate metrics, seed metrics, per-task/per-regime tables, pairwise tests, stress sweep, ablations, failure cases, figures, and LaTeX tables.
3. Update repository docs to reflect the actual terminal gate.
4. Rewrite `paper/main.tex` as either a strong-revise evidence report or a negative archive report.
5. Compile and copy only `108.pdf` to `C:/Users/wangz/Downloads/108.pdf`.
6. Verify finite CSVs, py_compile, LaTeX log, PDF hash, no Desktop PDF, clean child repo, public GitHub push, and root report consistency.

## RAM Discipline

Use vectorized or aggregate group simulation and write summary tables directly. Keep all seeds, tasks, regimes, methods, stress levels, ablations, and failure cases; do not reduce experimental coverage to save memory.
