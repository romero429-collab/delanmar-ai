# Delanmar AI Build Roadmap

**Status:** Master twelve-phase engineering plan (revised). No phase is complete because it is documented.

This is the engineering track. The [OpenWorks pilot plan](strategy/DELANMAR_OPENWORKS_PILOT_SETUP.md) is the separate business-delivery track (its nine pilot phases 0-8 are unchanged and are not equivalent to these numbers). The [Core Architecture v1.0](DELANMAR_CORE_ARCHITECTURE_v1.0.md) remains the technical authority; the human owner retains final authority.

Related documents: [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) (authoritative inventory) and [PHASE_ACCEPTANCE_STANDARD.md](PHASE_ACCEPTANCE_STANDARD.md) (completion rules).

## Governing rule

**No agent may exercise authority that the Rust Core has not explicitly granted.**

LangChain, LangGraph, CrewAI, BeeAI, AG2, Python tools and future integrations must all operate through the same authorization contract. A framework integration that can bypass that contract is not an accepted integration.

## Preserve existing work

A functioning Rust prototype (`core/`) and Python bridge (`adapters/`) already exist. Build around and upgrade them; do not restart.

## Phases

| Phase | Name | Primary objective |
|---|---|---|
| [0](phases/PHASE_00_BASELINE_BOUNDARIES.md) | Baseline & Boundaries | Define scope, business workflows, owners and measurements. |
| [1](phases/PHASE_01_SECURITY_CORE.md) | Security & Core Foundation | Harden Rust identity, permissions and human approval. |
| [2](phases/PHASE_02_PERSISTENT_RECORDS_AUDIT.md) | Persistent Records & Auditability | Establish durable memory, records, logs and recovery. |
| [3](phases/PHASE_03_EXECUTIVE_OPERATIONS.md) | Executive & Operations Layer | Build the Executive Assistant and operational coordination. |
| [4](phases/PHASE_04_PROJECT_COORDINATION.md) | Project Coordination | Implement task management, dependencies and project tracking. |
| [5](phases/PHASE_05_COMMUNICATION_WORKFORCE.md) | Communication Workforce | Introduce selected communication agents. |
| [6](phases/PHASE_06_INTERNAL_OPERATIONS_WORKFORCE.md) | Internal Operations Workforce | Introduce selected internal operations agents. |
| [7](phases/PHASE_07_FRAMEWORK_CERTIFICATION.md) | Framework Certification & Integration | Validate all five framework adapters. |
| [8](phases/PHASE_08_BUSINESS_INTEGRATIONS.md) | Business Integrations | Connect approved business systems and external services. |
| [9](phases/PHASE_09_CONTROLLED_TESTING_PRODUCTION_OPS.md) | Controlled Testing & Production Operations | Test end-to-end workflows, reliability, monitoring and recovery. |
| [10](phases/PHASE_10_SUPERVISED_PILOT.md) | Supervised Pilot & Evaluation | Operate selected workflows and measure real outcomes. |
| [11](phases/PHASE_11_REUSABLE_PACKAGING.md) | Reusable Packaging & Expansion | Package validated capabilities and prepare evidence-based expansion. |

## Dependencies

Phase 0 -> Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phases 5-6 (Communication and Internal Operations) -> Phases 7-8 (Framework Certification and Business Integrations) -> Phase 9 -> Phase 10 -> Phase 11.

Some work can proceed in parallel (for example, Phase 1 Rust security design alongside Phase 0, and Phase 7 alongside Phases 2-6), but later phases cannot pass their acceptance gates until required dependencies are validated.

## Next development cycle

Phase 0 is the first active work package; Phase 1 Rust security design begins in parallel. Two synchronized tracks: engineering (this roadmap) builds the platform; business (the pilot plan) proves it solves real problems.
