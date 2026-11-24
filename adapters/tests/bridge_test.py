import json
import os
import subprocess
import sys
import threading
import time
import types
import unittest
from unittest.mock import patch

from delanmar_adapters.bridge import APPROVAL_REQUIRED, Bridge
from delanmar_adapters.beeai import beeai_handler
from delanmar_adapters.frameworks import guarded, langchain_tool, langgraph_gated_graph


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

    def test_stubbed_langchain_and_langgraph_denials_do_not_execute(self):
        called = []

        class FakeTool:
            @staticmethod
            def from_function(**kw):
                return kw["func"]

        class FakeGraph:
            def __init__(self, _state):
                self.nodes = {}

            def add_node(self, name, fn):
                self.nodes[name] = fn

            def set_entry_point(self, _name):
                pass

            def add_conditional_edges(self, _name, fn):
                self.route = fn

            def add_edge(self, *_args):
                pass

            def compile(self):
                return self

            def invoke(self):
                state = self.nodes["gate"]({})
                return self.nodes[self.route(state)](state)

        modules = {
            "langchain_core": types.ModuleType("langchain_core"),
            "langchain_core.tools": types.SimpleNamespace(StructuredTool=FakeTool),
            "langgraph": types.ModuleType("langgraph"),
            "langgraph.graph": types.SimpleNamespace(END="end", StateGraph=FakeGraph),
        }
        with patch.dict(sys.modules, modules):
            tool = langchain_tool(self.b, "admin", "fixture", lambda **kw: called.append(kw),
                                  "fixture", resource=RESOURCE, context=CONTEXT)
            self.assertEqual(tool(resource="tool-value")["status"], "deny")
            graph = langgraph_gated_graph(self.b, "admin", "fixture", lambda: called.append(True),
                                          resource=RESOURCE, context=CONTEXT)
            self.assertEqual(graph.invoke()["result"], "denied")
        self.assertEqual(called, [])

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


