# Source map

Authoritative public source used by this package:

`https://github.com/Scottcjn/Rustchain/blob/main/node/rip_200_round_robin_1cpu1vote.py`

| Short claim | Source evidence |
|---|---|
| The file defines six rotating fingerprint checks | `ROTATING_FINGERPRINT_CHECKS` lists `clock_drift`, `cache_timing`, `simd_bias`, `thermal_drift`, `instruction_jitter`, `anti_emulation`. |
| The configured active count is four | `ACTIVE_FINGERPRINT_CHECK_COUNT = 4`. |
| Selection is tied to the previous epoch block hash | `derive_measurement_nonce()` hashes `rip-309:<previous_epoch_block_hash>`. |
| The helper deterministically ranks check names | `select_active_fingerprint_checks()` sorts the names by SHA-256 of `<nonce>:<name>`. |
| A normal selection takes the first four ranked checks | The helper returns `tuple(ranked[:active_count])`. |
| Missing/all-zero previous hash fails closed to all six | The helper returns the full `ROTATING_FINGERPRINT_CHECKS` tuple for empty or all-zero input. |
| The demo result is deterministic | `rotation_demo.py` and `evidence/rotation_demo_output.txt` use the public fixed hash `"a" * 64` and assert the resulting selection. |

## Scope boundary

The package demonstrates this public helper and its fail-closed fallback. The source file itself notes that the live reward path uses `get_reward_active_fingerprint_checks`; the short does not claim that this standalone demo executes the complete node or attestation path.
