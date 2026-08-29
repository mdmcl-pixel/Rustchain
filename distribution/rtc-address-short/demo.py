"""Public-only RustChain RTC address derivation demo for a short-form video.

This script never generates, imports, exports, or handles a private key.
"""

from hashlib import sha256


def rtc_address_from_pubkey(pubkey: bytes) -> str:
    """Derive RustChain's RTC address from exactly 32 public-key bytes."""
    if len(pubkey) != 32:
        raise ValueError("public key must be exactly 32 bytes")
    return "RTC" + sha256(pubkey).hexdigest()[:40]


def main() -> None:
    # Public deterministic test vector: 0x00 through 0x1f.
    pubkey = bytes(range(32))
    digest = sha256(pubkey).hexdigest()
    address = rtc_address_from_pubkey(pubkey)

    print("Public key:", pubkey.hex())
    print("SHA-256:", digest)
    print("RTC address:", address)

    expected = "RTC630dcd2966c4336691125448bbb25b4ff412a49c"
    assert address == expected
    assert len(address) == 43
    assert address.startswith("RTC")
    print("Validation: PASS")


if __name__ == "__main__":
    main()
