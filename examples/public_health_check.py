#!/usr/bin/env python3
"""Read RustChain's public health and readiness endpoints with stdlib only."""

import json
from urllib.request import Request, urlopen

BASE_URL = "https://rustchain.org"


def fetch_json(path: str) -> dict:
    req = Request(
        BASE_URL + path,
        headers={"Accept": "application/json", "User-Agent": "rustchain-health-tutorial/1.0"},
    )
    with urlopen(req, timeout=10) as response:
        if response.status != 200:
            raise RuntimeError(f"{path}: HTTP {response.status}")
        return json.load(response)


def main() -> None:
    health = fetch_json("/health")
    ready = fetch_json("/ready")

    print("health.ok:", health.get("ok"))
    print("health.version:", health.get("version"))
    print("health.db_rw:", health.get("db_rw"))
    print("health.tip_age_slots:", health.get("tip_age_slots"))
    print("ready:", json.dumps(ready, sort_keys=True))

    if health.get("ok") is not True:
        raise SystemExit("Node reported unhealthy")


if __name__ == "__main__":
    main()