class BridgeFailureTest(unittest.TestCase):
    def fake_bridge(self, code, timeout=0.2):
        popen = subprocess.Popen
        with patch("delanmar_adapters.bridge.subprocess.Popen") as launch:
            launch.side_effect = lambda _args, **kw: popen([sys.executable, "-u", "-c", code], **kw)
            bridge = Bridge(binary="test-only", timeout=timeout)
        self.addCleanup(bridge.close)
        return bridge

    def assert_gate_fails_closed(self, bridge):
        invoked = []
        with self.assertRaises((RuntimeError, TimeoutError)):
            guarded(bridge, "admin", "fixture", RESOURCE, CONTEXT, lambda: invoked.append(True))
        self.assertEqual(invoked, [])
        self.assertIsNotNone(bridge._p.poll())
        self.assertTrue(bridge._p.stdin.closed)
        self.assertTrue(bridge._p.stdout.closed)
        with self.assertRaises(RuntimeError):
            bridge.check_action("admin", "fixture", resource=RESOURCE, context=CONTEXT)

    def test_terminated_process_fails_closed(self):
        bridge = self.fake_bridge("pass")
        bridge._p.wait(timeout=2)
        self.assert_gate_fails_closed(bridge)

    def test_unexpected_eof_fails_closed(self):
        bridge = self.fake_bridge("import sys,time; sys.stdin.readline(); sys.stdout.close(); time.sleep(10)")
        self.assert_gate_fails_closed(bridge)

    def test_malformed_and_mismatched_responses_fail_closed(self):
        replies = [
            "not json", "[]", '{"version":2,"version":2}', "{}",
            '{"version":true,"request_id":"bad","decision":"allow","reason":"permitted","principal":null}',
        ]
        for reply in replies:
            with self.subTest(reply=reply):
                code = f"import sys,time; sys.stdin.readline(); print({reply!r}, flush=True); time.sleep(10)"
                self.assert_gate_fails_closed(self.fake_bridge(code))

    def test_inconsistent_correlated_responses_fail_closed(self):
        variants = [
            {"decision": "allow", "reason": "no_permission", "principal": "agent:admin"},
            {"decision": "allow", "reason": "permitted", "principal": "agent:scheduler"},
            {"decision": "allow", "reason": "permitted", "principal": None},
            {"decision": "deny", "reason": "no_permission", "principal": None, "extra": 1},
            {"decision": "deny", "reason": "no_permission", "principal": None, "agents": []},
        ]
        for variant in variants:
            with self.subTest(variant=variant):
                code = ("import sys,json,time; req=json.loads(sys.stdin.readline()); "
                        f"r={variant!r}; r.update(version=2,request_id=req['request_id']); "
                        "print(json.dumps(r),flush=True); time.sleep(10)")
                self.assert_gate_fails_closed(self.fake_bridge(code))

    def test_incompatible_bridge_cannot_allow_consequential_actions(self):
        for action in APPROVAL_REQUIRED:
            with self.subTest(action=action):
                bridge = self.fake_bridge(
                    "import sys,json,time; req=json.loads(sys.stdin.readline()); "
                    "print(json.dumps(dict(version=2,request_id=req['request_id'],decision='allow',"
                    "reason='permitted',principal='agent:admin')),flush=True); time.sleep(10)"
                )
                called = []
                with self.assertRaises(RuntimeError):
                    guarded(bridge, "admin", action, RESOURCE, CONTEXT, lambda: called.append(True))
                self.assertEqual(called, [])

    def test_timeout_fails_closed_and_reaps_process(self):
        bridge = self.fake_bridge("import time; time.sleep(10)")
        start = time.monotonic()
        self.assert_gate_fails_closed(bridge)
        self.assertLess(time.monotonic() - start, 3)

    def test_blocked_write_and_oversized_response_fail_closed(self):
        bridge = self.fake_bridge("import time; time.sleep(10)")
        with self.assertRaises(TimeoutError):
            bridge.call(op="authorize", data="x" * 60000)
        self.assertIsNotNone(bridge._p.poll())
        bridge = self.fake_bridge(
            "import sys,time; sys.stdin.readline(); sys.stdout.write('x'*65537+'\\n'); "
            "sys.stdout.flush(); time.sleep(10)"
        )
        self.assert_gate_fails_closed(bridge)

    def test_valid_correlated_response_and_callback_exception_cleanup(self):
        bridge = self.fake_bridge(
            "import sys,json,time; req=json.loads(sys.stdin.readline()); "
            "print(json.dumps(dict(version=2,request_id=req['request_id'],decision='allow',"
            "reason='permitted',principal='agent:admin')),flush=True); time.sleep(10)"
        )
        with self.assertRaisesRegex(ValueError, "callback"):
            with bridge:
                guarded(bridge, "admin", "fixture", RESOURCE, CONTEXT,
                        lambda: (_ for _ in ()).throw(ValueError("callback")))
        self.assertIsNotNone(bridge._p.poll())

    def test_context_manager_cleans_up_on_exception(self):
        bridge = self.fake_bridge("import time; time.sleep(10)")
        with self.assertRaisesRegex(ValueError, "callback"):
            with bridge:
                raise ValueError("callback")
        self.assertIsNotNone(bridge._p.poll())
        bridge.close()

    def test_concurrent_calls_are_rejected(self):
        bridge = self.fake_bridge("import time; time.sleep(10)", timeout=0.5)
        errors = []

        def first_call():
            try:
                bridge.check_action("admin", "fixture", resource=RESOURCE, context=CONTEXT)
            except Exception as exc:
                errors.append(exc)

        thread = threading.Thread(target=first_call)
        thread.start()
        deadline = time.monotonic() + 2
        while not bridge._lock.locked() and time.monotonic() < deadline:
            time.sleep(0.001)
        try:
            with self.assertRaisesRegex(RuntimeError, "concurrent"):
                bridge.check_action("admin", "fixture", resource=RESOURCE, context=CONTEXT)
        finally:
            thread.join(timeout=3)
        self.assertFalse(thread.is_alive())
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], TimeoutError)


if __name__ == "__main__":
    unittest.main()
