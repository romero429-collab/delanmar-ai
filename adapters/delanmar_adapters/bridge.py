"""Client for the Rust bridge. Caller authentication is not yet implemented."""
import json
import os
import subprocess
import uuid

PROTOCOL_VERSION = 2


class Bridge:
    def __init__(self, *, binary=None):
        self.binary = binary or os.environ["DELANMAR_BRIDGE"]
        self._p = subprocess.Popen(
            [self.binary], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
        )

    def call(self, **request):
        request["version"] = PROTOCOL_VERSION
        request["request_id"] = uuid.uuid4().hex
        self._p.stdin.write(json.dumps(request) + "\n")
        self._p.stdin.flush()
        response = json.loads(self._p.stdout.readline())
        if (response.get("version") != PROTOCOL_VERSION
                or response.get("request_id") != request["request_id"]
                or response.get("decision") not in ("allow", "deny", "approval_required")
                or not isinstance(response.get("reason"), str)):
            raise RuntimeError("invalid bridge response")
        return response

    def authorize(self, agent, action, *, resource, context):
        """Return the full decision response: allow | deny | approval_required."""
        return self.call(op="authorize", agent=agent, action=action, resource=resource, context=context)

    def check_action(self, agent, action, *, resource, context):
        return self.authorize(agent, action, resource=resource, context=context)["decision"]

    def list_agents(self):
        response = self.call(op="list_agents")
        if response["decision"] != "allow":
            raise PermissionError(response["reason"])
        return response["agents"]

    def close(self):
        self._p.stdin.close()
        self._p.wait()
        self._p.stdout.close()
