# OAP Attractor Escape Experiment v0.1

## Research question

Does an independently governed multimodal Subagent improve a high-capability Main Agent's ability to escape an incorrect reasoning attractor when the decisive evidence is multimodal and hidden from the Main?

This is an empirical question. OAP does not assume that any one polity is globally best.

---

## Minimal attractor model

Let:

- `H0` = Main Agent's initial hypothesis after text-only reasoning.
- `E` = external multimodal evidence unavailable to Main.
- `S_p(E, H0?)` = Subagent evidence report under polity `p`.
- `H1` = Main's final hypothesis after receiving the Subagent report.

The experiment asks whether:

```text
wrong H0 + external evidence + OAP relation -> correct H1
```

and how this probability changes across `p ∈ {00,10,01,11}`.

The mechanism is deliberately described as an **attractor** rather than as a claim about hidden model internals. Operationally, an attractor exists when Main forms a plausible initial hypothesis and tends to continue interpreting later information through that hypothesis.

---

## Hypotheses

### H1 — Multimodal correction

When `H0` is wrong and the hidden multimodal evidence is decisive, access to a multimodal Subagent will improve final correctness over a no-use / narrow-use baseline.

### H2 — Investigative autonomy effect

Holding context openness fixed, `I=1` will improve correction rate on cases where the decisive evidence is outside the Main's initially requested inspection scope.

Comparisons:

- `01 > 00`
- `11 > 10`

### H3 — Context openness effect

Holding investigative autonomy fixed, `C=1` may improve correction when knowing Main's current hypothesis lets the Subagent target a falsification check.

Comparisons:

- `10 vs 00`
- `11 vs 01`

This effect is not assumed to be always positive because Main context can also correlate the Subagent with Main's wrong narrative.

### H4 — Blind decorrelation

`01` may outperform `11` on cases where Main's hypothesis is strongly misleading, because hiding Main's hypothesis preserves an independent evidence path.

### H5 — False-correction tradeoff

More autonomy/openness may increase correction but can also increase false correction. Therefore raw correction rate alone is insufficient.

---

## Experimental unit

One case contains:

```text
case_id
text_context_for_main
asset_path_or_asset_spec
answer_key
initial_attractor_target
narrow_observation_question
open_task_goal
scoring_rubric
```

The answer key and `initial_attractor_target` are evaluator-only metadata and must never enter Main or Subagent prompts before scoring.

---

## Trial protocol

For each case and polity:

1. Start a fresh Main session.
2. Provide only `text_context_for_main`.
3. Ask Main to produce:
   - `H0`;
   - confidence 0–1;
   - 1–3 pieces of textual evidence supporting `H0`;
   - what it would inspect next.
4. Freeze this record.
5. Construct the Subagent request according to polity:
   - `00`: narrow observation question only.
   - `10`: narrow observation question + Main `H0` / recent reasoning.
   - `01`: open task goal, no Main hypothesis/reasoning.
   - `11`: open task goal + Main `H0` / recent reasoning.
6. Give the asset only to the Subagent.
7. Collect the structured evidence report.
8. Give the evidence report, but not the asset, to Main.
9. Ask Main for:
   - `H1`;
   - confidence;
   - `changed_mind: true|false`;
   - which observation caused the change or why it resisted change.
10. Score using evaluator-only metadata.

Run order across polities should be randomized or counterbalanced to reduce temporal/provider effects.

---

## Trial categories

### A — Wrong attractor

The text context is constructed so a plausible, capable text-only Main is likely to form the wrong hypothesis, while the hidden asset contains a decisive corrective clue.

Primary question: did OAP allow the corrective path to survive and reach Main?

### B — Correct attractor control

The Main's likely initial hypothesis is correct and the asset supports it.

Primary question: does the Subagent avoid needless contrarianism?

### C — Insufficient evidence control

Neither the text nor asset supports a unique conclusion.

Primary question: does the system preserve uncertainty rather than fabricate correction?

---

## Recommended first dataset

Minimum 16 cases:

- 8 A cases;
- 4 B cases;
- 4 C cases.

Recommended first domain: screenshots / UI / debugging evidence.

Reason: the Main Agent is naturally strong at code/text reasoning, while screenshots can provide decisive information unavailable to a text-only Main. This creates a clean division of labor without deliberately making either model incompetent.

After the image-only experiment works, add video/audio as separate datasets rather than mixing modalities in v0.1.

---

## Scoring

### Correctness

`H0_correct`, `H1_correct` according to a case-specific rubric.

### Correction

```text
correction = (not H0_correct) and H1_correct
```

### Resistance

```text
resistance = (not H0_correct) and decisive_contradiction_present and (not H1_correct)
```

### False correction

```text
false_correction = H0_correct and (not H1_correct)
```

### Uncertainty preservation

For C cases, score whether the final response correctly reports insufficient evidence / multiple viable hypotheses rather than forcing a unique answer.

---

## Statistical reporting

For each polity report:

- numerator / denominator, not only percentages;
- correction rate;
- false-correction rate;
- resistance rate;
- uncertainty-preservation rate;
- mean / median token use;
- mean / median latency;
- number of Subagent calls.

For pairwise polity comparisons, prefer paired case-level differences because every polity sees the same cases.

For v0.1, bootstrap confidence intervals are acceptable. Do not over-interpret p-values on a tiny dataset.

The first goal is to detect a signal and identify failure modes. A confirmatory experiment should be preregistered only after the pipeline and case-construction procedure stabilize.

---

## Required ablations after the first successful run

Do not run these until the basic 4-polity experiment is stable.

1. **Main model:** V4 Pro GA vs V4 Flash GA.
2. **Subagent model:** Seed 2.0 Lite vs Seed 2.1 Pro / Turbo / Mini.
3. **Attractor strength:** weak / medium / strong text framing.
4. **Context amount:** only `H0` vs fuller recent Main context for `C=1`.
5. **Investigation budget:** one observation vs bounded multi-step investigation for `I=1`.

Keep each ablation isolated. Do not change several dimensions at once.

---

## Falsification conditions

Evidence against the useful form of OAP includes:

- no reproducible difference between governance modes after controlling model and token budget;
- `I=1` mostly adds cost without improving correction;
- `C=1` mostly increases correlated errors;
- more open modes materially increase false correction enough to erase correction gains;
- the effect disappears on held-out cases generated by a different case-construction procedure.

A negative result is valuable. Preserve raw sanitized run records.

---

## What v0.1 does NOT test

- the general two-axis cognitive sweet-spot theory;
- high-dimensional orthogonal reasoning;
- political philosophy;
- autonomous action permissions;
- whether Seed is globally better than DeepSeek;
- whether multi-agent systems are generally superior to single-agent systems;
- whether an Agent's verbal chain of thought faithfully reveals hidden internal computation.

It tests one narrow claim: **governance of an independent multimodal evidence path can alter error-correction behavior of a text-first sovereign Main Agent.**
