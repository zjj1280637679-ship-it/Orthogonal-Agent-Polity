---
name: oap-attractor-experiment
description: Implement and validate the DeepSeek-main plus multimodal-Seed-subagent OAP attractor escape experiment in this repository. Use this skill when working on the reference implementation, provider integration, MCP bridge, polity routing, experiment cases, live Ark runs, or result analysis.
---

# OAP Attractor Experiment Skill

You are implementing an empirical reference experiment, not redesigning the theory.

Read these files before changing code:

1. `THEORY.md`
2. `HARNESS_TASK.md`
3. `EXPERIMENT.md`
4. `SECURITY.md`

## Non-negotiable architecture

- Main / Sovereign: highest-capability configured DeepSeek V4 GA model, text-first in this experiment.
- Multimodal Subagent: default `doubao-seed-2-0-lite-260428`.
- Main never receives the original multimodal asset in the experimental condition.
- Subagent may observe/investigate but may not change the world.
- Main retains final decision authority.
- OAP polity is a governance constraint imposed by Main on Subagent, not a symmetric peer protocol.

## The four modes must be real information/permission gates

`00` — no Main-recent-context injection; no autonomous investigation.

`10` — inject Main hypothesis/recent context; no autonomous investigation.

`01` — hide Main hypothesis/recent reasoning; allow bounded independent investigation.

`11` — inject Main hypothesis/recent context; allow bounded independent investigation.

Do not implement the modes as four labels that all receive the same prompt and tools.

## Implementation order

1. Create `implementation/` package and offline fake-provider tests.
2. Implement polity/context/investigation gates.
3. Implement secret-safe Ark client.
4. Implement multimodal Seed evidence report.
5. Implement MCP server/bridge usable from DeepSeek-TUI.
6. Build deterministic synthetic experiment cases.
7. Run offline 4-polity smoke experiment.
8. Only then run live provider probes.
9. Run the live experiment on the same case set for all four polities.
10. Write sanitized results and a Markdown report.

## Evidence contract

Subagent returns observations, supporting/contradicting evidence, alternatives, uncertainty, and investigation steps. It does not return an authoritative final answer on behalf of Main.

The correct behavior is not "always disagree with Main". It is "remain falsifiable by external evidence".

## Security

A GitHub Repository Secret named `HUOSHANYINQINGAPI` exists for live Ark experiments. The workflow may map it to the runtime credential variable, but its value must never be committed or inserted into prompts/logs/artifacts.

Do not print environment variables. Do not dump HTTP headers. Never weaken this rule to debug a provider failure.

## Model IDs

Do not guess exact DeepSeek GA model IDs. Read configured IDs and probe them with tiny calls. Record only sanitized availability, returned model ID/name, usage, latency, and provider request ID.

## Experiment integrity

- Answer keys are evaluator-only.
- Blind modes must not receive Main's hypothesis by accidental logging/prompt reuse.
- Use fresh Main sessions for independent trials.
- Run identical cases across 00/10/01/11.
- Preserve false-correction and uncertainty controls, not only easy correction cases.
- Keep v0.1 exploratory; do not claim statistical proof from a tiny sample.

## Completion behavior

When the implementation is complete, leave:

- runnable commands in `implementation/README.md`;
- unit tests and polity tests passing;
- sanitized result data;
- an experiment report describing observed effect sizes and failures;
- a concise note explaining any DeepSeek-TUI integration limitation that forced a design change.

If a live secret is unavailable in the current execution environment, complete all offline work and stop at the live-test boundary rather than requesting the credential in chat.
