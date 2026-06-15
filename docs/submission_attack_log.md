# Submission Attack Log

Paper: 108 invariance_audits_for_robot_policies

This v4 pass rebuilds the paper around a stronger local evidence package. The result is STRONG_REVISE, not main-track submission.

## Attack 1: Equivariance already solves transformation structure.

Verdict: Strong threat, addressed locally.

Action: `equivariant_policy` is included. Proposed combined-stress success is `0.685 +/- 0.008` versus `0.563 +/- 0.008`.

## Attack 2: Augmentation and domain randomization already provide invariance.

Verdict: Strong threat, addressed locally.

Action: Aggressive augmentation and domain randomization are included, but both over-accept invalid transformations under physical stress.

## Attack 3: Conformal shift filtering already rejects invalid transforms.

Verdict: Strongest baseline, addressed locally.

Action: `conformal_shift_filter` is the strongest non-oracle baseline. Proposed success improves by `0.073 +/- 0.010`, with lower contact violation, unsafe action, and intervention cost.

## Attack 4: The audit may be too conservative.

Verdict: Addressed locally.

Action: Valid-invariance retention remains higher than the strongest baseline: `0.588` versus `0.454`.

## Attack 5: Ablations may not support the mechanism.

Verdict: Passed locally.

Action: The full model reaches `0.684 +/- 0.006`; the best removed component, `minus_conservatism_calibration`, reaches `0.654 +/- 0.006`.

## Attack 6: The benchmark might be saturated.

Verdict: Not saturated.

Action: Oracle success remains higher at `0.789 +/- 0.006`.

## Attack 7: No real robot or external simulator validates the result.

Verdict: Fatal for immediate submission.

Action: Mark STRONG_REVISE, not ready-to-submit. Require external validation before main-track submission.

## Terminal Condition

The paper earns continued development because the local gates pass, but it does not earn ICLR-main readiness. Terminal state for this pass: STRONG_REVISE.
