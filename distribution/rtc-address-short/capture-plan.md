# 9:16 capture plan

**Canvas:** 1080×1920 vertical. Keep all essential text inside the center 80% safe area so Shorts UI chrome does not cover it.

| Time | Visual / capture instruction | On-screen text |
|---|---|---|
| 0:00–0:04 | Tight crop of a terminal or editor showing only the words `public key → RTC address`. No private-key material anywhere on screen. | `PUBLIC KEY → RTC ADDRESS` |
| 0:04–0:10 | Open `rustchain-wallet/src/keys.rs` and frame the `rtc_address()` function. Slowly highlight `Sha256::digest(self.verifying_key.as_bytes())`. | `Ed25519 public key` + `SHA-256` |
| 0:10–0:17 | Continue highlight to `format!("RTC{}", &hex_hash[..40])`. Zoom enough that the prefix and `[..40]` are readable. | `"RTC" + first 40 hex chars` |
| 0:17–0:22 | Cut to a clean text card: `RTC` on first line; `40 hexadecimal characters` on second; `43 total` on third. | `43 characters total` |
| 0:22–0:35 | Terminal capture: run `python distribution/rtc-address-short/demo.py`. Start with command visible, then let all four output lines appear. Do not type or reveal any secret. | `PUBLIC TEST VECTOR` |
| 0:35–0:42 | Freeze on `RTC630dcd2966c4336691125448bbb25b4ff412a49c` and underline the `RTC` prefix, then the 40-char suffix. | `deterministic address` |
| 0:42–0:51 | Split card: left `Public key: safe to share when needed`; right `Private key: NEVER show`. Avoid displaying any real private-key string. | `PRIVATE KEY ≠ PUBLIC KEY` |
| 0:51–0:58 | Return to source function and terminal PASS output side-by-side. End on the repo URL. | `Source: github.com/Scottcjn/Rustchain` |

## Capture checklist

- Use the public deterministic vector from `demo.py`; never substitute a real wallet secret.
- Capture the current upstream `rtc_address()` implementation, not a paraphrased slide.
- Capture `Validation: PASS` in the terminal.
- Do not show a seed phrase, mnemonic, private key, wallet JSON, environment variables, browser autofill, clipboard history, or shell history containing credentials.
- If the editor sidebar exposes unrelated files, collapse it before recording.
- Keep source-code text large enough to read on a phone.
