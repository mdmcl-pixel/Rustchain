"""Regression PoC for rustchain-bounties #2819.

A dry-run should not mutate the target database, and the state root it reports
should describe the migration being previewed rather than the pre-migration
UTXO set.
"""

import os
import shutil
import sqlite3
import tempfile
import unittest

from utxo_genesis_migration import migrate


class TestGenesisDryRunPreview(unittest.TestCase):
    def setUp(self):
        fd, self.dry_db = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        fd, self.real_db = tempfile.mkstemp(suffix=".db")
        os.close(fd)

        conn = sqlite3.connect(self.dry_db)
        conn.execute(
            "CREATE TABLE balances "
            "(miner_id TEXT PRIMARY KEY, amount_i64 INTEGER NOT NULL)"
        )
        conn.execute(
            "INSERT INTO balances (miner_id, amount_i64) VALUES (?, ?)",
            ("alice", 1_000_000),
        )
        conn.commit()
        conn.close()
        shutil.copyfile(self.dry_db, self.real_db)

    def tearDown(self):
        for path in (self.dry_db, self.real_db):
            try:
                os.unlink(path)
            except FileNotFoundError:
                pass

    @staticmethod
    def _tables(path):
        conn = sqlite3.connect(path)
        try:
            return {
                row[0]
                for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
                )
            }
        finally:
            conn.close()

    def test_dry_run_is_read_only_and_predicts_post_migration_root(self):
        before = self._tables(self.dry_db)
        self.assertEqual(before, {"balances"})

        dry = migrate(self.dry_db, dry_run=True)
        after = self._tables(self.dry_db)

        # Dry-run contract: inspecting a migration must not create schema or
        # otherwise alter the database supplied by the operator.
        self.assertEqual(after, before)

        # The reported preview root should equal the root obtained by actually
        # migrating an identical copy of the starting database.
        real = migrate(self.real_db, dry_run=False)
        self.assertEqual(dry["wallets_migrated"], real["wallets_migrated"])
        self.assertEqual(dry["total_nrtc"], real["total_nrtc"])
        self.assertEqual(dry["state_root"], real["state_root"])


if __name__ == "__main__":
    unittest.main()
