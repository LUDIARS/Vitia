# UX, action discovery, and onboarding audit

## Contents

1. Scope and neutrality
2. Action-discovery model
3. Tutorial algorithm
4. First-stage and peak-stage continuity
5. Observational play walkthrough
6. Vitia integration and metrics
7. Source boundary

## 1. Scope and neutrality

Use this audit when a customer or player must discover an action, understand a
system, complete a tutorial, or reach first value. Do not infer usability from a
genre, visual style, reputation, or a statement such as “this is intuitive.”

Run the same tasks with names and designer explanations hidden. Evaluate what a
representative user can perceive, predict, do, and recover from using the actual
experience.

## 2. Action-discovery model

Trace each required action through six observable links:

```text
user goal -> available action -> perceivable signifier -> attempted action
          -> system feedback -> recovery or next useful state
```

1. **User goal:** State what the user is trying to accomplish at this moment.
2. **Available action:** Verify that the interaction is actually possible and
   accessible with the current controls.
3. **Signifier:** Identify the visible, audible, spatial, textual, or motion cue
   that suggests where and how to act.
4. **Attempt:** Record the first action, hesitation, misclick, and workaround
   without explaining the intended answer.
5. **Feedback:** Check whether the result is timely, legible, and attributable to
   the user's action.
6. **Recovery:** Provide undo, retry, skip, help, or a safe return path.

Treat affordance and signifier as different jobs. The affordance concerns what
the user can do; the signifier helps the user perceive or predict it. A prominent
button can still promise the wrong action, and a possible action can remain
undiscoverable.

## 3. Tutorial algorithm

Teach the smallest complete unit that produces meaningful value.

1. Define the prerequisite knowledge and one target action.
2. Show the target in the same context where it will be used.
3. Give one concise cue and allow a safe attempt.
4. Return immediate, action-specific feedback.
5. Require the action again in a slightly different context to check transfer.
6. Fade prompts as demonstrated competence increases.
7. Keep replay, help, control reference, accessibility alternatives, and skip
   available without punishment.
8. Measure unaided success later; tutorial completion alone is not learning.

Avoid front-loaded text dumps, teaching several interacting systems at once,
permanent prompts, surprise failure for an unintroduced rule, and rewards that
make users click through without understanding.

## 4. First-stage and peak-stage continuity

Compare the first meaningful stage with the experience's most valuable or most
enjoyable stage. The first stage should teach the grammar of the real experience,
not a disposable mini-game or a promise that later systems do not fulfill.

Build a continuity matrix:

| Dimension | First meaningful stage | Peak-value stage | Gap to resolve |
|---|---|---|---|
| Core player/customer goal | | | |
| Required actions | | | |
| Decision or skill | | | |
| Feedback and reward | | | |
| Distinctive product promise | | | |
| Failure and recovery | | | |
| Paid boundary, if any | | | |

For every peak-stage requirement, identify where it is introduced, practiced,
combined, and later recalled. For every first-stage element, identify whether it
remains meaningful later. A short experience may legitimately make its first
stage its peak stage; do not assume a long escalation curve is superior.

## 5. Observational play walkthrough

Use a developer-observer walkthrough or think-aloud session to expose mismatches
between intended and perceived design.

1. Define representative tasks without describing the solution.
2. Before each interaction, record what the participant appears to notice and
   ask what they expect an action to do without leading them.
3. Record the action, result, interpretation, recovery, and time to resume.
4. Classify each breakdown:
   - action unavailable or inaccessible;
   - signifier missed;
   - mapping misunderstood;
   - feedback absent, delayed, or ambiguous;
   - prerequisite concept missing;
   - recovery path missing;
   - tutorial prompt understood but not transferred.
5. Fix one link at a time and repeat with new representative participants.

Designer commentary is diagnostic context, not user evidence. Do not count an
explanation given during observation as successful discoverability.

## 6. Vitia integration and metrics

- **Acedia:** discoverability, cognitive load, time to first value, and recovery.
- **Luxuria:** the first truthful demonstration of the desired experience.
- **Superbia:** competence feedback and authentic mastery without status shame.
- **Gula:** repeatable value and prompt fading without compulsive reinforcement.
- **Ira:** frustration caused by blocked goals, ambiguous rules, or lost control.
- **Avaritia:** locating price, value, and paid boundaries before commitment.

Use task success, unaided action discovery, error recovery, time to first value,
prompt dependence, later transfer, abandonment, accessibility failures, and
support contacts. Pair completion with comprehension and customer outcome.

```text
Neutral task name:
Representative user and context:
Target action and user value:
Available affordance:
Expected signifier:
Observed first action:
Feedback and recovery:
Tutorial step and fade rule:
Later transfer task:
Primary outcome:
Harm or accessibility guardrail:
```

## 7. Source boundary

The workflow is reinforced by the Notion lesson
[#7. ボタンはなぜ膨らむのか？](https://app.notion.com/p/1b439cbfbab9806fa993fef0dbde8463),
which explicitly centers game clarity, affordance/signifier analysis,
developer-observer play commentary, tutorials, and comparing a first stage with
the most enjoyable stage. Its linked
[ゲームデザイン課題](https://app.notion.com/p/23839cbfbab981ad884bc91bec1ca46d)
provides concrete mappings from cues to desired actions and from first-stage
learning to later play.

The page exposes an attached `UXを考える.pptx` and several bookmark blocks, but
their binary contents and target URLs were not returned by the available Notion
integration. This reference therefore does not attribute unobserved slide or
bookmark claims to those materials.

Academic interpretation is bounded by Hartson's distinction among interaction
affordances, cognitive-load research, and worked-example fading; see
[evidence.md](evidence.md). These sources support testable design procedures,
not a universal tutorial sequence or guaranteed conversion effect.
