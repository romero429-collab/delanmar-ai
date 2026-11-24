# Delanmar Core Architecture v1.0

**Status:** Foundational engineering constitution and target architecture

**Scope:** Delanmar AI platform, integrations, workforce, and applications

## 1. Purpose and authority

Delanmar AI is a human-led, multi-language, multi-framework AI operating platform. Its technologies have distinct responsibilities; agent frameworks are integration environments, not competing foundations.

This document is the primary technical authority for the repository. Component designs and implementations must conform to it; the [workforce blueprint](strategy/DELANMAR_AI_WORKFORCE_v1.1.md) defines business roles and human approval requirements. The human owner retains final business authority. Changes to this constitution require an explicit version update and rationale.

This is a target architecture, not a claim that every control, contract, integration, or agent is implemented or verified. See [implementation architecture and status](docs/ARCHITECTURE.md) for the current state.

## 2. Technology responsibilities

| Component | Technology | Architectural responsibility |
|---|---|---|
| Delanmar Core | Rust | Trusted system foundation: identity, permissions, security, state, governance, and execution control |
| Delanmar Kernel | Mojo | AI execution, model interfaces, inference, and compute-intensive or optimized processing where justified |
| Delanmar Bridge | Bazel | Build orchestration, dependencies, reproducibility, and cross-language integration contracts |
| Delanmar Adapters | Python and other languages | Framework integrations, APIs, tools, external services, libraries, and specialized capabilities |
| Delanmar Workforce | Delanmar agents | Apply governed platform capabilities to business responsibilities |

“Kernel” names Mojo's architectural role; Mojo is a programming language and compute environment, not an operating-system kernel by itself. Rust remains the trusted system foundation. “Bridge” names the build and integration-contract role of Bazel: Bazel is a build system, not a runtime communications bridge. Rust-defined APIs, protocols, and bindings provide runtime communication across boundaries.

## 3. Logical layers

| Layer | Technology or component | Responsibility |
|---|---|---|
| L0 | Rust | Core system, security, identity, state, and governance |
| L1 | Mojo | AI compute and execution kernel |
| L2 | Bazel | Build, dependency, and integration orchestration |
| L3 | Python and other languages | Language adapters and external capabilities |
| L4 | Agent frameworks | Agent construction and orchestration through Delanmar adapters |
| L5 | Delanmar agents | 24 specialized business agents |
| L6 | Business applications | Customer service, scheduling, administration, research, and other workflows |

These are responsibility layers, not a mandatory runtime call sequence. Bazel is cross-cutting build infrastructure; it does not mediate runtime messages. The Business Operations Director is a coordinating role, not a twenty-fifth specialist.

## 4. Engineering rules

1. **Rust owns platform authority.** Frameworks, adapters, tools, and compute workloads must not bypass core identity, permissions, governance, or execution controls. Human approval and final authority remain with the designated human decision-maker.
2. **Mojo owns specialized compute.** Use it for workloads where its performance or AI capabilities justify it; it does not own security policy or business authority.
3. **Bazel owns reproducibility.** Each supported component must have a documented build and dependency contract, including its toolchains, dependency versions, and verification path.
4. **Adapters preserve interoperability.** Rust, Mojo, Python, and other languages communicate through documented, versioned interfaces and bindings rather than hidden dependencies. Runtime boundaries must authenticate and authorize operations as appropriate, fail closed when a required decision is unavailable, and retain an auditable record of consequential actions and approvals.
5. **Frameworks remain replaceable.** Delanmar owns agent identity, business memory, permissions, and workflow definitions. Framework-specific representations are adapter concerns, not the source of platform authority.

## 5. Agent framework adapter layer

Each framework connects through a standardized Delanmar adapter interface and is subject to the same core controls. These are intended integration environments; inclusion here does not mean an integration is implemented, installed, or tested.

| Framework | Intended responsibility |
|---|---|
| LangChain | Models, tools, retrieval, and integrations |
| LangGraph | Stateful agent workflows and orchestration |
| CrewAI | Specialized agent teams and task delegation |
| BeeAI | Agent interoperability and framework integration |
| AG2 | Multi-agent conversations, collaboration, and coordination |

Adapters must translate framework-specific inputs, outputs, and lifecycle events into the Delanmar contract, route governed actions through the core, and preserve approvals, state references, and audit history. Framework-provided tools or delegation cannot grant additional authority. A framework change must preserve the agent's Delanmar identity and policies; portability requires compatible adapters and verified migration of state and workflows, not merely swapping a dependency.

## 6. Common agent contract

Every Delanmar agent must expose, through the standardized interface:

- A unique, stable identity.
- Its assigned role and responsibilities.
- Its capabilities and available tools.
- Its permissions and security boundaries.
- Its input and output formats.
- References to its memory and state, subject to access control.
- Its communication protocol.
- Task status and execution history.
- Escalation conditions and human approval requirements.

The core owns the authoritative identity, permissions, and governance decisions. An adapter may represent these to a framework but cannot expand them. Contract versions and compatibility must be documented at each boundary; records and references must remain portable without exposing data to unauthorized agents or services. The contract is a requirement for future implementation, not a claim that the current interfaces provide every field.

For example, the Receptionist could move from CrewAI to LangGraph while retaining its Delanmar identity, permissions, business rules, and approved state, provided both adapters and the migration satisfy this contract.

## 7. Workforce, applications, and future interoperability

The workforce serves Delanmar business applications using shared, governed context and the responsibilities and approval rules in the workforce blueprint. Agents may prepare recommendations and drafts, but consequential actions require the appropriate human approval. Business-specific data and policy should remain separate from reusable platform and agent definitions.

Delanmar must operate independently. Documented interfaces may enable future interoperability with Kiyoshi AI OS, but Delanmar must not depend on Kiyoshi being completed first.
