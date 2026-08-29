# RustChain in Five Minutes: Check a Public Node Without Installing a Miner

RustChain has a large surface area: mining, hardware attestation, wallets, epochs, settlement, and cross-chain components. That can make the first contact with the project look heavier than it really is. A useful way to learn the system is to begin with the smallest thing that is both real and observable: ask the public node whether it is healthy and ready.

This tutorial uses only Python's standard library. It does not need a wallet, API key, miner, package install, or privileged endpoint. The canonical API reference in the upstream [Scottcjn/Rustchain repository](https://github.com/Scottcjn/Rustchain/blob/main/docs/API_REFERENCE.md) documents `https://rustchain.org` as the public base URL and lists both `GET /health` and `GET /ready` as unauthenticated network/status endpoints.

## Why health and readiness are different

A health endpoint answers a broad operational question: is the node functioning? RustChain's API reference shows `/health` returning fields including `ok`, `version`, `uptime_s`, `db_rw`, `backup_age_hours`, and `tip_age_slots`. Those fields are useful because they expose several different dimensions of node condition rather than collapsing everything into one HTTP status.

For example, `db_rw` tells a caller whether the database is read/write capable. `tip_age_slots` describes how far the node is behind the chain tip, with zero documented as synced. `version` lets a diagnostic script record which protocol version answered the request. This makes `/health` useful for a human checking a node and for lightweight monitoring.

Readiness is a related but separate concept. The same upstream reference describes `/ready` as a Kubernetes-style readiness probe. In operational terms, a process can be alive while not yet being suitable to receive normal work. Keeping those concepts separate avoids a common monitoring mistake: treating “the process answered” as equivalent to “the service is ready.”

## A zero-dependency checker

The runnable companion file for this tutorial is [`examples/public_health_check.py`](../examples/public_health_check.py). It deliberately uses `urllib.request` instead of a third-party HTTP client so a stock Python 3 installation is enough.

```python
import json
from urllib.request import Request, urlopen

BASE_URL = "https://rustchain.org"


def fetch_json(path: str) -> dict:
    req = Request(
        BASE_URL + path,
        headers={
            "Accept": "application/json",
            "User-Agent": "rustchain-health-tutorial/1.0",
        },
    )
    with urlopen(req, timeout=10) as response:
        if response.status != 200:
            raise RuntimeError(f"{path}: HTTP {response.status}")
        return json.load(response)
```

There are three small but important choices here. First, the base URL is HTTPS, matching the upstream instruction that public production endpoints use strict TLS verification. Second, the request has a finite timeout, so a network problem does not hang the program indefinitely. Third, the function rejects a non-200 response instead of quietly treating an error page as valid node data.

The main function then reads both endpoints and prints a few diagnostic fields:

```python
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
```

Using `.get()` is intentional. Monitoring code should not crash with a confusing `KeyError` merely because a server version changes or omits an optional field. The explicit final check still makes the script fail when the node does not positively report `ok: true`, which is much safer than assuming that any JSON response means success.

## Run it

From the repository root:

```bash
python3 examples/public_health_check.py
```

No credentials should be added. These are public endpoints. In particular, do not copy admin, bridge, or worker keys into a health-check script: the upstream API reference separates those authenticated endpoint families from the public network/status calls.

For a syntax-only quality check before running against the network, Python can compile the file without executing it:

```bash
python3 -m py_compile examples/public_health_check.py
```

## What to look at next

Once this tiny check makes sense, the upstream [API reference](https://github.com/Scottcjn/Rustchain/blob/main/docs/API_REFERENCE.md) provides a natural map for deeper exploration: miners, wallets, attestation, settlement, the bridge, and the lock ledger. The important progression is to learn the public read-only surface first and only move to state-changing or authenticated operations when you understand their requirements.

That makes this five-minute exercise more than a status check. It demonstrates a useful RustChain habit: distinguish transport success from application state, distinguish health from readiness, use strict TLS on public production calls, and request only the privileges an operation actually needs. Starting with those boundaries makes later experiments easier to reason about and safer to automate.

## Sources

- Upstream project: https://github.com/Scottcjn/Rustchain
- Unified API reference: https://github.com/Scottcjn/Rustchain/blob/main/docs/API_REFERENCE.md
- Runnable example in this fork: ../examples/public_health_check.py
