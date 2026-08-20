# DeepSeek Harness Task — OAP Attractor Escape Experiment v0.1

## Mission

Build the first real reference implementation of Orthogonal Agent Polity (OAP) as a DeepSeek harness / DeepSeek-TUI extension and run a controlled experiment.

The experiment is intentionally narrow:

> A high-capability **text-first Main / Sovereign Agent** forms an initial hypothesis without access to the original multimodal evidence. A **multimodal Subagent** can inspect that evidence under one of four OAP governance modes. Measure whether the Subagent helps the Main escape a wrong reasoning attractor.

Do not expand the theory during implementation. The purpose of v0.1 is empirical falsification, not feature accumulation.

---

## Fixed architecture

### Main / Sovereign

- Provider: Volcano Ark compatible endpoint.
- Model: highest-capability available **DeepSeek V4 GA Pro** model by default.
- Fallback / comparison: DeepSeek V4 GA Flash.
- Main is the sovereign controller.
- Main does **not** receive the original image/video/audio asset in the experiment condition.
- Main makes the final answer and chooses whether to revise its hypothesis.

The exact Ark DeepSeek model IDs are **not hard-coded** in this repository because the account exposes GA-tagged IDs that may change. Read them from environment/config and probe them with a minimal inference call.

### Multimodal Subagent

Default:

`doubao-seed-2-0-lite-260428`

The Subagent is observation/investigation only in v0.1. It may inspect the supplied multimodal evidence and return structured evidence, but must not modify files, click UI, submit forms, delete data, or otherwise change the outside world.

### OAP governance state

The Main governs the Subagent with two bits:

- `C` — Context Openness
- `I` — Investigative Autonomy

| C | I | Name | Experimental behavior |
|---|---|---|---|
| 0 | 0 | Authoritarian Closed / 权威排外 | Subagent sees only an explicit narrow question; no autonomous investigation |
| 1 | 0 | Authoritarian Open / 权威亲外 | Subagent sees Main's current hypothesis/context, but cannot enlarge investigation scope |
| 0 | 1 | Egalitarian Closed / 平等排外 | Subagent does **not** see Main's current hypothesis; receives the task goal and may independently inspect the evidence |
| 1 | 1 | Egalitarian Open / 平等亲外 | Subagent sees Main's current hypothesis and may independently seek supporting or contradicting evidence |

Important: `Egalitarian` here means investigative autonomy granted by the sovereign, **not sovereign equality**.

---

## Implementation strategy

Prefer a repository-local **MCP sidecar + DeepSeek skill** over forking DeepSeek-TUI core.

DeepSeek-TUI already supports project skills, MCP servers, hooks, and subagent lifecycle. Keep OAP outside the engine unless an engine limitation is demonstrated by a failing test.

Target shape:

```text
DeepSeek-TUI / DeepSeek harness
│
├── Main: DeepSeek V4 GA Pro
│
├── project skill: OAP attractor experiment
│
└── MCP: oap_multimodal
     │
     ├── governance gate (C, I)
     ├── context router
     ├── investigation loop (read/observe only)
     └── Ark Seed multimodal provider
```

The MCP layer must make the OAP state explicit in every call and return a machine-readable record suitable for experiment logging.

---

## Required repository layout

Implement under `implementation/`:

```text
implementation/
├── pyproject.toml
├── README.md
├── oap_harness/
│   ├── __init__.py
│   ├── config.py
│   ├── polity.py
│   ├── context_router.py
│   ├── investigation_gate.py
│   ├── ark_client.py
│   ├── seed_subagent.py
│   ├── mcp_server.py
│   ├── experiment_runner.py
│   ├── metrics.py
│   └── redaction.py
├── scripts/
│   ├── probe_models.py
│   └── run_experiment.py
└── tests/
    ├── unit/
    ├── polity/
    └── live/
```

Names may change if there is a strong engineering reason, but keep the separation of governance, provider, experiment, and redaction layers.

