# Harden the Chain — Step 2: Reproduce a Known Fix — Mock Signature Mode

**Bounty:** `Scottcjn/rustchain-bounties#398`  
**Contributor:** `mdmcl-pixel`  
**Method:** static source review plus an offline policy reproduction; no production endpoint was probed or exploited.  
**Assistance disclosure:** prepared and validated with GPT-5.6 Sol under the repository owner's direction.

## Scope

Step 2 asks for a known BuilderFred finding to be explained in three parts: what the attack looked like before the fix, where the fix is visible in code, and whether the fix is sufficient. I selected **Mock Signature Mode** because the repository contains a focused historical fix, regression tests, and a later WSGI hardening change that make the security boundary unusually clear.

Primary source commits:

- `248948bd68cac079163b886052a76a552699b547` — `fix: fail closed on mock signature mode outside test runtime`
- `6e19c549ed8bcc179fc216cce298c291b165d759` — `fix: enforce mock signature guard during WSGI startup (#4535)`

Current source also keeps mock-signature support described as testing-only and disabled for production.

## 1. Attack before the fix

Mock signatures are useful in tests because they let a developer exercise higher-level request and state logic without requiring a real Ed25519 signature for every fixture. That convenience becomes a security problem if the same bypass can be enabled in a non-test runtime.

Before the runtime guard was added, the important failure mode was not that mock signatures existed; it was that **configuration alone could enable the bypass without forcing the process to refuse production startup**. In that state, a request accepted by the mock-signature path could satisfy a signature gate without demonstrating possession of the corresponding private signing key.

That changes an authenticity check into a configuration-dependent assertion. If such a mode were accidentally enabled in a production deployment, an actor would not need to defeat Ed25519 cryptography; they would only need to reach a path that accepts the mock format. The resulting risk is impersonation or unauthorized acceptance at any boundary that relies on the affected signature check.

I did not send a mock signature to a live RustChain service. The reproduction below models only the pre-fix and post-fix runtime policy evidenced by the public patch.

## 2. The fix in code

Commit `248948bd68cac079163b886052a76a552699b547` added `enforce_mock_signature_runtime_guard()` to the integrated node. Its behavior is straightforward:

1. If `TESTNET_ALLOW_MOCK_SIG` is false, startup proceeds.
2. If mock signatures are enabled and the runtime is explicitly `test`, `testing`, or `ci`, startup proceeds.
3. Otherwise, the function raises `RuntimeError` and refuses unsafe startup.

The same commit wired that guard into the direct `__main__` startup path and added regression tests for the three important cases: production + mock enabled must fail, test + mock enabled may run, and production + mock disabled may run.

A later hardening commit, `6e19c549ed8bcc179fc216cce298c291b165d759`, added the guard to `node/wsgi.py` immediately after the integrated node module is loaded and before the Flask application is exposed. It also added a test proving that WSGI startup raises before initialization continues when the guard detects an unsafe mock-signature configuration.

This is important defense in depth. Protecting only `python node/...py` would leave a deployment gap if production normally starts through WSGI. The later change closes that official entry-point gap.

## 3. Offline reproduction

The accompanying script `evidence/mock_signature_guard_reproduction.py` is deliberately small and non-networked. It reconstructs only the policy transition demonstrated by the historical patch.

It evaluates three cases:

- **production + mock enabled:** old policy starts; hardened policy blocks.
- **production + mock disabled:** both policies start.
- **test + mock enabled:** both policies start because the bypass is intentionally test-scoped.

The captured execution output is:

```text
RustChain mock-signature guard — offline policy reproduction
==============================================================
production + mock enabled: before=STARTS; after=BLOCKED
production + mock disabled: before=STARTS; after=STARTS
test + mock enabled: before=STARTS; after=STARTS
Validation: PASS
```

The assertions make the reproduction fail if the expected policy matrix is changed accidentally.

## 4. Why the fix is sufficient — and its boundary

For the configuration error it targets, the fix is strong because it converts an insecure production setting from **fail open** to **fail closed**. A production operator cannot merely set the mock-signature flag and unknowingly continue serving requests through the normal direct or WSGI startup path. The regression tests make that invariant explicit.

The control has four layers:

- production default: mock signatures disabled;
- runtime environment check: mocks limited to `test`, `testing`, or `ci`;
- startup failure: unsafe non-test configuration raises rather than warns;
- official WSGI enforcement: the guard is called before the application is served.

The remaining boundary is architectural: a guard can only protect entry points that call it. The official WSGI path does, and the direct startup path added by the original fix does. A hypothetical custom launcher that imports internals while deliberately bypassing the official startup contract would need to preserve the same guard. That is not a weakness in Ed25519 itself; it is a deployment-integration requirement.

## Conclusion

The original weakness was a dangerous testing feature crossing a runtime trust boundary. The fix is appropriate because it does not remove the useful test facility; instead, it makes the facility explicitly test-scoped and makes unsafe production startup impossible through the documented application entry paths. The historical patch, regression tests, WSGI follow-up, and offline reproduction all support the same conclusion: **mock-signature mode is now designed to fail closed outside test runtime**.
