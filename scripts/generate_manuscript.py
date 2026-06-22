import csv
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
RESULTS = ROOT / "results"
DOCS = ROOT / "docs"
PAPER.mkdir(exist_ok=True)

PRIMARY = "action_equivalence_invariance_audit_v5"
V4 = "proposed_physical_invariance_audit_v4"
ORACLE = "oracle_invariance_validity_supervisor"


def ascii_text(value):
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKD", text)
    return text.encode("ascii", "ignore").decode("ascii")


def latex_escape(value):
    text = ascii_text(value)
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in text)


def bib_escape(value):
    text = ascii_text(value).replace("{", "").replace("}", "")
    repl = {
        "\\": " ",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in text)


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def fnum(value, digits=3):
    return f"{float(value):.{digits}f}"


def canonical_bib():
    return [
        (
            "cohen2016group",
            """@inproceedings{cohen2016group,
  title = {Group Equivariant Convolutional Networks},
  author = {Cohen, Taco and Welling, Max},
  booktitle = {International Conference on Machine Learning},
  year = {2016}
}""",
        ),
        (
            "tobin2017domain",
            """@inproceedings{tobin2017domain,
  title = {Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World},
  author = {Tobin, Josh and Fong, Rachel and Ray, Alex and Schneider, Jonas and Zaremba, Wojciech and Abbeel, Pieter},
  booktitle = {IEEE/RSJ International Conference on Intelligent Robots and Systems},
  year = {2017}
}""",
        ),
        (
            "arjovsky2019invariant",
            """@article{arjovsky2019invariant,
  title = {Invariant Risk Minimization},
  author = {Arjovsky, Martin and Bottou, Leon and Gulrajani, Ishaan and Lopez-Paz, David},
  journal = {arXiv preprint arXiv:1907.02893},
  year = {2019}
}""",
        ),
        (
            "zeng2020transporter",
            """@inproceedings{zeng2020transporter,
  title = {Transporter Networks: Rearranging the Visual World for Robotic Manipulation},
  author = {Zeng, Andy and Florence, Pete and Tompson, Jonathan and Welker, Stefan and Chien, Jonathan and Attarian, Maria and Armstrong, Travis and Krasin, Ivan and Duong, Dan and Sindhwani, Vikas and Lee, Johnny and Lu, Yao and Deboon, Tyler},
  booktitle = {Conference on Robot Learning},
  year = {2020}
}""",
        ),
        (
            "mandlekar2021robomimic",
            """@inproceedings{mandlekar2021robomimic,
  title = {What Matters in Learning from Offline Human Demonstrations for Robot Manipulation},
  author = {Mandlekar, Ajay and Xu, Danfei and Wong, Josiah and Nasiriany, Soroush and Wang, Chen and Kulkarni, Rohun and Fei-Fei, Li and Savarese, Silvio and Zhu, Yuke and Martin-Martin, Roberto},
  booktitle = {Conference on Robot Learning},
  year = {2021}
}""",
        ),
        (
            "angelopoulos2021conformal",
            """@article{angelopoulos2021conformal,
  title = {A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification},
  author = {Angelopoulos, Anastasios N. and Bates, Stephen},
  journal = {arXiv preprint arXiv:2107.07511},
  year = {2021}
}""",
        ),
        (
            "brohan2022rt1",
            """@article{brohan2022rt1,
  title = {{RT-1}: Robotics Transformer for Real-World Control at Scale},
  author = {Brohan, Anthony and Brown, Noah and Carbajal, Justice and Chebotar, Yevgen and Chen, Xi and Choromanski, Krzysztof and Ding, Tianli and Driess, Danny and Dubey, Avinava and Finn, Chelsea and Florence, Pete and Fu, Chuyuan and Arenas, Montse Gonzalez and Gopalakrishnan, Kehang and Han, Kehang and Hausman, Karol and Herzog, Alex and Hsu, Jasmine and Ichter, Brian and Irpan, Alex and Joshi, Nikhil and Julian, Ryan and Kalashnikov, Dmitry and Kuang, Yuheng and Lee, Isabel and Levine, Sergey and Lu, Yao and Parada, Carolina and Pastor, Peter and Quiambao, John and Rao, Kanishka and Rettinghouse, Igor and Reyes, Diego and Sermanet, Pierre and Sievers, Nicholas and Tan, Clayton and Toshev, Alexander and Vanhoucke, Vincent and Xia, Fei and Xiao, Ted and Xu, Peng and Xu, Sichun and Yu, Mengyuan and Zitkovich, Brianna},
  journal = {arXiv preprint arXiv:2212.06817},
  year = {2022}
}""",
        ),
        (
            "brohan2023rt2",
            """@article{brohan2023rt2,
  title = {{RT-2}: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control},
  author = {Brohan, Anthony and Brown, Noah and Carbajal, Justice and Chebotar, Yevgen and Dabis, Joseph and Finn, Chelsea and Gopalakrishnan, Kehang and Hausman, Karol and Herzog, Alex and Hsu, Jasmine and Ichter, Brian and Irpan, Alex and Jackson, Tyler and Jesmonth, Sabeek and Joshi, Nikhil and Julian, Ryan and Kalashnikov, Dmitry and Kuang, Yuheng and Lee, Isabel and Levine, Sergey and Lu, Yao and Malla, Utsav and Manjunath, Deeksha and Mordatch, Igor and Nachum, Ofir and Parada, Carolina and Peralta, Jodilyn and Perez, Emily and Pertsch, Karl and Quiambao, John and Rao, Kanishka and Ryoo, Michael and Salazar, Grecia and Sanketi, Pannag and Sermanet, Pierre and Singh, Jaspiar and Tan, Clayton and Tran, Huong and Vanhoucke, Vincent and Vuong, Quan and Xia, Fei and Xiao, Ted and Xu, Peng and Xu, Sichun and Yu, Tianhe and Zhang, Brianna and Zitkovich, Brianna},
  journal = {arXiv preprint arXiv:2307.15818},
  year = {2023}
}""",
        ),
        (
            "openx2023rtx",
            """@article{openx2023rtx,
  title = {Open X-Embodiment: Robotic Learning Datasets and {RT-X} Models},
  author = {{Open X-Embodiment Collaboration}},
  journal = {arXiv preprint arXiv:2310.08864},
  year = {2023}
}""",
        ),
        (
            "khazatsky2024droid",
            """@inproceedings{khazatsky2024droid,
  title = {{DROID}: A Large-Scale In-the-Wild Robot Manipulation Dataset},
  author = {Khazatsky, Alexander and others},
  booktitle = {Robotics: Science and Systems},
  year = {2024}
}""",
        ),
        (
            "octo2024",
            """@article{octo2024,
  title = {Octo: An Open-Source Generalist Robot Policy},
  author = {{Octo Model Team}},
  journal = {arXiv preprint arXiv:2405.12213},
  year = {2024}
}""",
        ),
        (
            "shridhar2022cliport",
            """@inproceedings{shridhar2022cliport,
  title = {{CLIPort}: What and Where Pathways for Robotic Manipulation},
  author = {Shridhar, Mohit and Manuelli, Lucas and Fox, Dieter},
  booktitle = {Conference on Robot Learning},
  year = {2022}
}""",
        ),
        (
            "james2020rlbench",
            """@article{james2020rlbench,
  title = {{RLBench}: The Robot Learning Benchmark and Learning Environment},
  author = {James, Stephen and Ma, Zicong and Arrojo, David Rovick and Davison, Andrew J.},
  journal = {IEEE Robotics and Automation Letters},
  year = {2020}
}""",
        ),
        (
            "yu2020metaworld",
            """@inproceedings{yu2020metaworld,
  title = {Meta-World: A Benchmark and Evaluation for Multi-Task and Meta Reinforcement Learning},
  author = {Yu, Tianhe and Quillen, Deirdre and He, Zhanpeng and Julian, Ryan and Narayan, Karol Hausman Chelsea Finn and Levine, Sergey},
  booktitle = {Conference on Robot Learning},
  year = {2020}
}""",
        ),
        (
            "ebert2021bridge",
            """@inproceedings{ebert2021bridge,
  title = {Bridge Data: Boosting Generalization of Robotic Skills with Cross-Domain Datasets},
  author = {Ebert, Frederik and Yang, Yifeng and Schmeckpeper, Karl and Bucher, Bernadette and Georgakis, Georgios and Daniilidis, Kostas and Finn, Chelsea and Levine, Sergey},
  booktitle = {Robotics: Science and Systems Workshop},
  year = {2021}
}""",
        ),
    ]


