# Vitia 2.0.0: value and performance

## Meaning of the assessment

Vitia describes the emotional value an offer can provide to a specified audience. For each of the seven domains, record two independent judgments:

- **Value (価値 / 主材料):** how desirable and meaningful that experience is to this audience in this context.
- **Performance (パフォーマンス / 裏付け・達成可能な土壌):** how convincingly the offer can deliver that particular value, through its rules, mechanisms, implementation, presentation, discoverability, accessibility, and delivery conditions.

Performance includes credible feasibility before release as well as observed delivery after release. State which is being assessed. A documented design can support a feasibility hypothesis; it does not establish an experienced result. Performance is not a CPU or frame-rate score, although those can be relevant evidence.

Do not average the seven domains, multiply value by performance, or create a single overall Vitia score. A strong domain can be a meaningful attraction for a particular audience even when other domains are low. Strong value with weak performance means an appealing proposition with a delivery gap; do not erase the appeal by averaging it with the gap. Strong performance with weak value means effective delivery of something this audience may not value.

The word “high” denotes a rubric judgment. It does not mean statistically significant, popular with everyone, competitively superior, or likely to sell. Name the audience and the evidence needed to support resonance. A niche audience is a valid scope; do not infer its size from the score.

## Label neutrality

Bracket artifact names, genre/category labels, reputation, moral framing, and proposed Latin domains before extracting evidence. Describe the sought experience and delivery conditions in plain language, then map them to domain IDs. Repeat the extraction with neutral replacement names.

For equal evidence and context-only relabeling, both axes, evidence status, and guardrails must remain equal. `label_context` is validated but excluded from scoring. The script does not perform or verify the extraction itself: the analyst records the rename-check result and references. If that check has not passed, known pairs receive `neutrality_unconfirmed` instead of a domain conclusion.

Audience and actual usage context are substantive inputs; changing them may legitimately change the human assessment. A renamed product is not a changed audience.

## Scoring anchors

Use the same anchors within a declared audience/context and explain the evidence supporting each judgment. Intermediate scores are permitted when the rationale supports the distinction; extra decimal places do not add measurement precision.

| Score | Value | Performance |
| --- | --- | --- |
| `null` | Insufficient evidence about appeal. | Insufficient evidence about delivery or feasibility. |
| 0 | Evidence supports no meaningful appeal in the assessed scope. | Evidence supports no viable way to deliver this value in the assessed scope. |
| 0.25 | A minor or weakly desired benefit. | Substantial delivery gaps or obstacles. |
| 0.50 | A meaningful but moderate attraction. | A plausible path or partial delivery with material gaps. |
| 0.75 | A strong, clearly articulated attraction. | A credible path or consistent delivery with limited gaps. |
| 1.00 | A central attraction with strong evidence within the declared scope. | The declared value is convincingly achievable or delivered across the assessed conditions. |

Score strength and evidence confidence are different. Record rationale, source references, basis, and confidence separately for each axis. Do not discount a score by multiplying it by confidence or evidence coverage. Do not treat absence, a nonexistent release history, or an unselected audit as zero.

Use [domains.md](domains.md) to distinguish each domain's desired benefit from its delivery evidence. In particular, frustration is not delivered Ira value, friction is not delivered Acedia value, and usage frequency alone is not Gula value.

## JSON input contract

`scripts/score_vitia.py` validates analyst-authored assessments and returns a consistent profile. It does not extract facts from a product, estimate appeal automatically, or independently verify citations.

Required top-level fields are `schema_version: 2`, a nonempty `audience`, and a nonempty `context`. Unknown top-level, domain, axis, neutrality, or label-context keys are rejected.

| Field | Contract |
| --- | --- |
| `domains` | Object keyed by `superbia`, `avaritia`, `luxuria`, `invidia`, `gula`, `ira`, `acedia`. Omitted domains become unknown pairs. |
| Domain entry | An object containing `value` and `performance`; either may be omitted or `null` for an unknown axis. |
| Axis `score` | A finite number in [0, 1], or `null`. Booleans and numeric strings are invalid. |
| Axis `basis` | `observed`, `measured`, `documented`, `hypothesis`, or `unknown`. Default `unknown`. |
| Axis `rationale` | A nonempty explanation for a known score. Unknown axes may explain the information gap. |
| Axis `evidence_refs` | Array of nonempty reference strings. At least one is required for a known score, including a hypothesis. |
| Axis `confidence` | A finite number in [0, 1] or `null`; default `null`. This is stated confidence in the evidence interpretation, not a calibrated probability. |
| `neutrality_check` | Object with `status` (`passed`, `failed`, `not_checked`) and `evidence_refs`. Checked results require a reference to the extraction comparison. Default `not_checked`. |
| `high_threshold` | Descriptive threshold in (0, 1]; default 0.75. Record the reason for any override in `context` and hold it fixed during comparisons. |
| `risk_flags` | Array of observed risk IDs; default []. Flags do not alter either axis. |
| `label_context` | Optional strings keyed by `artifact_name`, `category_name`, `declared_domain`, `reputation_label`, or `source_frame`. Context-only. |

A known score requires a non-`unknown` basis. An unknown score requires `basis: unknown` and `confidence: null`. References and an explanation of missing evidence may still be recorded. Cite both delivery and appeal evidence when they differ; do not copy one rationale across the two axes merely to fill fields.

A reusable input is provided in [assessment.example.json](assessment.example.json):

