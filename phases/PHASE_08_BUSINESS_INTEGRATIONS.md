# Phase 8 — Business Integrations

**Status:** Not accepted. Maturity per [IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md); completion is governed by [PHASE_ACCEPTANCE_STANDARD.md](../PHASE_ACCEPTANCE_STANDARD.md).

## Objective
Connect approved business systems and external services.

## Required deliverables
- Introduce external services only when the workflow needs them.
- Each integration has its own permissions, credentials, data boundaries and error-handling policy.

## Dependencies
Phase 2, the Phase 0 workflow and Phase 7 pilot certification for frameworks used by that workflow; unrelated frameworks do not block pilot integrations.

## Related business pilot stage
Pilot Phase 6 in the [OpenWorks pilot plan](../strategy/DELANMAR_OPENWORKS_PILOT_SETUP.md) (business track; numbering is not equivalent).

## Acceptance
- **Minimum maturity: Tested** for each integration in the selected workflow.
- Demonstrate separately managed credentials, least-privilege permissions, data boundaries, error handling and auditable actions for each integration.
- Test permitted operations and deny unauthorized access, out-of-bound data transfers and restricted actions without approval; verify safe handling of unavailable services and credentials.
- Record revision, environment, commands or procedure, results, limitations and reviewer; update the implementation status and obtain human-owner approval.

## Governing rule
No agent may exercise authority that the Rust Core has not explicitly granted.