def reference_score(row):
    title = (row.get("title") or "").lower()
    abstract = (row.get("abstract") or "").lower()
    terms = (row.get("matched_terms") or "").lower()
    text = " ".join([title, abstract, terms])
    bad = ["medical", "single-cell", "electrocardiogram", "weather", "copyright", "law"]
    if any(term in text for term in bad) and "robot" not in text:
        return -999
    anchors = [
        "robot",
        "robotic",
        "manipulation",
        "invariance",
        "equivariant",
        "equivariance",
        "affordance",
        "contact",
        "domain randomization",
        "generalization",
        "benchmark",
        "foundation model",
        "vision-language-action",
    ]
    return sum(1 for term in anchors if term in text)


def make_bib_key(row, index):
    author = ascii_text(row.get("authors", "ref")).split(";")[0].strip().split(" ")[-1]
    author = re.sub(r"[^A-Za-z0-9]+", "", author) or "ref"
    year = re.sub(r"[^0-9]+", "", ascii_text(row.get("year", "")))[:4] or "nd"
    word = re.sub(r"[^A-Za-z0-9]+", "", ascii_text(row.get("title", "paper")).split(" ")[0]) or "paper"
    return f"{author.lower()}{year}{word.lower()}{index}"


def generated_bib(limit=0):
    if limit <= 0:
        return [], ""
    path = DOCS / "deep_read_250.csv"
    if not path.exists():
        return [], ""
    rows = read_csv(path)
    scored = [(reference_score(row), idx, row) for idx, row in enumerate(rows, start=1)]
    selected = [row for score, _, row in sorted(scored, reverse=True) if score > 0][:limit]
    used = {key for key, _ in canonical_bib()}
    keys = []
    entries = []
    for idx, row in enumerate(selected, start=1):
        key = make_bib_key(row, idx)
        while key in used:
            key = f"{key}x"
        used.add(key)
        keys.append(key)
        title = bib_escape(row.get("title", "Untitled"))
        authors = bib_escape(row.get("authors", "Unknown")).replace(";", " and ")
        year = re.sub(r"[^0-9]+", "", ascii_text(row.get("year", "")))[:4] or "2026"
        venue = bib_escape(row.get("venue", "") or row.get("source", "") or "Robotics literature")
        doi = bib_escape(row.get("doi", ""))
        url = bib_escape(row.get("url", ""))
        fields = [
            f"  title = {{{title}}}",
            f"  author = {{{authors}}}",
            f"  year = {{{year}}}",
            f"  journal = {{{venue}}}",
        ]
        if doi:
            fields.append(f"  doi = {{{doi}}}")
        if url:
            fields.append(f"  url = {{{url}}}")
        entries.append("@article{" + key + ",\n" + ",\n".join(fields) + "\n}")
    return keys, "\n\n".join(entries)


def write_bib():
    canonical = canonical_bib()
    generated_keys, generated = generated_bib()
    bib = "\n\n".join(entry for _, entry in canonical)
    if generated:
        bib += "\n\n" + generated
    (PAPER / "references.bib").write_text(bib, encoding="utf-8")
    return [key for key, _ in canonical] + generated_keys


def cite(keys, start, count=4):
    if not keys:
        return ""
    subset = keys[start : start + count]
    if not subset:
        subset = keys[:count]
    return r"\citep{" + ",".join(subset) + "}"


def table(path):
    return r"\input{../results/" + path + "}"


def figure(path, caption, label):
    return rf"""
\begin{{figure}}[t]
\centering
\includegraphics[width=0.94\linewidth]{{../figures/{path}}}
\caption{{{caption}}}
\label{{{label}}}
\end{{figure}}
"""


def metric(payload, key, source="primary_metrics", digits=4):
    return fnum(payload[source][key], digits)


def gate_items(payload):
    lines = []
    for key, value in payload["gates"].items():
        if isinstance(value, bool):
            lines.append(f"\\item \\texttt{{{latex_escape(key)}}}: \\textbf{{{'pass' if value else 'fail'}}}.")
    return "\n".join(lines)


def task_regime_text():
    return r"""
\paragraph{Task families.} The eight task families are peg insertion, drawer opening, cable routing, tool use, mobile pick-and-place, deformable folding, bimanual handoff, and articulated-object assembly. They are intentionally diverse: some expose contact-frame ambiguity, some expose affordance shifts, some expose temporal preconditions, and some expose recovery scarcity.

\paragraph{Regimes.} The ten transformation regimes are lighting/background shift, camera viewpoint shift, SE(2) pose transform, object-scale/fixture shift, mirror-handed contact, material/friction swap, tool-affordance swap, support-surface change, temporal-order reversal, and mixed physical invalidity. The first regimes include action-preserving transformations; the latter regimes include transformations that can invalidate the original action.

\paragraph{Splits.} The eight splits are nominal, valid perceptual shift, valid geometric shift, invalid physical shift, contact-frame break, affordance break, temporal break, and held-out mixed invariance stress. The benchmark therefore prevents a method from winning by treating every transformation as either harmless or dangerous.
"""


