# Sources and Claim Map

Canonical source used for technical claims:

- RustChain Unified API Reference: https://github.com/Scottcjn/Rustchain/blob/main/docs/API_REFERENCE.md

## Claim map

| Claim | Source location |
|---|---|
| `/health` is a public GET endpoint with no authentication | API Reference → Network & Status → `GET /health` |
| `/health` response documents `ok`, `uptime_s`, `db_rw`, `backup_age_hours`, and `tip_age_slots` | API Reference → `GET /health` response and field table |
| `db_rw` describes whether the database is read/write capable | API Reference → `GET /health` field table |
| `tip_age_slots` describes slots behind tip, with 0 documented as synced | API Reference → `GET /health` field table |
| `/ready` is documented separately as a Kubernetes-style readiness probe | API Reference → `GET /ready` |
| `/ready` example response contains `ready: true` | API Reference → `GET /ready` response |

## Editorial guardrails

The package does not claim that either endpoint guarantees end-to-end application correctness, profitability, miner eligibility, or uninterrupted availability. The narration distinguishes the endpoints only using their documented purpose and response fields.