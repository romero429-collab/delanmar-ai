# Phase 07 — Adapter and Framework Integration

**Status:** Preliminary LangChain, LangGraph, CrewAI and BeeAI seams; AG2 absent. None are verified integrations.

## Objective and scope
Implement replaceable adapters to the Delanmar contract for LangChain, LangGraph, CrewAI, BeeAI and AG2.

## Existing components to reuse
`adapters/delanmar_adapters/bridge.py`, `frameworks.py`, `beeai.py`, existing adapter tests and the constitution's framework responsibilities.

## Required work
- Translate each framework's inputs, outputs, tools and lifecycle events into the common contract without transferring platform authority to the framework.
- Route every governed action and delegation through core authorization and preserve identity, state references, approvals and audit context.
- Select and manage compatible dependency versions; document supported integrations, limitations and migration requirements.
- Certify one suitable adapter for Alpha first; complete the other adapters incrementally.

## Dependencies
Phases 2–4 for enforced core authority, contract and bridge; Phases 1 and 6 for supported dependency and build paths.

## Testing requirements
Run shared conformance and integration tests for each framework, including identity preservation, task state, denial, approvals, outages, tool/delegation bypass and migration of approved state. Test supported dependency versions.

## Acceptance criteria
- One adapter passes the applicable gate before Alpha uses it; Phase 7 closes only when all five have passed the same contract and security tests.
- Framework replacement preserves authorized identity, policy, state and audit references under documented migration conditions.

## Outstanding risks
API churn, optional dependency drift, ungated framework tools, incomplete state portability and misleading claims based on seams alone.

## Handoff
Deliver a certified adapter to Phase 8, then support controlled expansion in Phases 9–11.
