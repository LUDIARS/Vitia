# Vitia selection and composition algorithm

## Contents

1. Label-neutrality invariant
2. Input contract
3. Domain scoring
4. Selection rules
5. Composition rules
6. Strategy generation
7. Experiment protocol

## 1. Label-neutrality invariant

Complete the evidence pass before exposing the proposed Vitia domain or any
moralized description to the evaluator.

1. Replace product, category, reputation, and domain names with neutral IDs.
2. Record only observable features, outcomes, costs, behavior, constraints,
   provenance, and uncertainty.
3. Diagnose the bottleneck in plain language.
4. Score the normalized evidence.
5. Restore the names without changing signals.
6. Require the primary, secondary, penalties, and guardrails to remain equal.

In compact form, for evidence `E` and any context-only relabeling `L`:

`score(E, L1) = score(E, L2) = score(E)`

If a relabeling changes the result, the evaluation is contaminated. Discard the
domain conclusion, mark it exploratory, and repeat the evidence extraction.
The `label_context` input in `scripts/score_vitia.py` is validated and reported
but deliberately excluded from every score.

## 2. Input contract

Collect the following. Mark absent items as unknown.

- **Offer**: features, customer outcomes, price, switching cost, delivery constraints, and verified proof.
- **Audience**: job to be done, context, awareness stage, alternatives, motivation, objections, and accessibility needs.
- **Objective**: acquisition, conversion, expansion, retention, reactivation, or recovery.
- **Environment**: channel, timing, public versus private use, frequency, and competitive set.
- **Evidence**: research, analytics, interviews, experiments, confidence, and provenance.
- **Safety**: age, vulnerability, regulated context, privacy, reversibility, and foreseeable harms.
- **Context-only labels**: artifact name, category name, declared domain,
  reputation, and source framing. Store these separately and never convert them
  into signals without independent evidence.

Never infer sensitive traits, mental states, or neurological states from weak behavioral proxies.

## 3. Domain scoring

Normalize observed signals to `[0, 1]`. Score only signals supported by evidence
from the label-neutral pass. The script uses:

`raw(domain) = weighted mean of observed signals`

`coverage_factor = 0.5 + 0.5 * observed_weight_coverage`

`adjusted(domain) = clamp(raw * (0.6 + 0.4 * confidence) * coverage_factor - risk_penalty, 0, 1)`

The confidence and coverage factors prevent a strong but isolated signal from looking conclusive while retaining a provisional hypothesis. The weights are routing heuristics, not psychometric coefficients. Calibrate them with experiment data for each product.

| Domain | High-value routing signals |
|---|---|
| Superbia | identity relevance, status visibility, aspiration, public consumption, credible proof |
| Avaritia | economic stakes, measurable value, loss salience, price sensitivity, ownership potential |
| Luxuria | sensory vividness, affect intensity, immediacy, trialability, novelty, reward clarity |
| Invidia | social comparison, visible reference group, aspiration, attainability, deservingness |
| Gula | repeat frequency, reward clarity, variety potential, habit opportunity, satiation risk |
| Ira | frustration, perceived injustice, blocked goal, autonomy threat, repairability |
| Acedia | decision friction, effort, delay, choice complexity, present bias, reversibility |

Use `scripts/score_vitia.py --example` to see the machine-readable schema.

## 4. Selection rules

1. Reject blocked uses before scoring.
2. Select the highest adjusted score as primary when it is at least `0.45`.
3. Label the result exploratory when no score reaches `0.45`, confidence is below `0.50`, or signal coverage is below `0.50`.
4. Select a secondary only when:
   - its score is at least `0.50`;
   - its signal coverage is at least `0.50`;
   - it is within `0.15` of the primary;
   - it has a different job in the customer journey; and
   - the pair is not prohibited.
5. Use no more than two active domains in one treatment. Test additional mechanisms separately.
6. Explain why any near-scoring domain was excluded.

## 5. Composition rules

Assign the primary to the main bottleneck and the secondary to proof, activation, or continuity.

| Pair | Recommended division of labor |
|---|---|
| Superbia + Avaritia | identity or mastery promise + economic justification |
| Superbia + Invidia | desired identity + attainable peer reference; audit status shame |
| Avaritia + Luxuria | rational value proof + vivid product experience |
| Avaritia + Acedia | payoff clarity + low-friction next action |
| Luxuria + Gula | initial experience + repeat-value design; mandatory compulsion audit |
| Invidia + Acedia | relatable peer pathway + smallest next action |
| Gula + Acedia | repeat-value loop + easy activation and return |
| Ira + Acedia | acknowledge blocked goal + restore control with an easy repair path |

Do not combine **Ira + Invidia** for persuasive targeting: grievance plus comparison readily becomes humiliation, scapegoating, or polarization. Treat **Luxuria + Gula** as high risk in gambling-like, sexual, substance, eating, or child-directed contexts.

## 6. Strategy generation

Build one strategy card per treatment:

```text
Counterfactual rename check:
Audience hypothesis:
Bottleneck:
Primary domain / job:
Secondary domain / job (optional):
Verified feature -> customer outcome -> mechanism:
Proposition:
Proof:
Message angle:
CTA:
Channel and moment:
Boundary condition:
```

Require a truth-bearing bridge at `feature -> outcome`. If the bridge is unknown, propose research rather than copy.

## 7. Experiment protocol

For each strategy:

1. Define a neutral or current-experience control.
2. Change one mechanism at a time where practical.
3. Preselect one primary outcome: qualified conversion, activation, retention, recovery, or willingness to pay.
4. Add a guardrail: refund, regret, complaint, unsubscribe, hide/report, trust rating, or harmful overuse.
5. Define the target population and exclusion criteria before analysis.
6. Define a minimum sample or decision horizon appropriate to the traffic and effect size.
7. Record a disconfirming result, such as conversion lift accompanied by unacceptable regret or complaint growth.
8. Promote a tactic only when value and guardrail metrics both pass.

Do not call a result causal without an appropriate control and assignment method.
