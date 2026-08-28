# Deriving a RustChain RTC address from an Ed25519 public key

**Author:** `mdmcl-pixel`  
**Assistance disclosure:** prepared and validated with GPT-5.6 Sol under the repository owner's direction.

RustChain wallets use Ed25519 keys, and the current RustChain wallet implementation derives a native address from the **public key**, not from the private key. The implementation in `rustchain-wallet/src/keys.rs` documents the rule directly:

`RTC address = "RTC" + sha256(pubkey_bytes)[:40]` (hex)

Upstream implementation: https://github.com/Scottcjn/Rustchain/blob/main/rustchain-wallet/src/keys.rs

This tutorial reproduces that address-derivation step with a tiny Python program that uses only the standard library. It does **not** create, import, export, or reveal a private key. That is intentional: an RTC address can be derived from public material alone, and private signing material should never be pasted into a tutorial, bounty claim, chat, issue, or public repository.

## 1. What the upstream code does

The RustChain wallet's `KeyPair::rtc_address()` method takes the 32-byte Ed25519 verifying key, hashes those bytes with SHA-256, converts the 32-byte digest to lowercase hexadecimal, keeps the first 40 hexadecimal characters, and prefixes them with `RTC`.

The result is therefore:

- `RTC` prefix: 3 characters
- truncated SHA-256 hex: 40 characters
- total address length: 43 characters

The upstream tests also check that generated addresses start with `RTC`, have length 43, contain hexadecimal characters after the prefix, and are deterministic for the same keypair.

## 2. Why use the public key

A public key is designed to be shared. A private key is not.

That distinction matters operationally. A bounty maintainer may need a public RTC address so they know where to send a reward. They do **not** need the private key that controls that address. The same principle applies to examples: a derivation demo can safely use a fixed sample public key and still demonstrate the exact address transformation.

The runnable example in this repository uses the deterministic byte sequence `00 01 02 ... 1f` as a 32-byte sample public key. It is only a test vector; it is not presented as a real wallet keypair and it does not control funds.

## 3. Run the example

The runnable file is:

`examples/rtc_address_from_pubkey.py`

Run it with Python 3.10+:

```bash
python examples/rtc_address_from_pubkey.py
```

No third-party packages are required.

The program performs four steps:

1. Confirm the supplied public key is exactly 32 bytes.
2. Compute `SHA-256(public_key_bytes)`.
3. Take the first 40 hexadecimal characters of the digest.
4. Prefix the result with `RTC`.

For the fixed sample key, the full SHA-256 digest is:

`630dcd2966c4336691125448bbb25b4ff412a49c732db2c8abc1b8581bd710dd`

Keeping the first 40 hex characters and adding the prefix gives:

`RTC630dcd2966c4336691125448bbb25b4ff412a49c`

## 4. Why the length check matters

Ed25519 public keys are 32 bytes. If an example silently accepted any input length, it could teach the wrong contract: a random string, wallet name, compressed key from another curve, or truncated value could be hashed into something that *looks* like an RTC address while not representing the input type the RustChain wallet code expects.

The example therefore rejects invalid lengths before hashing. It deliberately tries a short input during its self-test and confirms that the failure is explicit.

That does not prove that an arbitrary 32-byte value corresponds to a usable secret key. The example is only demonstrating the address-format transformation implemented by RustChain. Real wallet creation should still use the project's supported wallet software so key generation and storage are handled correctly.

## 5. Determinism and verification

Address derivation must be deterministic: the same public key bytes should always produce the same RTC address. The sample program pins the expected result as a test vector and asserts:

- the exact derived address matches the known expected value;
- the result starts with `RTC`;
- the result has exactly 43 characters;
- every character after `RTC` is lowercase hexadecimal;
- an invalid public-key length is rejected.

If any of those properties change, the program stops instead of printing a misleading success message.

## 6. What this example does not do

This is not a wallet generator, signer, miner, transfer client, seed manager, or recovery tool. It never handles private material. It also does not claim that deriving an address proves ownership. Ownership comes from possessing the corresponding private signing key and successfully producing valid signatures where required.

That separation is useful for understanding the system:

1. **The public key identifies the verification key.**
2. **The RTC address is a compact deterministic identifier derived from that public key.**
3. **The private key proves control by signing; it should remain secret.**

For the production wallet implementation, key generation, signing, verification, and the authoritative address derivation logic, use the upstream RustChain repository:

https://github.com/Scottcjn/Rustchain
