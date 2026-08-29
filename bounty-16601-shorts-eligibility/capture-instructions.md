# Capture Instructions

Canvas: 1080x1920, 30 fps, 45–55 seconds.

1. 0–5s: generated title card: `CHECK ELIGIBILITY FIRST`.
2. 5–18s: screen-capture the public `docs/API_REFERENCE.md` heading for `GET /lottery/eligibility`, then highlight the `miner_id` query parameter.
3. 18–25s: zoom to the documented eligible JSON; highlight `eligible: true`, `rotation_size`, `slot`, `slot_producer`.
4. 25–32s: cut to the documented not-eligible JSON; highlight `eligible: false` and `reason: not_attested` while keeping the documented 200 OK context visible.
5. 32–45s: generated comparison card: `HTTP 200` on top, `ELIGIBLE? READ THE BODY` below.
6. 45–50s: screen-capture the next API section, `GET /api/settlement/{epoch}`.
7. 50–55s: generated end card: `REQUEST OK ≠ ELIGIBLE ≠ SETTLED` and `github.com/Scottcjn/Rustchain`.

Use only repository captures and generated text cards. Do not show private keys, wallet secrets, invented balances, or third-party media.
