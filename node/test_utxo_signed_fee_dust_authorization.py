"""Regression PoC for rustchain-bounties #2819.

The UTXO transfer signature authenticates the requested ``fee`` value.  This
PoC expects the endpoint not to settle a transaction whose final ledger fee is
larger than the fee covered by that signature.
"""

import json
import os
import sqlite3
import tempfile
import time
import unittest

from flask import Flask

from utxo_db import UNIT, UtxoDB
from utxo_endpoints import UTXO_SIGNATURE_DOMAIN, register_utxo_blueprint


class TestSignedFeeDustAuthorization(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp.close()
        self.db_path = self.tmp.name

        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "CREATE TABLE IF NOT EXISTS balances "
            "(miner_id TEXT PRIMARY KEY, amount_i64 INTEGER DEFAULT 0)"
        )
        conn.commit()
        conn.close()

        self.db = UtxoDB(self.db_path)
        self.db.init_tables()
        self.sender = "RTC_test_aabbccdd"

        # The verifier deliberately accepts only the exact V2 payload in which
        # the wallet authorized fee=0.  No real key material is needed for this
        # state-transition PoC.
        self.verified_payloads = []

        def verify_requested_zero_fee(_pubkey, message, _signature):
            payload = json.loads(message)
            self.verified_payloads.append(payload)
            return (
                payload.get("domain") == UTXO_SIGNATURE_DOMAIN
                and payload.get("from") == self.sender
                and payload.get("fee") == 0.0
            )

        app = Flask(__name__)
        app.config["TESTING"] = True
        register_utxo_blueprint(
            app,
            self.db,
            self.db_path,
            verify_sig_fn=verify_requested_zero_fee,
            addr_from_pk_fn=lambda _pk: self.sender,
            current_slot_fn=lambda: 100,
            dual_write=False,
        )
        self.client = app.test_client()

        self.assertTrue(
            self.db.apply_transaction(
                {
                    "tx_type": "mining_reward",
                    "inputs": [],
                    "outputs": [{"address": self.sender, "value_nrtc": UNIT}],
                    "timestamp": int(time.time()),
                    "_allow_minting": True,
                },
                block_height=1,
            )
        )

    def tearDown(self):
        os.unlink(self.db_path)

    def test_effective_fee_must_not_exceed_fee_covered_by_signature(self):
        # Leave 500 nRTC of change.  coin_select() treats change below the
        # 1,000-nRTC dust threshold as fee, despite the signed requested fee=0.
        amount_nrtc = UNIT - 500

        response = self.client.post(
            "/utxo/transfer",
            json={
                "from_address": self.sender,
                "to_address": "bob",
                "amount_rtc": amount_nrtc / UNIT,
                "fee_rtc": 0,
                "public_key": "aabbccdd" * 8,
                "signature": "test-signature",
                "nonce": 1,
            },
        )
        data = response.get_json()

        self.assertTrue(
            any(payload.get("fee") == 0.0 for payload in self.verified_payloads),
            self.verified_payloads,
        )

        # Security expectation: a fee not covered by the signature must not be
        # silently applied.  Current code returns HTTP 200 and records 500 nRTC.
        self.assertNotEqual(response.status_code, 200, data)

        conn = sqlite3.connect(self.db_path)
        try:
            row = conn.execute(
                "SELECT fee_nrtc FROM utxo_transactions "
                "WHERE tx_type='transfer' ORDER BY rowid DESC LIMIT 1"
            ).fetchone()
        finally:
            conn.close()

        self.assertIsNone(row, "unauthorized effective fee reached the ledger")


if __name__ == "__main__":
    unittest.main()
