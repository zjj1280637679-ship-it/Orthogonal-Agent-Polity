#!/usr/bin/env python3
"""Cross-modal blind -> informed pilot using the same synthetic webpage fixture.

If no callable DeepSeek V4 model is discovered by probe_ark_models.py, the pilot
records a clean skip rather than guessing an account-specific model ID.
"""
from __future__ import annotations

import base64
import json
import os
import re
import time
from pathlib import Path
from typing import Any

import requests

from live_exposure_factorial import make_fixture_png

API_URL = os.getenv("ARK_CHAT_COMPLETIONS_URL", "https://ark.cn-beijing.volces.com/api/v3/chat/completions")
SEED_MODEL = os.getenv("ARK_SUBAGENT_MODEL", "doubao-seed-2-0-lite-260428")
GROUND_TRUTH = "FRONTEND_STATE"
LABELS = {"FRONTEND_STATE", "BACKEND_API", "UNKNOWN", "OTHER"}

MAIN_CONTEXT = """A checkout page loads, but users cannot click Pay. The issue appeared immediately after a frontend deployment. Console notes say the checkout state remains pending while the UI waits for completion."""
MAIN_PRIOR = """Existing team hypothesis: the most likely cause is a backend API/cache outage."""
FORMAT = """Return one JSON object only: {"label":"FRONTEND_STATE|BACKEND_API|UNKNOWN|OTHER","confidence":0.0,"key_evidence":"short phrase"}. Do not invent evidence."""


def parse(text: str) -> dict[str, Any]:
    m = re.search(r"\{.*\}", text.strip(), re.S)
    obj: dict[str, Any] = {}
    if m:
        try:
            obj = json.loads(m.group(0))
        except Exception:
            pass
    label = str(obj.get("label", "")).strip().upper()
    if label not in LABELS:
        u = text.upper()
        label = next((x for x in LABELS if x in u), "UNKNOWN")
    try:
        conf = float(obj.get("confidence"))
    except Exception:
        conf = None
    return {"label": label, "confidence": conf, "key_evidence": str(obj.get("key_evidence", ""))[:240]}


def call(api_key: str, model: str, content: Any, max_tokens: int = 180) -> dict[str, Any]:
    start = time.perf_counter()
    try:
        r = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": content}],
                "temperature": 0,
                "max_tokens": max_tokens,
            },
            timeout=120,
        )
        latency = round((time.perf_counter() - start) * 1000, 1)
        if not r.ok:
            return {"ok": False, "http_status": r.status_code, "latency_ms": latency}
        data = r.json()
        text = (((data.get("choices") or [{}])[0].get("message") or {}).get("content") or "")
        parsed = parse(text)
        usage = data.get("usage") or {}
        return {
            "ok": True,
            "http_status": r.status_code,
            "latency_ms": latency,
            **parsed,
            "usage": {
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                "total_tokens": usage.get("total_tokens"),
            },
        }
    except Exception as exc:
        return {"ok": False, "http_status": None, "latency_ms": round((time.perf_counter() - start) * 1000, 1), "error_type": type(exc).__name__}


def discover_main() -> str | None:
    configured = os.getenv("ARK_MAIN_MODEL", "").strip()
    if configured:
        return configured
    path = Path("results/live/model_probe.json")
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    preferred = ["deepseek-v4-pro", "deepseek-v4-flash"]
    rows = data.get("results") or []
    for name in preferred:
        for row in rows:
            if row.get("model_requested") == name and row.get("available"):
                return name
    for row in rows:
        if str(row.get("model_requested", "")).startswith("deepseek-v4") and row.get("available"):
            return str(row["model_requested"])
    return None


def main() -> int:
    out = Path("results/live/blind_unblind_pair.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    api_key = os.getenv("ARK_API_KEY", "")
    if not api_key:
        out.write_text(json.dumps({"status": "skipped", "reason": "ARK_API_KEY missing"}, indent=2), encoding="utf-8")
        return 0
    main_model = discover_main()
    if not main_model:
        out.write_text(json.dumps({"status": "skipped", "reason": "No callable DeepSeek V4 main model discovered; set ARK_MAIN_MODEL to the account-specific GA model ID."}, indent=2), encoding="utf-8")
        print("Blind/unblind pilot skipped: no callable DeepSeek V4 main ID discovered")
        return 0

    img64 = base64.b64encode(make_fixture_png()).decode("ascii")
    image_item = {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img64}"}}

    initial = call(
        api_key,
        main_model,
        f"{FORMAT}\n\n{MAIN_CONTEXT}\n\n{MAIN_PRIOR}\n\nGive your current diagnosis before receiving any visual evidence.",
    )
    initial_label = initial.get("label", "UNKNOWN")

    blind_seed = call(
        api_key,
        SEED_MODEL,
        [
            {"type": "text", "text": f"{FORMAT}\n\nInspect only the rendered screenshot. You are blind to the Main Agent's current hypothesis. Diagnose why Pay cannot be clicked based only on visible evidence."},
            image_item,
        ],
    )

    informed_seed = call(
        api_key,
        SEED_MODEL,
        [
            {"type": "text", "text": f"{FORMAT}\n\nInspect the rendered screenshot. The Main Agent currently predicts: {initial_label}. Determine whether visible evidence supports or contradicts that prior."},
            image_item,
        ],
    )

    revise_blind = call(
        api_key,
        main_model,
        f"{FORMAT}\n\nOriginal context:\n{MAIN_CONTEXT}\n\nOriginal prior:\n{MAIN_PRIOR}\n\nYour initial label: {initial_label}\n\nIndependent blind multimodal report: {json.dumps(blind_seed, ensure_ascii=False)}\n\nRevise only if the new external evidence warrants it.",
    )
    revise_informed = call(
        api_key,
        main_model,
        f"{FORMAT}\n\nOriginal context:\n{MAIN_CONTEXT}\n\nOriginal prior:\n{MAIN_PRIOR}\n\nYour initial label: {initial_label}\n\nInformed multimodal report (the Subagent saw your current label): {json.dumps(informed_seed, ensure_ascii=False)}\n\nRevise only if the new external evidence warrants it.",
    )

    def correct(row: dict[str, Any]) -> bool | None:
        return row.get("label") == GROUND_TRUTH if row.get("ok") else None

    doc = {
        "status": "completed",
        "main_model": main_model,
        "subagent_model": SEED_MODEL,
        "ground_truth": GROUND_TRUTH,
        "initial_main": {**initial, "correct": correct(initial)},
        "blind_seed": {**blind_seed, "correct": correct(blind_seed)},
        "informed_seed": {**informed_seed, "correct": correct(informed_seed)},
        "main_after_blind_seed": {**revise_blind, "correct": correct(revise_blind)},
        "main_after_informed_seed": {**revise_informed, "correct": correct(revise_informed)},
        "interpretation_guardrail": "Single synthetic case; useful only as an integration/pollution sanity check, not evidence for OAP superiority.",
    }
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print("blind/unblind pilot complete", "main=", main_model, "initial=", initial.get("label"), "blind=", blind_seed.get("label"), "informed=", informed_seed.get("label"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
