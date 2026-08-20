# Security Contract for Live OAP Experiments

## Secret source

The live Volcano Ark credential is expected through a GitHub secret named:

`HUOSHANYINQINGAPI`

For **GitHub Actions** experiments, this value must exist specifically as an **Actions repository secret** (or as an environment secret referenced by the job). GitHub's newer Copilot/Agents, Codespaces, Dependabot and Actions secret stores are separate scopes; creating a secret for another product does not automatically make it available through the Actions `secrets` context.

GitHub Actions maps the Actions secret into the process environment as:

```yaml
env:
  ARK_API_KEY: ${{ secrets.HUOSHANYINQINGAPI }}
```

The secret value must never be committed, printed, echoed, uploaded, or copied into model prompts.

If `${{ secrets.HUOSHANYINQINGAPI }}` resolves to an empty string, the experiment must record a clean `ARK_API_KEY missing` skip and make **no provider request**.

---

## Hard rules

1. **No secret in Git history.**
   - no `.env` with values;
   - no hard-coded token;
   - no example that resembles the real token;
   - no secret in commit messages, issues, PR bodies, test fixtures, snapshots, or artifacts.

2. **No secret in model context.**
   The API key is transport authentication, not task context. Main and Subagent must never see it.

3. **No secret in logs.**
   - redact `Authorization` headers completely;
   - redact any value loaded from `ARK_API_KEY`;
   - do not dump HTTP client objects or full request headers on exceptions;
   - sanitize tracebacks if a client library includes request metadata.

4. **No live secret on untrusted PR execution.**
   Live API tests must not run automatically for pull requests from arbitrary code changes.

5. **Live tests are opt-in / trusted-trigger only.**
   Preferred production form is `workflow_dispatch` on a reviewed workflow. During the current experimental branch, an explicit marker-file push (`.oap-live-run`) is also allowed because it is a deliberate operator action on the owner-controlled branch and the workflow only commits sanitized results. Do not broaden that trigger to arbitrary PRs.

6. **Offline CI first.**
   Unit and polity tests must run with fake providers and require no credentials.

7. **Artifacts are sanitized.**
   Experiment outputs may contain model IDs, token counts, latency, prompts designed for the experiment, evidence reports, and scores. They must not contain request headers or environment dumps.

---

## Local development

Supported local variables:

```text
ARK_API_KEY
OAP_MAIN_MODEL_PRO
OAP_MAIN_MODEL_FLASH
OAP_MULTIMODAL_MODEL
ARK_BASE_URL
```

Use a local `.env` only if the runtime needs it. `.env` is ignored by Git.

Repository examples must contain blank or obviously fake placeholders only.

---

## Redaction tests

Implementation must include tests proving:

- `ARK_API_KEY` value is removed from structured logs;
- `Authorization: Bearer ...` is removed;
- exceptions from the HTTP layer do not serialize request headers;
- experiment JSONL does not contain environment variables;
- GitHub Actions debug output does not use `set -x` around credential-bearing commands.

A useful test pattern is to inject a conspicuous fake secret such as:

`OAP_TEST_SECRET_DO_NOT_LEAK_123456789`

then assert that it appears nowhere in captured logs/results.

Never use the real secret for redaction tests.

---

## GitHub Actions policy

Recommended split:

### `ci.yml`

Runs on push / pull request:

- lint;
- unit tests;
- polity routing tests;
- fake-provider experiment smoke test;
- secret redaction tests.

No Ark secret is mapped into the job.

### live experiment workflow

Trusted/manual trigger only:

- maps Actions secret `HUOSHANYINQINGAPI` to `ARK_API_KEY`;
- performs provider smoke tests before the full experiment;
- writes/uploads only sanitized results;
- never commits raw HTTP response objects containing headers.

If the secret is unavailable, record `ARK_API_KEY is not configured` without printing environment state.

---

## Provider request logging

Default log shape:

```json
{
  "provider": "volcano-ark",
  "model": "configured model id",
  "request_kind": "chat_completions",
  "status": "completed",
  "latency_ms": 1234,
  "usage": {},
  "request_id": "sanitized provider request id"
}
```

Forbidden log fields:

```text
authorization
api_key
headers
cookies
full_environment
```

---

## Incident rule

If a real API key is ever committed or printed into a public GitHub artifact/log:

1. stop live experiments;
2. rotate/revoke the key in Volcano Ark immediately;
3. replace the GitHub secret;
4. remove the leaked material from current repository content/artifacts;
5. treat removal from the latest commit as insufficient if the secret entered Git history;
6. document the incident without reproducing the key.

Security takes priority over experiment continuity.
