---
name: dream-thinking
description: Reflective sleep-and-dream heuristic for learning from recent experience. Use when the user asks to sleep on something, dream about it, reflect overnight, learn from yesterday, or extract lessons after a meaningful task, conversation, or debugging session. Avoid for first-pass analysis, simple factual lookups, direct execution, or tasks that do not benefit from reflection.
---

# Dream Thinking

Turn fresh context into a short sleep → dream → wake cycle that produces clearer understanding by morning.

Read recent context first. Ground every dream in real material from the active session and any prior dream logs the user explicitly provides.

Adjacent skills: **brainstorming** (divergent generation) → **thinking** (convergent planning) → **recursive-thinking** (adversarial stress-testing) → **dream-thinking** (retrospective learning).

Use this only when there is fresh, meaningful material to reflect on and plain analysis is not already enough.
If the task is first-pass planning or diagnosis, use **thinking** or **recursive-thinking** instead.

Typical chaining:
- use **thinking** to converge on a plan
- use **recursive-thinking** to challenge that plan when risk or ambiguity is high
- use **dream-thinking** after execution, conflict, or reflection-worthy experience

## How it works

Symbolic recombination as a reasoning tool. **Sleep** = gather tensions. **Dream** = re-encode through concrete imagery that preserves structural relationships. **Interpret** = extract what the imagery reveals that literal analysis missed. **Wake** = convert to action. The value comes from defamiliarization — breaking literal fixation by seeing familiar material through an unfamiliar lens.

## Modifiers

Works with zero arguments. These natural-language modifiers adjust behavior when provided:

- **Tone:** "nightmare version" (risk-focused), "show what's working" (alignment-focused), or balanced (default)
- **Depth:** "quick dream" (1 scene, brief) vs. full cycle (1-3 scenes, detailed — default)
- **Focus:** "dream about X" (targeted) vs. general (everything recent — default)

## Workflow

1. **Prepare for sleep.** List recent tensions, unanswered questions, and repeated patterns. Prefer the smallest set that captures the real conflict. If no genuine tension exists, offer a brief reflection instead — a forced dream teaches nothing.
2. **Enter dream state.** Recombine fragments into 1-3 symbolic scenes. One scene for a single tension; more only when materially different patterns need reconciliation.
3. **Interpret.** Explain what each scene suggests using both mood and function categories. Apply apophenia guards before committing.
4. **Wake up.** Convert to explicit lessons, changed understanding, and concrete next actions.
5. **Record.** Emit a dream log using [dream-log-template.md](./references/dream-log-template.md). If the environment provides a user-approved memory system, save non-obvious or decision-relevant motifs there for longitudinal tracking. Otherwise, keep the insight in the dream log only.

## Brief Reflection Fallback

If there is no real tension, skip dream imagery and output:
1. What happened
2. What seems to matter
3. What to watch next
4. What action, if any, follows

## Symbol Quality

A good symbol **maps to a specific source element** (not a vague mood), **preserves structural relationships** (if A depends on B, the symbol keeps that), **highlights a property literal description obscures** (brittle dependency → glass), and **can be interpreted in more than one way**.

A weak symbol maps to a general feeling, could be swapped for any other image, has one obvious interpretation, or adds atmosphere without insight.

**Falsifiability test:** someone familiar with the source material should be able to judge whether the mapping is accurate or stretched. If it works equally well for any source, it is too vague — replace it.

## Dream Categories

**By mood:** Pleasant (alignment, strengths) · Nightmare (risk, hidden regressions) · Vision (plausible future, pattern glimpse) · Dream within a dream (false framing, recursive observation).

**By function:** Integration (unexpected connections across subsystems) · Regression (something working breaks) · Transformation (something changes purpose) · Absence (something expected is missing) · Conflict (two elements can't coexist).

Mood sets the scene. Function guides interpretation.

## Apophenia Guards

- **Outsider test:** would someone who didn't create this symbol reach the same interpretation?
- **Prediction test:** does this interpretation predict something verifiable?
- **Alternative test:** could a different symbol have generated the same interpretation? If yes, the insight comes from prior knowledge, not the dream.

An interpretation that fails all three is decoration. Drop it or flag it as speculative.

## Decision Rules

- Dream imagery is a reasoning tool, not an excuse for ungrounded fiction.
- Keep interpretation strength proportional to evidence strength.
- Name whether each conclusion is observed, inferred, or unknown.
- Recurring motifs are pattern candidates, not truths — meaningful only when they change interpretation across runs.
- End with actionable insight unless the user wants interpretation only.
- If plain analysis already surfaced the key insight, keep the cycle brief. The dream should add something.

## Output Contract

For a full cycle, output:
1. **Dream** — symbolic scenes with source-to-symbol mapping inline
2. **Interpretation** — what each scene suggests, with apophenia guards applied
3. **Dream Log** — structured log (canonical output) with morning insight, next actions, confidence, motif tracking

For the brief reflection fallback, output the reflection only.

## Avoid

- ungrounded poetry that teaches nothing
- inventing source material not present in context
- forcing categories the context doesn't support
- using symbols that sound vivid but do not change interpretation, prediction, or action
- full dream cycle when brief reflection would serve better
