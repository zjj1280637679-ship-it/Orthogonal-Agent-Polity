# Ark Model Pool for OAP Experiments

This file records the model pool reported as available in the experiment owner's Volcano Ark account. Treat availability and quota as runtime facts: probe before use and do not hard-code assumptions about future availability.

## Main candidates

Use the highest-capability callable DeepSeek V4 GA model as Main / Sovereign.

Priority:

1. DeepSeek V4 **Pro GA** — default Main.
2. DeepSeek V4 **Flash GA** — speed/cost comparison Main.

The exact Ark IDs exposed to this account include a GA marker and are intentionally not written here until confirmed by the runtime probe. Supply them through configuration.

## Multimodal Subagent pool

First reference Subagent:

- `doubao-seed-2-0-lite-260428`

Additional models reported available for later ablations:

- `doubao-seed-2-1-turbo-260628`
- `doubao-seed-2-1-pro-260628`
- `doubao-seed-2-0-mini-260428`
- `doubao-seed-2-0-pro-260215`
- `doubao-seed-2-0-code-preview-260215`
- `doubao-seed-1-8-251228`

## Experimental resource note

The account owner reports that these model allocations are independent and refresh daily, with roughly 2,000,000 tokens available per model under the current free allocation.

Treat that as an **account-specific experimental budget**, not a public pricing/quota guarantee. Record actual provider usage returned by each run.

## Resource policy

Do not spend all models at once merely because quota is available.

Order:

1. fake/offline tests;
2. tiny live provider probes;
3. V4 Pro + Seed 2.0 Lite reference experiment;
4. repeat / repair failed cases;
5. only then model ablations.

Use additional independent model budgets to increase replication or isolate model effects, not to silently change the reference system mid-experiment.
