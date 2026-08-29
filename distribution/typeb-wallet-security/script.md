# Narration script — “What a RustChain Wallet Actually Does With Your Keys”

**Target duration:** 4–5 minutes  
**Author credit:** `@mdmcl-pixel`

## Script

A wallet address, a public key, and a private key are not the same thing — and mixing them up is one of the easiest ways to make a crypto tutorial dangerous.

So this walkthrough stays inside RustChain's current public wallet source and follows the key lifecycle without displaying any real secret.

The implementation lives in `rustchain-wallet/src/keys.rs`. RustChain's `KeyPair` stores two Ed25519 objects: a `SigningKey` and a `VerifyingKey`. The signing key is the secret half. The verifying key is the public half.

When a new keypair is generated, the wallet asks the operating system for 32 random bytes. Those bytes become the Ed25519 signing key, and the verifying key is derived from it. The important boundary is immediate: the private signing material exists because it must authorize signatures. It is not something a tutorial, screenshot, issue comment, or support chat should ever need.

RustChain also exposes the public key in two display formats. `public_key_hex()` returns the verifying-key bytes encoded as hexadecimal. `public_key_base58()` encodes the same public bytes in Base58. Those are representations of public data, not replacements for the private key.

Now look at address derivation. The `rtc_address()` method takes the verifying-key bytes — again, the public side — and hashes them with SHA-256. It hex-encodes the 32-byte hash, takes the first 40 hexadecimal characters, and prefixes them with `RTC`.

That gives the native address format used by this wallet implementation: three characters of prefix plus forty hexadecimal characters, forty-three characters total. The upstream tests explicitly check the prefix, total length, hexadecimal suffix, and determinism.

Determinism matters here. The same public key must always produce the same RTC address. The test suite calls `rtc_address()` twice on one keypair and asserts the addresses match.

But deriving an address is not the same as proving ownership of it.

Ownership comes from the signing key. The `sign()` method uses the private `SigningKey` to sign a message and returns the signature bytes. The corresponding `verify()` method checks the message and signature with the public `VerifyingKey`. The source rejects signatures that are not exactly 64 bytes before verification.

That separation is the core security story:

The public key can be used to derive the address and verify signatures. The private key is what creates those signatures. Knowing an RTC address does not give you the private key. Knowing a public key does not give you the private key. And reproducing the address formula does not authorize a transfer.

We can demonstrate the public side safely with a deterministic test vector. Use thirty-two public bytes from `00` through `1f`. Hash those bytes with SHA-256. The digest begins `630dcd2966c4336691125448bbb25b4ff412a49c...`. Keep the first forty hex characters and add the prefix. The result is:

`RTC630dcd2966c4336691125448bbb25b4ff412a49c`.

That demo never generates or reads a real private key. It proves only that the public address formula is reproducible.

There is one more detail worth noticing in the source. `KeyPair` exposes private-key export helpers because software sometimes has to persist or migrate key material. That makes operational handling especially important: a wallet file or exported secret is sensitive even when the address derived from it is public.

So if you are documenting RustChain wallet behavior, the safe rule is simple.

Show the public key if the task requires it. Show the RTC address. Show deterministic public test vectors. Show signature verification with disposable test keys in a controlled example if necessary.

But never record or paste a real seed phrase, mnemonic, private key, recovery secret, wallet JSON containing secret material, environment variable, or clipboard history.

RustChain's current wallet source makes the roles clear: public key for identification and verification, private key for signing, and RTC address as a deterministic hash-derived identifier of the public key.

That is the boundary a safe wallet tutorial should preserve.
