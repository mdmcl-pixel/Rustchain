# Publication metadata

## Primary title
What a RustChain Wallet Actually Does With Your Keys

## Alternate titles
1. RustChain Wallet Security: Address vs Public Key vs Private Key
2. From Ed25519 Keypair to RTC Address — Without Exposing Secrets

## Description
A source-backed walkthrough of RustChain's current Ed25519 wallet key lifecycle: key generation, public-key formats, native RTC address derivation, message signing, and signature verification.

The production kit deliberately separates public data from secret material. Recording instructions use public source and deterministic test vectors only; no real seed phrase, mnemonic, private key, recovery data, or wallet JSON needs to appear on screen.

Source repository: https://github.com/Scottcjn/Rustchain
Source file: https://github.com/Scottcjn/Rustchain/blob/main/rustchain-wallet/src/keys.rs
Author: @mdmcl-pixel

## Tags
`RustChain`, `RTC`, `Ed25519`, `wallet security`, `cryptography`, `open source`, `blockchain`

## Chapters
- 0:00 Address vs public vs private key
- 0:20 Inside RustChain `KeyPair`
- 0:55 Generating Ed25519 keys
- 1:25 Public-key encodings
- 1:55 Deriving the native RTC address
- 2:35 Format and determinism tests
- 2:55 Signing vs verification
- 3:30 Public deterministic demo
- 4:00 What never belongs in a tutorial
- 4:30 Source and recap

## Thumbnail concepts
1. `ADDRESS ≠ PUBLIC KEY ≠ PRIVATE KEY`
2. `PUBLIC → SHA-256 → RTC`
3. `NEVER SHOW THE PRIVATE KEY`

## Rights
Original package prepared for @mdmcl-pixel. Elyan Labs may publish it on official channels with permanent author attribution under rustchain-bounties #16601.
