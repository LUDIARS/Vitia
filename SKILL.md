---
name: vitia
description: "Design label-neutral, ethical, evidence-aware marketing, UX, onboarding, pricing, and monetization strategies. Analyze observed product and audience evidence before mapping it to the seven Vitia lenses: Superbia, Avaritia, Luxuria, Invidia, Gula, Ira, and Acedia. Use for positioning, conversion or retention diagnosis, tutorials, first-value UX, in-game purchases, subscriptions, price fairness, sales hypotheses, behavioral mechanisms, and marketing experiments. Never let a product name, category label, moral framing, reputation, or declared deadly-sin domain affect the evidence or score."
---

# Vitia

## Governing rule — label neutrality (highest priority)

This rule overrides every other Vitia routing or composition instruction.

- Extract observable facts, customer outcomes, costs, behavior, and constraints before reading a proposed domain conclusion.
- Treat product names, category names, the seven Latin names, moral descriptions, reputation, and source language such as “human bug” or “exploitation” as context-only labels.
- Require the same evidence to produce the same score, guardrails, and recommendation regardless of those labels.
- Apply the Latin names only after the bottleneck and candidate mechanisms have been identified in plain language.
- Run a counterfactual rename check: replace every name and declared domain with neutral placeholders. If the conclusion changes, discard it and repeat the evidence pass.

When label-neutrality cannot be demonstrated, return an exploratory assessment rather than a domain conclusion.

Treat the seven Latin domains as a strategy-selection interface, not as a scientific taxonomy of people. Convert product truth and audience context into falsifiable marketing hypotheses without deception, coercion, or unsupported neuroscience claims.

## Workflow

1. Run the label-neutral evidence pass.
   - Hide or bracket names, moral adjectives, reputation, and any proposed Vitia classification.
   - Write the objective, observed behavior, customer outcome, cost, friction, and evidence in plain language.
   - Run the counterfactual rename check before scoring.
2. Establish the truth ledger.
   - Record the offer, audience, job to be done, price or cost, proof, constraints, channel, funnel stage, and desired outcome.
   - Separate verified facts, reasonable hypotheses, and unknowns.
   - Ask only for missing facts that could materially change the strategy. Otherwise state assumptions.
3. Screen safety before persuasion.
   - Read [references/ethics.md](references/ethics.md).
   - Stop persuasive optimization when a blocked condition applies. Offer neutral information, user-protective design, or research instead.
4. Audit experience and monetization when material.
   - For discoverability, affordances, tutorials, first-stage design, or time to first value, read [references/ux-onboarding.md](references/ux-onboarding.md).
   - For games or play-like products where the promise depends on rules, challenge, failure, cooperation, competition, spectatorship, or repeat mastery, read [references/game-experience.md](references/game-experience.md) and run `python scripts/audit_game_experience.py <input.json>` when repeatability is useful.
   - For pricing, subscriptions, ads, in-game purchases, randomized rewards, or paywalls, read [references/monetization.md](references/monetization.md).
   - Evaluate the mechanics and outcomes, never the monetization-model name alone.
5. Score the seven domains.
   - Read [references/algorithm.md](references/algorithm.md).
   - For repeatable scoring, run `python scripts/score_vitia.py <input.json>`.
   - Treat missing signals as unknown, never as zero, when making a qualitative assessment.
6. Route supporting mechanisms when the artifact or bottleneck makes them material.
   - Read [references/mechanisms.md](references/mechanisms.md).
   - For repeatable opportunity and readiness auditing, run `python scripts/audit_marketing_mechanisms.py <input.json>`.
   - Keep supporting-module scores separate from the seven-domain scores. Resolve readiness gaps before deployment.
7. Select one primary domain and at most one secondary domain.
   - Read the selected sections of [references/domains.md](references/domains.md).
   - Give each selected domain a distinct job. Do not stack synonyms for intensity.
   - Apply the conflict and caution rules in `references/algorithm.md`.
8. Generate a strategy card.
   - State the audience insight as a hypothesis.
   - Map a verified feature to a customer outcome and then to the selected mechanism.
   - Provide the proposition, message angle, proof, call to action, channel, and failure condition.
9. Design a test.
   - Read [references/research-methods.md](references/research-methods.md) to distinguish causal tests, factorial mechanism tests, attribute tradeoff research, and proposition prioritization.
   - Compare the proposed treatment with a meaningful control.
   - Choose one primary behavioral metric and at least one trust or harm guardrail.
   - Define the segment before observing results; do not reverse-engineer vulnerable targets.
10. Audit the final output.
   - Remove fabricated urgency, hidden defaults, shame, scapegoating, addictive reward schedules, and deterministic brain claims.
   - Preserve user agency, disclosure, reversibility, and easy exit.

## Required output

Return sections in this order:

1. **Neutrality check**: bracketed labels and result of the counterfactual rename check.
2. **Truth ledger**: verified, assumed, unknown.
3. **Diagnosis**: objective, bottleneck, audience context in plain language.
4. **Experience and monetization audit**: when material, discoverability, tutorial, play promise, challenge and recovery, social fairness, repeat value, value exchange, total cost, agency, and revenue-quality guardrails.
5. **Domain selection**: scores or qualitative strength, primary, optional secondary, and reasons for excluding close alternatives.
6. **Supporting mechanism audit**: when material, module, opportunity evidence, readiness gaps, and relationship to the selected domain.
7. **Strategy card**: mechanism, proposition, proof, message, CTA, channel, and boundary conditions.
8. **Experiment**: control, treatment, primary metric, guardrail metric, duration or stopping rule, and disconfirming result.
9. **Ethics check**: risks found and mitigations.

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