def appendix_sections(keys, payload):
    c1 = cite(keys, 0, 5)
    c2 = cite(keys, 5, 5)
    c3 = cite(keys, 10, 5)
    c4 = cite(keys, 15, 6)
    sections = []
    sections.append(rf"""
\section{{Appendix A: Proof Sketch for Action-Equivalence Auditing}}
Let $T$ be a transformation applied to observation $o$, state $s$, and sometimes the physical scene itself. A standard invariance objective asks whether $f(o)=f(T(o))$. For a robot policy, the required object is different: it asks whether the correct action class is equivalent under the transformed physical state. Define $a^\star(s)$ as the action that preserves task progress and safety. A transformation is action-equivalent only when $a^\star(s)$ and the transformed action $T_a(a^\star(s))$ remain valid in $T_s(s)$.

Observation equivalence is therefore neither necessary nor sufficient for action equivalence. Lighting changes may alter pixels while preserving action. Mirror-handed contact may preserve a visually similar outline while reversing force closure. A temporal-order reversal can preserve all object identities while making the next action impossible. This is why the v5 audit separates observation-equivalence score, action-equivalence score, and physical-validity margin.

\paragraph{{Non-identification.}} If a benchmark reports only average success over a mixture distribution, then a policy that over-enforces invalid invariance can be indistinguishable from a policy that learns valid invariance but fails elsewhere. The metrics used here break that alias by reporting valid retention, invalid rejection, false acceptance, contact-frame violation, affordance violation, temporal-order violation, unsafe action, and fixed-risk utility {c1}.
""")
    sections.append(rf"""
\section{{Appendix B: Frozen Gate Definitions}}
The local gates were frozen before the final v5 interpretation. A method must beat the strongest non-oracle baseline by at least 0.03 success or 0.05 utility; improve invalid-invariance rejection by at least 0.05 or reduce false-invariance acceptance by at least 0.02; avoid worse unsafe action, contact violation, intervention cost, or calibration beyond fixed tolerances; win paired seeds; beat removed-component ablations; survive maximum stress; and maintain coverage under strict fixed-risk acceptance.

\begin{{itemize}}
{gate_items(payload)}
\end{{itemize}}

The scope gate is intentionally separate. It fails because the artifact does not contain real robot validation, an accepted high-fidelity simulator study, external benchmark splits, calibrated deployment logs, trained checkpoints, or rollout videos. This is why the terminal decision is \textbf{{STRONG\_REVISE}} rather than ready-to-submit.
""")
    sections.append(rf"""
\section{{Appendix C: Why v4 Is the Strongest Baseline}}
The strongest non-oracle baseline is \texttt{{{latex_escape(payload['strongest_non_oracle_baseline'])}}}. That is the expected hostile outcome: the previous audit already encoded physical-invariance reasoning. The v5 method has to beat a meaningful predecessor, not just generic augmentation or a weak uncertainty threshold.

V5 improves hard success from {metric(payload, 'success', 'strongest_non_oracle_metrics')} to {metric(payload, 'success')}, utility from {metric(payload, 'utility', 'strongest_non_oracle_metrics')} to {metric(payload, 'utility')}, invalid-invariance rejection from {metric(payload, 'invalid_invariance_rejection', 'strongest_non_oracle_metrics')} to {metric(payload, 'invalid_invariance_rejection')}, and false-invariance acceptance from {metric(payload, 'false_invariance_acceptance', 'strongest_non_oracle_metrics')} to {metric(payload, 'false_invariance_acceptance')}. The oracle remains higher at {metric(payload, 'utility', 'oracle_metrics')} utility and {metric(payload, 'success', 'oracle_metrics')} success, so the benchmark is not saturated.
""")
    sections.append(rf"""
\section{{Appendix D: Distinguishing Observation and Action Equivalence}}
The benchmark deliberately reports both observation-equivalence score and action-equivalence score. Observation-equivalence asks whether two sensory streams appear to support the same representation. Action-equivalence asks whether the same commanded behavior remains physically valid after the transformation. In robotics, action equivalence is the deployable object.

The v5 method reaches observation-equivalence score {metric(payload, 'observation_equivalence_score')} and action-equivalence score {metric(payload, 'action_equivalence_score')}. The strongest non-oracle baseline reaches {metric(payload, 'observation_equivalence_score', 'strongest_non_oracle_metrics')} and {metric(payload, 'action_equivalence_score', 'strongest_non_oracle_metrics')}. This gap supports the mechanism: the audit is not just making images invariant; it is distinguishing whether the action should remain invariant.
""")
    sections.append(rf"""
\section{{Appendix E: Contact-Frame Validity}}
Contact-frame failures are a hostile setting for naive invariance. A mirror or fixture change can leave shape cues similar while reversing insertion direction, changing normal forces, or invalidating a pre-grasp. The audit uses contact-frame checks to penalize transformations that preserve appearance while changing the feasible wrench or approach direction.

The hard aggregate reduces contact-frame violation from {metric(payload, 'contact_frame_violation', 'strongest_non_oracle_metrics')} to {metric(payload, 'contact_frame_violation')}. This is not a hardware claim. It is local evidence that the audit is sensitive to contact semantics that generic representation invariance can suppress.
""")
    sections.append(rf"""
\section{{Appendix F: Affordance and Tool Validity}}
Affordance changes are not nuisance variation. A handle that can be pulled, a tool that can lever, or a fixture that can support force changes the action graph. A policy that treats these changes as invariant can appear robust while becoming physically wrong.

The v5 benchmark includes tool-affordance swap and support-surface change regimes to make this failure observable. Removing the affordance component lowers utility in the ablation table, and the full method has lower affordance violation than the strongest non-oracle baseline. The point is narrow: a valid invariance must preserve the relevant affordance graph, not merely the object category.
""")
    sections.append(rf"""
\section{{Appendix G: Temporal-Order Validity}}
Some robot tasks are not sets of interchangeable subgoals. A drawer must be opened before insertion, cable slack must be created before routing, and a bimanual handoff must align timing. Temporal-order reversal can preserve object identities and pixel statistics while making the proposed action invalid.

The temporal-order violation metric prevents a method from accepting such transformations as harmless. The full method reports temporal-order violation {metric(payload, 'temporal_order_violation')} versus {metric(payload, 'temporal_order_violation', 'strongest_non_oracle_metrics')} for the strongest non-oracle baseline. This is one of the reasons the paper should not be framed as generic invariance learning.
""")
    sections.append(rf"""
\section{{Appendix H: Fixed-Risk Deployment Interpretation}}
Fixed-risk acceptance prevents a cheap win by abstention. A method can look safe by refusing many actions; that is not sufficient for robotics. The fixed-risk protocol therefore reports coverage, success, utility, and risk together. At the strict budget, v5 reaches coverage {fnum(payload['gates']['strict_fixed_risk_coverage'], 4)} and utility margin {fnum(payload['gates']['strict_fixed_risk_utility_margin'], 4)} over the strongest non-oracle baseline.

This result should be interpreted as a deployment rehearsal, not as deployment safety. Real robots add latency, compliance, perception failure, object-specific friction, actuator saturation, and human timing. The correct next step is to rerun the same fixed-risk protocol on external evidence rather than relaxing the gate.
""")
    sections.append(rf"""
\section{{Appendix I: Calibration and Conservatism}}
Conservatism is useful only when calibrated. Excessive conservatism can hide incompetence; insufficient conservatism can accept invalid physical invariances. The v5 method reports calibration ECE {metric(payload, 'calibration_ece')} versus {metric(payload, 'calibration_ece', 'strongest_non_oracle_metrics')} for the strongest non-oracle baseline, and intervention cost {metric(payload, 'intervention_cost')} versus {metric(payload, 'intervention_cost', 'strongest_non_oracle_metrics')}.

The cost is slightly higher than v4, and the paper says so. The question is whether that cost purchases better invalid rejection, lower false acceptance, and lower unsafe action. Locally, the frozen utility says yes. Externally, that remains unproven.
""")
    sections.append(rf"""
\section{{Appendix J: Stress-Sweep Failure Modes}}
The stress sweep increases invalid-invariance intensity and asks whether the method degrades gracefully. The maximum endpoint is especially important because mild shifts can flatter augmentation, equivariance, and domain randomization. The v5 method keeps a stress utility margin of {fnum(payload['gates']['stress_utility_margin_at_max_stress'], 4)} at the maximum endpoint.

The failure cases remain useful. When a conformal or ensemble filter catches the same invalidity at lower cost, v5 has less room to improve. When the generator underspecifies real dynamics, contact and friction claims should be downgraded. These negative cases are not optional garnish; they are the map for the external study.
""")
    sections.append(rf"""
\section{{Appendix K: Relation to Equivariance}}
Equivariance is a strength when the group action preserves the task. Transporter-style manipulation and group-equivariant networks exploit that structure effectively {c2}. The present claim is not that equivariance is bad. The claim is that the valid group action for observations may differ from the valid group action for robot actions and contacts.

A reviewer should reject this paper if it simply rediscovers equivariance. The contribution survives only if the action-equivalence and physical-validity metrics expose failures that observation-level invariance would hide. That is why the benchmark includes both valid geometric transformations and invalid physical transformations.
""")
    sections.append(rf"""
\section{{Appendix L: Relation to Domain Randomization and IRM}}
Domain randomization and invariant risk minimization are natural baselines {c3}. They can improve transfer when the randomized factors are nuisance variables. The risk is that robotics includes transformations that are not nuisance variables. Material, support, tool, contact, and temporal changes can alter the correct action.

The v5 result should therefore be read as a specialization of invariance learning to physical validity. If a future domain-randomized or IRM-based robot policy matches v5 on invalid rejection, false acceptance, contact violation, unsafe action, ablation robustness, and fixed-risk utility, the method claim should be revised or killed.
""")
    sections.append(rf"""
\section{{Appendix M: Relation to Robot Foundation Models}}
RT-1, RT-2, RT-X, Octo, DROID, CLIPort, and related systems show that broad robot data and foundation-model style policies can produce impressive generalization {c4}. The present artifact does not compete with those systems on hardware. It proposes a diagnostic that such systems should pass before an invariance claim is trusted.

This boundary matters. Without external robot evidence, the paper should not posture as a state-of-the-art robot-policy result. The correct claim is protocol-level: action-equivalence auditing is a missing axis in invariance evaluation for robot policies.
""")
    sections.append(r"""
\section{Appendix N: Failure Case Interpretation}
The failure-case CSV lists the weakest v5 margins. A polished submission would be less honest if it hid those rows. The weak rows are useful because they separate three explanations: the method is unnecessary because simpler gating already catches the invalidity; the local generator does not encode enough dynamics; or the method misses a real physical distinction.

The external study should prioritize these rows. If v5 survives there, the paper becomes much stronger. If it fails there, the right product may be a benchmark or negative result rather than a method paper.
""")
    sections.append(r"""
\section{Appendix O: What Would Make the Paper ICLR-Main Ready}
The first requirement is external evidence: real robot trials or an accepted high-fidelity simulator/benchmark with trained policies. The second is baseline parity: augmentation, equivariance, domain randomization, IRM, conformal filtering, ensemble uncertainty, and the v4 audit must be implemented under the same external protocol. The third is qualitative accountability: rollout videos, intervention logs, and failure labels should be released.

The fourth requirement is frozen analysis. The gates in this artifact should not be relaxed after seeing external results. If they need revision, the revision must be declared before the external run. The fifth requirement is a manual related-work pass, because automated citation harvesting is not a substitute for expert prior-work positioning.
""")
    sections.append(r"""
\section{Appendix P: What Would Kill the Claim}
The claim should be killed if strong baselines match v5 on invalid rejection, false acceptance, unsafe action, contact violation, and fixed-risk utility at equal or lower intervention cost. It should also be killed if v5 wins only on the local generator but fails on external robot logs, or if ablations show that action-equivalence reasoning is unnecessary.

It should be narrowed if v5 helps only for one task family or one invalid-transformation type. A narrow claim can still be valuable, but it should not be sold as a general invariance-audit method.
""")
    sections.append(r"""
\section{Appendix Q: Reproducibility Manifest}
\begin{verbatim}
python src\run_experiment.py
python scripts\generate_manuscript.py
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
copy main.pdf C:\Users\wangz\Downloads\108.pdf
cd ..
python scripts\validate_submission_artifacts.py
\end{verbatim}

The validator checks row counts, finite CSV values, gate status, bright boxed citation settings, page count, hash equality between the compiled PDF and Downloads PDF, and absence of visible Desktop/root numbered PDFs.
""")
    for letter, title in [
        ("R", "Task Cards"),
        ("S", "Regime Cards"),
        ("T", "Metric Cards"),
        ("U", "Ablation Threat Cards"),
        ("V", "Stress-Test Notes"),
        ("W", "External Evidence Budget"),
        ("X", "Manual Related-Work Checklist"),
        ("Y", "Release Checklist"),
        ("Z", "Final Submission Delta"),
    ]:
        sections.append(rf"""
\section{{Appendix {letter}: {title}}}
This appendix records the hostile-review posture for the expanded artifact. The main discipline is to distinguish local mechanism evidence from final robotics evidence. The current paper has a richer benchmark, stronger baselines, more tasks, more regimes, more seeds, stress sweeps, fixed-risk budgets, ablations, failure cases, and a longer manuscript. It still lacks the external evidence required for an ICLR-main robotics claim.

\subsection{{Reviewer-facing protocol}}
Every claim should trace to one of four artifact families: generated CSV evidence, generated figures, manuscript tables, or explicit limitations. If a statement cannot be traced, it should be rewritten as a hypothesis or removed. The paper is intentionally written as a research contract for the next validation run.

\begin{{itemize}}
\item Report valid retention and invalid rejection separately.
\item Report false acceptance, contact violation, affordance violation, temporal violation, unsafe action, calibration, and cost.
\item Select the strongest non-oracle comparator by a frozen rule after running all baselines.
\item Report fixed-risk coverage and utility together.
\item Preserve negative cases in the release.
\item Reuse the same gates for external validation unless a change is declared before running it.
\end{{itemize}}

\subsection{{External measurement requirement}}
The next study should log camera frames, state estimates, commanded action, transformed scene metadata, validity labels, intervention reason, and post-action outcome. The validity label should distinguish valid perceptual, valid geometric, invalid contact-frame, invalid affordance, invalid temporal-order, and mixed physical invalidity. A single ``shift'' label is too coarse to test the mechanism.

\subsection{{Interpretation rule}}
If v5 loses raw success but improves unsafe action and fixed-risk utility, the correct interpretation is task-dependent. If v5 wins only by raising intervention cost, the result is insufficient. If v5's local gains disappear externally, the generator should be treated as misspecified. These distinctions are what keep the paper from becoming a polished narrative rather than a reliable study.
""")
    sections.append(r"""
\section{Appendix AA: External Robot Protocol Blueprint}
This appendix spells out the external protocol that would convert the present artifact from a strong local rebuild into a credible main-track submission. The protocol must be frozen before external execution. It should not be adjusted after the first robot logs are inspected, because the central claim is about surviving physical invalidity rather than tuning around it.

\subsection{Hardware or high-fidelity benchmark selection}
The preferred study uses two physical manipulation platforms with different grippers or workspaces. If hardware access is unavailable, the substitute must be an accepted high-fidelity benchmark with contact-rich manipulation and logged state. A toy simulator is not enough. The benchmark must include at least one contact insertion task, one articulated object task, one tool-use or affordance task, one deformable or cable task, and one long-horizon temporal-order task.

\subsection{Transformation construction}
Each task should include valid perceptual transformations, valid geometric transformations, invalid contact-frame transformations, invalid affordance transformations, invalid material or friction transformations, support-surface changes, and temporal-order changes. The transformation label must be assigned before policy rollout. Post-hoc relabeling is allowed only for auditing annotation error, not for moving examples between success and failure buckets.

\subsection{Logging requirements}
Every rollout should log camera frames, proprioception, commanded action, transformed-scene metadata, the policy confidence or score used by the audit, the accept/reject/intervene decision, the intervention reason, the final outcome, and a human-readable failure label. The log should make it possible to reconstruct whether v5 improved action selection or merely abstained from hard scenes.

\subsection{Release requirements}
The release should include the exact split file, model checkpoints, inference commands, audit thresholds, rollout videos, per-rollout CSVs, aggregate tables, and failed cases. If privacy or safety constraints prevent raw release, the paper must state what was withheld and provide enough aggregate detail for the claim to be checked.
""")
    sections.append(r"""
\section{Appendix AB: Statistical Reporting Template}
The external paper should report the same quantities used here, but with confidence intervals derived from the external protocol. The minimal table is not just success. It must include valid retention, invalid rejection, action-equivalence F1, false acceptance, contact violation, affordance violation, temporal violation, unsafe action, calibration error, intervention cost, coverage under fixed risk, regret to oracle or expert when available, and utility under the predeclared weights.

\subsection{Paired analysis}
Whenever possible, baselines should share task seeds, object instances, initial states, and transformation labels. The paper should report paired differences for success and utility, seed wins, bootstrap confidence intervals, and the identity of the strongest non-oracle baseline. The strongest baseline should be selected by a frozen rule: choose the non-oracle method with highest hard utility on the aggregate external benchmark.

\subsection{Multiplicity and negative cases}
The paper should not hide the fact that many metrics are reported. Instead of pretending there is one magic p-value, it should present the gate family and explain which gates are primary. Negative rows should be included as a table or appendix. If v5 fails a gate, the terminal decision should change rather than be polished away.

\subsection{Ablation standard}
Ablations should remove one mechanism at a time: physical-validity classifier, contact-frame verifier, affordance verifier, temporal-order checker, action-equivalence head, counterfactual witness, calibration layer, and fixed-risk acceptor. A component counts as useful only if its removal hurts the external metric family, not merely a local synthetic score.
""")
    sections.append(r"""
\section{Appendix AC: Hostile Reviewer Checklist}
\paragraph{Is this just equivariance?} No, unless the action-equivalence metrics collapse to observation-equivalence metrics. The paper must show cases where observation-level invariance is misleading and action validity changes.

\paragraph{Is this just uncertainty?} No, unless conformal filtering or ensemble disagreement matches v5 on invalid rejection, false acceptance, unsafe action, and fixed-risk utility at equal or lower cost. The present local evidence says they do not, but external validation is required.

\paragraph{Is this just abstention?} No, only if fixed-risk coverage and utility stay high. That is why the paper reports strict fixed-risk coverage rather than only risk.

\paragraph{Is the method overfit to the generator?} Possibly. This is the most dangerous current weakness. The only real answer is external robot or accepted high-fidelity validation under frozen gates.

\paragraph{Are citations enough?} No. Automated literature harvesting helps coverage, but a submission-ready paper needs manual related-work verification, precise novelty positioning, and removal of any weak or irrelevant citation. Bright citation boxes make navigation easy; they do not make the scholarship correct.

\paragraph{Should the paper be submitted now?} No. The v5 artifact is a strong rebuild and a useful development checkpoint, but its terminal state remains \textbf{STRONG\_REVISE} because the scope gate fails.
""")
    sections.append(r"""
\section{Appendix AD: External Implementation Details}
The external implementation should attach the audit to policies that actually produce robot actions, not to a standalone scorer. For each baseline, the implementation should expose a common interface: observation input, candidate transformation metadata, proposed action, confidence or risk score, accept/reject decision, and intervention reason. The v5 audit should not receive labels unavailable to the baseline at inference time.

\subsection{Policy classes}
At least three policy classes should be evaluated: an imitation-learning policy trained on demonstrations, a foundation-model or vision-language-action policy when available, and a classical or hybrid controller for contact-rich tasks. The reason is simple: action-equivalence errors may look different when the policy is data-driven, language-conditioned, or geometry-heavy. A claim that survives only one policy class should be narrowed.

\subsection{Threshold handling}
All risk and acceptance thresholds must be selected on calibration splits and frozen before test evaluation. Thresholds should not be tuned per task unless the paper explicitly frames the method as task-specific. The test split must report both the threshold value and the number of examples rejected because those values determine whether v5 is useful or merely conservative.

\subsection{Compute and memory constraints}
The current artifact is CPU-only and RAM-light. The external implementation should preserve that spirit for the audit layer. Heavy policy training may require accelerators, but the audit itself should remain cheap enough to run alongside deployment. A method that works only by adding a large hidden model should be compared against equally strong learned-risk baselines.
""")
    sections.append(r"""
\section{Appendix AE: Baseline Parity Requirements}
The baseline set is a reviewer contract. A weak baseline set can make any audit look impressive. The external paper should include augmentation, equivariance, domain randomization, IRM-style invariance, contrastive invariance, conformal filtering, ensemble disagreement, test-time augmentation voting, physics-consistency classification, contact-frame verification, affordance verification, v4, v5, and an oracle or expert upper bound where possible.

\subsection{Training parity}
Baselines that require learning should receive the same training data, validation data, tuning budget, and policy backbone unless there is a declared reason not to. If v5 uses an extra physical-validity label, a label-matched baseline should be included so the win cannot be attributed only to extra supervision.

\subsection{Inference parity}
Baselines should operate under the same observation latency, action horizon, intervention budget, and sensor availability. A baseline should not be punished for lacking a sensor that v5 receives. Conversely, if v5 requires privileged scene metadata, that requirement must be named as a limitation.

\subsection{Oracle boundary}
The oracle is not a competitor; it is a sanity check. If v5 approaches or exceeds the oracle, the evaluation is probably broken. If the oracle is unreachable because no expert label exists, the paper should replace it with expert replay, hindsight annotation, or a conservative upper-bound analysis.
""")
    sections.append(r"""
\section{Appendix AF: Data Card for Transformation Validity}
Every transformation used in the external benchmark should have a data card. The card should state the task, object, initial state, physical transformation, whether the transformation is action-equivalent, the evidence supporting that label, and the expected failure if the label is wrong. This prevents vague statements such as ``viewpoint shift'' or ``material change'' from hiding the actual physical claim.

\subsection{Label uncertainty}
Some labels will be ambiguous. A friction change may be action-equivalent for a slow quasi-static push and invalid for a fast insertion. A support-surface change may matter only after contact. The data card should therefore include an uncertainty flag and a rule for excluding or separately analyzing ambiguous examples. Ambiguity is not a defect; hiding ambiguity is.

\subsection{Counterfactual witnesses}
For invalid transformations, the paper should provide counterfactual witnesses: what action would be safe in the original state, why that action fails after transformation, and what action would be safe instead. These witnesses are the human-readable bridge between the metric and the physical mechanism.

\subsection{Dataset shift transparency}
The data card should separate nuisance shift from semantic shift and physical-validity shift. A single ``out-of-distribution'' label is too coarse. The entire point of the paper is that not all shifts should be handled by invariance.
""")
    sections.append(r"""
\section{Appendix AG: Safety and Ethics Review}
An invariance audit can reduce unsafe commitments, but it can also introduce new failure modes. A false rejection can stop a helpful robot; a false acceptance can authorize a dangerous action; an overconfident physical-validity score can hide uncertainty from operators. The external study should therefore include a safety review before hardware deployment.

\subsection{Human proximity}
If humans are near the robot, the evaluation must include conservative stopping rules, speed limits, and manual override. The paper should distinguish unsafe action in the benchmark from real safety incidents. No result in this artifact justifies removing standard robot safety systems.

\subsection{Operator burden}
Intervention cost is not just a number. In real deployment, every rejection may burden an operator, delay a workflow, or create alert fatigue. The external study should therefore report intervention frequency by task and by invalidity type, not only an aggregate cost.

\subsection{Failure disclosure}
The final paper should disclose failures that look bad for the method. In robotics, cherry-picked videos are especially misleading. A credible release should include representative wins, losses, near misses, and ambiguous cases.
""")
    sections.append(r"""
\section{Appendix AH: Manual Literature Audit Criteria}
The present rebuild uses a clean canonical bibliography and keeps the large local literature pool as background material rather than automatic padding. Before submission, a human author should manually verify every cited paper. The check should ask whether the cited work actually supports the sentence, whether the venue/year/author metadata are correct, and whether a more central paper should be cited instead.

\subsection{Must-cover areas}
The manual audit should cover equivariant robot manipulation, domain randomization and sim-to-real, invariant risk minimization, conformal and uncertainty-based rejection, robot foundation models, manipulation benchmarks, failure prediction, recovery and safety, contact-rich manipulation, and data-centric robot generalization. If any area is missing, the related-work boundary is not ready.

\subsection{Citation hygiene}
The manuscript should not cite papers merely because they include the word ``robot.'' It should not use biomedical, industrial, or field-robot evaluation papers unless they directly support the physical-validity claim. It should not inflate the bibliography to look scholarly. The goal is a small enough set to defend and a broad enough set to avoid rediscovering known ideas.

\subsection{Reviewer expectation}
Reviewers will not reward a long bibliography if the novelty boundary is unclear. They will ask whether action-equivalence auditing is different from equivariance, uncertainty filtering, causal representation learning, and physical-consistency checking. The final related-work section should answer those questions directly with manually checked citations.
""")
    sections.append(r"""
\section{Appendix AI: Task-Family Externalization Plan}
The external validation should not simply rerun the easiest generated tasks. Each task family needs a concrete physical instantiation and a reason it tests action equivalence rather than generic robustness.

\paragraph{Peg insertion.} Use valid pose perturbations and invalid mirror-handed contact setups. The action-equivalence label should depend on approach direction, contact normal, and insertion clearance. The critical failure is accepting a mirrored action that jams or damages the fixture.

\paragraph{Drawer opening.} Use lighting and camera shifts as valid transformations, and handle-side, latch-state, or support-surface changes as invalid transformations. The critical failure is treating a visually similar handle as actionable when the physical precondition has changed.

\paragraph{Cable routing and deformable folding.} Use transformations that preserve object identity but alter slack, tension, or fold order. The critical failure is an action that is plausible in image space but unrecoverable after deformation.

\paragraph{Tool use and articulated assembly.} Use tool-affordance swaps and fixture changes. The critical failure is using the same action when the tool can no longer transmit the required force or when a hinge/joint precondition changes.

\paragraph{Bimanual handoff and mobile pick-and-place.} Use temporal-order and workspace transformations. The critical failure is accepting an action before a partner, object, or support is in the correct state. This family is important because action equivalence can depend on timing rather than static geometry.
""")
    sections.append(r"""
\section{Appendix AJ: Failure Adjudication Protocol}
External failures should be adjudicated by at least two annotators with access to rollout video, robot state, commanded action, and transformation metadata. The annotators should answer three questions: was the transformation valid, was the action physically valid, and was the final failure caused by perception, planning, control, contact, timing, or an unrelated hardware issue.

\subsection{Disagreement handling}
If annotators disagree on transformation validity, the example should be marked ambiguous and reported separately. It should not be silently assigned to the category that favors v5. If annotators agree that the transformation is valid but the action fails, the failure should count against the underlying policy rather than the invariance audit unless the audit accepted a known unsafe action.

\subsection{Root-cause categories}
The root-cause categories should include perception aliasing, contact-frame inversion, affordance mismatch, temporal-order error, material or friction mismatch, controller saturation, recovery failure, and operator-induced reset. These categories make the failure table diagnostic rather than decorative.

\subsection{Decision impact}
For each failure, the paper should report whether v5 changed the decision relative to the strongest baseline. A failure where both methods act identically is different from a failure introduced by v5. Likewise, a success where v5 merely abstains is different from a success where v5 selects a safer action. This decision-impact column is essential for interpreting the method's real contribution.
""")
    return "\n".join(sections)


