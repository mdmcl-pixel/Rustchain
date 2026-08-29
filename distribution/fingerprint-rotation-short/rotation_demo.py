"""Deterministic public demo of RustChain's six-check rotation helper."""

import hashlib

CHECKS = (
    "clock_drift",
    "cache_timing",
    "simd_bias",
    "thermal_drift",
    "instruction_jitter",
    "anti_emulation",
)


def select(previous_epoch_block_hash: str) -> tuple[str, ...]:
    normalized = (previous_epoch_block_hash or "").strip().lower()
    if not normalized or normalized == "0" * 64:
        return CHECKS
    nonce = hashlib.sha256(f"rip-309:{normalized}".encode()).hexdigest()
    ranked = sorted(
        CHECKS,
        key=lambda name: hashlib.sha256(f"{nonce}:{name}".encode()).hexdigest(),
    )
    return tuple(ranked[:4])


def main() -> None:
    previous_hash = "a" * 64
    active = select(previous_hash)
    print("Previous epoch hash:", previous_hash)
    print("Active checks:", ", ".join(active))
    assert active == (
        "thermal_drift",
        "cache_timing",
        "instruction_jitter",
        "anti_emulation",
    )
    assert select("") == CHECKS
    print("Missing-hash fail-closed count:", len(select("")))
    print("Validation: PASS")


if __name__ == "__main__":
    main()
