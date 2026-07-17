# Evidence-aware supporting mechanism audits

## Contents

1. Use and separation rules
2. Audit protocol
3. Color in context
4. Behavioral contingency
5. Processing fluency
6. Choice architecture
7. Mental simulation
8. Social norms
9. Attention hierarchy
10. Integration with Vitia

## 1. Use and separation rules

Use these modules to improve how a selected Vitia strategy is expressed, delivered, or tested. They are supporting mechanisms, not additional personality labels and not proof that the seven-domain system is scientifically validated.

- Route a module only from observed offer, artifact, audience, or funnel evidence.
- Keep **opportunity** separate from **readiness**. A relevant mechanism is not ready to deploy until its claim, measurement, and guardrails are specified.
- Treat every output as an experiment hypothesis, not an effect-size prediction.
- Read [evidence.md](evidence.md) before making a scientific claim.
- Do not let a module score modify the seven-domain score automatically.

For deterministic routing, run:

```text
python scripts/audit_marketing_mechanisms.py <input.json>
python scripts/audit_marketing_mechanisms.py --example
python scripts/audit_marketing_mechanisms.py --list-signals
```

Signals use `[0, 1]`. Omit unknown signals; never encode unknown as zero. The script reports opportunity and readiness coverage independently.

## 2. Audit protocol

For each materially relevant module:

1. State the observable bottleneck and the evidence that it exists.
2. Record opportunity signals without inferring hidden traits or mental states.
3. Record readiness signals: truthful hypothesis, baseline, behavioral outcome, and harm guardrail.
4. Run the audit and select only modules marked `testable` or `needs_evidence`.
5. Resolve `needs_evidence` before deployment or label the work exploratory.
6. Change one mechanism at a time where practical.
7. Measure customer value and harm alongside conversion.

## 3. Color in context

**Supports:** Luxuria for experience and tone, Superbia for credible brand meaning, Acedia for legibility and navigation.

1. Define the functional role of color: hierarchy, category cue, brand meaning, state, or affective tone.
2. Specify hue, lightness, chroma, surrounding colors, medium, task, and exposure context.
3. Form a context- and audience-specific hypothesis. Do not use a universal color-emotion lookup table.
4. Preserve contrast, non-color redundancy, and material-information visibility.
5. Randomize the color treatment while holding copy, layout, offer, and targeting constant.
6. Measure behavior plus comprehension, accessibility, and brand-fit outcomes.

## 4. Behavioral contingency

**Supports:** Gula for repeated value and feedback, Acedia for cue and response effort, Avaritia for utilitarian consequences.

1. Define one observable target behavior and its baseline rate.
2. Map the setting and antecedent cues immediately available before the behavior.
3. Map response effort and the actual utilitarian and informational consequences.
4. Record consequence timing, consistency, and the customer's next useful state.
5. Change one cue, effort, or consequence property while preserving voluntary choice.
6. Measure the target behavior, customer outcome, overuse, opt-out, and adverse displacement.

Use this as consumer behavior analysis, not clinical ABA. Do not diagnose motives from clicks or use punishment, deprivation, or compulsive schedules as marketing tools.

## 5. Processing fluency

**Supports:** Acedia for comprehension and completion, Luxuria for coherent perceptual experience.

1. Locate the processing bottleneck: reading, parsing, comparison, navigation, or meaning integration.
2. Measure the original with comprehension and task outcomes, not readability alone.
3. Change one source of avoidable difficulty: hierarchy, terminology, figure-ground contrast, grouping, or semantic coherence.
4. Preserve qualifications, uncertainty, and decision-relevant detail.
5. Test comprehension, completion, decision quality, and misplaced trust.

Fluent content can feel true or familiar without being accurate. Never optimize ease by hiding risk or compressing away informed consent.

## 6. Choice architecture

**Supports:** Acedia for decision friction, Avaritia for transparent option and cost comparison.

1. Diagnose choice-set complexity, task difficulty, preference uncertainty, effort-minimizing goals, and observed deferral.
2. Do not treat option count alone as evidence of overload.
3. Choose one transparent intervention: grouping, progressive disclosure, comparison aid, or a disclosed reversible default.
4. Preserve option parity and access to the full set.
5. Measure qualified choice, deferral, switching, regret, accidental action, and undo.

Average nudge effectiveness is disputed and highly heterogeneous. Use local randomized evidence and do not import a generic uplift estimate.

## 7. Mental simulation

**Supports:** Luxuria for anticipated experience, Superbia for credible future use or mastery.

1. Identify a real use episode that is difficult to evaluate from abstract claims.
2. Choose process-focused simulation when the next actions matter; choose outcome-focused content only when the outcome is verifiable.
3. Trace every scene from feature to customer outcome.
4. Retain analytical facts, material terms, and uncertainty next to the scenario.
5. Compare the scenario with a factual control on qualified trial, recall, comprehension, and regret.

Do not use narrative immersion to suppress scrutiny or depict results the product cannot deliver.

## 8. Social norms

**Supports:** Invidia for relevant peer pathways, Superbia for belonging and contribution.

1. Define the exact behavior, reference group, time window, denominator, and data source.
2. Separate descriptive norms (what people do) from injunctive norms (what is approved).
3. Check whether the message could normalize undesirable behavior for an already-better segment.
4. Use an attainable pathway rather than superiority, popularity pressure, or shame.
5. Compare with a non-normative control and analyze behavior by baseline segment.

Never fabricate counts, ratings, scarcity, popularity, or similarity to the audience.

## 9. Attention hierarchy

**Supports:** Luxuria for perceptual entry, Acedia for detection and action clarity.

1. Assign one job to each visual element: brand, proposition, proof, material term, or action.
2. Define the attention bottleneck and expected exposure duration.
3. Change one hierarchy variable such as size, position, contrast, grouping, or clutter.
4. Measure detection or attention together with recall, comprehension, and qualified action.
5. Confirm that salient elements transfer attention to the message and do not obscure material information.

Attention is an intermediate measure, not proof of persuasion, preference, or customer benefit.

## 10. Integration with Vitia

Assign one supporting module a distinct job under the selected domain strategy:

```text
Primary Vitia domain / bottleneck:
Supporting module / delivery or measurement job:
Observed opportunity signals:
Readiness gaps:
Mechanism hypothesis:
Treatment and control:
Behavioral outcome:
Trust or harm guardrail:
Disconfirming result:
```

Prefer one supporting module per treatment. When two are inseparable, state what each changes and use a factorial design or staged test if traffic permits.
