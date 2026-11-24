# Phase 1 — Security & Core Foundation

**Status:** Not accepted. Maturity per [IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md); completion is governed by [PHASE_ACCEPTANCE_STANDARD.md](../PHASE_ACCEPTANCE_STANDARD.md).

## Objective
Harden Rust identity, permissions and human approval.

## Required deliverables
- Upgrade the existing Rust agent registry (`core/src/lib.rs`); preserve the prototype and bridge.
- Implement individual agent permissions.
- Authenticate bridge callers.
- Establish fail-closed authorization.
- Implement approval requests and decisions.
- Prevent frameworks from executing tools outside the Rust-controlled authorization path.

## Dependencies
Phase 0 scope. Security design may begin in parallel with Phase 0.

## Related business pilot stage
Pilot Phase 1 in the [OpenWorks pilot plan](../strategy/DELANMAR_OPENWORKS_PILOT_SETUP.md) (business track; numbering is not equivalent).

## Acceptance
All deliverables above meet the applicable maturity level under the acceptance standard, with evidence, negative tests for authorization where relevant, and human-owner approval.

## Governing rule
No agent may exercise authority that the Rust Core has not explicitly granted.
