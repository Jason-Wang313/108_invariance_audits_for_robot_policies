# Paper 108 Expanded-Submission Plan

Paper: `108_invariance_audits_for_robot_policies`

Timestamp: 2026-06-22 23:28:47 +08:00

Target venue posture: ICLR-main-target, hostile-review standard.

Terminal honesty rule: do not optimize for pretty results. Optimize for results that survive hostile review. Freeze the protocol before interpreting final numbers; report all predefined outcomes honestly. Mark ICLR-main ready only if the artifact contains real robot, accepted high-fidelity benchmark, external benchmark, calibrated deployment logs, trained-checkpoint, or rollout-video evidence. Otherwise mark `STRONG_REVISE` or `KILL_ARCHIVE`.

## Current Weakness

The v4.1 artifact is only 6 pages and uses a local diagnostic benchmark. It supports the narrow mechanism that some invariances are physically invalid, but it is not a real submission because it lacks external robot evidence, trained policies, deployment logs, high-fidelity simulation, and a full theory/related-work/error-analysis treatment.

## Scope Expansion

- Expand from the v4.1 suite to a heavier CPU-only/RAM-light benchmark with additional tasks, invariance regimes, splits, methods, seeds, stress levels, fixed-risk/acceptance budgets, ablations, and falsification cases.
- Keep memory light by emitting compact cell-level rows rather than oversized per-episode logs.
- Preserve the central claim: observation-level invariance is not enough for robot policies; transformations must preserve the physically correct action.
- Add theory separating observation equivalence, action equivalence, contact-frame equivalence, affordance equivalence, and temporal-order equivalence.
- Include failure modes and decision gates before seeing final v5 results.

## Frozen Empirical Protocol

- Tasks: peg insertion, drawer opening, cable routing, tool use, mobile pick-and-place, deformable folding, bimanual handoff, articulated-object assembly.
- Regimes: lighting/background shift, camera viewpoint shift, SE(2) pose transform, object-scale/fixture shift, mirror-handed contact, material/friction swap, tool-affordance swap, support-surface change, temporal-order reversal, and mixed physical invalidity.
- Splits: nominal, valid perceptual shift, valid geometric shift, invalid physical shift, contact-frame break, affordance break, temporal break, held-out mixed invariance stress.
- Methods: no-invariance BC, aggressive augmentation, equivariant policy, domain randomization, invariant-risk-minimization proxy, contrastive invariance learner, causal representation proxy, conformal shift filter, ensemble disagreement filter, test-time augmentation voting, physics-consistency classifier, contact-frame verifier, affordance-graph verifier, v4 proposed physical-invariance audit, v5 action-equivalence invariance audit, and oracle invariance-validity supervisor.
- Seeds: 10.
- Episodes per cell: 6.
- Ablations: remove physical-validity classifier, contact-frame test, affordance consistency, temporal-order check, action-equivalence head, counterfactual transform witness, conservatism calibration, and fixed-risk acceptor.
- Stress sweep: 10 invalid-invariance intensity levels.
- Fixed acceptance/risk budgets: 0.08, 0.12, 0.16, 0.20.
- Negative/falsification cases: include transformations that are genuinely valid, transformations that are easy for conformal shift filtering, transformations where augmentation should win, and transformations where the proposed method should abstain.

## Frozen Metrics

- Primary: success, valid-invariance retention, invalid-invariance rejection, action-equivalence F1, false-invariance acceptance, contact-frame violation, affordance violation, temporal-order violation, unsafe action, calibration ECE, intervention cost, regret to oracle, and utility.
- Invariance diagnostics: observation-equivalence score, action-equivalence score, physical-validity margin, contact-frame margin, affordance-consistency margin, temporal-consistency margin, and over-invariance rate.
- Statistical checks: paired seed differences against the strongest non-oracle baseline, seed-level CI, ablation margins, stress monotonicity, and fixed-risk coverage/utility.

## Predefined Gates

- Local success gate: v5 beats the strongest non-oracle baseline by at least 0.03 success or 0.05 utility under hard invariance stress.
- Diagnostic gate: v5 improves invalid-invariance rejection by at least 0.05 or reduces false-invariance acceptance by at least 0.04.
- Safety gate: v5 does not increase contact-frame violation, unsafe action, temporal-order violation, or intervention cost beyond predefined tolerances.
- Pairwise gate: v5 wins at least 8/10 paired seeds on success or utility against the strongest non-oracle baseline.
- Ablation gate: the full v5 method beats every removed-component variant on success or utility.
- Stress gate: v5 remains above the strongest non-oracle baseline at the highest invalid-invariance stress level.
- Fixed-risk gate: v5 maintains useful coverage at the strictest feasible risk budget and beats the strongest non-oracle baseline on utility.
- Scope gate: fail unless real robot, accepted high-fidelity benchmark, external benchmark, calibrated deployment logs, trained checkpoint, or rollout-video evidence is present.

## Manuscript Expansion

- Generate a 25+ page ICLR-style manuscript from results, not hand padding.
- Add bright boxed clickable citation links with `hyperref` color boxes.
- Add sections for theory, benchmark design, baselines, metrics, results, stress tests, ablations, fixed-risk deployment, falsification cases, related-work pressure, reproducibility, limitations, and appendices.
- Keep all claims tied to generated evidence. If the scope gate fails, explicitly state that the paper remains `STRONG_REVISE` and is not ICLR-main-ready.

## Artifact Rules

- Canonical numbered PDF: `C:/Users/wangz/Downloads/108.pdf`.
- Do not copy PDFs to the visible Desktop.
- Do not leave `C:/Users/wangz/robotics_massive_pool_paper_factory/108.pdf` or a child-root `108.pdf`.
- Validate CSV finite values, PDF page count, citation/link settings, artifact placement, and stale documentation before commit.
- Render representative PDF pages to `tmp/pdfs/` for visual QA and delete temporary renders before final commit.
