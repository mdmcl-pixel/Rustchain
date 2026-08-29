# Syndication frontmatter — RTC address derivation tutorial

## Canonical source

`https://github.com/mdmcl-pixel/Rustchain/blob/bounty-16497-poa-tutorial/docs/rtc-address-derivation-from-public-key.md`

Author credit: `@mdmcl-pixel`

Cover image:
`https://github.com/mdmcl-pixel/Rustchain/blob/bounty-16497-poa-tutorial/syndication/rtc-address-derivation/cover.svg`

## dev.to

```yaml
---
title: "How RustChain Derives a Native RTC Address From an Ed25519 Public Key"
published: false
description: "A code-backed walkthrough of RustChain's current public-key-to-address formula, with a deterministic test vector and no private-key handling."
tags: rust, cryptography, blockchain, opensource
canonical_url: https://github.com/mdmcl-pixel/Rustchain/blob/bounty-16497-poa-tutorial/docs/rtc-address-derivation-from-public-key.md
cover_image: https://raw.githubusercontent.com/mdmcl-pixel/Rustchain/bounty-16497-poa-tutorial/syndication/rtc-address-derivation/cover.svg
---
```

Suggested dev.to excerpt:

> RustChain's native wallet address is deterministic: hash the 32-byte Ed25519 public key with SHA-256, keep the first 40 hex characters, and prefix `RTC`. This tutorial reproduces the current upstream implementation with a public test vector while keeping private-key material completely out of scope.

## Hashnode

```yaml
---
title: "How RustChain Derives a Native RTC Address From an Ed25519 Public Key"
subtitle: "Reproducing the current upstream wallet formula with a public deterministic test vector"
slug: rustchain-rtc-address-ed25519-public-key
tags:
  - Rust
  - Cryptography
  - Blockchain
  - Open Source
canonical: https://github.com/mdmcl-pixel/Rustchain/blob/bounty-16497-poa-tutorial/docs/rtc-address-derivation-from-public-key.md
cover: https://raw.githubusercontent.com/mdmcl-pixel/Rustchain/bounty-16497-poa-tutorial/syndication/rtc-address-derivation/cover.svg
---
```

Suggested Hashnode excerpt:

> This article follows the current `rustchain-wallet/src/keys.rs` implementation and shows, step by step, how a 32-byte Ed25519 public key becomes a 43-character native RTC address. The runnable example uses public data only.

## Attribution / syndication permission

Elyan Labs may cross-post this article to official dev.to and Hashnode properties with permanent attribution to `@mdmcl-pixel`, under the Type D terms of rustchain-bounties #16601. The canonical source above should remain attached so search engines and readers can identify the original.
