# Label-neutral game-experience integrity audit

## Contents

1. Scope and neutrality
2. Evidence contract
3. Play-promise integrity
4. Challenge, learning, failure, and recovery
5. Player agency and social fairness
6. Repeat value without compulsion
7. Audit algorithm and Vitia integration
8. Source boundary

## 1. Scope and neutrality

Use this audit when the product's value depends on play, challenge, simulation,
competition, cooperation, spectatorship, or repeated mastery. It evaluates the
relationship among the promised experience, rules, player action, feedback, and
outcomes. It does not decide whether a genre, aesthetic, difficulty label, or
monetization model is inherently good.

Hide the title, franchise, genre, reputation, moral description, and proposed
Vitia domain during the evidence pass. The same observed rules and outcomes
must produce the same audit after a counterfactual rename. Treat designer intent
and a slide's confident wording as hypotheses until the playable experience or
representative-user evidence supports them.

## 2. Evidence contract

Record the following before scoring:

- intended player and use context, including relevant prior knowledge;
- one-sentence experience promise and the customer outcome it implies;
- player goal, available actions, rules, constraints, uncertainty, and end state;
- first meaningful stage, peak-value stage, and the path between them;
- success, failure, feedback, retry, help, exit, and accessibility paths;
- solo, cooperative, competitive, and spectator roles;
- what changes across repetitions and what can become saturated;
- paid boundaries and whether payment follows frustration, social pressure,
  depletion, loss, near miss, or accumulated investment;
- evidence source, confidence, and material unknowns.

Do not convert a declared feature such as “deep strategy,” “fair competition,”
or “easy to learn” directly into a positive signal. Observe the decisions,
counterplay, rule parity, unaided task success, or learning transfer it predicts.

## 3. Play-promise integrity

Trace the experience as:

```text
audience context -> promised experience -> player goal -> available action
                 -> rule-created obstacle -> feedback -> measurable outcome
```

1. State the promise in one sentence without genre names.
2. Identify the smallest playable interaction that can truthfully demonstrate it.
3. Verify that obstacles create the intended decision or skill rather than only
   delaying access to value.
4. Check that feedback makes the relationship between action, rule, and outcome
   understandable.
5. Compare the first meaningful stage with the peak-value stage. The first stage
   should teach the grammar of the real experience, not a disposable substitute.
6. Check rule–fiction alignment: presentation may simplify reality, but the
   fiction should help players predict the actual rule unless surprise is the
   tested value.

A one-sentence description is a diagnostic constraint, not a demand that every
product be simple. Extra systems are justified when they reinforce, extend, or
deliberately contrast the central promise and this can be observed.

## 4. Challenge, learning, failure, and recovery

Audit challenge as a learnable relationship, not as a fixed difficulty rating.

1. Define the prerequisite knowledge and the target decision or skill.
2. Give a clear goal and enough uncertainty to make the result meaningful.
3. Observe whether skill, strategy, or understanding can improve the outcome.
4. Make feedback timely and diagnostic: a player should be able to form a better
   next hypothesis, not merely learn that they lost.
5. Provide a proportionate retry, undo, checkpoint, hint, practice, or exit path.
6. Test later transfer without the original prompt.
7. Compare novice and experienced contexts; do not make one presumed knowledge
   level stand in for every player.
8. Separate productive challenge from avoidable confusion, inaccessible input,
   punitive repetition, or pain introduced to sell relief.

Record both successful and failed attempts. A completion rate without the
strategy used, recovery behavior, and later transfer cannot show learning.

## 5. Player agency and social fairness

For cooperation, competition, guilds, rankings, and spectator-facing play:

- define the distinct value sought by the player, teammate, opponent, and
  spectator; winning and producing an interesting contest are not identical;
- verify rule parity, disclosed handicaps, anti-cheat enforcement, matchmaking
  assumptions, and a meaningful route to contest or recover from error;
