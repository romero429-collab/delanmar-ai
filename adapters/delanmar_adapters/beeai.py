"""BeeAI is exposed over the same contract rather than imported: BeeAI agents
(served via its Agent Communication Protocol) call the Rust bridge through `guarded`.
Kept as a thin documented seam until a BeeAI version is pinned and tested."""
from .bridge import Bridge
from .frameworks import guarded


def beeai_handler(bridge: Bridge, agent: str, action: str, fn):
    """Return a plain callable suitable for registering as a BeeAI agent/tool body."""
    return lambda **kw: guarded(bridge, agent, action, fn, **kw)
