# Vitia value/performance assessment

Vitia 2.0.0 assesses the appeal of seven types of emotional value for a specified audience and context. Each domain has independent value and performance axes. The user-approved purpose is to retain audience-specific strengths without averaging them away.

## Domain and implementation

- Domain: `vitia-assessment` — validate and interpret evidence-linked value/performance profiles.
- Stack: Python 3.9 or later, standard library only; local JSON input/output, no service or network.
- Architecture: `score_vitia.py` owns CLI I/O; `vitia_contract.py` validates inputs; `vitia_assessment.py` interprets profiles; `vitia_guardrails.py` owns shared safety constants.
- Existing game-experience and marketing-mechanism audits retain their current contracts. Public imports of the safety constants from `score_vitia` remain available.

## Required behavior

1. Require schema version 2 and explicit audience/context. Reject v1 signals instead of guessing two axes from one old score.
2. Return every domain with both axes. Missing scores are `null`, never zero. Reject booleans, nonfinite numbers, out-of-range scores, unknown domain/axis keys, and scored entries without rationale and evidence references.
3. Preserve value and performance scores independently. Do not average domains, multiply the axes, subtract risk penalties from them, or discount them by confidence.
4. Keep observed, measured, documented, hypothetical, and unknown evidence distinguishable. Confidence describes evidence uncertainty and is not itself an axis.
5. Interpret known pairs using the declared descriptive threshold; this is an authored rubric, not statistical significance or a success forecast. Low values and missing evidence do not automatically require product changes.
6. Exclude context-only names and declared domains from scoring. Withhold pair conclusions when the extraction neutrality check has not passed.
7. Report safety flags independently; blocked flags stop persuasive adoption, even with high value and performance. Unknown flags require review.
8. Preserve version 2.0.0 in the skill metadata, CLI/report output, and migration guidance. Revisor owns its separate local release state; an implementation PR must not change `.revisor-version`.

The full scoring anchors, JSON contract, and migration rules are in [algorithm.md](../../references/algorithm.md); domain-specific judgments are in [domains.md](../../references/domains.md). Regression cases cover audience-specific peaks, independence, unknowns, evidence validation, neutrality, and retained audit imports. Session policy determines whether tests may be run.
