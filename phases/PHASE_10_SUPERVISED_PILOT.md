# Phase 10 — Supervised Pilot & Evaluation

**Status:** Not accepted. Maturity per [IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md); completion is governed by [PHASE_ACCEPTANCE_STANDARD.md](../PHASE_ACCEPTANCE_STANDARD.md).

## Objective
Operate selected workflows and measure real outcomes.

## Required deliverables
- Run the selected Delanmar workflow with human oversight.
- Measure actual results against the Phase 0 baseline.
- Stop or roll back when controls fail.

## Dependencies
Phase 9 pilot-readiness gate for the selected workflow, including applicable security, authorization, operational and human-approval gates.

## Related business pilot stage
Pilot Phase 7 in the [OpenWorks pilot plan](../strategy/DELANMAR_OPENWORKS_PILOT_SETUP.md) (business track; numbering is not equivalent).

## Acceptance
- **Minimum maturity: Piloted** for the selected workflow, not the entire platform.
- Demonstrate a controlled real-world run with human oversight, documented exceptions and stop or rollback when controls fail.
- Report actual outcomes against Phase 0 baseline definitions, including measurement period, sample size, data sources and limitations.
- Confirm positive and negative authorization tests for the pilot scope remain valid, including restricted actions and approval bypasses; record any incidents and corrective actions.
- Record revision, environment, commands or procedure, results, limitations and reviewer; update the implementation status and obtain human-owner approval of the evaluation and any expansion, revision, pause or stop decision.

## Governing rule
No agent may exercise authority that the Rust Core has not explicitly granted.