- distinguish freely chosen cooperation from contribution quotas, gifting debt,
  status shame, or spend pressure;
- let players mute, leave, decline, or change roles without disproportionate loss;
- measure procedural fairness, harassment, social obligation, team abandonment,
  and spend concentration alongside engagement;
- treat a competitive loss followed immediately by a paid power offer as a
  pressure event requiring monetization review.

The “magic circle” and similar labels can organize discussion, but they are not
evidence that participants accepted the same rules. Observe consent, parity,
expectations, and enforcement.

## 6. Repeat value without compulsion

Identify what makes a second or hundredth session valuable:

- new strategic states, opponent behavior, combinations, roles, mastery, or
  expression;
- consequential choices and viable counterplay rather than a solved dominant path;
- variation that changes decisions, not only reward presentation;
- optional social interaction that creates new situations without requiring
  constant availability or spending;
- recovery from satiation through meaningful variety, rest, completion, or exit.

Then run a pressure-stack audit:

```text
trigger -> current emotional state -> action -> reward or loss -> next ask -> exit
```

Escalate review when two or more of these coincide: near miss, player-perceived
control over a random result, variable rewards, loss chasing, social obligation,
status comparison, expiring progress, sunk cost, sleep-disrupting notification,
or an offer placed after failure. Do not optimize a gambling-like near-miss or
compulsive schedule. Preserve budgets, stopping cues, cooling-off, history,
non-random alternatives, and easy exit where payment or material loss is possible.

## 7. Audit algorithm and Vitia integration

Run the deterministic audit with:

```text
python scripts/audit_game_experience.py <input.json>
python scripts/audit_game_experience.py --example
python scripts/audit_game_experience.py --list-signals
```

The four lens scores are evidence-coverage heuristics. They do not measure fun,
diagnose a player, predict sales, or alter either axis of the seven-domain Vitia value/performance profile. Underlying findings may be cited as delivery evidence, with a separate performance judgment. The audit's input and output contract is unchanged in 2.0.0.

- **Play promise:** informs Luxuria's truthful experience and Superbia's mastery
  claim.
- **Challenge and learning:** informs Superbia, Ira, and Acedia through competence,
  blocked goals, feedback, and recovery.
- **Agency and fairness:** informs Invidia, Ira, and Superbia in social play.
- **Repeat value:** informs Gula while distinguishing durable variety from
  compulsion.

For paid boundaries, always combine this audit with [monetization.md](monetization.md).
For action discovery and tutorial transfer, also use
[ux-onboarding.md](ux-onboarding.md).

## 8. Source boundary

The practitioner synthesis was reinforced by eight locally supplied teaching
decks reviewed in full on 2026-07-17 (449 slides): `UX.pptx`, `UXQ.pptx`,
`UXを考える.pptx`, `遊びの哲学.pptx`, `面白さを議論してみよう.pptx`,
`挑戦と失敗.pptx`, `知識と教養.pptx`, and `当たり前を作る話.pptx`.
Particularly relevant sections were the UX flow and self-determination sequence
(`UX.pptx`, slides 2–29), tutorial, memory, signifier, and audience sections
(`UXを考える.pptx`, slides 31–75), play definitions and social-play discussion
(`遊びの哲学.pptx`, slides 3–43), and monetization self-defense cases
(`UXQ.pptx`, slides 37–141).

The decks are teaching and practitioner sources, not outcome studies. Their
specific market shares, payer percentages, optimal frequencies, company claims,
and deterministic neuroscience language were not cached as facts. The audit
retains observable questions and protective boundaries while requiring separate
verification for empirical claims.

Academic boundaries are summarized in [evidence.md](evidence.md). Malone's work
supports testable challenge, fantasy, and curiosity hypotheses; GameFlow is an
evaluation model rather than a validated universal score; game-specific
self-determination research supports autonomy and competence as situated
associations; and near-miss gambling evidence is used as a risk boundary, never
as an engagement recipe.