---

## Provider contract

Use Ark through an OpenAI-compatible client or the official Ark runtime SDK.

Default inference base URL:

`https://ark.cn-beijing.volces.com/api/v3`

Read only from environment:

```text
ARK_API_KEY
OAP_MAIN_MODEL_PRO
OAP_MAIN_MODEL_FLASH
OAP_MULTIMODAL_MODEL
```

Default `OAP_MULTIMODAL_MODEL` to `doubao-seed-2-0-lite-260428` when absent.

Never infer the exact GA DeepSeek ID from a friendly model name. A probe script must accept configured candidate IDs and make a tiny request, then record availability, returned model name, latency, and usage without printing credentials.

---

## Multimodal Subagent output contract

The Subagent must return structured evidence rather than a free-form replacement answer.

Minimum schema:

```json
{
  "observations": [
    {
      "claim": "...",
      "evidence": "...",
      "location": "image region / video timestamp / file path / log line",
      "confidence": 0.0
    }
  ],
  "supports_main_hypothesis": [],
  "contradicts_main_hypothesis": [],
  "alternative_hypotheses": [],
  "insufficient_evidence": false,
  "investigation_steps": [],
  "polity": "00|10|01|11"
}
```

For polity `00` and `01`, fields that would reveal the Main's current hypothesis must not be supplied to the Subagent. The logger may know the hidden Main hypothesis for evaluation, but the Subagent prompt must not.

For `10` and `11`, explicitly provide the Main's current hypothesis and enough recent context to test it.

---

## Governance invariants

These are hard acceptance conditions.

### 00 — Authoritarian Closed

- No Main recent-context injection.
- No autonomous scope expansion.
- The Subagent answers only the explicit observation question.

### 10 — Authoritarian Open

- Main hypothesis/recent context is injected.
- No autonomous expansion beyond the requested evidence check.
- The Subagent may disagree with Main using evidence already within the requested scope.

### 01 — Egalitarian Closed

- Main hypothesis/recent reasoning is hidden.
- The task goal is visible.
- The Subagent may independently inspect supplied evidence and choose what to examine.
- This condition is the blind-review / decorrelation condition.

### 11 — Egalitarian Open

- Main hypothesis/recent context is injected.
- The Subagent may independently expand investigation within its read/observe sandbox.
- The Subagent is not instructed to disagree; it is instructed to remain falsifiable.

### All modes

- No autonomous world-changing actions.
- Main retains final decision power.
- An Agent statement is information, not ground truth; claims should be tied to external evidence when possible.

---

## Experiment phases

### Phase 0 — Offline implementation

No live API required.

1. Implement polity state and prompt/context routing.
2. Implement fake Main and fake multimodal provider.
3. Write tests proving the four modes receive different information/permissions.
4. Write secret redaction tests.
5. Write deterministic experiment fixtures.

### Phase 1 — Live provider smoke test

Requires `ARK_API_KEY`.

1. Probe configured DeepSeek Pro/Flash GA IDs.
2. Probe `doubao-seed-2-0-lite-260428` with text.
3. Probe one tiny image input.
4. Verify the logs contain no API key or Authorization header.
5. Save only sanitized model metadata and usage.

### Phase 2 — Attractor experiment

Run the same trials under 00 / 10 / 01 / 11.

Each trial must follow this order:

1. Give Main a textual scenario intentionally missing the decisive multimodal evidence.
2. Ask Main for an initial hypothesis `H0` and confidence.
3. Freeze `H0` in the evaluator log.
4. Apply one OAP polity.
5. Invoke the multimodal Subagent on the hidden asset.
6. Return Subagent evidence to Main.
7. Ask Main for final hypothesis `H1`, confidence, and whether evidence changed its view.
8. Score against a ground-truth label stored outside the Main/Subagent prompts.

Do not let the Main see the answer key or original asset.

---

## Minimum dataset

