# Research methods for Vitia hypotheses

These methods measure causal effects or preference structure. They are not
persuasion mechanisms and must not change a Vitia domain score. Use domain and
mechanism analysis to generate hypotheses, then choose the design that answers
the actual research question.

## Method routing

| Research question | Default method | Primary result |
|---|---|---|
| Did one treatment cause a behavioral change? | Randomized controlled experiment | Treatment-control difference with uncertainty |
| Do two mechanisms interact? | Randomized factorial experiment | Main effects and interaction |
| What tradeoffs do customers make among offer attributes? | Choice-based conjoint / discrete-choice experiment | Attribute-level preference estimates and choice simulation |
| Which standalone propositions are relatively most and least important? | Case 1 Best–Worst Scaling | Relative item scores |

Do not use conjoint or Best–Worst Scaling to claim campaign causality. Do not
use an A/B test to infer the complete preference structure behind a click.

## 1. Randomized mechanism test

**Inputs:** eligible population, randomization unit, control, one changed
mechanism, primary behavioral outcome, guardrail, duration or stopping rule.

1. Write the treatment contrast and disconfirming result before exposure.
2. Randomize at the unit that can remain independent; use cluster randomization
   when users, teams, stores, or communities can contaminate one another.
3. Hold the offer, proof, audience rules, and measurement constant apart from
   the named treatment.
4. Check allocation, exposure, attrition, missingness, and sample-ratio mismatch.
5. Estimate the treatment-control difference with an interval, not only a
   significance label. Analyze predefined heterogeneous effects sparingly.
6. Report the guardrail and null or adverse results with the primary outcome.

For a binary metric, the transparent baseline estimate is:

```text
absolute difference = conversions_treatment / exposed_treatment
                    - conversions_control / exposed_control
```

Use an estimator appropriate to the randomization and outcome for inference.
Peeking, repeated testing, clustered data, and covariate adjustment require a
prespecified analysis rather than a universal cached threshold.

## 2. Factorial mechanism test

Use a factorial design when two supporting mechanisms cannot be separated in
normal delivery and traffic can support the interaction estimate.

1. Create four cells: neither mechanism, A only, B only, and A+B.
2. Randomize independently to A and B when operationally valid.
3. Estimate the main effect of each factor and the A×B interaction.
4. Treat an interaction as a separate estimand; do not infer it by comparing
   whether one cell is significant and another is not.
5. Keep enough observations for the interaction, which is usually less precise
   than a main effect.

## 3. Choice-based conjoint / discrete-choice experiment

Use this for offer design and price-feature tradeoffs, not for testing a finished
headline.

1. Derive a small set of decision-relevant attributes from product truth and
   qualitative research. Make levels realistic, mutually intelligible, and
   operationally possible.
2. Generate an efficient or balanced set of choice tasks. Include a realistic
   opt-out or current-state option when customers can decline the market choice.
3. Randomize profile and task order and prevent dominated or impossible bundles.
4. Ask respondents to choose among complete profiles; reserve holdout tasks.
5. Estimate level utilities with a model suited to the sample and design, then
   validate prediction on holdouts and inspect heterogeneity.
6. Simulate only feasible market alternatives. Report sampling, model, and
   external-validity limits.

Price coefficients and willingness-to-pay ratios can be unstable or misleading
when price is unrealistic, preferences are heterogeneous, or model assumptions
are weak. Never use inferred utilities as diagnoses of an individual.

## 4. Case 1 Best–Worst Scaling

Use this to prioritize standalone value propositions, proof points, objections,
or desired outcomes when ordinary rating scales produce ties or scale-use bias.

1. Define a single construct and a nonredundant item list.
2. Build repeated subsets so items appear approximately equally often and in
   varied combinations and positions.
3. In each subset, ask for the most and least important item.
4. As a transparent descriptive baseline, compute for item `i`:

```text
count score_i = (best selections_i - worst selections_i) / appearances_i
```

The score ranges from `-1` to `1`. Use a conditional-logit or hierarchical model
when population inference, covariates, or individual heterogeneity matter.
5. Check design balance, task comprehension, position effects, and stability.
6. Validate the highest-ranked propositions in a behavioral experiment before
   calling them effective messages.

## Evidence and limits

- Neyman, J. (1923/1990). [On the Application of Probability Theory to Agricultural Experiments. Essay on Principles. Section 9](https://doi.org/10.1214/ss/1177012031). Provides a foundational randomization-based treatment-effect framework.
- Rubin, D. B. (1974). [Estimating Causal Effects of Treatments in Randomized and Nonrandomized Studies](https://doi.org/10.1037/h0037350). Formalizes causal effects through potential outcomes and assignment mechanisms.
- Green, P. E., & Srinivasan, V. (1990). [Conjoint Analysis in Marketing: New Developments With Implications for Research and Practice](https://doi.org/10.1177/002224299005400402). Reviews conjoint measurement, reliability, validity, and choice simulation.
- Louviere, J. et al. (2013). [An Introduction to the Application of (Case 1) Best–Worst Scaling in Marketing Research](https://doi.org/10.1016/j.ijresmar.2012.10.002). Explains Case 1 BWS theory, application, interpretation, and limitations.

The portable cache is the question-to-design routing and transparent baseline
algorithm. Sample size, estimator, stopping rule, and multiplicity adjustment
must be chosen for the actual design rather than copied as universal constants.
