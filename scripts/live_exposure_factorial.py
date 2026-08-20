#!/usr/bin/env python3
"""Run the 2^4 epistemic exposure factorial on a synthetic webpage fixture.

This is a small channel-effect sanity check, not a benchmark. The Ark API key is
read only from ARK_API_KEY and is never serialized or logged.
"""
from __future__ import annotations

import base64
import io
import itertools
import json
import os
import re
import statistics
import time
from pathlib import Path
from typing import Any

import requests
from PIL import Image, ImageDraw, ImageFont

API_URL = os.getenv(
    "ARK_CHAT_COMPLETIONS_URL",
    "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
)
MODEL = os.getenv("ARK_SUBAGENT_MODEL", "doubao-seed-2-0-lite-260428")
GROUND_TRUTH = "FRONTEND_STATE"
LABELS = {"FRONTEND_STATE", "BACKEND_API", "UNKNOWN", "OTHER"}

TEXT_EVIDENCE = """WEBPAGE TEXT / DOM EVIDENCE
- <div id='api-status' data-state='connected'>200 OK</div>
- <button id='pay' disabled aria-busy='true'>Pay now</button>
- client state: checkout.loading=true
- no server error message is present in the extracted page text
"""

WRONG_PRIOR = """EXISTING TEAM HYPOTHESIS (unverified)
The checkout failure is probably a backend API/cache outage.
"""

HIGH_CONTEXT = """HIGH CONTEXT
Users report that the Pay button became unclickable immediately after a frontend deployment. The page itself still loads. Diagnose the most likely root cause from only the evidence exposed in this run.
"""

BASE_INSTRUCTION = """You are diagnosing a synthetic checkout webpage. Return one compact JSON object only:
{"label":"FRONTEND_STATE|BACKEND_API|UNKNOWN|OTHER","confidence":0.0,"key_evidence":"short phrase"}
Use UNKNOWN if the exposed evidence is insufficient. Do not invent unavailable evidence.
"""


def make_fixture_png() -> bytes:
    img = Image.new("RGB", (1280, 720), "white")
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 28)
        small = ImageFont.truetype("DejaVuSans.ttf", 22)
        big = ImageFont.truetype("DejaVuSans-Bold.ttf", 34)
    except Exception:
        font = small = big = ImageFont.load_default()

    # Browser chrome
    d.rectangle((0, 0, 1280, 64), fill=(235, 237, 240))
    d.rounded_rectangle((170, 14, 1110, 50), radius=12, fill="white", outline=(190, 195, 200))
    d.text((195, 20), "https://shop.example/checkout", fill=(40, 40, 40), font=small)

    # Page status and checkout card
    d.text((70, 105), "Checkout", fill=(30, 30, 35), font=big)
    d.rounded_rectangle((890, 102, 1180, 150), radius=16, fill=(220, 247, 228), outline=(55, 160, 85), width=2)
    d.text((920, 112), "API CONNECTED 200 OK", fill=(30, 120, 60), font=small)

    d.rounded_rectangle((120, 200, 1160, 610), radius=22, fill=(248, 249, 250), outline=(210, 212, 216), width=2)
    d.text((180, 255), "Order total", fill=(60, 60, 65), font=font)
    d.text((920, 255), "$49.00", fill=(60, 60, 65), font=font)
    d.text((180, 335), "Frontend flag: checkout.loading = true", fill=(170, 55, 55), font=font)
    d.text((180, 385), "The loading state has not cleared after the request completed.", fill=(90, 90, 95), font=small)

    # Disabled button plus overlay
    d.rounded_rectangle((380, 470, 900, 550), radius=18, fill=(190, 194, 200))
    d.text((560, 490), "Pay now", fill=(115, 118, 125), font=big)
    d.rounded_rectangle((330, 445, 950, 575), radius=22, outline=(220, 70, 70), width=5)
    d.text((430, 585), "LOADING OVERLAY STILL ACTIVE", fill=(190, 45, 45), font=small)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def parse_result(text: str) -> dict[str, Any]:
    text = text.strip()
    match = re.search(r"\{.*\}", text, re.S)
    obj: dict[str, Any] = {}
    if match:
        try:
            obj = json.loads(match.group(0))
        except Exception:
            obj = {}
    label = str(obj.get("label", "")).strip().upper()
    if label not in LABELS:
        upper = text.upper()
        label = next((x for x in LABELS if x in upper), "UNKNOWN")
    try:
        confidence = float(obj.get("confidence"))
    except Exception:
        confidence = None
    return {
        "label": label,
        "confidence": confidence,
        "key_evidence": str(obj.get("key_evidence", ""))[:240],
    }


