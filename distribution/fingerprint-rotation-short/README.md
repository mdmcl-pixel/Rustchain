# RustChain Shorts package — rotating hardware checks

**Bounty route:** Scottcjn/rustchain-bounties#16601, Type C  
**Author:** @mdmcl-pixel  
**Target duration:** 50–58 seconds  
**Pitch:** explain, from current public source, that RustChain defines six hardware fingerprint checks, normally selects four deterministically from previous-epoch state, and fails closed to all six if the previous hash is unavailable.

## Package

- `script.md` — narration + hook
- `capture-plan.md` — exact 9:16 capture instructions
- `metadata.md` — title variants, description, tags and attribution
- `SOURCES.md` — claim-by-claim source map
- `rotation_demo.py` — deterministic stdlib demonstration using a fake public block hash
- `evidence/rotation_demo_output.txt` — captured output with `Validation: PASS`

## Validation

The public demo was executed with the fixed previous-epoch hash `a` repeated 64 times. It deterministically selected:

`thermal_drift, cache_timing, instruction_jitter, anti_emulation`

and verified that an empty previous hash returns all six checks.

## Accuracy boundary

This package demonstrates the public selection helper in `node/rip_200_round_robin_1cpu1vote.py`. It does not claim to run the complete live reward path, node, or hardware attestation flow.

## Publication permission

Elyan Labs may publish this original package on official channels with permanent `@mdmcl-pixel` author attribution under bounty #16601.
