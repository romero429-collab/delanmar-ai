"""Single-call-at-a-time Rust bridge client. Caller authentication is not implemented."""
import json
import math
import os
import selectors
import subprocess
import threading
import time
import uuid

PROTOCOL_VERSION = 2
MAX_MESSAGE_BYTES = 65536
APPROVAL_REQUIRED = frozenset({
    "transfer_money", "issue_payment", "change_banking_details", "sign_legal_agreement",
    "employment_decision", "exceptional_pricing", "delete_important_records",
    "change_security_controls", "grant_access",
})


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate response field")
        result[key] = value
    return result


class Bridge:
    def __init__(self, *, binary=None, timeout=5.0):
        if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("timeout must be a positive finite number")
        if os.name != "posix":
            raise RuntimeError("bridge pipe I/O is supported only on POSIX")
        self.binary = binary or os.environ["DELANMAR_BRIDGE"]
        self.timeout = timeout
        self._lock = threading.Lock()
        self._closed = False
        self._p = subprocess.Popen(
            [self.binary], stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=0
        )

    def call(self, **request):
        if not self._lock.acquire(blocking=False):
            raise RuntimeError("concurrent bridge operations are unsupported")
        try:
            if self._closed:
                raise RuntimeError("bridge is closed")
            request["version"] = PROTOCOL_VERSION
            request["request_id"] = uuid.uuid4().hex
            payload = (json.dumps(request, allow_nan=False) + "\n").encode("utf-8")
            if len(payload) > MAX_MESSAGE_BYTES:
                raise ValueError("request too large")
            try:
                line = self._exchange(payload)
                if self._p.poll() is not None:
                    raise RuntimeError("bridge process terminated")
                response = json.loads(line, object_pairs_hook=_unique_object)
                self._validate_response(response, request)
                return response
            except TimeoutError:
                raise
            except (ValueError, UnicodeDecodeError, TypeError, OSError, EOFError) as exc:
                raise RuntimeError("invalid bridge response") from exc
        except Exception:
            self._shutdown()
            raise
        finally:
            self._lock.release()

    def _exchange(self, payload):
        deadline = time.monotonic() + self.timeout
        stdin_fd = self._p.stdin.fileno()
        stdout_fd = self._p.stdout.fileno()
        os.set_blocking(stdin_fd, False)
        os.set_blocking(stdout_fd, False)
        data = bytearray()
        view = memoryview(payload)
        with selectors.DefaultSelector() as selector:
            selector.register(stdin_fd, selectors.EVENT_WRITE)
            selector.register(stdout_fd, selectors.EVENT_READ)
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("bridge request timed out")
                events = selector.select(remaining)
                if not events:
                    raise TimeoutError("bridge request timed out")
                for key, _ in events:
                    if key.fd == stdin_fd:
                        try:
                            written = os.write(stdin_fd, view)
                        except BlockingIOError:
                            continue
                        if not written:
                            raise EOFError("bridge stdin closed")
                        view = view[written:]
                        if not view:
                            selector.unregister(stdin_fd)
                    else:
                        try:
                            chunk = os.read(stdout_fd, min(4096, MAX_MESSAGE_BYTES + 1 - len(data)))
                        except BlockingIOError:
                            continue
                        if not chunk:
                            raise EOFError("bridge stdout closed")
                        data.extend(chunk)
                        if len(data) > MAX_MESSAGE_BYTES:
                            raise ValueError("response too large")
                        if b"\n" in data:
                            if not data.endswith(b"\n") or data.count(b"\n") != 1 or view:
                                raise ValueError("unexpected bridge response")
                            return bytes(data)

    @staticmethod
    def _validate_response(response, request):
        if not isinstance(response, dict):
            raise ValueError("response must be an object")
        required = {"version", "request_id", "decision", "reason", "principal"}
        if not required <= response.keys() or response.keys() - required - {"agents"}:
            raise ValueError("invalid response fields")
        decision, reason, principal = response["decision"], response["reason"], response["principal"]
        if (type(response["version"]) is not int or response["version"] != PROTOCOL_VERSION
                or response["request_id"] != request["request_id"]
                or decision not in ("allow", "deny", "approval_required")
                or not isinstance(reason, str) or not reason
                or (principal is not None and (not isinstance(principal, str) or not principal))):
            raise ValueError("invalid response values")
        if decision != "deny" and principal is None:
            raise ValueError("missing principal")
        reasons = {
            "allow": {"permitted"} if request.get("op") == "authorize" else {"roster_available"},
            "approval_required": {"approval_required"},
            "deny": {"malformed_request", "request_too_large", "unsupported_version", "caller_not_authenticated",
                     "caller_mismatch", "authorization_unavailable", "unknown_agent", "no_permission"},
        }
        if reason not in reasons[decision]:
            raise ValueError("decision and reason disagree")
        if (request.get("op") == "authorize" and decision == "allow"
                and request.get("action") in APPROVAL_REQUIRED):
            raise ValueError("consequential action cannot be allowed")
        if principal is not None and request.get("op") == "authorize" and principal != "agent:" + request.get("agent", ""):
            raise ValueError("principal does not match agent")
        if "agents" in response:
            agents = response["agents"]
            if (request.get("op") != "list_agents" or decision != "allow"
                    or not isinstance(agents, list)
                    or any(not isinstance(agent, dict)
                           or set(agent) != {"id", "name", "department"}
                           or not all(isinstance(value, str) and value for value in agent.values())
                           or agent["department"] not in ("communication", "internal_operations",
                                                          "executive", "project")
                           for agent in agents)):
                raise ValueError("unexpected agents")
        elif request.get("op") == "list_agents" and decision == "allow":
            raise ValueError("missing agents")

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

    def _shutdown(self):
        if self._closed:
            return
        self._closed = True
        if self._p.poll() is None:
            try:
                self._p.kill()
            except ProcessLookupError:
                pass
        try:
            self._p.wait(timeout=1)
        except subprocess.TimeoutExpired:
            pass
        self._p.stdin.close()
        self._p.stdout.close()

    def close(self):
        if not self._lock.acquire(blocking=False):
            raise RuntimeError("concurrent bridge operations are unsupported")
        try:
            self._shutdown()
        finally:
            self._lock.release()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