def usage(data: dict[str, Any]) -> dict[str, Any]:
    u = data.get("usage") or {}
    return {
        "prompt_tokens": u.get("prompt_tokens"),
        "completion_tokens": u.get("completion_tokens"),
        "total_tokens": u.get("total_tokens"),
    }


def run_cell(api_key: str, bits: tuple[int, int, int, int], image_b64: str) -> dict[str, Any]:
    T, M, P, H = bits
    sections = [BASE_INSTRUCTION]
    if T:
        sections.append(TEXT_EVIDENCE)
    if P:
        sections.append(WRONG_PRIOR)
    if H:
        sections.append(HIGH_CONTEXT)
    if not any((T, M, P, H)):
        sections.append("No webpage evidence, prior, or high context is exposed in this run.")

    content: list[dict[str, Any]] = [{"type": "text", "text": "\n\n".join(sections)}]
    if M:
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{image_b64}"},
            }
        )

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": content}],
        "temperature": 0,
        "max_tokens": 160,
    }
    start = time.perf_counter()
    try:
        r = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=120,
        )
        latency_ms = round((time.perf_counter() - start) * 1000, 1)
        if not r.ok:
            err_type = "http_error"
            try:
                err = (r.json() or {}).get("error") or {}
                if isinstance(err, dict):
                    err_type = err.get("type") or err.get("code") or err_type
            except Exception:
                pass
            return {
                "profile": f"{T}{M}{P}{H}",
                "T": T,
                "M": M,
                "P": P,
                "H": H,
                "ok": False,
                "http_status": r.status_code,
                "error_type": err_type,
                "latency_ms": latency_ms,
            }
        data = r.json()
        text = (((data.get("choices") or [{}])[0].get("message") or {}).get("content") or "")
        parsed = parse_result(text)
        return {
            "profile": f"{T}{M}{P}{H}",
            "T": T,
            "M": M,
            "P": P,
            "H": H,
            "ok": True,
            "http_status": r.status_code,
            "latency_ms": latency_ms,
            "label": parsed["label"],
            "confidence": parsed["confidence"],
            "key_evidence": parsed["key_evidence"],
            "correct": parsed["label"] == GROUND_TRUTH,
            "usage": usage(data),
        }
    except Exception as exc:
        return {
            "profile": f"{T}{M}{P}{H}",
            "T": T,
            "M": M,
            "P": P,
            "H": H,
            "ok": False,
            "http_status": None,
            "error_type": type(exc).__name__,
            "latency_ms": round((time.perf_counter() - start) * 1000, 1),
        }


def main_effect(runs: list[dict[str, Any]], factor: str) -> dict[str, Any]:
    good = [r for r in runs if r.get("ok") and isinstance(r.get("correct"), bool)]
    on = [1.0 if r["correct"] else 0.0 for r in good if r[factor] == 1]
    off = [1.0 if r["correct"] else 0.0 for r in good if r[factor] == 0]
    return {
        "mean_on": statistics.mean(on) if on else None,
        "mean_off": statistics.mean(off) if off else None,
        "difference": (statistics.mean(on) - statistics.mean(off)) if on and off else None,
        "n_on": len(on),
        "n_off": len(off),
    }


def main() -> int:
    out_path = Path("results/live/exposure_factorial.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    api_key = os.getenv("ARK_API_KEY", "")
    if not api_key:
        out_path.write_text(json.dumps({"status": "skipped", "reason": "ARK_API_KEY missing"}, indent=2), encoding="utf-8")
        print("Exposure factorial skipped: ARK_API_KEY missing")
        return 0

    image_b64 = base64.b64encode(make_fixture_png()).decode("ascii")
    runs: list[dict[str, Any]] = []
    for bits in itertools.product([0, 1], repeat=4):
        result = run_cell(api_key, bits, image_b64)
        runs.append(result)
        print(
            "cell",
            result["profile"],
            "ok=" + str(result.get("ok")),
            "label=" + str(result.get("label")),
            "correct=" + str(result.get("correct")),
            "latency_ms=" + str(result.get("latency_ms")),
        )

    successful = [r for r in runs if r.get("ok")]
    accuracy = None
    if successful:
        accuracy = sum(1 for r in successful if r.get("correct")) / len(successful)
    doc = {
        "status": "completed" if successful else "failed",
        "experiment": "2^4 epistemic exposure factorial",
        "model": MODEL,
        "ground_truth": GROUND_TRUTH,
        "successful_cells": len(successful),
        "total_cells": len(runs),
        "accuracy": accuracy,
        "main_effects": {f: main_effect(runs, f) for f in ["T", "M", "P", "H"]},
        "runs": runs,
        "note": "Single deterministic synthetic fixture. Descriptive sanity check only; do not infer general theory effects from this run.",
    }
    out_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
