"""Framework adapters. Each imports its framework lazily so one missing package
does not break the others. Every adapter routes actions through the Rust approval gate.
NOTE: framework APIs here are unverified against installed versions (see docs/ARCHITECTURE.md)."""
from .bridge import Bridge


def guarded(bridge: Bridge, agent: str, action: str, fn, *args, **kwargs):
    """Run fn only if the core allows it; otherwise return a pending-approval marker."""
    decision = bridge.check_action(agent, action)
    if decision != "allowed":
        return {"status": decision, "agent": agent, "action": action}
    return {"status": "done", "result": fn(*args, **kwargs)}


def langchain_tool(bridge: Bridge, agent: str, action: str, fn, description: str):
    from langchain_core.tools import StructuredTool

    return StructuredTool.from_function(
        func=lambda **kw: guarded(bridge, agent, action, fn, **kw),
        name=f"{agent}_{action}",
        description=description,
    )


def langgraph_gated_graph(bridge: Bridge, agent: str, action: str, fn):
    """Graph: gate -> (execute | await_human)."""
    from typing import TypedDict
    from langgraph.graph import END, StateGraph

    class S(TypedDict, total=False):
        decision: str
        result: object

    g = StateGraph(S)
    g.add_node("gate", lambda s: {"decision": bridge.check_action(agent, action)})
    g.add_node("execute", lambda s: {"result": fn()})
    g.add_node("await_human", lambda s: {"result": "pending human approval"})
    g.set_entry_point("gate")
    g.add_conditional_edges(
        "gate", lambda s: "execute" if s["decision"] == "allowed" else "await_human"
    )
    g.add_edge("execute", END)
    g.add_edge("await_human", END)
    return g.compile()


def crewai_agent(bridge: Bridge, agent_id: str):
    from crewai import Agent

    meta = next(a for a in bridge.list_agents() if a["id"] == agent_id)
    return Agent(
        role=meta["name"],
        goal=f"Perform {meta['name']} duties within approved permissions; escalate consequential actions to the human owner.",
        backstory="Delanmar AI workforce specialist. Human owner has final authority.",
        allow_delegation=False,
    )
