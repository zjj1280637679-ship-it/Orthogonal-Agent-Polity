# Orthogonal-Agent-Polity

A low-dimensional semantic framework for modeling how a sovereign Main Agent governs Subagents through orthogonal polity coordinates. Runtime permissions are operationalizations; observed Agent behaviors are emergent phenotypes.

## Theory

See [THEORY.md](./THEORY.md) for the current theoretical outline of Orthogonal Agent Polity (OAP).

## Reference experiment

The first engineering target is a DeepSeek harness multimodal-agent experiment:

- **Main / Sovereign:** a high-capability DeepSeek V4 GA model without multimodal input enabled.
- **Subagent:** a multimodal Doubao Seed model, initially `doubao-seed-2-0-lite-260428`.
- **Question:** can different OAP governance operationalizations change the probability that the Main Agent escapes a wrong reasoning attractor after the Subagent observes external multimodal evidence?

The implementation work is specified in [HARNESS_TASK.md](./HARNESS_TASK.md), with experiment design in [EXPERIMENT.md](./EXPERIMENT.md), model resources in [MODEL_POOL.md](./MODEL_POOL.md), and secret-handling rules in [SECURITY.md](./SECURITY.md).

### Epistemic exposure pilot

A secondary full-factorial experiment is documented in [EXPOSURE_FACTORIAL.md](./EXPOSURE_FACTORIAL.md).

It treats actual information exposure as a separate experimental lattice:

```text
E = (T, M, P, H)
```

where `T` = webpage text/DOM evidence, `M` = rendered multimodal evidence, `P` = prior hypothesis exposure, and `H` = high-context exposure. These four factors produce 16 controlled cells and are **not** new OAP polity axes.

The branch contains secret-safe live runners under `scripts/` and a trusted marker-trigger workflow under `.github/workflows/oap-live-exposure-pilot.yml`.

DeepSeek-TUI / DeepSeek harness can load the repository-local skill under `.deepseek/skills/oap-attractor-experiment/`.
