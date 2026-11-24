import unittest

from delanmar_adapters.bridge import Bridge
from delanmar_adapters.frameworks import guarded


class BridgeTest(unittest.TestCase):
    def setUp(self):
        self.b = Bridge()

    def tearDown(self):
        self.b.close()

    def test_roster(self):
        self.assertEqual(len(self.b.list_agents()), 24)

    def test_guard_blocks_payment(self):
        r = guarded(self.b, "bookkeeping", "issue_payment", lambda: 1 / 0)
        self.assertEqual(r["status"], "requires_human_approval")

    def test_guard_runs_routine(self):
        r = guarded(self.b, "admin", "create_task", lambda: 42)
        self.assertEqual(r, {"status": "done", "result": 42})


if __name__ == "__main__":
    unittest.main()
