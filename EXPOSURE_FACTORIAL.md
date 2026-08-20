# Epistemic Exposure Factorial (T × M × P × H)

This document adds an experimental information-exposure layer to the OAP prototype.

It does **not** add new OAP polity axes.

OAP polity semantics remain the governance-level model. The exposure profile below is a controlled experimental description of what an Agent is actually allowed to observe in a specific run.

## 1. Four Boolean exposure factors

For a webpage diagnosis task define:

- `T` — Text evidence exposed: extracted DOM / accessibility / textual page evidence is shown.
- `M` — Multimodal evidence exposed: rendered screenshot / image / video evidence is shown.
- `P` — Prior exposed: an existing hypothesis or another Agent's current belief is shown.
- `H` — High context exposed: broader task narrative, history, intent, deployment context, or surrounding situational context is shown.

Thus:

```text
E = (T, M, P, H) ∈ {0,1}^4
```

which yields 16 full-factorial exposure cells.

## 2. Interpretation

Examples:

- `1000`: text-only blind inspection.
- `0100`: multimodal-only blind inspection.
- `1100`: text + multimodal evidence, but no prior and no high context.
- `0110`: multimodal evidence plus prior; useful for measuring prior contamination of visual interpretation.
- `1101`: text + multimodal + high context, but no prior.
- `1111`: fully exposed condition.

These are experimental cells, not Agent personalities and not polity names.

## 3. Channel isolation rules

The experiment is only meaningful if channels do not leak into each other.

- `P=0` means the prompt must not indirectly reveal the existing hypothesis through `H`.
- `H=0` means no task-history narrative beyond the minimum question required to answer.
- `T=0` means no extracted DOM/text channel. Text that is visibly present *inside the rendered image* remains part of `M`; the experiment controls information channels, not semantic OCR impossibility.
- `M=0` means no screenshot/image/video is supplied.
- Constant response-format instructions are not counted as `T`; `T` specifically denotes webpage textual evidence.

## 4. Synthetic webpage pilot fixture

The first live API pilot uses a reproducible synthetic checkout-page failure.

Ground truth label:

```text
FRONTEND_STATE
```

The fixture is constructed so that multimodal and DOM evidence indicate a stuck frontend loading state while an intentionally incorrect prior points toward a backend/API-cache outage.

This is not intended as a realistic benchmark. It is a channel-effect sanity check before moving to real webpages.

## 5. Full-factorial analysis

For every run record:

- profile bits `T/M/P/H`;
- model;
- predicted label;
- confidence if available;
- correctness against the fixture ground truth;
- compact evidence statement;
- provider token usage;
- latency;
- parse/API failure state.

Primary pilot statistic:

```text
Accuracy(T,M,P,H)
```

Main effects are estimated descriptively as:

```text
Effect(X) = mean(correct | X=1) - mean(correct | X=0)
```

for `X ∈ {T,M,P,H}`.

The 16-cell pilot is too small for strong inferential claims. It exists to validate the runtime, expose surprising interactions, and motivate replicated runs.

## 6. Blind → commit → unblind protocol

The same fixture also supports a cross-modal blind-review pilot:

```text
Phase 1
Main: text/high-context channel → initial hypothesis H_M
Subagent: multimodal channel, without H_M → independent hypothesis H_S

Phase 2
Freeze H_M, H_S and their evidence provenance.

Phase 3
Reveal H_M to the Subagent and/or H_S to Main.
Run targeted verification and produce H_final.
```

This approximates **reciprocal epistemic blinding / cross-modal blind review**. It is not claimed to be identical to classical clinical double-blind methodology.

Useful comparisons:

- blind Seed vs informed Seed;
- Main revision after blind Seed report vs Main revision after informed Seed report;
- error correlation across modalities;
- whether exposure to an incorrect prior reduces independent evidence recovery.

## 7. Relation to OAP

The exposure lattice is deliberately separate from OAP semantics:

```text
Polity semantics
    ↓ chooses / constrains information governance
Operationalization
    ↓ determines runtime permissions and routing
Exposure profile E=(T,M,P,H)
    ↓ actual information presented in this run
Agent output
    ↓
Emergent behavior
```

A particular polity may *tend* to produce particular exposure profiles under one implementation, but the mapping is an operationalization hypothesis rather than a definition.

For the current DeepSeek + Seed reference implementation:

- `01`-like runs are naturally compatible with blind multimodal investigation (`P=0`, reduced shared context).
- `11`-like runs are naturally compatible with informed multimodal investigation (`P=1` and/or richer `H`).

The experiment should test whether those mappings are useful rather than assume that they are true.
