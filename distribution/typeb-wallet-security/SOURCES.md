# Factual source map

Primary source: `https://github.com/Scottcjn/Rustchain/blob/main/rustchain-wallet/src/keys.rs`

| Narration claim | Source evidence |
|---|---|
| `KeyPair` stores Ed25519 signing and verifying keys | `KeyPair { signing_key: SigningKey, verifying_key: VerifyingKey }`. |
| New key generation starts from 32 random bytes | `KeyPair::generate()` creates `[0u8; 32]`, fills it with `getrandom::fill`, then passes it to `SigningKey::from_bytes`. |
| The public key is derived from the signing key | `let verifying_key = signing_key.verifying_key();`. |
| Public key can be displayed as hex or Base58 | `public_key_hex()` and `public_key_base58()` encode `self.verifying_key.as_bytes()`. |
| RTC address is SHA-256 of public/verifying-key bytes, truncated to 40 hex chars and prefixed with RTC | `KeyPair::rtc_address()` implements exactly this formula. |
| Native address is 43 chars and deterministic | `test_rtc_address_format()` asserts prefix/length/hex; `test_rtc_address_deterministic()` derives twice and asserts equality. |
| Signing uses the private signing key | `sign()` calls `self.signing_key.sign(message)`. |
| Verification uses the public verifying key | `verify()` calls `self.verifying_key.verify(message, &sig)`. |
| Signature length is checked at 64 bytes | `verify()` returns `InvalidSignature` when `signature.len() != 64`. |
| Private-key export helpers exist | `export_private_key()` and `export_private_key_bytes()` return the signing-key bytes in encoded/raw form. |
| Public deterministic address example | The fixed public vector `00..1f` hashes to `630dcd...` and produces `RTC630dcd2966c4336691125448bbb25b4ff412a49c`; independently validated in the related public-only demo under `distribution/rtc-address-short/` on the dedicated package branch. |

## Explicit non-claims

This production kit does not claim that:
- address derivation proves ownership;
- a public key can create a valid signature;
- knowing an address or public key reveals the private key;
- the wallet source alone proves mining eligibility, hardware attestation, or token value.
