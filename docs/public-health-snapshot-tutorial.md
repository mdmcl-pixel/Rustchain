# A safe, read-only RustChain health snapshot in Python

RustChain is a DePIN blockchain built around Proof of Antiquity: instead of treating old computers as obsolete, the project uses hardware attestation and age-sensitive reward multipliers to make physical machines part of network identity. The upstream README describes six hardware-oriented checks, including clock drift, cache timing, SIMD identity, thermal entropy, instruction-path jitter, and anti-emulation detection. This tutorial does **not** attempt to reproduce or bypass those checks. It stays on the public, read-only side of the network and shows how to collect a small operational snapshot safely.

The goal is deliberately narrow: fetch the public `/health` and `/api/miners` JSON endpoints, validate what comes back, cap how much data is read, and print only a bounded subset of fields. That makes the example useful for dashboards, uptime notes, classroom demos, or a local monitoring prototype without needing an API key, wallet secret, transaction, miner enrollment, or production write.

Upstream project: https://github.com/Scottcjn/Rustchain  
Project site: https://rustchain.org

## Why bother with defensive reads?

A five-line `requests.get(...).json()` demo is convenient, but operational tooling benefits from a few extra constraints. Public endpoints can be slow, unavailable, misconfigured, or unexpectedly large. A monitor should fail clearly rather than hang forever or trust every field blindly.

The example in `examples/rustchain_health_snapshot.py` therefore uses only the Python standard library and adds four basic guardrails:

1. **Timeouts.** Every live request has a finite timeout.
2. **Content-type checking.** The client expects JSON rather than silently parsing an HTML error page.
3. **Response-size bounding.** Reads are capped at 1 MB so a monitoring helper cannot accidentally consume an unbounded response.
4. **Field normalization.** The output keeps only a small set of expected values and treats wrong types as missing instead of guessing.

Those checks are not RustChain consensus logic. They are ordinary client-side hygiene around a public status feed.

## Run it offline first

The script includes an embedded sample mode so its parsing and output can be tested without touching the network:

```bash
python examples/rustchain_health_snapshot.py --sample
```

The output is a small JSON document with normalized health fields and a limited miner list. You can reduce the list further:

```bash
python examples/rustchain_health_snapshot.py --sample --miner-limit 2
```

Sample mode is important for repeatable tests. A unit test should not fail merely because a public node is temporarily unreachable.

## Live read-only mode

When network access is available, omit `--sample`:

```bash
python examples/rustchain_health_snapshot.py
```

By default the script reads:

```text
https://rustchain.org/health
https://rustchain.org/api/miners
```

You can point it at another compatible public node without editing code:

```bash
python examples/rustchain_health_snapshot.py \
  --base-url https://rustchain.org \
  --timeout 5 \
  --miner-limit 3
```

The script performs **GET requests only**. It does not submit attestations, claim jobs, move RTC, modify a wallet, or call any administrative route.

## Reading the snapshot carefully

The normalized `health` object exposes only four fields when they have the expected type:

- `ok`: a Boolean status flag if the endpoint supplies one.
- `epoch`: a numeric epoch value if present.
- `miners`: a numeric miner count if present.
- `version`: a string version value if present.

The miner list similarly keeps only `miner_id`, `architecture`/`arch`, and numeric `weight`, and it truncates the list to the requested limit.

This is intentionally conservative. Public APIs evolve. A field being absent does not automatically mean the network is unhealthy, and a field being present does not prove every subsystem is functioning. Treat the snapshot as an observation layer, not consensus truth.

## Tests

The companion unit test uses sample and mocked data, so it is deterministic and non-destructive:

```bash
python -m unittest tests/test_rustchain_health_snapshot.py -v
```

The tests check that:

- a non-object health payload is rejected;
- miner output obeys the configured row limit;
- an oversized response is rejected before JSON parsing;
- the command-line sample mode produces valid JSON without network access.

That last property is useful in CI because it separates **our parser correctness** from **remote service availability**.

## Extending it safely

A reasonable next step is to write each snapshot to a timestamped local file and compare only stable, documented fields over time. For example, you could alert when repeated reads fail or when a value stops changing for an unexpectedly long period. Keep the monitor read-only and rate-limited.

Avoid turning a status script into an attestation or security-testing client by accident. RustChain exposes security-sensitive components and has separate bounty scopes for authorized testing. Reading public health data is one thing; fuzzing, exploitation, or attempts to defeat hardware identity checks are different activities and should only happen under an explicit authorized scope.

## What this demonstrates

The useful lesson is not merely how to call two URLs. It is how to build a small client that behaves predictably around a public blockchain service:

- constrain network operations;
- validate response shape;
- bound output;
- keep an offline test path;
- distinguish observation from proof.

That pattern generalizes well to explorers, public DePIN dashboards, and agent monitoring systems. For RustChain specifically, it provides a lightweight way to observe the public network while leaving Proof-of-Antiquity attestation, wallets, rewards, and consensus untouched.

## Source notes

The project description and Proof-of-Antiquity framing in this tutorial are based on the current upstream RustChain README:

https://github.com/Scottcjn/Rustchain/blob/main/README.md

The runnable example is intentionally narrower than the full RustChain API. It uses only public status reads and makes no claim that those endpoints alone establish miner authenticity, payout correctness, or consensus safety.

Authorship disclosure: this tutorial and example were prepared with OpenAI GPT-5.6 Sol assistance under operator authorization and then validated with the included offline tests.
