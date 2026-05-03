# Prompt Patterns And Provider Notes

Use this reference when the main prompt-engineering workflow needs a concrete
pattern, provider-specific reminder, or source-grounded checklist. Keep the
main prompt portable unless the target runtime makes a provider detail
material.

## Source Synthesis

The source set converges on a few durable ideas:

- start with a clear task, context, constraints, and output contract
- use examples when the task requires judgment, style calibration, or exact
  format imitation
- make evaluation part of prompt development, not an afterthought
- isolate variable and untrusted input from stable instructions
- prefer small, measurable prompt changes over broad rewrites
- account for provider and model behavior instead of assuming one universal
  prompt style
- optimize prompts for operational concerns such as token cost, latency,
  cacheability, safety, and maintainability after correctness is measurable

Primary sources:

- OpenAI prompt engineering guide:
  <https://developers.openai.com/api/docs/guides/prompt-engineering>
- OpenAI resilient-prompt eval flywheel:
  <https://developers.openai.com/cookbook/examples/evaluation/building_resilient_prompts_using_an_evaluation_flywheel>
- OpenAI GPT-5 prompting guide:
  <https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide>
- OpenAI prompt caching guide:
  <https://developers.openai.com/api/docs/guides/prompt-caching>
- Anthropic Claude prompting best practices:
  <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>
- Anthropic test and evaluate guidance:
  <https://platform.claude.com/docs/en/test-and-evaluate/develop-tests>
- Anthropic prompt engineering tutorial:
  <https://github.com/anthropics/prompt-eng-interactive-tutorial>
- Google Cloud prompt engineering overview:
  <https://cloud.google.com/discover/what-is-prompt-engineering>

Adjacent skill examples from the supplied source set:

- <https://skills.sh/google-labs-code/stitch-skills/enhance-prompt>
- <https://skills.sh/github/awesome-copilot/prompt-builder>
- <https://skills.sh/wshobson/agents/prompt-engineering-patterns>
- <https://skills.sh/supercent-io/skills-template/prompt-repetition>
- <https://skills.sh/jeffallan/claude-skills/prompt-engineer>
- <https://skills.sh/github/awesome-copilot/ai-prompt-engineering-safety-review>

Use these as adjacent workflow inspiration, not as structure to copy. This repo
keeps its own frontmatter, folder structure, and concise workflow style.

## Prompt Anatomy

Use only the sections the task needs.

```text
Role or stance:
Task:
Context:
Inputs:
Tools and boundaries:
Output format:
Examples:
Quality bar:
Failure handling:
```

Guidance:

- Put immutable policy and task framing before long variable context.
- Put user-controlled, retrieved, or external content behind explicit labels.
- Make the output contract concrete when another program or human workflow
  depends on it.
- Name allowed uncertainty. Tell the model when to ask for clarification, make a
  labeled assumption, refuse, or return a partial result.
- If examples conflict with instructions, expect examples to win in practice;
  remove or rewrite the conflicting example.

## Pattern Selector

- **Direct instruction:** use for simple, one-shot behavior with low ambiguity.
- **Structured prompt:** use when the model must keep task, context, constraints,
  and output format distinct.
- **Few-shot examples:** use when tone, format, classification boundary, or
  judgment is hard to specify abstractly.
- **Schema or structured output:** use when downstream code parses the result.
- **Tool-use prompt:** use when the model must decide whether, when, or how to
  call tools.
- **Chain-of-work instructions:** use when the task has a required sequence, but
  ask for concise reasoning artifacts rather than hidden chain-of-thought.
- **Rubric prompt:** use for grading, review, scoring, or ranking.
- **Repetition:** use sparingly for non-negotiable constraints the model has
  empirically dropped; prefer clearer structure first.

## Provider Notes

Verify current official provider docs when prompt behavior depends on model,
API, structured-output, tool-calling, reasoning, caching, pricing, or safety
settings. Treat provider notes here as reminders, not a substitute for current
docs.

### OpenAI

- Check current official OpenAI docs when the prompt depends on a specific API,
  model, structured-output mode, tool behavior, prompt caching, or model upgrade.
- For cache-aware prompts, keep stable instructions and large reusable context
  in a stable prefix, and put per-request data later.
- For GPT-5-family prompt work, prefer model-specific official guidance when
  upgrading existing prompts or changing reasoning and verbosity behavior.
- When using structured outputs or tool calls, keep prompt instructions aligned
  with the API schema or tool definition instead of duplicating conflicting
  requirements.

### Anthropic Claude

- Claude prompts often benefit from explicit structure and clearly delimited
  context. XML-style tags can be useful when they make boundaries unambiguous.
- Put examples and evaluation cases close to the behavior they are meant to
  teach.
- Use Anthropic's test-and-evaluate guidance when the main risk is regression,
  not first-pass prompt wording.

### Google / Gemini

- Use provider-specific Gemini guidance when the target runtime is Gemini or
  Vertex AI. The generic principles still apply, but API capabilities,
  grounding, multimodal inputs, and safety settings may change the prompt shape.

## Safety And Injection Checks

Prompt changes that process untrusted content should include checks for:

- instruction override attempts inside user, retrieved, file, or webpage text
- data exfiltration requests or attempts to reveal hidden instructions
- tool calls that could mutate state, spend money, send messages, or cross trust
  boundaries
- unsafe reliance on generated citations, calculations, code, or legal/medical
  claims without verification
- prompt examples that accidentally teach policy bypasses

Escalate to a security skill when prompt injection, data exposure, tool abuse,
or tenant/user boundary violations are the primary risk.
