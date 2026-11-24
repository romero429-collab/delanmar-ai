# Phase 9 — Controlled Testing & Production Operations

**Status:** Not accepted. Maturity per [IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md); completion is governed by [PHASE_ACCEPTANCE_STANDARD.md](../PHASE_ACCEPTANCE_STANDARD.md).

## Objective
Test end-to-end workflows, reliability, monitoring and recovery.

## Required deliverables
- End-to-end tests.
- Retry and timeout behavior.
- Process and service recovery.
- Audit verification.
- Security testing.
- Monitoring and system health.
- Human handoff testing.
- Verify Bazel version and toolchain compatibility, dependency resolution, reproducible builds and CI integration. Bazel orchestrates builds and dependencies; it is not a runtime communications or authorization layer. Rust Core retains runtime authorization authority.
- Verify the Mojo toolchain and evaluate at least one justified compute workload for actual value. The existing metric example is not a validated kernel or production capability. Mojo does not own identity, permissions, approval or business authority.

Mojo is optional for the first pilot unless the selected workflow demonstrates a concrete need. The Bazel and Mojo work is required for full Phase 9 acceptance, but does not block pilot readiness when those capabilities are not required by the selected workflow; any build and compute components actually used by the pilot must be verified for that use. Record deferred work and limitations.

## Dependencies
Phases 1-8 as required by the selected workflow.

## Related business pilot stage
Pilot Phase 6 in the [OpenWorks pilot plan](../strategy/DELANMAR_OPENWORKS_PILOT_SETUP.md) (business track; numbering is not equivalent).

## Acceptance
- **Minimum maturity: Tested** for the selected workflow's pilot-readiness gate and for all Phase 9 deliverables before full phase acceptance.
- Before a supervised pilot, demonstrate end-to-end normal and exceptional workflows, audit verification, monitoring, retries and timeouts, recovery and human handoff; resolve critical defects and document remaining limitations.
- Test permitted actions and denial of unauthorized, malformed and unauthenticated requests, approval bypasses and unavailable authorization decisions across the selected workflow.
- For full phase acceptance, record Bazel version and toolchain compatibility, dependency resolution, reproducibility and CI results, plus Mojo toolchain verification and results of an evaluated, justified compute workload.
- Record revision, environment, commands or procedure, results, limitations and reviewer; update the implementation status and obtain human-owner approval for pilot readiness and separately for full phase acceptance.

## Governing rule
No agent may exercise authority that the Rust Core has not explicitly granted.
