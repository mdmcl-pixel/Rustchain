#!/usr/bin/env python3
"""Educational Proof-of-Antiquity reward-weight model.

This is NOT RustChain consensus or payout code. It demonstrates how configured
multipliers change relative shares when applied to baseline eligible work.
"""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Machine:
    name: str
    baseline_work: float
    multiplier: float

    @property
    def weighted_score(self) -> float:
        return self.baseline_work * self.multiplier


def normalized_shares(machines: Iterable[Machine]) -> list[tuple[Machine, float]]:
    fleet = list(machines)
    if not fleet:
        raise ValueError("fleet must contain at least one machine")

    for machine in fleet:
        if machine.baseline_work < 0:
            raise ValueError(f"baseline_work must be non-negative: {machine.name}")
        if machine.multiplier <= 0:
            raise ValueError(f"multiplier must be positive: {machine.name}")

    total = sum(machine.weighted_score for machine in fleet)
    if total <= 0:
        raise ValueError("fleet weighted score must be greater than zero")

    return [(machine, machine.weighted_score / total) for machine in fleet]


def main() -> None:
    fleet = [
        Machine("PowerPC G4", 1.0, 2.5),
        Machine("Power Mac G5", 1.0, 2.0),
        Machine("Apple Silicon M1", 1.0, 1.2),
        Machine("Modern x86_64", 1.0, 1.0),
    ]

    rows = normalized_shares(fleet)

    print("Educational Proof-of-Antiquity reward weighting")
    print("NOT consensus, attestation, wallet, or payout code")
    print()
    print(f"{'Machine':<20} {'Work':>7} {'Mult':>7} {'Weighted':>10} {'Share':>9}")
    print("-" * 58)
    for machine, share in rows:
        print(
            f"{machine.name:<20} "
            f"{machine.baseline_work:>7.2f} "
            f"{machine.multiplier:>7.2f} "
            f"{machine.weighted_score:>10.2f} "
            f"{share * 100:>8.2f}%"
        )

    total_weight = sum(machine.weighted_score for machine, _ in rows)
    total_share = sum(share for _, share in rows)

    print("-" * 58)
    print(f"{'Total':<20} {'':>7} {'':>7} {total_weight:>10.2f} {total_share * 100:>8.2f}%")

    shares = {machine.name: share for machine, share in rows}
    assert abs(total_weight - 6.7) < 1e-12
    assert abs(total_share - 1.0) < 1e-12
    assert abs(shares["PowerPC G4"] - (2.5 / 6.7)) < 1e-12
    assert abs(shares["Modern x86_64"] - (1.0 / 6.7)) < 1e-12

    print()
    print("Validation: PASS")


if __name__ == "__main__":
    main()
