# RustChain Shorts package — RTC address derivation

**Bounty route:** Scottcjn/rustchain-bounties#16601, Type C — Shorts / clip kit  
**Author:** @mdmcl-pixel  
**Target:** 50–58 second vertical short  
**Pitch:** show the exact current RustChain formula that turns a 32-byte Ed25519 public key into a native `RTC…` address, backed by upstream source and a deterministic public test vector.

## Package contents

- `script.md` — timed short-form narration with hook
- `capture-plan.md` — exact 9:16 capture instructions and security-safe recording checklist
- `metadata.md` — title variants, description, tags, first-frame text and attribution
- `SOURCES.md` — claim-by-claim mapping to current public RustChain source
- `demo.py` — standard-library public-key-only deterministic demo
- `evidence/demo_output.txt` — captured successful run showing `Validation: PASS`

## Validation

The deterministic demo was executed with Python. It uses public bytes `0x00` through `0x1f`, derives:

`RTC630dcd2966c4336691125448bbb25b4ff412a49c`

and its assertions pass.

The authoritative implementation covered by the package is current upstream `rustchain-wallet/src/keys.rs`, where `KeyPair::rtc_address()` computes SHA-256 over the Ed25519 verifying-key bytes, hex-encodes it, takes the first 40 hex characters, and prefixes `RTC`.

## Safety boundary

No private key, seed phrase, mnemonic, recovery data, or production wallet file is required by this package. The recording plan explicitly uses a public deterministic vector and tells the publisher not to expose shell history, clipboard history, environment variables, or wallet secrets.

## Publication permission

This package is original work prepared for @mdmcl-pixel. It may be published by Elyan Labs on official channels with permanent author attribution under the terms of bounty #16601.
