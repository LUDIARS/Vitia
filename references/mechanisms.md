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
10. Regulatory fit
11. Construal-level alignment
12. Self-determination support
13. Goal-gradient progress
14. Information scent
15. Elaboration depth
16. Credible signaling
17. Integration with Vitia

## 1. Use and separation rules

Use these modules to improve how a selected Vitia strategy is expressed, delivered, or tested. They are supporting mechanisms, not additional personality labels and not proof that the seven-domain system is scientifically validated.

- Route a module only from observed offer, artifact, audience, or funnel evidence.
- Keep **opportunity** separate from **readiness**. A relevant mechanism is not ready to deploy until its claim, measurement, and guardrails are specified.
- Treat every output as an experiment hypothesis, not an effect-size prediction.
- Read [evidence.md](evidence.md) before making a scientific claim.
- Use [research-methods.md](research-methods.md) for causal or preference
  measurement; research methods are not scored as persuasion mechanisms.
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

## 10. Regulatory fit

**Supports:** Superbia for advancement goals, Avaritia for security and loss
avoidance, Acedia for goal-pursuit framing.

1. Infer a promotion or prevention orientation from the current goal and
   decision context, not from a fixed personality label.
2. Separate the desired end from the means: eager advancement and vigilant
   protection are not interchangeable with positive and negative wording.
3. Cross matched and mismatched variants while holding the offer, evidence,
   and claim strength constant.
4. Measure qualified behavior, comprehension, trust, and heterogeneous effects.

A message that feels right is not necessarily true. Do not use fit to intensify
fear, conceal uncertainty, or profile an individual without consent.

## 11. Construal-level alignment

**Supports:** Luxuria for anticipated desirability, Avaritia for future value,
Acedia for concrete next action.

1. Define the distance dimension: time, space, social distance, or probability.
2. Diagnose whether the decision needs abstract purpose or concrete feasibility.
3. Create abstract and concrete variants from identical product facts.
4. Cross framing with a near or distant context and measure comprehension,
   decision quality, and action.

This differs from mental simulation: simulation constructs a use episode;
construal alignment changes the level of representation. Never remove material
details merely because the decision is distant.

## 12. Self-determination support

**Supports:** Superbia for authentic mastery, Gula for sustainable engagement,
Acedia for self-endorsed activation.

1. Locate the need most affected by the experience: autonomy, competence, or
   relatedness.
2. Replace controlling language with meaningful choice and a truthful rationale.
3. Make competence feedback specific to real progress and skill.
4. Make connection optional and nonpressuring; preserve easy exit.
5. Measure sustained qualified use, perceived pressure, customer benefit, and
   dependency indicators.

This differs from behavioral contingency: it asks whether engagement is
self-endorsed, not only whether cues and consequences alter behavior.

## 13. Goal-gradient progress

**Supports:** Gula for repeated progress, Acedia for completion momentum,
Avaritia for progress toward earned value.

1. Define the valued goal, real starting state, completion rule, and reward.
2. Measure effort or drop-off across remaining distance before changing the UI.
3. Test one truthful progress representation or credit for work already done.
4. Disclose expiry and reset rules and preserve value before completion.
5. Measure completion and pace together with abandonment, regret, and overuse.

Do not fabricate a head start or use accumulated progress as sunk-cost pressure.
Goal-gradient evidence is a hypothesis about distance and effort, not permission
for an addictive loop.

## 14. Information scent

**Supports:** Acedia for search and navigation effort, Avaritia for locating
decision-relevant costs and benefits.

1. Define the user's information goal and the exact destination that satisfies it.
2. Map proximal cues such as labels, snippets, icons, and link placement to the
   expected destination value.
3. Test with representative tasks and vocabulary.
4. Measure findability, path cost, misclicks, comprehension, and task success.
5. Keep material terms visible even when they are not the most-clicked target.

This differs from processing fluency: scent predicts where information is;
fluency concerns the effort of processing it after encounter.

## 15. Elaboration depth

**Supports:** Avaritia for consequential tradeoffs, Superbia for defensible
identity claims, Acedia for the ability to scrutinize complex evidence.

1. Measure situational motivation and ability to examine the claim.
2. Separate supported argument quality from incidental cues such as celebrity,
   polish, repetition, or source attractiveness.
3. Vary argument quality and peripheral cues independently where feasible.
4. Measure comprehension and immediate judgment plus delayed persistence or
   resistance to counterargument.
5. Improve access to evidence rather than suppressing scrutiny.

Central and peripheral processing are not permanent audience types. Do not
reduce ability, create distraction, or hide terms to make weak arguments work.

## 16. Credible signaling

**Supports:** Superbia for earned quality distinction, Avaritia for reducing
pre-purchase quality uncertainty.

1. Identify the information asymmetry and why quality cannot be verified before
   purchase.
2. Specify what the seller commits, what failure costs the seller, and why that
   bond should correlate with quality.
3. Make standards, exclusions, duration, evidence, and remedy verifiable.
4. Compare the commitment with a claim-only control and measure term
   comprehension, trust, quality inference, and actual claims or remedies.

This differs from social norms: the evidence is the seller's enforceable bond,
not other customers' behavior. Cost alone is not credibility, and an obscure
warranty or empty badge can backfire.

## 17. Integration with Vitia

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
