# Phase 1 — Security & Core Foundation

**Status:** Not accepted. Maturity per [IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md); completion is governed by [PHASE_ACCEPTANCE_STANDARD.md](../PHASE_ACCEPTANCE_STANDARD.md).

## Objective
Harden Rust identity, permissions and human approval.

## Required deliverables
- Upgrade the existing Rust agent registry (`core/src/lib.rs`); preserve the prototype and bridge.
- Implement individual agent permissions.
- Authenticate bridge callers.
- Establish fail-closed authorization.
- Implement and record approval requests and decisions.
- Prevent frameworks from executing tools outside the Rust-controlled authorization path.

## Dependencies
Phase 0 scope. Security design may begin in parallel with Phase 0.

## Related business pilot stage
Pilot Phase 1 in the [OpenWorks pilot plan](../strategy/DELANMAR_OPENWORKS_PILOT_SETUP.md) (business track; numbering is not equivalent).

## Acceptance
- **Minimum maturity: Tested** for the Rust Core, bridge and approval boundary in scope.
- Demonstrate an authoritative identity and individually assigned permissions for every agent; test permitted actions and recorded approval requests and decisions.
- Test that unauthenticated requests, unknown agents, unauthorized actions, malformed requests and missing or unavailable authorization decisions, including authorization-service failures, fail safely without executing the action.
- Test that framework tools and delegation cannot bypass the Core or exercise authority beyond its explicit decision.
- Record revision, environment, commands or procedure, results, limitations and reviewer; update the implementation status and obtain human-owner approval.

## Governing rule
No agent may exercise authority that the Rust Core has not explicitly granted.
