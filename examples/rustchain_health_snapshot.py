#!/usr/bin/env python3
"""Create a bounded, read-only RustChain health snapshot.

Live mode reads public JSON endpoints only. Sample mode is fully offline and
exists so the parser/normalizer can be tested without touching a network.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Any

DEFAULT_BASE_URL = "https://rustchain.org"
MAX_RESPONSE_BYTES = 1_000_000
DEFAULT_TIMEOUT = 8.0
DEFAULT_MINER_LIMIT = 5

SAMPLE_HEALTH = {
    "ok": True,
    "epoch": 123,
    "miners": 4,
    "version": "sample",
}
SAMPLE_MINERS = [
    {"miner_id": "RTCsample0001", "architecture": "ppc64", "weight": 2.5},
    {"miner_id": "RTCsample0002", "architecture": "x86_64", "weight": 1.0},
    {"miner_id": "RTCsample0003", "architecture": "arm64", "weight": 1.2},
]


class SnapshotError(RuntimeError):
    """Raised when a public endpoint cannot be read safely."""


def fetch_json(url: str, *, timeout: float = DEFAULT_TIMEOUT) -> Any:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "rustchain-health-snapshot/1.0"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "")
            if "json" not in content_type.lower():
                raise SnapshotError(
                    f"{url} returned unexpected content type {content_type!r}"
                )
            raw = response.read(MAX_RESPONSE_BYTES + 1)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise SnapshotError(f"failed to read {url}: {exc}") from exc

    if len(raw) > MAX_RESPONSE_BYTES:
        raise SnapshotError(
            f"{url} exceeded the {MAX_RESPONSE_BYTES}-byte response limit"
        )

    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SnapshotError(f"{url} did not return valid UTF-8 JSON") from exc


def _as_number(value: Any) -> float | int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    return None


def normalize_health(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise SnapshotError("health payload must be a JSON object")

    return {
        "ok": payload.get("ok") if isinstance(payload.get("ok"), bool) else None,
        "epoch": _as_number(payload.get("epoch")),
        "miners": _as_number(payload.get("miners")),
        "version": payload.get("version")
        if isinstance(payload.get("version"), str)
        else None,
    }


def _extract_miners(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        rows = payload
    elif isinstance(payload, dict):
        rows = payload.get("miners", [])
    else:
        rows = []

    if not isinstance(rows, list):
        return []

    out: list[dict[str, Any]] = []
    for item in rows:
        if isinstance(item, dict):
            out.append(item)
    return out


def normalize_miners(payload: Any, *, limit: int = DEFAULT_MINER_LIMIT) -> list[dict[str, Any]]:
    if limit < 0:
        raise ValueError("limit must be non-negative")

    normalized: list[dict[str, Any]] = []
    for item in _extract_miners(payload)[:limit]:
        miner_id = item.get("miner_id")
        architecture = item.get("architecture", item.get("arch"))
        weight = _as_number(item.get("weight"))

        normalized.append(
            {
                "miner_id": miner_id if isinstance(miner_id, str) else None,
                "architecture": architecture if isinstance(architecture, str) else None,
                "weight": weight,
            }
        )
    return normalized


def build_snapshot(
    health_payload: Any,
    miners_payload: Any,
    *,
    miner_limit: int = DEFAULT_MINER_LIMIT,
) -> dict[str, Any]:
    return {
        "health": normalize_health(health_payload),
        "miners": normalize_miners(miners_payload, limit=miner_limit),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read public RustChain status data without auth or writes."
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"RustChain public base URL (default: {DEFAULT_BASE_URL})",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"per-request timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    parser.add_argument(
        "--miner-limit",
        type=int,
        default=DEFAULT_MINER_LIMIT,
        help=f"maximum miner rows in output (default: {DEFAULT_MINER_LIMIT})",
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="run entirely offline using embedded sample payloads",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.miner_limit < 0:
        print("error: --miner-limit must be non-negative", file=sys.stderr)
        return 2

    if args.sample:
        health_payload = SAMPLE_HEALTH
        miners_payload = SAMPLE_MINERS
    else:
        base = args.base_url.rstrip("/")
        try:
            health_payload = fetch_json(f"{base}/health", timeout=args.timeout)
            miners_payload = fetch_json(f"{base}/api/miners", timeout=args.timeout)
        except SnapshotError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

    snapshot = build_snapshot(
        health_payload,
        miners_payload,
        miner_limit=args.miner_limit,
    )
    print(json.dumps(snapshot, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
