# Proof of Antiquity, explained with a tiny offline reward model

RustChain is a DePIN network built around **Proof of Antiquity (PoA)**: instead of rewarding only raw throughput or stake, the project gives older and more unusual real hardware higher reward multipliers. The upstream RustChain README describes examples such as a PowerPC G4 at 2.5x, a Power Mac G5 at 2.0x, Apple Silicon M1 at 1.2x, modern x86_64 at 1.0x, and several older architectures at still higher tiers.

This tutorial turns that idea into a small, transparent Python model you can run locally. It does **not** implement RustChain consensus, attestation, wallet logic, or payout rules. It is an educational calculator that answers one narrow question:

> If several machines contribute the same baseline amount of eligible work, how do different PoA multipliers change their relative reward weight?

That distinction matters. Real RustChain eligibility depends on hardware attestation and network rules. A multiplier only matters after the network accepts the machine as genuine. The script below deliberately avoids pretending that a text label such as `"PowerPC G4"` proves anything about the underlying hardware.

Upstream project: https://github.com/Scottcjn/Rustchain

## 1. What the model represents

Suppose four machines each contribute one unit of baseline eligible work:

- PowerPC G4 — 2.5x
- Power Mac G5 — 2.0x
- Apple Silicon M1 — 1.2x
- Modern x86_64 — 1.0x

The educational model computes:

`weighted_score = baseline_work × antiquity_multiplier`

Then it normalizes every machine's weighted score by the fleet total:

`share = machine_weighted_score / total_weighted_score`

This produces a relative allocation, not an on-chain RTC payout. It is useful because it makes the incentive structure visible without requiring a miner, wallet, node, or network connection.

## 2. Run the example

The runnable file is:

`examples/poa_reward_model.py`

Run it with Python 3.10+:

```bash
python examples/poa_reward_model.py
```

The program uses only the Python standard library.

It prints a table containing each sample machine, its baseline work, the configured multiplier, weighted score, and normalized fleet share. It also performs internal assertions so the example fails loudly if the arithmetic changes unexpectedly.

## 3. Why normalization is useful

A multiplier by itself can be hard to reason about. Saying “2.5x” tells you how one machine is weighted relative to a 1.0x baseline, but not how a mixed fleet divides a fixed reward pool.

In the four-machine example, the total weighted score is:

`2.5 + 2.0 + 1.2 + 1.0 = 6.7`

So the G4's educational share is:

`2.5 / 6.7 ≈ 37.31%`

The modern x86_64 machine's share is:

`1.0 / 6.7 ≈ 14.93%`

Nothing magical happened to the baseline work. The difference comes entirely from the multiplier.

That makes PoA's economic preference easy to see: holding baseline work equal, verified older hardware receives more weight.

## 4. The important caveat: identity is not self-reported

The most important thing this model leaves out is also the thing that makes RustChain interesting: **hardware attestation**.

The upstream project describes multiple fingerprint checks, including clock-skew or oscillator drift, cache timing, SIMD identity, thermal behavior, instruction-path jitter, and anti-emulation checks. Those mechanisms are intended to distinguish real machines from VMs or emulators.

This tutorial does not reproduce those checks and does not claim to validate hardware. A user cannot earn a higher tier merely by changing a string in this script. In a real system, the network must first accept the machine's evidence.

That separation is a useful design lesson:

1. **Attestation answers “what machine is this?”**
2. **The multiplier answers “how should accepted work be weighted?”**

Mixing those two questions would make the model misleading.

## 5. Experiment safely

Try changing only `baseline_work` values in the sample fleet. For example, give the modern x86_64 machine 3.0 units of baseline work while leaving the G4 at 1.0. The modern machine may then receive a larger absolute share even with a lower antiquity multiplier.

That shows another important property: a multiplier changes weighting; it does not erase contribution volume.

You can also add a new sample tier. Keep the multiplier clearly labeled as an educational input unless it is copied from current upstream documentation. RustChain's rules can evolve, so the upstream repository remains the source of truth.

## 6. What this teaches about RustChain

The small model highlights why Proof of Antiquity is different from systems that optimize only for modern hardware performance. RustChain's public design explicitly values preservation and hardware diversity. In a simplified equal-work comparison, the weighting mechanism makes that preference quantitative.

The script is intentionally boring: no network calls, no wallet, no mining, no claims about actual payment. That is a feature. It isolates one concept—relative reward weighting—so it can be inspected, changed, and verified offline.

For the real implementation, current multiplier tables, hardware requirements, and attestation logic, use the upstream RustChain repository:

https://github.com/Scottcjn/Rustchain
