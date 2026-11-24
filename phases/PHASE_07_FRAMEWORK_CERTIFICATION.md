# Phase 7 — Framework Certification & Integration

**Status:** Not accepted. Maturity per [IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md); completion is governed by [PHASE_ACCEPTANCE_STANDARD.md](../PHASE_ACCEPTANCE_STANDARD.md).

## Objective
Certify the frameworks used by the pilot and independently certify all five framework adapters for operational use.

## Required deliverables
- Support LangChain, LangGraph, CrewAI, BeeAI and AG2 through the Rust authorization contract.
- AG2 needs a real adapter.
- BeeAI must move beyond its current callable seam.
- Dependencies for each certified adapter must be version-pinned.
- Framework tools and delegation cannot grant authority beyond the Rust Core's explicit decision.

## Certification tracks

- **Pilot certification:** Every framework actually used by the selected pilot workflow must pass compatibility, authorization and security tests. Frameworks not used by that workflow are not pilot prerequisites. Pilot certification permits use within the approved supervised pilot before full platform certification, subject to all applicable readiness gates. No exception may bypass Rust Core authorization.
- **Platform certification:** Each of LangChain, LangGraph, CrewAI, BeeAI and AG2 must independently pass compatibility, authorization and security tests before that framework is enabled for operational use beyond the approved supervised pilot. Full platform certification requires all five, including a real AG2 adapter and BeeAI beyond its callable seam.

Documenting these requirements does not complete either track. Each track requires its own evidence and human-owner approval.

## Dependencies
Phase 1; may proceed in parallel with Phases 2-6. Pilot certification for every framework used by the selected workflow must pass before Phase 9 pilot-readiness testing; full platform certification is not a prerequisite for an otherwise validated pilot.

## Related business pilot stage
Pilot Phase 6 in the [OpenWorks pilot plan](../strategy/DELANMAR_OPENWORKS_PILOT_SETUP.md) (business track; numbering is not equivalent).

## Acceptance
- **Minimum maturity: Tested** for each framework within the certification track being accepted; full phase acceptance requires full platform certification.
- Demonstrate each in-scope, version-pinned adapter, including compatibility and security tests, and positive authorization tests for permitted actions.
- Demonstrate denial of unauthorized actions, tool and delegation bypass attempts, and unavailable authorization decisions for each in-scope framework. No framework may exceed a Rust Core decision.
- Record revision, environment, commands or procedure, results, limitations and reviewer; update the implementation status and obtain human-owner approval for the specific track.

## Governing rule
No agent may exercise authority that the Rust Core has not explicitly granted.
