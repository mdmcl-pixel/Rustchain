"""Offline reconstruction of RustChain's mock-signature runtime guard.

This does not contact RustChain or verify/exploit any live endpoint. It models
the policy evidenced by the historical fix and current regression guard.
"""

TEST_RUNTIMES = {"test", "testing", "ci"}


def vulnerable_policy(mock_signature_enabled: bool, runtime: str) -> str:
    """Pre-guard policy: enabling mock signatures did not fail startup."""
    return "STARTS"


def hardened_policy(mock_signature_enabled: bool, runtime: str) -> str:
    """Post-fix policy: mock signatures are permitted only in test runtimes."""
    if not mock_signature_enabled:
        return "STARTS"
    if runtime.strip().lower() in TEST_RUNTIMES:
        return "STARTS"
    return "BLOCKED"


cases = [
    ("production + mock enabled", True, "production", "BLOCKED"),
    ("production + mock disabled", False, "production", "STARTS"),
    ("test + mock enabled", True, "test", "STARTS"),
]

print("RustChain mock-signature guard — offline policy reproduction")
print("=" * 62)

for name, enabled, runtime, expected_after in cases:
    before = vulnerable_policy(enabled, runtime)
    after = hardened_policy(enabled, runtime)
    print(f"{name}: before={before}; after={after}")
    assert after == expected_after

assert vulnerable_policy(True, "production") == "STARTS"
assert hardened_policy(True, "production") == "BLOCKED"
print("Validation: PASS")
