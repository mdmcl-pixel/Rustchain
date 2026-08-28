# RustChain architecture security assessment — Bounty #398 Step 1

**Author:** `mdmcl-pixel`  
**Payout address:** `RTCedb6d5ad094e32eb8f4931702f41d0b1291a4bbe`  
**Assistance disclosure:** prepared and validated with GPT-5.6 Sol under the repository owner's direction.

This assessment is a static, non-destructive review of the current RustChain architecture. It covers the four points required by Step 1 of `Scottcjn/rustchain-bounties#398`: the `/attest/submit` flow, hardware fingerprinting and VM-farm resistance, epoch reward calculation/distribution, and one security risk worth prioritizing.

## 1. Attestation and `/attest/submit`

RustChain treats hardware attestation as the admission path into the RIP-200 mining/reward system. A miner first obtains a short-lived challenge nonce and then submits an attestation containing its miner/wallet identity, challenge material, device information, hardware signals, fingerprint results, and—on supported modern paths—Ed25519 signature material.

The important security idea is that the node should not accept a bare statement such as “I am this miner and I own this hardware.” The request is progressively checked. The challenge/nonce binds the submission to a recent server-issued value and makes straightforward replay of an old successful request less useful. Payload-shape and type validation keeps malformed client-controlled structures away from deeper cryptographic and database logic. Where an Ed25519 public key and signature are used, the signature binds the claimed identity and attestation message to a key under the miner's control. The node then evaluates hardware evidence and hardware binding before recording the attestation and using it for current-epoch participation.

The repository has dedicated attestation regression, signature-verification, challenge-binding and fuzz tests, which is appropriate for this surface because `/attest/submit` crosses several trust boundaries at once: untrusted JSON, cryptographic identity, hardware claims, nonce state, SQLite state and ultimately reward eligibility.

A useful architectural property is that attestation state and epoch enrollment are conceptually separate. “The node recently accepted evidence from this miner” is not identical to “this miner is entitled to a particular historical epoch reward.” Keeping a per-epoch enrollment snapshot avoids making old settlements depend only on a mutable “latest attestation” row.

## 2. Hardware fingerprinting and VM-farm resistance

RustChain's anti-farm model does not rely on a user-supplied CPU model string. The repository describes a multi-signal hardware-fingerprinting design involving timing/entropy measurements, cache behavior, SIMD/architecture characteristics, thermal or timing drift, instruction jitter and anti-emulation checks. Hardware-binding and replay/collision logic then uses those observations to make it harder for many logical identities to masquerade as many independent physical machines.

The security benefit comes from combining signals with different spoofing costs. A VM can easily claim `x86_64`, a core count or a model name. It is harder to reproduce a coherent set of physical timing relationships, stable machine identifiers and architecture-specific characteristics while also avoiding anti-emulation indicators. Hardware binding adds another control: once a physical identity is associated with one wallet/miner identity, a second wallet should not be able to claim the same machine as independent capacity without an explicit migration/rebind process.

This is defense in depth rather than a mathematical proof that virtualization is impossible. Timing measurements contain noise; operating-system activity, temperature, virtualization quality and hardware revisions can shift results. Therefore thresholds that are too strict risk false positives, while thresholds that are too forgiving reduce Sybil resistance. The safest architecture is the one RustChain is moving toward: multiple independent signals, explicit validation of input shape, stable binding state, replay/collision detection, regression tests and conservative handling of ambiguous evidence.

The reward system should also avoid treating a client-provided “all checks passed” flag as authoritative. The node should derive eligibility from evidence it validates itself, and it should distinguish “fingerprint accepted,” “hardware identity bound,” “wallet cryptographically proven” and “eligible for a multiplier” rather than collapsing them into one boolean.

## 3. Epoch rewards: calculation and distribution

RIP-200 is framed as one-CPU/one-vote with Proof-of-Antiquity weighting. The public project material describes a fixed per-epoch reward pot and hardware-dependent weighting, where verified vintage hardware can receive a larger relative multiplier than baseline modern hardware. The core fairness requirement is that the epoch pot is divided among the miners that were actually eligible for that epoch, with deterministic weights and without creating extra value through rounding or repeated settlement.

Current repository code includes `node/rip_200_round_robin_1cpu1vote.py` and a `calculate_epoch_rewards_time_aged` path. The settlement integrity work in the repository is especially important: eligibility for a historical epoch should prefer the durable `epoch_enroll` snapshot for that epoch rather than depend solely on `miner_attest_recent`, because the latter represents recent/latest attestation state and can change after the epoch ends.

At settlement time, the architecture should therefore follow this sequence:

1. Resolve the exact epoch and reject invalid/future epochs.
2. Acquire an idempotent settlement claim/lock for that epoch.
3. Read the canonical per-epoch eligible miner set.
4. Resolve validated hardware/antiquity weights.
5. Normalize each miner's weight against the total eligible weight.
6. Allocate the fixed epoch pot deterministically, including a defined rounding policy.
7. Credit balances/ledger records and mark the epoch settled in the same atomic transaction.
8. Make repeated settlement calls return the existing result rather than credit again.

This turns reward calculation into a reproducible state transition instead of “whoever happens to be visible in a latest-state table when the job runs.”

## 4. Security risk: multiple settlement paths and state divergence

The risk I would prioritize is **cross-path epoch settlement divergence/concurrency**. The repository has historically contained more than one path capable of settling or calculating epoch rewards. Even if each path is locally careful, two independent writers are dangerous if they do not share one atomic `claim_epoch()`/settled guard and one canonical schema.

A failure mode is straightforward: settlement path A checks that epoch N is unsettled; settlement path B performs the same check before A commits; both calculate valid-looking rewards; each credits balances through its own connection; only afterward do they mark N settled. The result can be duplicate credit. A different form of the same architectural problem appears when one path reads `epoch_enroll` while another reads mutable `miner_attest_recent`: both may settle only once yet produce different recipient sets for the same epoch.

I am not claiming this as a new vulnerability. The repository already contains settlement-integrity work and discussion around unifying settlement paths. The architectural recommendation is to finish that convergence: **one canonical settlement entry point, one epoch-state schema, one shared transaction/lock, one eligibility source, and one idempotent audit record**. Secondary services and auto-settlers should invoke that primitive rather than reimplementing credits themselves.

That change has high leverage because settlement is the final boundary between consensus/attestation data and spendable balances. Strong idempotency there limits the financial impact of races, retries, service restarts and schema drift even when earlier components fail in unexpected ways.

## Conclusion

RustChain's strongest security theme is layered evidence: recent nonce, signed identity where available, multi-signal physical fingerprinting, hardware binding, per-epoch enrollment and deterministic weighted settlement. The critical design principle is to preserve those layers all the way to the ledger. A valid attestation should not automatically imply every later privilege, and a valid reward calculation should not be independently executable by several state writers. Consolidating settlement into one atomic, auditable transition would materially strengthen the architecture while preserving the project's Proof-of-Antiquity model.
