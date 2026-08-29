# Script — Check Eligibility Before You Talk About Rewards

**Target:** 45–55 seconds, vertical 9:16

**Hook (0–5s)**
Before talking about RustChain rewards, check whether the miner is eligible at all.

**5–18s**
RustChain documents a public `GET /lottery/eligibility` endpoint. You pass a `miner_id`, and the response tells you whether that miner is eligible in the current epoch.

**18–32s**
An eligible response can include `eligible: true`, the current rotation size, slot, and slot producer. A non-eligible response can still return HTTP 200, with `eligible: false` and a reason such as `not_attested`.

**32–45s**
That distinction matters: a successful API request is not the same thing as reward eligibility. Read the response state, not just the HTTP status.

**45–53s**
And settlement is separate again: RustChain documents historical epoch settlement through `/api/settlement/{epoch}`.

**End card**
REQUEST OK ≠ ELIGIBLE ≠ SETTLED

No earnings guarantee is implied.
