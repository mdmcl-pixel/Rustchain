# Short script — “RustChain Does Not Trust the Same Hardware Test Every Time”

**Target duration:** 50–58 seconds  
**Format:** 9:16 vertical  
**Author credit:** `@mdmcl-pixel`  
**Hook:** “RustChain has six hardware checks — but the active subset can rotate from epoch to epoch.”

## Narration

RustChain has six hardware checks — but the active subset can rotate from epoch to epoch.

The current RIP-200 code lists clock drift, cache timing, SIMD bias, thermal drift, instruction jitter, and anti-emulation. The configured active count is four.

For a real previous-epoch block hash, the code derives a SHA-256 nonce, ranks the six check names deterministically from that nonce, and selects four. That means the subset is reproducible from chain state instead of being chosen by the miner.

Here is a public fixed-hash demo. It selects thermal drift, cache timing, instruction jitter, and anti-emulation.

There is also a fail-closed rule: if the previous hash is missing or all zeros, the helper activates all six checks rather than using a predictable fallback subset.

That is a small detail, but it shows the design goal: hardware evidence should be harder to game by preparing for one permanently fixed checklist.
