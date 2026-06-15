# Experiment Rigor Checklist

## v4 Local Evidence

- [x] Paper-specific physical-invariance audit benchmark.
- [x] 5 robot task families.
- [x] 7 invariance regimes.
- [x] 5 stress splits.
- [x] 9 methods including strong non-oracle baselines and oracle ceiling.
- [x] 7 seeds.
- [x] 84 episodes per task/regime/split/method group.
- [x] Error bars.
- [x] Paired seed comparisons.
- [x] Ablations for physical-validity classification, contact-frame testing, affordance consistency, temporal-order checking, and conservatism calibration.
- [x] Stress sweep.
- [x] Failure cases.
- [x] Generated figures and LaTeX tables.
- [x] Finite CSV audit.

## ICLR Main Bar Still Missing

- [ ] Real-robot validation.
- [ ] Independent high-fidelity simulator benchmark.
- [ ] Trained learned policy/model checkpoint.
- [ ] External implemented competing baselines.
- [ ] Qualitative robot rollouts or videos.

Decision: pass local mechanism-evidence gate; fail final main-track deployment-evidence gate; mark STRONG_REVISE.
