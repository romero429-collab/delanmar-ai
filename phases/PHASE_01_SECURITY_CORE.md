# Phase 1 — Security & Core Foundation

**Status:** Not accepted; human-owner and security approval are pending. Maturity per [IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md); completion is governed by [PHASE_ACCEPTANCE_STANDARD.md](../PHASE_ACCEPTANCE_STANDARD.md).

**Current PR #7 v2 limitation:** The production bridge denies all requests because caller authentication is incomplete. Production per-agent grants are empty, and resource and context fields are not enforced. There is no trusted launcher, workload isolation or execution broker; networked and multitenant operation are unsupported. Approval workflows, audit enforcement and framework execution enforcement are not implemented. An approval-related decision is not an approval or execution capability.

The [security design](../docs/PHASE_01_SECURITY_DESIGN.md) is a historical proposal, including its proposed v1 contract, not the implemented v2 contract or evidence that its controls exist. The requirements below are future deliverables and acceptance criteria, not claims of present enforcement or promises of implementation.

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
Phase 0 scope. Security design may begin in parallel with Phase 0. Establish and verify a trusted launcher, workload identity and isolation before implementing or relying on approvals; authentication of a distinct human approver is also required.

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
