"""Client for the Bazel-built Rust bridge. All Python code reaches the core only through this.

The launcher (this class) binds the bridge process to one agent identity over a private
inherited pipe. The agent id in each request is only a claim; the core rejects it unless
it matches the bound caller. This does NOT yet prevent a framework from bypassing the
helper (execution broker: Phase 1 Increments 3-4)."""
import json
import os
import subprocess

PROTOCOL_VERSION = 1


class Bridge:
    def __init__(self, caller, binary=None):
        self.binary = binary or os.environ["DELANMAR_BRIDGE"]
        self.caller = caller
        r, w = os.pipe()
        try:
            self._p = subprocess.Popen(
                [self.binary, "--caller-fd", str(r)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
                pass_fds=(r,),
            )
            os.write(w, json.dumps({"version": PROTOCOL_VERSION, "agent": caller}).encode())
        finally:
            os.close(r)
            os.close(w)

    def call(self, **request):
        request["version"] = PROTOCOL_VERSION
        self._p.stdin.write(json.dumps(request) + "\n")
        self._p.stdin.flush()
        return json.loads(self._p.stdout.readline())

    def authorize(self, agent, action):
        """Return the full decision response: allow | deny | approval_required."""
        return self.call(op="authorize", agent=agent, action=action)

    def check_action(self, agent, action):
        return self.authorize(agent, action)["decision"]

    def list_agents(self):
        return self.call(op="list_agents")["agents"]

    def close(self):
        self._p.stdin.close()
        self._p.wait()
        self._p.stdout.close()
