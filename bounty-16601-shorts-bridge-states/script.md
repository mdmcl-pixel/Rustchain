# Script — “A Bridge Transfer Is Not One Step”

**Target:** 48–55 seconds.

**Hook (0–5s)**
A RustChain bridge transfer is not one magic jump from RTC to another chain.

**5–15s**
The public API reference documents `/api/bridge/initiate`. For RustChain-origin deposits, that route is operator-assisted and admin-authenticated because native RTC is locked before external mint or release handling.

**15–28s**
After initiation, the bridge status is not simply “done.” The documented state machine includes `pending`, then `locked`, then `confirming` while external confirmations are still in progress.

**28–40s**
Only `completed` means the transfer completed successfully. The API also defines `failed` and `voided`, so software should read the actual transfer status rather than infer settlement from initiation alone.

**40–50s**
The status endpoint even exposes external confirmations and required confirmations, making progress explicit.

**Close (50–55s)**
For cross-chain RTC, state matters: initiated is not completed. Read the status.
