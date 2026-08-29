# 9:16 capture plan

| Time | Visual / capture instruction | On-screen text |
|---|---|---|
| 0:00–0:05 | Large six-item checklist animating into view. | `6 hardware checks` |
| 0:05–0:13 | Open `node/rip_200_round_robin_1cpu1vote.py`; frame `ROTATING_FINGERPRINT_CHECKS` and `ACTIVE_FINGERPRINT_CHECK_COUNT = 4`. | `4 active` |
| 0:13–0:22 | Scroll to `select_active_fingerprint_checks()`. Highlight the previous-hash normalization and nonce derivation. | `previous epoch hash → nonce` |
| 0:22–0:31 | Highlight the deterministic `sorted(... sha256(...))` ranking and `ranked[:active_count]`. | `deterministic selection` |
| 0:31–0:42 | Terminal: run `python distribution/fingerprint-rotation-short/rotation_demo.py`; keep the four selected checks visible. | `public fixed-hash demo` |
| 0:42–0:50 | Highlight the fail-closed branch returning all checks when the hash is missing/all zeros. | `missing hash → all 6` |
| 0:50–0:58 | End card with six checks and the source URL. | `Harder to prepare for one fixed checklist` |

## Recording safety

- This package uses only public source and a fake public block-hash test vector.
- Do not display environment variables, API keys, wallets, private keys, seeds, or shell history.
- Avoid claiming this demo reproduces the entire live reward-attestation pipeline; it demonstrates the public rotation helper only.
