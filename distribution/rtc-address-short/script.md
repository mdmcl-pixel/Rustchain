# Short script — “How RustChain Turns a Public Key Into an RTC Address”

**Target duration:** 50–58 seconds at roughly 135–150 words/minute  
**Format:** 9:16 vertical  
**Author credit:** `@mdmcl-pixel`  
**Hook:** “A RustChain wallet address is not your public key — it is a short fingerprint of it.”

## Narration

A RustChain wallet address is not your public key — it is a short fingerprint of it.

The current RustChain wallet uses Ed25519 keys. To derive the address, it takes the 32 public-key bytes, hashes them with SHA-256, converts that hash to hex, keeps the first 40 hex characters, and adds the prefix `RTC`.

So the format is simple: `RTC` plus 40 hex characters — 43 characters total.

Here is a public test vector. The public key is just bytes zero through thirty-one. The script hashes it and produces `RTC630dcd2966c4336691125448bbb25b4ff412a49c`.

The important security boundary: this derivation needs only the public key. Your private key is for signing and should never be shown in a video, screenshot, issue, or chat.

That is how RustChain turns a public Ed25519 key into a compact RTC address.
