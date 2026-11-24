import unittest

from delanmar_adapters.bridge import Bridge
from delanmar_adapters.frameworks import guarded


class BridgeTest(unittest.TestCase):
    def setUp(self):
        self.b = Bridge("bookkeeping")

    def tearDown(self):
        self.b.close()

    def test_roster(self):
        self.assertEqual(len(self.b.list_agents()), 24)

    def test_default_deny_production_policy(self):
        self.assertEqual(self.b.check_action("bookkeeping", "create_task"), "deny")

    def test_guard_blocks_payment(self):
        r = guarded(self.b, "bookkeeping", "issue_payment", lambda: 1 / 0)
        self.assertEqual(r["status"], "deny")

    def test_claimed_identity_must_match_caller(self):
        r = self.b.authorize("admin", "create_task")
        self.assertEqual((r["decision"], r["reason"]), ("deny", "caller_mismatch"))

    def test_unknown_caller_denied(self):
        b = Bridge("nobody")
        try:
            r = b.authorize("nobody", "create_task")
            self.assertEqual(r["decision"], "deny")
            self.assertEqual(r["reason"], "caller_not_authenticated")
        finally:
            b.close()


if __name__ == "__main__":
    unittest.main()
