"""Client for the Bazel-built Rust bridge. All Python code reaches the core only through this."""
import json
import os
import subprocess


class Bridge:
    def __init__(self, binary=None):
        self.binary = binary or os.environ["DELANMAR_BRIDGE"]
        self._p = subprocess.Popen(
            [self.binary], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
        )

    def call(self, **request):
        self._p.stdin.write(json.dumps(request) + "\n")
        self._p.stdin.flush()
        resp = json.loads(self._p.stdout.readline())
        if "error" in resp:
            raise ValueError(resp["error"])
        return resp

    def check_action(self, agent, action):
        return self.call(op="check_action", agent=agent, action=action)["decision"]

    def list_agents(self):
        return self.call(op="list_agents")["agents"]

    def close(self):
        self._p.stdin.close()
        self._p.wait()
