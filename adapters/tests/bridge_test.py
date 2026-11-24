import json
import os
import subprocess
import unittest

from delanmar_adapters.bridge import Bridge
from delanmar_adapters.beeai import beeai_handler
from delanmar_adapters.frameworks import guarded


RESOURCE = {"kind": "fixture", "id": "one"}
CONTEXT = {"operation": "read", "purpose": "test"}


class BridgeTest(unittest.TestCase):
    def setUp(self):
        self.b = Bridge()

    def tearDown(self):
        self.b.close()

    def test_roster_denied_without_authentication(self):
        with self.assertRaises(PermissionError):
            self.b.list_agents()

    def test_production_denies_all_claimed_identities(self):
        for agent in ("bookkeeping", "admin", "nobody"):
            r = self.b.authorize(agent, "create_task", resource=RESOURCE, context=CONTEXT)
            self.assertEqual((r["decision"], r["reason"]), ("deny", "caller_not_authenticated"))
            self.assertTrue(r["request_id"])
            self.assertIsNone(r["principal"])

    def test_guard_does_not_execute(self):
        r = guarded(self.b, "bookkeeping", "issue_payment", RESOURCE, CONTEXT, lambda: 1 / 0)
        self.assertEqual(r["status"], "deny")

    def test_beeai_seam_forwards_gate_and_callback_metadata(self):
        class FakeBridge:
            def check_action(self, agent, action, *, resource, context):
                self.request = (agent, action, resource, context)
                return "allow"

        fake = FakeBridge()
        handler = beeai_handler(fake, "admin", "fixture", lambda **kw: kw,
                                resource=RESOURCE, context=CONTEXT)
        result = handler(resource="callback-resource", context="callback-context")
        self.assertEqual(fake.request, ("admin", "fixture", RESOURCE, CONTEXT))
        self.assertEqual(result["result"], {"resource": "callback-resource",
                                            "context": "callback-context"})
        denied = beeai_handler(self.b, "admin", "fixture", lambda: 1 / 0,
                               resource=RESOURCE, context=CONTEXT)
        self.assertEqual(denied()["status"], "deny")

    def test_constructor_cannot_claim_caller(self):
        with self.assertRaises(TypeError):
            Bridge("admin")
        with self.assertRaises(TypeError):
            Bridge(caller="admin")

    def test_malformed_contract_denied(self):
        for request in (
            {"op": "authorize", "agent": "admin", "action": "x"},
            {"op": "authorize", "agent": "admin", "action": "x",
             "resource": RESOURCE, "context": {**CONTEXT, "extra": 1}},
        ):
            with self.assertRaises(RuntimeError):
                self.b.call(**request)

    def test_hostile_same_user_launcher_cannot_assert_identity(self):
        r, w = os.pipe()
        try:
            p = subprocess.Popen(
                [os.environ["DELANMAR_BRIDGE"], "--caller-fd", str(r)],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, pass_fds=(r,),
            )
            os.close(r)
            r = -1
            os.write(w, b'{"version":1,"agent":"admin"}')
            os.close(w)
            w = -1
            request = {"version": 2, "request_id": "hostile-1", "op": "authorize",
                       "agent": "admin", "action": "create_task",
                       "resource": RESOURCE, "context": CONTEXT}
            out, _ = p.communicate(json.dumps(request) + "\n", timeout=5)
            response = json.loads(out)
            self.assertEqual(response["request_id"], "hostile-1")
            self.assertEqual((response["decision"], response["reason"]),
                             ("deny", "caller_not_authenticated"))
        finally:
            if r != -1:
                os.close(r)
            if w != -1:
                os.close(w)


if __name__ == "__main__":
    unittest.main()
