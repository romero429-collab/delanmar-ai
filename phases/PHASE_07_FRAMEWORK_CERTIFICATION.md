# Phase 7 — Framework Certification & Integration

**Status:** Not accepted. Maturity per [IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md); completion is governed by [PHASE_ACCEPTANCE_STANDARD.md](../PHASE_ACCEPTANCE_STANDARD.md).

## Objective
Validate all five framework adapters.

## Required deliverables
- LangChain, LangGraph, CrewAI, BeeAI and AG2 must each pass individual compatibility and security tests.
- AG2 needs a real adapter.
- BeeAI must move beyond its current callable seam.
- All dependencies must be version-pinned.
- No adapter may bypass the Rust authorization contract.

## Dependencies
Phase 1; may proceed in parallel with Phases 2-6 but must complete before Phase 9 gates.

## Related business pilot stage
Pilot Phase 6 in the [OpenWorks pilot plan](../strategy/DELANMAR_OPENWORKS_PILOT_SETUP.md) (business track; numbering is not equivalent).

## Acceptance
All deliverables above meet the applicable maturity level under the acceptance standard, with evidence, negative tests for authorization where relevant, and human-owner approval.

## Governing rule
No agent may exercise authority that the Rust Core has not explicitly granted.
