# Hostile Reviewer Response

Paper: 108 Invariance Audits for Robot Policies

## Strongest Technical Threats

- Equivariant neural networks and equivariant robot policies already encode transformation structure.
- Transporter-style manipulation already uses action-space equivariance for rearrangement.
- Domain randomization and augmentation already make robot policies robust to nuisance variation.
- Invariant risk minimization and contrastive invariance learning already seek stable representations.
- Conformal and uncertainty filters already reject some distribution shifts.

## ICLR Main Response

The v4 rebuild narrows the claim to physical-validity auditing: deciding which invariances preserve the correct robot action and which erase contact frame, material, affordance, force-direction, or temporal-order distinctions. The local benchmark supports that boundary. Proposed combined-invariance success is `0.685 +/- 0.008` versus `0.612 +/- 0.006` for `conformal_shift_filter`; invalid-invariance rejection improves by `0.144`; false-invariance acceptance drops by `0.047`; contact violation and unsafe action both decrease; and the strongest-baseline paired comparison is 7/7 seeds in favor of the proposed method.

## Remaining Hostile Review

A hostile reviewer would still be right to reject a main-track submission today if it claimed deployment readiness. The evidence is local and synthetic; the baselines are diagnostic executable models rather than external robot systems; and there is no real robot or independently validated high-fidelity simulator result.

## Honest Action

The paper is marked `STRONG_REVISE`. Continue only if the next version adds real robot or high-fidelity external validation, implemented learned baselines, and qualitative rollouts.
