# Sources and claim map

Canonical source: https://github.com/Scottcjn/Rustchain/blob/main/docs/API_REFERENCE.md

## Claim map

- **Bridge API manages cross-chain transfers and follows RIP-0305 Track C** → `docs/API_REFERENCE.md`, section `6. Bridge (Cross-Chain)`.
- **RustChain-origin deposits are operator-assisted/admin-authenticated because native RTC balances are locked before external mint/release handling** → `POST /api/bridge/initiate` introduction and Auth field.
- **Initiation response can report `status: pending`** → documented success response for `/api/bridge/initiate`.
- **Status progression includes `pending`, `locked`, `confirming`, `completed`, `failed`, `voided`** → `GET /api/bridge/status/{tx_hash}` status-values table.
- **`completed` is defined as transfer completed successfully** → same status-values table.
- **Status response exposes `external_confirmations` and `required_confirmations`** → documented `/api/bridge/status/{tx_hash}` response example.

Verification performed against the public API reference on 2026-08-29. No live bridge transaction, admin endpoint access, or private credential was used.