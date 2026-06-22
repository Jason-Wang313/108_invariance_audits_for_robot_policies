# Experiment Rigor Checklist

- [x] Frozen v5 plan before final interpretation.
- [x] CPU-only, RAM-light executable benchmark.
- [x] 8 task families.
- [x] 10 transformation regimes.
- [x] 8 splits.
- [x] 16 methods including v4 and oracle.
- [x] 10 paired seeds.
- [x] 102400 main cell rows.
- [x] 48000 stress-sweep cell rows.
- [x] 51200 fixed-risk cell rows.
- [x] 8000 ablation cell rows.
- [x] 24 failure cases.
- [x] Strongest non-oracle baseline selected by frozen aggregate utility rule.
- [x] Success, diagnostic, safety, pairwise, ablation, stress, and fixed-risk gates pass.
- [x] Failure cases and limitations reported honestly.
- [ ] Real robot validation.
- [ ] Independent high-fidelity benchmark.
- [ ] External benchmark split.
- [ ] Trained learned-policy checkpoints.
- [ ] Rollout videos and deployment logs.

Conclusion: rigorous local evidence, still below final submission evidence standard.
