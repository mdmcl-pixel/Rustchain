# Sources

Canonical source: https://github.com/Scottcjn/Rustchain/blob/main/docs/API_REFERENCE.md

Claim map:

- `/lottery/eligibility` is a public GET endpoint taking required `miner_id`: API_REFERENCE.md, Attestation section, `GET /lottery/eligibility`.
- Eligible example includes `eligible: true`, `rotation_size`, `slot`, and `slot_producer`: same endpoint's documented eligible 200 response.
- Not-eligible example is also documented as 200 OK and includes `eligible: false`, `reason: not_attested`, and `slot_producer: null`: same endpoint's documented not-eligible response.
- Historical settlement is separately queried through `GET /api/settlement/{epoch}`: API_REFERENCE.md, Settlement section.

Editorial inference: `REQUEST OK ≠ ELIGIBLE ≠ SETTLED` summarizes the documented separation of HTTP request success, the eligibility response field, and the distinct settlement endpoint. It is not a quoted protocol slogan.

No benchmark, token-price, or guaranteed-earnings claim is made.
