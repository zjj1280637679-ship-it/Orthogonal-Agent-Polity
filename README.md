# Orthogonal-Agent-Polity

A framework for modeling and dynamically switching multi-agent relationships through orthogonal axes of context openness and investigative autonomy.

## Theory

See [THEORY.md](./THEORY.md) for the first formal outline of Orthogonal Agent Polity (OAP).

## Reference experiment

The first engineering target is a DeepSeek harness multimodal-agent experiment:

- **Main / Sovereign:** a high-capability DeepSeek V4 GA model without multimodal input enabled.
- **Subagent:** a multimodal Doubao Seed model, initially `doubao-seed-2-0-lite-260428`.
- **Question:** can different OAP governance modes change the probability that the Main Agent escapes a wrong reasoning attractor after the Subagent observes external multimodal evidence?

The implementation work is specified in [HARNESS_TASK.md](./HARNESS_TASK.md), with experiment design in [EXPERIMENT.md](./EXPERIMENT.md) and secret-handling rules in [SECURITY.md](./SECURITY.md).

DeepSeek-TUI / DeepSeek harness can load the repository-local skill under `.agents/skills/oap-attractor-experiment/`.
