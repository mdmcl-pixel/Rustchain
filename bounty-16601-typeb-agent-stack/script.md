# RustChain: Can a Blockchain Verify a Machine?

**Target runtime:** ~5 minutes

RustChain is easiest to understand when you stop thinking of it as a token first and start with the machine.

The project describes itself as a DePIN network for vintage hardware. Its core idea is Proof of Antiquity: physical computers participate through hardware attestation, and the system is designed to distinguish real machines from virtualized or emulated copies. The public README describes checks based on oscillator drift, cache timing, SIMD identity, thermal entropy, instruction jitter, and anti-emulation signals. Those signals are used as evidence about the physical substrate behind a participant.

That changes the usual DePIN question. Many networks ask what service a device can provide: storage, wireless coverage, rendering, or general compute. RustChain asks an additional question: what is this machine, and can the network verify that it is the kind of physical hardware it claims to be? The README frames that as hardware-attested agent identity and Sybil resistance for machine participants.

The second layer is age. RustChain's public documentation gives different antiquity multipliers to hardware classes. A PowerPC G4 example is listed at 2.5x, while modern x86-64 is shown as the 1.0 baseline. That multiplier is not a speed benchmark, and it should not be read as a guaranteed income figure. It is a protocol weighting concept: the project deliberately values preservation and hardware diversity rather than simply rewarding the fastest new processor.

The third layer is the agent economy. RustChain's README describes autonomous agents as first-class participants and says an agent's signing key can function as its wallet identity. The ecosystem also points to Beacon for agent discovery, BoTTube for AI-native media, and TrashClaw for local agent operation. The important connection is that identity, communication, and payment can be tied to cryptographic keys and, where relevant, hardware evidence.

That is why the physical-machine angle matters beyond nostalgia. If software agents can create many cheap virtual identities, a system that cares about one physical participant per machine needs stronger evidence than a self-reported CPU name or an IP address. RustChain's approach is to combine several physical and microarchitectural signals rather than trust a single field. The documentation presents this as a way to make large-scale emulation and VM farms harder to pass off as diverse vintage hardware.

There is also a preservation thesis. The project argues that keeping usable older machines in service can give them a reason to remain maintained rather than discarded. That does not mean every old computer is automatically efficient, profitable, or environmentally superior. The narrower claim is that the protocol intentionally gives value to longevity and diversity, which is unusual in computing markets that normally depreciate old hardware.

So the stack can be summarized in four steps. First, a physical machine presents attestation evidence. Second, the network evaluates whether the hardware claim is credible. Third, protocol rules apply the relevant participation and antiquity weighting. Fourth, cryptographic identities can interact with the broader agent ecosystem for discovery, media, and payments.

The result is a different design question for decentralized infrastructure: instead of asking only how much compute a machine can produce today, RustChain asks whether a network can verify the machine itself, preserve heterogeneous hardware, and let software agents participate without pretending that every identity is equally costly to create.

For the exact current rules, multipliers, endpoints, and implementation details, use the canonical RustChain repository and its linked documentation. This overview is intentionally descriptive, not a promise of earnings or a claim that any anti-emulation method is infallible.