# Exact vertical capture instructions

Canvas: **1080×1920**, 30 fps, target 48–55 seconds. Use only the public RustChain API reference plus generated text cards.

1. **0–5s:** Full-screen card: `BRIDGE TRANSFER ≠ ONE STEP`.
2. **5–15s:** Screen-capture `docs/API_REFERENCE.md`, Bridge section, highlighting `POST /api/bridge/initiate` and the paragraph stating RustChain-origin deposits are operator-assisted/admin-authenticated and lock native RTC before external handling.
3. **15–28s:** Generated vertical state card, animate one line at a time: `pending → locked → confirming → completed`.
4. **28–40s:** Return to API reference status table. Highlight `completed`, then `failed`, then `voided` without changing the source wording.
5. **40–50s:** Capture the example status response and box `external_confirmations` and `required_confirmations`.
6. **50–55s:** End card: `INITIATED ≠ COMPLETED` / `READ THE STATUS` / `github.com/Scottcjn/Rustchain`.

Accessibility: minimum 54 px captions, high contrast, keep source text zoomed to one relevant block at a time. Do not show real admin keys, wallet secrets, or private credentials.