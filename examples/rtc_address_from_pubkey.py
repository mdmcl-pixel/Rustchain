#!/usr/bin/env python3
"""Derive a RustChain RTC address from a 32-byte Ed25519 public key.

This educational example uses public material only. It does not create or expose
private keys and is not a replacement for the supported RustChain wallet tools.
"""

from hashlib import sha256


def rtc_address_from_pubkey(pubkey: bytes) -> str:
    if len(pubkey) != 32:
        raise ValueError("RustChain Ed25519 public key must be exactly 32 bytes")
    digest = sha256(pubkey).hexdigest()
    return "RTC" + digest[:40]


def main() -> None:
    pubkey = bytes(range(32))
    address = rtc_address_from_pubkey(pubkey)

    print("RustChain RTC address derivation demo")
    print("Public key (hex):", pubkey.hex())
    print("SHA-256:", sha256(pubkey).hexdigest())
    print("RTC address:", address)

    expected = "RTC630dcd2966c4336691125448bbb25b4ff412a49c"
    assert address == expected
    assert len(address) == 43
    assert address.startswith("RTC")
    assert all(c in "0123456789abcdef" for c in address[3:])

    try:
        rtc_address_from_pubkey(b"short")
    except ValueError as exc:
        print("Invalid-length check:", exc)
    else:
        raise AssertionError("invalid-length public key was not rejected")

    print("Validation: PASS")


if __name__ == "__main__":
    main()
