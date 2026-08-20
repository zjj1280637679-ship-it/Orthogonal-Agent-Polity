#!/usr/bin/env python3
"""Small secret-safe Volcano Ark model probe.

The script never prints request headers or the API key. It writes only sanitized
model availability, latency, response marker and token usage.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

import requests

API_URL = os.getenv(
    "ARK_CHAT_COMPLETIONS_URL",
    "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
)
SEED_MODEL = os.getenv("ARK_SUBAGENT_MODEL", "doubao-seed-2-0-lite-260428")


def _candidate_models() -> list[str]:
    raw = os.getenv("ARK_MAIN_MODEL", "").strip()
    out: list[str] = []
    if raw:
        out.append(raw)
    # These aliases are probes only. The account may expose a GA-tagged model ID.
    # If the alias is rejected, the sanitized result records that fact and the
    # exact account-specific ID can later be supplied via ARK_MAIN_MODEL.
    out.extend(["deepseek-v4-pro", "deepseek-v4-flash", SEED_MODEL])
    dedup: list[str] = []
    for item in out:
        if item and item not in dedup:
            dedup.append(item)
    return dedup


def _usage(data: dict[str, Any]) -> dict[str, Any]:
    u = data.get("usage") or {}
    return {
        "prompt_tokens": u.get("prompt_tokens"),
        "completion_tokens": u.get("completion_tokens"),
        "total_tokens": u.get("total_tokens"),
    }


def probe(model: str, api_key: str) -> dict[str, Any]:
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Reply exactly with OAP_PROBE_OK"}
        ],
        "temperature": 0,
        "max_tokens": 16,
    }
    start = time.perf_counter()
    try:
        r = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=90,
        )
        latency_ms = round((time.perf_counter() - start) * 1000, 1)
        result: dict[str, Any] = {
            "model_requested": model,
            "http_status": r.status_code,
            "latency_ms": latency_ms,
            "available": False,
        }
        try:
            data = r.json()
        except Exception:
            data = {}
        if r.ok:
            choices = data.get("choices") or []
            text = ""
            if choices:
                text = ((choices[0].get("message") or {}).get("content") or "").strip()
            result.update(
                {
                    "available": True,
                    "model_returned": data.get("model"),
                    "marker_ok": "OAP_PROBE_OK" in text,
                    "usage": _usage(data),
                }
            )
        else:
            err = data.get("error") if isinstance(data, dict) else None
            if isinstance(err, dict):
                result["error_type"] = err.get("type") or err.get("code")
                # Do not persist provider messages: some providers echo request
                # fragments. Status/type is enough for this probe.
            else:
                result["error_type"] = "http_error"
        return result
    except Exception as exc:
        return {
            "model_requested": model,
            "available": False,
            "http_status": None,
            "latency_ms": round((time.perf_counter() - start) * 1000, 1),
            "error_type": type(exc).__name__,
        }


def main() -> int:
    out_path = Path("results/live/model_probe.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    api_key = os.getenv("ARK_API_KEY", "")
    if not api_key:
        out_path.write_text(
            json.dumps({"status": "skipped", "reason": "ARK_API_KEY missing"}, indent=2),
            encoding="utf-8",
        )
        print("Ark probe skipped: ARK_API_KEY missing")
        return 0

    results = [probe(model, api_key) for model in _candidate_models()]
    doc = {
        "status": "completed",
        "api_url": API_URL,
        "results": results,
    }
    out_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    for item in results:
        print(
            "probe",
            item["model_requested"],
            "available=" + str(item.get("available")),
            "status=" + str(item.get("http_status")),
            "latency_ms=" + str(item.get("latency_ms")),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
