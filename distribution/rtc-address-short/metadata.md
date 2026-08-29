# Publication metadata

## Primary title
How RustChain Turns an Ed25519 Public Key Into an RTC Address

## Alternate titles
1. RustChain Wallet Addresses Explained in 60 Seconds
2. From Public Key to RTC Address: The Exact RustChain Formula

## Description
RustChain's current wallet derives a native RTC address from a 32-byte Ed25519 public key by hashing the public-key bytes with SHA-256, taking the first 40 hexadecimal characters, and prefixing them with `RTC`.

This short uses the actual upstream `rtc_address()` implementation and a public deterministic test vector. No private keys, seeds, mnemonics, or wallet secrets are used or displayed.

Source: https://github.com/Scottcjn/Rustchain
Implementation: https://github.com/Scottcjn/Rustchain/blob/main/rustchain-wallet/src/keys.rs

Author: @mdmcl-pixel

## Tags
`RustChain`, `RTC`, `Ed25519`, `cryptography`, `wallet`, `blockchain`, `open source`, `Proof of Antiquity`

## Hook text
A RustChain wallet address is not your public key — it is a short fingerprint of it.

## Pinned-comment suggestion
The derivation shown here uses public-key bytes only. Never publish a wallet private key, seed phrase, mnemonic, or recovery material.

## Thumbnail / first-frame text
`PUBLIC KEY → RTC ADDRESS`

## Attribution / rights
Package text, capture instructions, and deterministic demo in this directory are original work prepared for @mdmcl-pixel. Elyan Labs may publish the package on official channels with author attribution under the terms of rustchain-bounties #16601.