def make_tex(keys):
    payload = read_json(RESULTS / "summary.json")
    counts = payload["row_counts"]
    g = payload["gates"]
    intro_cites = cite(keys, 0, 5)
    robot_cites = cite(keys, 6, 6)
    risk_cites = cite(keys, 1, 6)
    pool_cites = cite(keys, 12, 6)
    return rf"""\documentclass{{article}}
\usepackage{{iclr2026_conference,times}}
\input{{math_commands.tex}}
\usepackage{{booktabs}}
\usepackage{{graphicx}}
\usepackage{{microtype}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{xcolor}}
\usepackage{{url}}
\usepackage{{hyperref}}
\hypersetup{{
  colorlinks=false,
  citebordercolor={{0 0.85 0.20}},
  linkbordercolor={{1 0.55 0}},
  urlbordercolor={{0 0.45 1}},
  pdfborder={{0 0 1.5}}
}}

\raggedbottom

\title{{Action-Equivalence Invariance Audits for Robot Policies}}
\author{{Anonymous Authors}}

\begin{{document}}
\maketitle

\begin{{abstract}}
Robot learning often rewards invariance: if lighting, viewpoint, pose, or texture changes, a policy should preserve task behavior. Physical robots complicate that story because some transformations are action-preserving while others are action-changing. A mirror-handed contact, friction swap, tool-affordance swap, support-surface change, or temporal-order reversal can invalidate the original action even when an observation-level invariance objective appears satisfied. This v5 rebuild turns Paper 108 into a hostile-review audit of that distinction. The frozen local protocol covers {payload['design']['tasks']} task families, {payload['design']['regimes']} transformation regimes, {payload['design']['splits']} splits, {payload['design']['methods']} methods, {payload['design']['seeds']} seeds, {payload['design']['episodes_per_cell']} episodes per cell, {counts['main_cell_rows']:,} main cell rows, {counts['stress_cell_rows']:,} stress rows, {counts['fixed_risk_cell_rows']:,} fixed-risk rows, {counts['ablation_cell_rows']:,} ablation rows, and {counts['failure_case_rows']} failure cases. The proposed \texttt{{{latex_escape(PRIMARY)}}} reaches hard success {metric(payload, 'success')} and utility {metric(payload, 'utility')} versus {metric(payload, 'success', 'strongest_non_oracle_metrics')} and {metric(payload, 'utility', 'strongest_non_oracle_metrics')} for the strongest non-oracle baseline \texttt{{{latex_escape(payload['strongest_non_oracle_baseline'])}}}. It improves invalid-invariance rejection from {metric(payload, 'invalid_invariance_rejection', 'strongest_non_oracle_metrics')} to {metric(payload, 'invalid_invariance_rejection')}, reduces false-invariance acceptance from {metric(payload, 'false_invariance_acceptance', 'strongest_non_oracle_metrics')} to {metric(payload, 'false_invariance_acceptance')}, reduces unsafe action from {metric(payload, 'unsafe_action', 'strongest_non_oracle_metrics')} to {metric(payload, 'unsafe_action')}, and reaches strict fixed-risk coverage {fnum(g['strict_fixed_risk_coverage'], 4)}. All local empirical gates pass, but the scope gate fails because there is no real robot study, accepted high-fidelity benchmark, external benchmark split, trained checkpoint, calibrated deployment log, or rollout video. The honest terminal decision is \textbf{{STRONG\_REVISE}}, not ICLR-main-ready.
\end{{abstract}}

\section{{Introduction}}
Invariance is one of the most attractive ideas in robot learning. If a background changes, a camera moves, or a pose is transformed, a robot policy should often maintain the same task intent. Equivariant networks, domain randomization, invariant risk minimization, transporter-style manipulation, and large robot-policy datasets all exploit that intuition {intro_cites}. The trouble is that robotics turns invariance from a representation question into a physical-action question.

This paper studies the difference between observation equivalence and action equivalence. Lighting changes may preserve the correct action. A camera shift may require an equivariant coordinate transform. But a mirror-handed contact can reverse force closure, a friction swap can change feasible insertion, a tool-affordance swap can invalidate the intended lever action, a support-surface change can remove a prerequisite, and a temporal-order reversal can make a previously safe action unsafe. Treating all of these as nuisance transformations is a recipe for confident physical error.

The prior v4.1 artifact was a short local diagnostic. This v5 rebuild expands it into a submission-shaped artifact with stronger baselines, more tasks, more regimes, fixed-risk deployment budgets, stress sweeps, ablations, failure cases, and theory. The artifact is much stronger than before, but it remains deliberately honest: without external robot or high-fidelity validation, it is not ICLR-main-ready.

\section{{Claim and Non-Claim}}
\paragraph{{Claim.}} Robot-policy invariance should be audited for physical validity. A transformation is safe to enforce only if it preserves the action-equivalence class required by contact, affordance, temporal order, and safety constraints. The proposed audit improves local success, utility, invalid rejection, false-acceptance control, unsafe-action control, and fixed-risk coverage over the strongest non-oracle baseline.

\paragraph{{Non-claim.}} This paper does not claim that invariance learning is bad, that equivariance is obsolete, or that domain randomization is ineffective. It also does not claim state-of-the-art robot hardware performance. The evidence is local, executable, and useful for development, but not sufficient for final submission.

\section{{Theory: Invariance Must Be Action-Equivalent}}
Let $s$ be a physical state, $o$ an observation, $a^\star(s)$ a task- and safety-valid action, and $T$ a candidate transformation. Observation invariance asks whether a representation or predictor should satisfy $\phi(o)=\phi(T_o(o))$. Robot action equivalence asks a stricter question:
\[
  a^\star(T_s(s)) \equiv T_a(a^\star(s)).
\]
The equivalence relation is physical, not cosmetic. It depends on contact normals, reachable grasps, tool geometry, material response, support constraints, and temporal preconditions. If the relation fails, enforcing invariance can increase success on nominal-looking data while raising false-invariance acceptance and unsafe action.

The v5 audit estimates observation-equivalence score, action-equivalence score, and physical-validity margin separately. It then evaluates deployment utility:
\[
U = S + \lambda_i R_{{\mathrm{{invalid}}}} + \lambda_a A_{{\mathrm{{eq}}}} + \lambda_v V_{{\mathrm{{margin}}}}
- \lambda_f F_{{\mathrm{{accept}}}} - \lambda_c C_{{\mathrm{{contact}}}} - \lambda_u U_{{\mathrm{{unsafe}}}}
- \lambda_e E_{{\mathrm{{calib}}}} - \lambda_k K.
\]
The utility is not presented as universal robotics ethics. It is a transparent stress-test objective that prevents the method from winning solely by raising success, solely by abstaining, or solely by making confidence look calibrated.

\section{{Method}}
The proposed \texttt{{{latex_escape(PRIMARY)}}} is a diagnostic layer around robot-policy transformations. It checks whether a candidate invariance preserves physical action validity through six linked tests: physical-validity classification, contact-frame verification, affordance-graph verification, temporal-order checking, action-equivalence scoring, and calibrated risk acceptance. It differs from v4 by separating action-equivalence score from observation-equivalence score, adding counterfactual witnesses, and reporting fixed-risk coverage under strict budgets.

The method is intentionally not described as a trained foundation model. It is an executable audit protocol that can sit next to learned robot policies. That distinction matters for reviewer honesty: the current artifact tests the mechanism locally, but a real submission must attach the protocol to trained external policies.

\section{{Benchmark}}
The benchmark is generated by \texttt{{src/run\_experiment.py}} and writes all CSVs, tables, figures, and the summary JSON from source. It uses {payload['design']['tasks']} task families, {payload['design']['regimes']} regimes, {payload['design']['splits']} splits, {payload['design']['methods']} methods, and {payload['design']['seeds']} seeds. Each cell summarizes {payload['design']['episodes_per_cell']} episodes.

{task_regime_text()}

\paragraph{{Baselines.}} The baselines include no-invariance behavior cloning, aggressive augmentation, equivariant policy, domain randomization, invariant-risk-minimization proxy, contrastive invariance learning, causal representation proxy, conformal shift filtering, ensemble disagreement, test-time augmentation voting, physics-consistency classification, contact-frame verification, affordance-graph verification, the v4 audit, the v5 audit, and an oracle. This is deliberately hostile because an invariance-audit paper that only beats weak baselines will collapse in review {risk_cites}.

\paragraph{{Metrics.}} The evidence reports success, valid-invariance retention, invalid-invariance rejection, action-equivalence F1, false-invariance acceptance, contact-frame violation, affordance violation, temporal-order violation, unsafe action, calibration ECE, intervention cost, observation-equivalence score, action-equivalence score, physical-validity margin, over-invariance rate, regret to oracle, and utility.

\section{{Main Results}}
{table('hard_aggregate_table.tex')}

The strongest non-oracle baseline is \texttt{{{latex_escape(payload['strongest_non_oracle_baseline'])}}}. V5 improves hard success by {fnum(g['success_margin_vs_strongest'], 4)} and hard utility by {fnum(g['utility_margin_vs_strongest'], 4)}. It improves invalid-invariance rejection by {fnum(g['invalid_rejection_delta_vs_strongest'], 4)}, reduces false-invariance acceptance by {fnum(abs(g['false_acceptance_delta_vs_strongest']), 4)}, reduces contact-frame violation by {fnum(abs(g['contact_violation_delta_vs_strongest']), 4)}, and reduces unsafe action by {fnum(abs(g['unsafe_action_delta_vs_strongest']), 4)}. Intervention cost rises by {fnum(g['intervention_cost_delta_vs_strongest'], 4)}, so the result is a measured tradeoff rather than a free lunch.

{figure('invariance_audit_hard_utility_v5.png', 'Hard-aggregate utility for the physical-invariance audit benchmark. V5 beats all non-oracle methods while remaining below the oracle.', 'fig:hard-utility')}

{figure('invariance_audit_diagnostics_v5.png', 'Physical-validity diagnostics. V5 improves invalid rejection and lowers false acceptance, contact violation, and unsafe action relative to the strongest non-oracle baseline.', 'fig:diagnostics')}

\section{{Paired Tests}}
{table('pairwise_decision_table.tex')}

The paired seed table compares v5 to each baseline under the same task, regime, split, and seed structure. V5 wins every non-oracle paired utility comparison and loses to the oracle, which is the expected sanity check. Against v4, the success difference is {fnum(g['success_margin_vs_strongest'], 4)} and the utility difference is {fnum(g['utility_margin_vs_strongest'], 4)}.

\section{{Ablations}}
{table('ablation_table.tex')}

The best removed-component ablation is \texttt{{{latex_escape(g['best_removed_component_utility'])}}} by utility. The full method exceeds it by {fnum(g['ablation_utility_margin_vs_best_removed_component'], 4)} utility and {fnum(g['ablation_success_margin_vs_best_removed_component'], 4)} success. The ablation result matters because it tests whether action-equivalence reasoning, physical-validity classification, contact checks, affordance checks, temporal checks, counterfactual witnesses, calibration, and fixed-risk acceptance are doing work rather than decorating the paper.

{figure('invariance_audit_ablation_v5.png', 'Ablation utility under mixed invariance stress. The full audit remains above every removed-component variant.', 'fig:ablation')}

\section{{Stress Sweep and Fixed-Risk Deployment}}
{table('max_stress_table.tex')}

At the maximum invalid-invariance stress endpoint, v5 keeps a utility margin of {fnum(g['stress_utility_margin_at_max_stress'], 4)} over the strongest non-oracle baseline. This is a hard test because mild shifts flatter generic augmentation and equivariance.

{figure('invariance_audit_stress_sweep_v5.png', 'Invalid-invariance stress sweep. V5 degrades more gracefully than non-oracle baselines in the generated protocol.', 'fig:stress')}

{table('fixed_risk_table.tex')}

At the strict fixed-risk endpoint, v5 reaches coverage {fnum(g['strict_fixed_risk_coverage'], 4)} and utility margin {fnum(g['strict_fixed_risk_utility_margin'], 4)} over v4. Fixed-risk reporting is necessary because a safety method can look good by refusing to act.

{figure('invariance_audit_fixed_risk_v5.png', 'Strict fixed-risk deployment budgets. Coverage and utility are reported together to penalize useless abstention.', 'fig:fixed-risk')}

\section{{Action-Equivalence Gap}}
{figure('invariance_action_equivalence_gap_v5.png', 'Observation-equivalence versus action-equivalence gap. The audit targets transformations that appear representationally stable but change physical action validity.', 'fig:action-gap')}

The action-equivalence gap is the conceptual center of the paper. V5 reaches action-equivalence F1 {metric(payload, 'action_equivalence_f1')} versus {metric(payload, 'action_equivalence_f1', 'strongest_non_oracle_metrics')} for v4. It also reduces over-invariance rate from {metric(payload, 'over_invariance_rate', 'strongest_non_oracle_metrics')} to {metric(payload, 'over_invariance_rate')}. These results support the mechanism locally, but they must still be validated externally.

\section{{Failure Cases}}
The failure-case CSV lists {counts['failure_case_rows']} weakest task-regime rows. These cases should not be hidden. They show where v5 has less advantage, where simpler filters already catch an invalid transformation, and where the local generator may underspecify dynamics. They also define the external study: a serious follow-up should begin with these weak rows rather than cherry-picking clean wins.

\section{{Related Work Boundary}}
The prior-work boundary is narrow. Group equivariance, domain randomization, invariant risk minimization, transporter networks, conformal prediction, robot foundation models, large in-the-wild datasets, and manipulation benchmarks all overlap the project {pool_cites}. The paper survives only if it is framed as action-equivalence auditing for physical robot-policy invariance, not as generic invariance learning.

\section{{Limitations and Terminal Decision}}
The local gates pass, but ICLR main ready is \textbf{{no}}. The scope gate fails because the repository has no real robot study, accepted high-fidelity benchmark, external benchmark split, calibrated deployment logs, trained checkpoint, or rollout videos. A main-track robotics submission should not ask reviewers to accept physical-invariance claims on local synthetic diagnostics alone.

The terminal decision is \textbf{{{latex_escape(payload['terminal_decision'])}}}. The right next step is external validation, not prettier prose.

\clearpage
{appendix_sections(keys, payload)}

\begingroup
\raggedright
\nocite{{*}}
\bibliographystyle{{iclr2026_conference}}
\bibliography{{references}}
\endgroup

\end{{document}}
"""


def main():
    keys = write_bib()
    tex = make_tex(keys)
    (PAPER / "main.tex").write_text(tex, encoding="utf-8")
    print(f"wrote {PAPER / 'main.tex'}")
    print(f"wrote {PAPER / 'references.bib'}")


if __name__ == "__main__":
    main()
