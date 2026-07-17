---
name: vitia
description: "Design ethical, evidence-aware marketing and sales strategies by analyzing an offer through seven behavioral lenses: Superbia, Avaritia, Luxuria, Invidia, Gula, Ira, and Acedia. Use when asked to position a product or feature, choose persuasive angles, diagnose conversion or retention problems, compose behavioral mechanisms, write a sales hypothesis, plan marketing experiments, or audit color, contingencies, fluency, choices, simulation, norms, attention, goal framing, distance, autonomy, progress, navigation, elaboration, and credible signals. Do not use the seven labels as personality diagnoses."
---

# Vitia

Treat the seven Latin domains as a strategy-selection interface, not as a scientific taxonomy of people. Convert product truth and audience context into falsifiable marketing hypotheses without deception, coercion, or unsupported neuroscience claims.

## Workflow

1. Establish the truth ledger.
   - Record the offer, audience, job to be done, price or cost, proof, constraints, channel, funnel stage, and desired outcome.
   - Separate verified facts, reasonable hypotheses, and unknowns.
   - Ask only for missing facts that could materially change the strategy. Otherwise state assumptions.
2. Screen safety before persuasion.
   - Read [references/ethics.md](references/ethics.md).
   - Stop persuasive optimization when a blocked condition applies. Offer neutral information, user-protective design, or research instead.
3. Score the seven domains.
   - Read [references/algorithm.md](references/algorithm.md).
   - For repeatable scoring, run `python scripts/score_vitia.py <input.json>`.
   - Treat missing signals as unknown, never as zero, when making a qualitative assessment.
4. Route supporting mechanisms when the artifact or bottleneck makes them material.
   - Read [references/mechanisms.md](references/mechanisms.md).
   - For repeatable opportunity and readiness auditing, run `python scripts/audit_marketing_mechanisms.py <input.json>`.
   - Keep supporting-module scores separate from the seven-domain scores. Resolve readiness gaps before deployment.
5. Select one primary domain and at most one secondary domain.
   - Read the selected sections of [references/domains.md](references/domains.md).
   - Give each selected domain a distinct job. Do not stack synonyms for intensity.
   - Apply the conflict and caution rules in `references/algorithm.md`.
6. Generate a strategy card.
   - State the audience insight as a hypothesis.
   - Map a verified feature to a customer outcome and then to the selected mechanism.
   - Provide the proposition, message angle, proof, call to action, channel, and failure condition.
7. Design a test.
   - Read [references/research-methods.md](references/research-methods.md) to distinguish causal tests, factorial mechanism tests, attribute tradeoff research, and proposition prioritization.
   - Compare the proposed treatment with a meaningful control.
   - Choose one primary behavioral metric and at least one trust or harm guardrail.
   - Define the segment before observing results; do not reverse-engineer vulnerable targets.
8. Audit the final output.
   - Remove fabricated urgency, hidden defaults, shame, scapegoating, addictive reward schedules, and deterministic brain claims.
   - Preserve user agency, disclosure, reversibility, and easy exit.

## Required output

Return sections in this order:

1. **Truth ledger**: verified, assumed, unknown.
2. **Diagnosis**: objective, bottleneck, audience context.
3. **Domain selection**: scores or qualitative strength, primary, optional secondary, and reasons for excluding close alternatives.
4. **Supporting mechanism audit**: when material, module, opportunity evidence, readiness gaps, and relationship to the selected domain.
5. **Strategy card**: mechanism, proposition, proof, message, CTA, channel, and boundary conditions.
6. **Experiment**: control, treatment, primary metric, guardrail metric, duration or stopping rule, and disconfirming result.
7. **Ethics check**: risks found and mitigations.

Prefer plain language in customer-facing copy. Keep the Latin domain names in analysis or internal labels unless the user explicitly wants them exposed.

## Domain routing

- **Superbia**: identity, mastery, distinction, or credible status signaling.
- **Avaritia**: economic value, gain, loss, ownership, or price justification.
- **Luxuria**: anticipated experience, sensory vividness, affect, or immediate desire.
- **Invidia**: social comparison, aspirational peers, reference groups, or competitive contrast.
- **Gula**: repeat use, reward learning, variety, satiation, or habit loops.
- **Ira**: blocked goals, unfairness, frustration, reactance, complaint recovery, or challenger positioning.
- **Acedia**: procrastination, present bias, choice overload, effort, delay, or activation friction.

Read [references/evidence.md](references/evidence.md) when making scientific claims, explaining why a mechanism was chosen, or extending an algorithm. Do not turn correlational or group-level findings into claims about an individual's brain.
