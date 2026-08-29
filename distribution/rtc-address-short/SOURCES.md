# Source map

Every technical statement in the short maps to current public RustChain source.

| Claim | Public source |
|---|---|
| RustChain wallet key management uses Ed25519 signing/verifying keys | `rustchain-wallet/src/keys.rs` imports `ed25519_dalek::{..., SigningKey, ..., VerifyingKey}` and stores them in `KeyPair` — https://github.com/Scottcjn/Rustchain/blob/main/rustchain-wallet/src/keys.rs |
| RTC address derivation hashes the verifying/public key bytes with SHA-256 | `KeyPair::rtc_address()` calls `Sha256::digest(self.verifying_key.as_bytes())` — same source file |
| Address is `RTC` plus the first 40 hex characters of the hash | `format!("RTC{}", &hex_hash[..40])` — same source file |
| Native address length is 43 characters | upstream `test_rtc_address_format()` asserts `addr.len() == 43` — same source file |
| Address derivation is deterministic | upstream `test_rtc_address_deterministic()` derives the address twice and asserts equality — same source file |
| The private/signing key is used for signing | `KeyPair::sign()` signs with `self.signing_key` — same source file |
| The demo test vector is deterministic and public-only | `distribution/rtc-address-short/demo.py` in this package; captured output in `evidence/demo_output.txt` |

## Scope note

The short explains address derivation only. It does not claim that deriving an address proves wallet ownership, hardware attestation, mining eligibility, or transaction validity.