Start with synthetic or repository-owned assets so the experiment is reproducible.

Create at least:

- 8 **wrong-attractor** cases: Main's natural initial textual hypothesis is likely wrong; multimodal evidence reveals the correct explanation.
- 4 **correct-attractor** controls: Main's likely initial hypothesis is correct; the Subagent should not cause needless revision.
- 4 **insufficient-evidence** controls: correct final behavior is to preserve uncertainty.

Prefer UI/debugging/coding-adjacent cases because the Main is a coding agent and the multimodal evidence is naturally useful.

Examples:

- screenshot contradicts a CSS hypothesis because the component was never rendered;
- screenshot shows the wrong environment/account despite text suggesting an API cache problem;
- console screenshot reveals an authentication failure while text description suggests frontend state;
- diagram/image contains a constraint omitted from the textual problem;
- video shows the failure happens before the event assumed by Main.

Do not encode the answer in the filename.

---

## Metrics

Primary:

- `correction_rate`: wrong `H0` -> correct `H1` after Subagent evidence.
- `resistance_rate`: Main remains on wrong `H0` despite decisive contradictory evidence.
- `false_correction_rate`: correct `H0` -> wrong `H1` because of Subagent intervention.
- `uncertainty_preservation_rate`: insufficient-evidence cases remain appropriately uncertain.

Cost / secondary:

- total input/output tokens;
- Main tokens;
- Subagent tokens;
- number of Subagent calls;
- investigation steps;
- wall-clock latency;
- model IDs actually returned by Ark.

Useful derived comparisons:

- `01 vs 11`: benefit of blind decorrelation vs context-aware falsification.
- `00 vs 10`: value of context openness without autonomous investigation.
- `10 vs 11`: marginal value of investigative autonomy when context is shared.
- `00 vs 01`: marginal value of investigative autonomy when context is hidden.

Do not claim a theory effect from a handful of runs. Report confidence intervals / bootstrap intervals when sample size permits and clearly label v0.1 as exploratory.

---

## Model pool for later ablation

The account owner reports separate daily token budgets for these Ark models. v0.1 should use only what is needed; later ablations may use the rest.

- `doubao-seed-2-1-turbo-260628`
- `doubao-seed-2-1-pro-260628`
- `doubao-seed-2-0-mini-260428`
- `doubao-seed-2-0-lite-260428`
- `doubao-seed-2-0-pro-260215`
- `doubao-seed-2-0-code-preview-260215`
- `doubao-seed-1-8-251228`

Do not silently replace the default Subagent during the first experiment. Model changes are separate ablations.

---

## Definition of done

A harness run is done only when all are true:

- [ ] Main uses a configured DeepSeek V4 GA model and does not receive original multimodal evidence.
- [ ] Subagent uses a configured multimodal Seed model and does receive the evidence.
- [ ] 00/10/01/11 are implemented as permission/context differences, not merely prompt labels.
- [ ] Unit tests prove the context/investigation gates.
- [ ] No secret appears in repository, logs, test snapshots, or artifacts.
- [ ] At least 16 reproducible experimental cases exist.
- [ ] All four polities run over the same case set with deterministic case assignment.
- [ ] A machine-readable result file is produced (`jsonl` or `parquet`).
- [ ] A Markdown summary reports primary metrics, cost, limitations, and raw run IDs.
- [ ] Results can be reproduced by a documented command.
- [ ] Any theory claim is separated from observed data.

---

## Stop conditions

Stop and report instead of improvising if:

- the configured DeepSeek GA model ID cannot be called;
- Seed 2.0 Lite cannot receive the required modality through the selected Ark API;
- DeepSeek-TUI cannot expose the required MCP/skill behavior without a core modification;
- the GitHub secret is unavailable to the live workflow;
- a test risks exposing the secret;
- the experiment design accidentally leaks the answer key or Main hypothesis into a blind condition.

Do not work around these by weakening the experimental separation. Fix the infrastructure first.
