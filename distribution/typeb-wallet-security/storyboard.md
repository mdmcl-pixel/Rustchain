# Storyboard — shot-by-shot capture plan

**Format:** 16:9, 1920×1080 master. Keep code at 150%+ editor zoom.

| Time | Shot | Exact capture instruction |
|---|---|---|
| 0:00–0:20 | Cold open | Three large labels on screen: `RTC address`, `public key`, `private key`. Cross out an equals sign between them. Do not show any real wallet material. |
| 0:20–0:55 | KeyPair structure | Open `rustchain-wallet/src/keys.rs`. Frame the `KeyPair` struct and highlight `signing_key: SigningKey` then `verifying_key: VerifyingKey`. |
| 0:55–1:25 | Generation | Highlight `KeyPair::generate()`: 32-byte seed, `SigningKey::from_bytes`, then `signing_key.verifying_key()`. Add overlay: `secret → signing` / `derived public → verifying`. |
| 1:25–1:55 | Public representations | Highlight `public_key_hex()` and `public_key_base58()`. Show only a fixed/public example string in any terminal card. |
| 1:55–2:35 | Address formula | Highlight `rtc_address()`: SHA-256 over verifying-key bytes, hex encoding, `RTC` + `[..40]`. Animate the formula as a clean text diagram. |
| 2:35–2:55 | Format tests | Scroll to `test_rtc_address_format()` and `test_rtc_address_deterministic()`. Highlight prefix, 43-char length and repeatability assertions. |
| 2:55–3:30 | Signing boundary | Highlight `sign()` using `self.signing_key`, then `verify()` using `self.verifying_key`. Frame the `signature.len() != 64` rejection. |
| 3:30–4:00 | Public-only demo | Terminal card reproducing the deterministic public-key hash and resulting RTC address. Use the fixed `00..1f` public vector; no real wallet file. |
| 4:00–4:30 | Safety card | Full-screen checklist: `Safe: address / public key / public test vector`; `Secret: private key / seed / mnemonic / recovery data`. |
| 4:30–end | Source + close | Return to the `KeyPair` struct and address method. Show repository link and author credit. |

## Publisher notes

- Collapse editor sidebars if they expose local file paths or unrelated sensitive files.
- Clear shell history before recording terminal scenes.
- Do not open a real wallet JSON file on camera.
- Use only fixed public test vectors or disposable test-only keys where a cryptographic operation must be shown.
- Avoid claims about token price, guaranteed earnings, or wallet security beyond what the cited source actually implements.
