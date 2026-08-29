# Script — Healthy ≠ Ready

**Target:** 45–55 seconds

**Hook:** A RustChain node can expose more than one kind of “okay.”

RustChain’s public API documents two separate checks: `/health` and `/ready`.

`/health` returns an `ok` flag, but it also exposes operational signals such as uptime, whether the database is read/write capable, backup age, and how many slots the node is behind the tip.

The same reference documents `/ready` separately as a Kubernetes-style readiness probe, returning a simple `ready` value.

That distinction matters when operating software: a detailed health response gives diagnostic context, while a readiness probe gives orchestration a compact signal about whether the service is ready.

So when checking RustChain infrastructure, don’t treat every green response as the same thing.

**End card:** HEALTH = diagnostics. READY = readiness signal.
