# Implementation Status

Inventory of current work in progress and its verification limits. Maturity terms are defined in [PHASE_ACCEPTANCE_STANDARD.md](PHASE_ACCEPTANCE_STANDARD.md). Verification snapshots in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) apply only to their stated revisions.

| Component | Implemented | Tested | Piloted | Production-ready | Notes |
|---|---|---|---|---|---|
| Rust core (`core/`): 24-agent roster, action policy, JSON-lines binary | Work in progress | Unit tests, per snapshot | No | No | Strict v2 contract includes resource, context and request ID, with structured decisions. Per-agent production grants are empty. No trustworthy caller authentication; descriptor self-assertion removed, so the production bridge denies all calls. Resource/context are not enforced. |
| Python bridge (`adapters/delanmar_adapters/bridge.py`) | Work in progress | Bridge tests, per snapshot | No | No | Subprocess client for the versioned contract; production calls deny without authentication. |
| LangChain and LangGraph helpers | Yes | Unverified | No | No | Unpinned; voluntary gate only, with no framework bypass prevention (Phase 7). |
| CrewAI helper | Roster-based helper | Unverified | No | No | Unpinned; roster lookup only, not an execution gate (Phase 7). |
| BeeAI | Callable seam only | Unverified | No | No | Must move beyond seam (Phase 7). |
| AG2 | No | No | No | No | Real adapter required (Phase 7). |
| Mojo (`mojo/`) | Metric example | Unverified | No | No | Toolchain unavailable in last snapshot; not a validated kernel or production capability. Phase 9 plans toolchain and workload evaluation. |
| Bazel build | Configuration | Unverified | No | No | Phase 9 plans toolchain, dependency, reproducibility and CI verification. |
| Agent workforce | Roster entries only | No | No | No | No operational agents. |
| Persistence, audit, secrets, backup/restore | No | No | No | No | Phase 2. |
| Approval workflow, execution broker, certification | No | No | No | No | Phase 1; an `approval_required` decision is not an approval or execution capability. |
| OpenWorks pilot plan | Documented | n/a | No | No | Business track; see [pilot plan](strategy/DELANMAR_OPENWORKS_PILOT_SETUP.md). |

## Unverified

Framework calls, CI, build reproducibility, security enforcement and recovery behavior are unverified.

Phase 7 separates certification of pilot-used frameworks from independent certification of all five for platform use. Neither track is complete merely because its requirements are documented.
