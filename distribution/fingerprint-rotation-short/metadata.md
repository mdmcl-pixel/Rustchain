# Publication metadata

## Primary title
RustChain Rotates Its Hardware Fingerprint Checks

## Alternate titles
1. Why RustChain Does Not Use One Fixed Hardware Checklist
2. Six Hardware Checks, Four Active: RustChain RIP-309 in 60 Seconds

## Description
RustChain's public RIP-200 code defines six hardware fingerprint checks and a deterministic selector that activates four for a normal previous-epoch hash. If that hash is missing or all zeros, the helper fails closed by activating all six.

This short shows the actual public source plus a fixed-hash local demonstration. It does not claim to reproduce the complete live node or hardware-attestation pipeline.

Source: https://github.com/Scottcjn/Rustchain
Code: https://github.com/Scottcjn/Rustchain/blob/main/node/rip_200_round_robin_1cpu1vote.py
Author: @mdmcl-pixel

## Tags
`RustChain`, `Proof of Antiquity`, `hardware fingerprinting`, `blockchain`, `security`, `open source`

## Hook
RustChain has six hardware checks — but the active subset can rotate from epoch to epoch.

## First-frame text
`6 CHECKS · 4 ACTIVE`

## Rights
Package text, code, and capture plan are original work prepared for @mdmcl-pixel. Elyan Labs may publish the package on official channels with author attribution under rustchain-bounties #16601.
