# Delanmar AI Build Roadmap

**Status:** Proposed execution roadmap; no phase is complete solely because it is documented.

This is the master execution plan for the existing repository. The [Core Architecture v1.0](DELANMAR_CORE_ARCHITECTURE_v1.0.md) remains the primary technical authority, the [workforce blueprint](strategy/DELANMAR_AI_WORKFORCE_v1.1.md) defines roles and approval requirements, and the human owner retains final authority. Resolve conflicts in favor of those authorities; changes to the constitution require its explicit version update and rationale. Record changes to this roadmap and phase gates with their rationale.

## Baseline

| Area | Present in this repository | Maturity and limitations |
|---|---|---|
| Governance and pilot | Constitution, workforce blueprint, and [OpenWorks pilot plan](strategy/DELANMAR_OPENWORKS_PILOT_SETUP.md) | Planning and target architecture; not evidence of deployment |
| Rust core | `core/` roster, shared action policy, JSON-lines binary and unit tests | Prototype; no caller authentication, per-agent permissions, durable audit or approval workflow |
| Runtime bridge | Rust binary and Python subprocess client in `adapters/` | Prototype; no versioned contract or enforced security boundary |
| Compute | `mojo/metrics.mojo` | Initial numeric example; interoperability and toolchain not verified |
| Build | `MODULE.bazel` and component build definitions | Configuration exists; cross-language builds and reproducibility not verified |
| Frameworks | Python LangChain, LangGraph and CrewAI helpers; BeeAI seam | Preliminary, unverified; AG2 absent and frameworks not pinned |
| Workforce and applications | 24 roster entries, including the Executive Personal Assistant | No operational employees or Command Center established |

The [implementation status](docs/ARCHITECTURE.md) records earlier Rust verification and the other verification limits. A roster entry, interface sketch, or framework tool is not an operational agent or an authorization boundary. Verify the current revision and environment before changing any status.

## Phases and gates

| Phase | Scope | Initial status | Exit deliverable |
|---|---|---|---|
| [00](phases/PHASE_00_CONSTITUTION.md) | Engineering constitution | Largely established; approval of this roadmap pending | Approved authority and execution roadmap |
| [01](phases/PHASE_01_INFRASTRUCTURE.md) | Development infrastructure | Partially established | Repeatable environment and evidence-backed baseline |
| [02](phases/PHASE_02_RUST_CORE.md) | Rust core hardening | Prototype exists | Trusted, tested core controls |
| [03](phases/PHASE_03_AGENT_CONTRACT.md) | Common agent contract | Not implemented | Versioned standard for agents and adapters |
| [04](phases/PHASE_04_RUNTIME_BRIDGE.md) | Runtime communication | Prototype exists | Reliable, governed and versioned boundary |
| [05](phases/PHASE_05_MOJO_KERNEL.md) | Mojo compute kernel | Initial example exists | Verified compute capability and interface |
| [06](phases/PHASE_06_BAZEL_BUILD.md) | Bazel build system | Configuration exists | Reproducible builds and tests for supported components |
| [07](phases/PHASE_07_FRAMEWORK_ADAPTERS.md) | Adapter and framework integrations | Preliminary seams exist; AG2 absent | Interchangeable, tested integrations |
| [08](phases/PHASE_08_ALPHA_EMPLOYEE.md) | First operational employee | Not started | Delanmar Alpha 0.1 |
| [09](phases/PHASE_09_WORKFORCE.md) | Full AI workforce | Roster exists, employees not operational | Governed 24-agent workforce |
| [10](phases/PHASE_10_ORCHESTRATION.md) | Business orchestration and Command Center | Not started | Manageable AI business operation |
| [11](phases/PHASE_11_PILOT_PRODUCTION.md) | OpenWorks pilot and production readiness | Pilot planning documented | Measured pilot and production-ready deployment process |

## Execution and dependencies

1. Establish Phase 0 authority and Phase 1 baseline first. Phase 1 verifies available tools and CI; Phase 6 later establishes the supported Bazel build and test gate.
2. Harden core authority in Phase 2, define the common contract in Phase 3, and apply both at the runtime boundary in Phase 4. Work may overlap, but adapters must not claim compliance before the relevant gates pass.
3. Phases 5 and 6 can proceed alongside core and contract work after the infrastructure baseline. Neither Bazel nor Mojo is a runtime authorization service. Any Mojo use in Alpha requires its verified interface; Alpha need not manufacture a compute workload merely to use Mojo.
4. Phase 7 follows the contract and bridge. Certify one suitable framework for Alpha before Phase 8; complete and test all five before closing Phase 7. Alpha does not need to wait for all five. Alpha additionally requires the core and its supported build/test path.
5. Expand incrementally after Alpha. Phase 9 establishes specialized employees; Phase 10 supplies broader coordination and oversight. Integrate these iteratively rather than assuming all agents must be deployed together. Phase 11 requires the controls and operational capabilities relevant to the selected pilot; full workforce and Command Center completion are required for the full program exit, not for an earlier limited, human-supervised pilot.

The OpenWorks plan has its own pilot phases 0–8; their numbering describes pilot rollout, not these platform build phases. Preserve its staged rollout and baseline/evaluation gates. Do not equate similarly numbered phases.

## Delanmar Alpha 0.1

The first vertical slice is the Executive Personal Assistant. A human submits a bounded task; the core authenticates the caller, recognizes the agent and authorizes its specific capabilities; a certified Python framework adapter executes an authorized task; the result crosses the versioned bridge, is validated, and the core records task and action outcomes. Restricted actions enter a recorded human approval workflow and do not execute without a valid approval and reauthorization. Denied, malformed, unavailable, or bypassed decisions fail closed.

Acceptance requires an end-to-end test from human instruction through execution to validated, audited completion, plus negative tests for unauthorized and approval-required actions. Drafting, task organization, correspondence preparation, and coordination are in scope only within explicitly granted capabilities; sending communications or making commitments requires the applicable policy and approval. The Alpha slice does not establish that the remaining workforce is operational.

## Evidence and completion

Every phase specification identifies scope, reuse, work, dependencies, tests, acceptance, risks, status and handoff. Maintain evidence tied to a revision, environment, commands, results, limitations and responsible reviewer. Distinguish implemented, locally tested, integrated, piloted and production-ready. Record failures and unresolved risks instead of treating skipped or unavailable tests as passes. Phase closure requires its acceptance evidence and human-owner approval; document approved exceptions without silently weakening security gates.

Immediate next steps: approve Phase 0, establish the Phase 1 environment and verification baseline, and only then prioritize implementation against the gates.
