# Paper 108 Terminal Audit

Date: 2026-06-15 17:32:12 +0100

## Terminal Decision

STRONG_REVISE

## Why Not KILL_ARCHIVE

The regenerated full local benchmark clears the predefined mechanism gates. The proposed method beats the strongest non-oracle baseline on combined-invariance success by `+0.073 +/- 0.010`, wins `7/7` paired seeds, improves invalid-invariance rejection by `+0.144`, reduces false-invariance acceptance by `-0.047`, reduces contact violation by `-0.016`, reduces unsafe action by `-0.016`, and lowers intervention cost by `-0.019`. Core ablations remain below the full model.

## Necessary Caveat

The claim must stay narrow. The evidence does not show that invariance learning is bad; it shows that robot-policy invariances need physical-validity auditing when contact, material, affordance, handedness, or temporal order changes.

## Why Not ICLR Main Ready

The evidence is still local and synthetic. The repo does not contain real-robot deployment, independent high-fidelity simulator validation, learned policy checkpoints, training curves, external benchmark comparisons, or rollout videos. The correct action is to preserve the paper as a strong-revise candidate, not to represent it as submission-ready.

## Required Next Evidence

- Real robot or independent high-fidelity simulator evaluation.
- Implemented learned baselines for augmentation, equivariance, domain randomization, IRM, contrastive invariance, and conformal shift filtering.
- Qualitative rollouts showing valid and invalid invariance transformations.
- External benchmark split such as LIBERO, RLBench, Meta-World, BridgeData, or a comparable hardware manipulation suite.
- A revised related-work section tied to those external results.
