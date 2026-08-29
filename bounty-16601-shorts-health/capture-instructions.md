# 9:16 Capture Instructions

Canvas: 1080×1920. Target duration: 45–55 seconds.

1. **0–4s — Hook card**
   - Large text: `HEALTHY ≠ READY`
   - Smaller text: `Two RustChain API checks`

2. **4–13s — API reference heading**
   - Screen-capture the current `docs/API_REFERENCE.md` section for `GET /health`.
   - Highlight `Auth: None` and the response block.

3. **13–28s — Health fields**
   - Crop/zoom the documented response.
   - Sequentially highlight: `ok`, `uptime_s`, `db_rw`, `backup_age_hours`, `tip_age_slots`.
   - Overlay: `Diagnostic context`.

4. **28–39s — Readiness**
   - Move to the `GET /ready` section.
   - Highlight the wording `Kubernetes-style readiness probe` and the documented `{ "ready": true }` response.
   - Overlay: `Compact readiness signal`.

5. **39–50s — Side-by-side generated card**
   - Left: `/health` → `diagnostics`
   - Right: `/ready` → `readiness`
   - Do not imply that one endpoint guarantees application correctness or availability beyond the documented fields.

6. **50–55s — End card**
   - `HEALTH = diagnostics`
   - `READY = readiness signal`
   - Footer: `Source: Scottcjn/Rustchain docs/API_REFERENCE.md`

Rights: all non-repository visuals are plain generated text cards. No third-party footage, logos, music, or stock assets required.