```sh
python scripts/score_vitia.py --version
python scripts/score_vitia.py --example
python scripts/score_vitia.py references/assessment.example.json
python -m scripts.score_vitia references/assessment.example.json
```

Use Python 3.9 or later. On Windows, an installed interpreter may be invoked with `py -3` instead of `python`. The CLI also accepts `-` for UTF-8 standard input. Invalid inputs produce a diagnostic on stderr and exit status 2.

## Output and interpretation

The output includes `vitia_version: 2.0.0`, `schema_version: 2`, audience, context, threshold, and a `domains` array containing all seven domains in stable domain order. Each entry retains both complete axes plus `interpretation`, `evidence_status`, and applicable `risk_flags`. There is no single `score`, automatic primary/secondary, or overall rank.

| Value / performance | Interpretation | Decision to consider |
| --- | --- | --- |
| High / high | `strength` | Candidate strength for this audience; preserve it when no material problem exists. |
| High / below threshold | `delivery_gap` | Retain the attraction and investigate its delivery gap. |
| Below threshold / high | `value_or_audience_review` | Review the proposition or audience relevance before adding more polish. |
| Below threshold / below threshold | `reconsider_focus` | Assess whether this domain matters to the intended experience at all. |
| Either unknown | `unconfirmed` | Gather the missing evidence; a known axis remains visible. |
| Both known; neutrality not passed | `neutrality_unconfirmed` | Repeat or complete the label-neutral extraction before drawing a conclusion. |

`evidence_status` is `unconfirmed` when either score is unknown, `provisional` when either basis is hypothetical or confidence is unspecified, and otherwise `evidence_recorded`. “Recorded” means the fields are present, not that the evidence was independently verified or has high confidence.

The top-level status is `blocked` for a blocking risk; otherwise `review_required` for any risk flag or a failed neutrality check; otherwise `partial` for incomplete/provisional domains or an unchecked neutrality pass; otherwise `assessed`. Read individual domains even when other domains remain unknown. No status establishes adoption permission, market size, causal effect, or product success.

Display all seven pairs with audience, evidence basis, and uncertainty. A value-first sort is optional for presentation; preserve both scores and keep unknowns identifiable. Do not substitute that sort for a commercial-advantage finding.

## Safety and strategy composition

Keep risks outside both axes. Blocking flags stop persuasive optimization; nonblocking or unknown flags require review. An empty risk list means no flags were reported, not that the safety review was completed. Read [ethics.md](ethics.md).

An assessment may identify several distinct audience attractions. When designing a concrete experiment, give each chosen domain a specific role and keep the treatment interpretable. Prefer one main value proposition and at most one supporting role in a single treatment; this is an experiment-design choice, not a limit on the seven-domain profile.

Examples include mastery plus economic justification, an initial sensory experience plus repeat value, or restored agency plus an easy repair path. Do not combine Ira and Invidia for persuasive targeting. Luxuria plus Gula requires attention to compulsion, especially in the contexts covered by the ethics reference.

Tie a truthful feature to an outcome, explain the proposition and delivery evidence, and propose adoption, repair, preservation, or research according to the actual objective. Low or unknown domains need not be improved. Supporting game-experience and mechanism audits inform evidence; their heuristic scores never automatically update either axis.

For an experiment, identify the audience before observing results, use a meaningful control, specify a primary outcome and a trust/harm guardrail, and state a disconfirming result. Select a method using [research-methods.md](research-methods.md). A score alone is not an experiment result.

## Synthetic example

The example JSON is an invented design exercise, not a report of user research. Its audience is adults seeking a satisfying, expressive short-session building game.

- A proposed showcase offers a strong identity/mastery attraction, while its planned tools and feedback leave a substantial delivery gap.
- A proposed repeat-play loop has both appealing variety and a credible design path. These remain hypotheses.
- A vivid first-use promise appears attractive, but the playable demonstration has not been assessed; its performance is unknown.
- Other domains have not been assessed. Their absence carries no negative judgment.
- The recorded rename check represents the comparison within this synthetic exercise only.

Use these statements to understand the schema. Replace every example rationale and reference with actual project evidence before using an assessment for a decision.

## Migration from 1.x

Version 1.x blended need/problem signals, delivery evidence, confidence, coverage, and risk penalties into a single weighted score. Its primary/secondary outputs answered a routing question; those values are not comparable to either 2.0.0 axis.

1. Retain the old report as historical evidence with its version.
2. Re-extract audience/context, desired emotional value, and delivery evidence separately.
3. Apply the 2.0.0 anchors, retaining unknowns and per-axis evidence. There is no automatic numeric conversion.
4. Replace `signals`, global/domain `confidence`, and old `scores/primary/secondary` consumption with the versioned input and `domains[].value/performance`.
5. Existing game-experience and marketing-mechanism audit inputs/outputs are unchanged. Their imports of `BLOCKING_FLAGS` and `RISK_PENALTIES` from `score_vitia` remain supported; `DOMAIN_WEIGHTS` and the old score example are removed.
6. Consumers that copy or hash audit/scoring sources must include the new transitive modules `scripts/vitia_assessment.py`, `scripts/vitia_contract.py`, and `scripts/vitia_guardrails.py`, as well as the files previously used. Update a pinned source manifest deliberately before calling it Vitia 2.0.0-backed.

The skill metadata, CLI, and score output identify this version as 2.0.0. Revisor owns its separate local release state; do not change `.revisor-version` through an implementation PR.
