# Phase 1 — Proposed Security Design

**Status: DESIGN ONLY — not implemented, approved, certified, or production-ready.** This is a proposal for human review, not a change to the [Core Architecture v1.0](../DELANMAR_CORE_ARCHITECTURE_v1.0.md), business policy, or either phase's acceptance status. Phase 1 design may proceed alongside Phase 0; implementation and use depend on the selected scope and owner decisions in the [worksheet](../strategy/PHASE_00_OWNER_INPUT_WORKSHEET.md). See the [security phase](../phases/PHASE_01_SECURITY_CORE.md), [acceptance standard](../PHASE_ACCEPTANCE_STANDARD.md), [status inventory](../IMPLEMENTATION_STATUS.md), and [workforce blueprint](../strategy/DELANMAR_AI_WORKFORCE_v1.1.md).

## 1. Inspected baseline and trust assumptions

At baseline `732aa39d9ce01c2b4b5b1c344ce3a8c11eed58b6`, [`core/src/lib.rs`](../core/src/lib.rs) has 24 stable roster strings and a shared six-action routine list. For a known agent, unknown actions currently yield `requires_human_approval`, not denial; unknown agents yield `unknown_agent`. The list does not bind actions to resources or individual roles. [`core/src/main.rs`](../core/src/main.rs) reads JSON lines on stdin and writes responses on stdout; no caller authentication or approval state exists.

[`bridge.py`](../adapters/delanmar_adapters/bridge.py) starts the executable selected by argument or `DELANMAR_BRIDGE`, sends synchronous JSON lines and reads responses; it has no contract version, authenticated principal, response correlation, or explicit timeout. [`frameworks.py`](../adapters/delanmar_adapters/frameworks.py) checks an action label in `guarded()` and invokes a Python callback; LangGraph likewise checks before calling `fn`, while CrewAI creates metadata without enforcing tools. The callback and arguments are not bound to the check, and frameworks can execute outside the helper. [`beeai.py`](../adapters/delanmar_adapters/beeai.py) is a callable seam; AG2 is absent.

[`core/src/lib.rs`](../core/src/lib.rs) has roster, policy and malformed-JSON unit tests; [`adapters/tests/bridge_test.py`](../adapters/tests/bridge_test.py) covers bridge and helper behavior, not an isolation boundary. [`core/Cargo.toml`](../core/Cargo.toml), [`core/BUILD.bazel`](../core/BUILD.bazel), [`adapters/BUILD.bazel`](../adapters/BUILD.bazel), and [`MODULE.bazel`](../MODULE.bazel) describe the existing build; their presence does not establish a verified deployment. The [architecture snapshot](ARCHITECTURE.md) records verification limits. No source or build changes are proposed in this design milestone.

**Trust model:** Rust policy and a small, isolated execution broker are trusted; framework code, model output, Python callbacks, supplied agent IDs, and input data are not. The broker owns privileged tool implementations and credentials. A trusted launcher, OS isolation and protected policy configuration are prerequisites, not properties of JSON lines. A malicious administrator, compromised host/kernel, or an attacker with the broker's OS privileges is outside the proposed local boundary; such compromise requires host-level incident response. Prototype tests use synthetic data only. No real business action is safe merely because this document exists.

## 2. Threat model

| Threat / boundary | Impact | Proposed mitigation |
|---|---|---|
| Unauthenticated local caller → bridge | Arbitrary caller asserts an agent and asks for authority | Authenticate the process/channel; map the authenticated principal to permitted agent identities in Rust; fail closed. For networked or multi-user use, authenticate each user/service and use protected transport and tenant isolation. |
| Unknown or impersonated agent → registry | Caller obtains another role's powers | Rust-owned immutable IDs, caller-to-agent binding, per-agent grants and audit; reject unknown IDs and unauthorized impersonation. Roster names alone are not credentials. |
| Unauthorized action or resource → policy | Data disclosure, modification or business commitment | Explicit per-agent action/resource/context grants; default deny, including unknown actions. Enforce at the broker and on every read as well as write. |
| Malformed, oversized or replayed request → protocol | Parser abuse, duplicate execution or confused decision | Strict bounded schema, version and sizes, unique request IDs, expiry and replay ledger; reject invalid or duplicate requests before execution. Network clients add transport integrity and anti-replay. |
| Framework tool or delegation → privileged resource | Bypass helper or expand authority | Separate process/OS identity, no direct credentials, deny direct resource/network access, broker-only tools, and independent authorization for each delegated action. Test direct and nested bypasses. |
| Compromised Python adapter → broker | Modified payloads, stolen data, forged responses | Treat adapter as hostile: authenticated constrained principal, broker reconstructs canonical operation and authorizes it, no secrets or direct resource access; validate responses and isolate the process. A compromised authorized adapter can still request operations granted to it; minimize grants. |
| Missing, stale or unavailable decision → executor | Action runs without authority | Timeouts, closed channels, invalid/mismatched responses, policy errors and process failure all block execution. Revalidate immediately before dispatch; no cached blanket allow. |
| Credentials → adapter, logs or source | Privilege escalation and data leakage | Only trusted broker holds least-privilege credentials; protected secret provider and rotation, no secrets in requests, logs or repository. A production secret store is future work, not implemented. |
| Business records → agent or cross-tenant access | Unauthorized disclosure or corruption | Authorize concrete record/resource and purpose; isolate stores and tenants, minimize data returned and redact audit payloads. No real records until storage and access controls are tested. |
| Forged human approval → approval service | Unauthorized consequential action | Authenticate a distinct human approver over a protected channel; check approver authority, bind decision to immutable request and expiration, audit and consume once. Agent assertions or self-approval are never proof. |

Locally, risks already include arbitrary execution by code running as the same user and bridge-binary substitution. Future networking adds remote attackers, transport interception, multi-user/tenant impersonation, shared services, key distribution and clock/replay concerns. Network exposure is prohibited until those controls have a separate reviewed deployment design.

## 3. Identity and proposed least-privilege policy

Rust owns a versioned registry: stable unique agent ID, blueprint role, capability descriptors, explicit action/resource/context grants, restrictions, approval eligibility and escalation triggers. Provision and change policy only through an authenticated, authorized human administrative process with audit and versioning. The existing 24 roster IDs are proposed as stable identifiers, not credentials. Define a policy entry and tests for each of the 24; agents without an owner-approved grant have no capabilities. The Business Operations Director remains a coordinating role, not a twenty-fifth specialist. Map each authenticated workload principal to only the agent IDs it may represent; never infer identity from an untrusted JSON field.

**PROPOSED — NOT OWNER-APPROVED.** Candidate permissions below apply only to synthetic or explicitly owner-approved pilot records, scoped to the assigned workflow and fields. “Draft” means internal preparation, not external communication, scheduling, record deletion or commitment. Even a listed candidate is denied until an explicit reviewed policy grants it.

| Agent ID / blueprint role | Candidate capability and explicit scoped permission | Restricted / denied; approval and escalation |
|---|---|---|
| `receptionist` / receive and route inquiries | Read assigned intake fields; classify and prepare an internal routing task | No outbound response or commitments; escalate missing/sensitive information and requests outside scope to human. |
| `interviewer` / gather requirements | Read assigned intake; prepare structured intake draft | No external questioning or writes outside draft scope; escalate ambiguity, sensitive data and unapproved requests. |
| `admin` / organize records and documents | Read approved assigned material; prepare internal document draft | No deletion, external publication or grants; escalate missing sources or sensitive records. |
| `data` / validate structured data | Read approved assigned fields; prepare validation report | No unrestricted record updates or bulk export; escalate discrepancies and unauthorized data. |
| `follow_up_caller` / follow-up and next steps | Read approved assigned status; prepare internal follow-up draft | No outbound calls/messages or commitments; escalate consent uncertainty, sensitive cases and any proposed contact. |

All other agents, actions, resources and contexts default to denied. The owner must explicitly decide whether any role may request approval for a particular action; `requires_human_approval` is not a generic escape hatch for unknown or prohibited actions. Blueprint high-impact categories, including payment, legal commitments, exceptional terms, personnel decisions, important-record deletion, access grants and security changes, require human authority; in this initial proposed subset they are **denied**, not automatically approvable. Owner-approved future rules may explicitly route eligible actions to human approval. Uncertainty, policy conflict, out-of-scope requests and inability to verify scope escalate to the owner without execution. A denial must not be changed into approval by delegation.

## 4. Versioned Rust authorization contract

**Proposed v1**, shared by every adapter and broker; reject unsupported versions and unknown fields. Separate authenticated transport principal from caller-supplied fields. Define canonical typed action schemas and resource identifiers; reject missing, malformed, oversized or ambiguous values. Parse and validate before evaluation, with no side effects on error. Use a collision-resistant, unique request ID; no PII or secrets in IDs.

| Request field | Meaning |
|---|---|
| `version`, `operation` | Contract version and typed operation, e.g. authorize or execute through the broker. |
| `request_id`, `correlation_id` | Unique request identity and cross-event correlation; retry semantics below. |
| authenticated caller | Obtained from the channel, not trusted from JSON; principal and permitted agent mapping. |
| `agent_id` | Stable Rust registry ID, checked against caller binding. |
| `action`, `resource` | Typed action and exact resource/tenant identifiers; resource version where applicable. |
| `parameters`, `context` | Canonical action parameters, purpose, workflow assignment, policy version, and any resource attributes required by policy. Reject unverifiable or caller-asserted authoritative attributes; broker obtains them from trusted sources. |
| `issued_at`, `expires_at`, `nonce` | Bounded validity and replay checks using trusted time; approval or execution reference when applicable. |

| Response field | Meaning |
|---|---|
| `version`, `request_id`, `correlation_id` | Must match the request and negotiated version. |
| `decision`, `reason_code` | Stable decision and non-sensitive explanation; never infer permission from absence of a denial. |
| `approval_id` | Present only when an eligible request is created or referenced; not proof of approval. |
| `audit_ref`, `policy_version` | Correlate to an emitted audit event and decision policy; an audit reference does not imply durable storage. |
| `expires_at` | Decision validity where applicable; not a reusable credential. |

Decision semantics:

| Result | Meaning and execution |
|---|---|
| `allowed` | Explicit policy permits this exact canonical operation in this context; only the trusted broker may execute it after immediate revalidation. A decision alone is not a bearer grant. |
| `denied` | Known caller/agent and valid request, but no applicable grant or an explicit prohibition; no execution. |
| `requires_human_approval` | Policy explicitly permits seeking approval for this exact operation; create a pending request, not execution authority. |
| `unknown_agent` | Agent ID absent from registry; no execution. A known agent not bound to the caller is denied. |
| `unauthenticated_caller` | Caller identity cannot be verified; no execution. |
| `invalid_request` | Schema, version, context, expiry or replay validation fails; no execution. |
| `authorization_unavailable` | Policy, authentication, required audit or decision service unavailable, timeout or invalid response; no execution. A transport failure may prevent a response, but must have the same fail-closed effect. |

Use an authenticated channel to bind responses to the connection; adapters validate version and correlation and never execute a callback after any result. Limit input line size, nesting and time; reject malformed UTF-8/JSON, duplicate keys and duplicate IDs. Record request IDs and canonical digests for a bounded retention window. Reusing an ID with different content is invalid; exact retries return the existing status, never run again. When replay/consumption state is lost, invalidate outstanding authorizations and approvals; do not resume privileged execution until state is safely re-established. Phase 2 must provide durable replay and audit state before recovery across restarts or real irreversible actions can be relied upon.

## 5. Human approval lifecycle

`Requested → Pending → Approved or Rejected → Executed or Cancelled`. Rejection terminates without execution; cancellation may also occur from Pending or Approved, including expiry. An Approved request is eligible for a **single** revalidated execution attempt, not a promise of execution. A failed or uncertain attempt remains non-executable pending human investigation/cancellation; never retry an external side effect blindly.

Each immutable approval record contains a unique approval ID, requesting principal and agent, exact canonical action, resource and relevant context/digest, policy and resource versions, request and expiry times, approver identity and decision timestamp, decision/reason, execution status and audit references. Show the human the exact operation and relevant context before decision. The authenticated human approver must be explicitly authorized, distinct from the requesting agent and workload, and cannot be an agent acting as approver. No self-approval or implied approval through silence.

On approval, verify identity, scope, pending state and expiry; atomically transition once. Immediately before execution, verify approval, caller binding, unchanged canonical digest and resource/policy versions, expiration, and current policy; invalidate and require a new request on any change. Atomically claim/consume approval and execution ID before dispatch, with concurrency tests. If an external effect times out after dispatch, record **unknown outcome**, block automatic replay, and reconcile with the external system or human; exactly-once external effects cannot be guaranteed without an integration's own idempotency/reconciliation. Rejection, expiry, cancellation, policy revocation and failures never execute.

Phase 1 may use a bounded, process-lifetime approval store and event sink for synthetic tests only, with restart invalidation and no real consequential actions. This is not a production approval system. Durable, recoverable records and reconciliation require Phase 2 and approved integrations; owner approval and access decisions remain open.

## 6. Bridge authentication and execution boundary

**Options for local use:**

| Option | Benefits | Limitations |
|---|---|---|
| Inherited private stdin/stdout pipes from a trusted launcher | Minimal changes to JSON-lines subprocess; possession of inherited descriptors identifies the launched session | Does not authenticate an agent or distinguish untrusted code sharing the same process/descriptors; arbitrary self-launched bridge instances are not trusted. Trusted launcher, restricted inheritance, binary integrity and isolated OS identity are required. |
| Unix-domain socket with restrictive permissions and OS peer credentials | Broker can verify peer user/process identity and support multiple isolated clients | Same OS user may impersonate another client; OS-specific, filesystem/namespace and lifecycle controls needed. Peer identity still needs mapping to agents. |
| Short-lived per-workload credential over a private channel | Finer principal mapping and revocation when combined with OS isolation | Token theft/replay and distribution risks; a token alone cannot contain compromised code with access to it. Never put tokens on command lines, in logs, or in repository files. |

**Proposed initial deployment:** trusted launcher starts a single protected Rust broker with private inherited channels to isolated adapter workloads; authenticate the channel/session and bind each workload principal to permitted agents. Use distinct OS identities or equivalent sandboxing and explicitly restricted descriptor inheritance. Verify the trusted binary/configuration, do not trust adapter-controlled `DELANMAR_BRIDGE`, and do not give adapters broker credentials or direct file, database, network, subprocess or tool access that can perform privileged actions. If the deployment cannot actually enforce these restrictions, it is not an authoritative boundary and must remain synthetic-only. A socket/peer-credential design is an alternative for separately launched clients, subject to the same isolation. Future network deployments require separately reviewed mutual authentication, encrypted transport, authorization per user/tenant, credential rotation and replay protection; local pipe trust does not transfer to a network.

Replace the `guarded()` callback pattern in future increments: untrusted framework code sends a typed operation to the trusted broker, not a function pointer. The broker derives canonical action, resource and parameters from the actual dispatch, asks Rust policy, verifies the exact decision/approval, and itself executes an allowlisted tool implementation. The tool has only the required scoped credentials. Calls to business resources must be inaccessible except through that broker, including via framework plugins, direct imports, shells, network, filesystem and delegation. Never expose raw privileged functions or credentials to a framework. Every delegated call is authenticated and independently evaluated for the recipient and exact operation; delegation cannot inherit or widen authority.

Bind policy evaluation to dispatch in the trusted boundary, avoiding check-then-use changes. Protect the broker from arbitrary dynamic tool registration, payload substitution and resource-version races; if an external system can change state independently, re-check and use its conditional-write/version facilities. On denial, invalid input, process crash, unavailable decision, or uncertain approval, do not invoke the tool. A successful check is not authorization for a different action, resource, parameter, context, principal, policy version or later replay. Isolation and actual enforcement—not a wrapper, prompt, or configuration flag—must be demonstrated before accepting any framework.

## 7. Audit and persistence boundary

Phase 1 emits structured, correlated events for authorization request and decision, approval request and decision, execution attempt and result, denial, and failures. Include event ID and time, contract/policy version, request/correlation/approval IDs, authenticated principal, agent ID, action type, resource reference, decision/reason code, outcome and approver identity where relevant. Avoid secrets and raw sensitive payloads; use minimized references and protected access. Correlate approval and execution with a digest of the canonical operation. Protect event integrity and define who can read them.

For Phase 1 synthetic testing use a bounded process-local sink, expose audit references and verify events; overflow or missing required audit blocks execution. Restart loses these events and invalidates pending state. **No durable audit history is claimed.** Phase 2 must implement and test durable append-only/tamper-evident storage as appropriate, authorization, retention/deletion, recovery, backups, audit/replay state and reconciliation, with owner-approved policies. Phase 1 evidence must state the sink and loss limits.

## 8. Test matrix and acceptance evidence

Use synthetic data and fake broker tools with a counter and side-effect recorder. Every negative authorization, approval, transport, or bypass test must assert **zero tool invocations and zero resource side effects**, not merely a denial string. For post-dispatch failures, assert no second invocation and explicit unknown outcome where applicable.

| Area | Positive tests | Negative / no-execution tests |
|---|---|---|
| Registry and policy | All 24 IDs unique, resolve to expected roles; each approved per-agent/action/resource grant permits its exact context. | Unknown IDs, wrong caller binding, cross-agent, cross-resource, missing grant, unknown action and explicit deny; exercise each agent with permitted cases where grants exist and denied cases for all. No grant means no positive execution case. |
| Authentication / protocol | Trusted launcher and bound caller; valid version and correlated response. | Unauthenticated/impersonated caller, unsupported version, malformed, duplicate-key, oversized, expired, missing fields, wrong correlation, replay and same ID with changed body. |
| Approvals | Eligible request → pending → authenticated authorized human approval → one exact execution; rejection and cancellation recorded. | Agent self-approval, wrong human, impersonation, changed action/resource/context/policy/version, replay, double submit, expired or revoked approval, concurrent consume and restart state loss; none executes. |
| Framework and delegation | Broker-mediated allowed typed operation invokes only the intended fake tool. | Direct callback/tool, raw resource access, plugin/import/shell/network attempts and nested delegation with expanded identity or scope blocked; framework helpers alone are not sufficient evidence. |
| Failures and audit | Events for request, decision, approval, execution and result have matching references; successful calls return correlated responses. | Rust process death, timeout, EOF, absent/malformed/mismatched decision, missing audit sink, adapter exception and broker error fail closed; denied/failure events recorded where sink available. |
| Execution and retries | Exact one-time authorized invocation with matching canonical inputs. | Parameter substitution, changed resource state, duplicate request, concurrent replay and timeout after dispatch; no duplicate side effect, uncertain external outcome requires reconciliation. |

Run Rust unit and integration tests plus Python bridge and adapter integration tests on the actual isolation mechanism. Record revision, environment, commands, results, side-effect evidence, known limitations and reviewer per [acceptance standard](../PHASE_ACCEPTANCE_STANDARD.md). Pilot-used framework certification and deployment-level isolation tests are separately required; all five frameworks are not prerequisites for a narrow pilot.

## 9. Small implementation increments

These are proposed future changes, not work performed here. Preserve the existing Rust core and JSON-lines bridge; do not deploy privileged business tools until the full boundary is demonstrably enforced.

| Increment and dependencies | Expected files / interfaces | Tests and expected behavior | Risks and acceptance evidence |
|---|---|---|---|
| 1. Registry and deny-by-default policy; owner reviews roles and grant vocabulary first | `core/src/lib.rs`; versioned registry/policy interface; tests in core | All 24 identities, per-agent grants, resource scoping and explicit deny; unknown actions denied. No execution exists in this increment. | Incorrect grants or misleading shared allowlist; reviewed policy table, unit results and explicit no-grant defaults. |
| 2. Versioned bridge and authenticated local principal; follows 1 | `core/src/lib.rs`, `core/src/main.rs`, `adapters/delanmar_adapters/bridge.py`, `adapters/tests/bridge_test.py`; request/response and launcher interface | Strict schema, correlation, caller-to-agent mapping, timeouts, malformed input, unknown caller and process failures all fail closed; compatibility migration is explicit, never silent fallback. | Self-asserted identity or same-user impersonation; demonstrate actual launcher/channel and OS isolation, not just parsing tests. |
| 3. Approval state machine and process-local audit; follows 1–2 and human-approver authentication design | `core/src/lib.rs`, `core/src/main.rs`, `adapters/delanmar_adapters/bridge.py`, core and adapter tests; approval and event interfaces | Exact binding, authorized distinct human, expiry, one-time consumption, denial and event correlation; restart invalidates in-memory state. | Simulated human identity or lost audit; test-only/synthetic mode and documented restart failure, no production claims. |
| 4. Trusted broker and isolated fake tools; follows 1–3 and reviewed isolation design | `core/src/` broker modules and binary entry point, `adapters/delanmar_adapters/bridge.py`, integration tests under `core/` and `adapters/tests/`; typed execute interface | Broker authorizes actual canonical operation then invokes only allowlisted fake tool; prove direct access, modified actions, replay and delegation cannot execute. | OS sandbox gaps, race conditions, compromised broker; independent adversarial test evidence and deployment prerequisites. No real credentials or business resources. |
| 5. Migrate selected adapter paths; follows 4 | `adapters/delanmar_adapters/frameworks.py`, relevant adapter modules and tests; broker-only tool/delegation interface | Replace callback authority with typed broker calls; selected framework positive and bypass tests show no direct privileged side effects. | Framework APIs/plugins can bypass wrappers; certify each pilot-used framework and underlying isolation, or leave it unavailable. |
| 6. Recovery and real integration readiness; follows Phase 2 persistence and approved pilot scope | Phase 2 record/audit interfaces, broker and integration tests; approved integration modules | Durable replay/approval/audit recovery, credential handling, conditional writes and reconciliation tested before real side effects. | Crash ambiguity and external duplicate effects; recovery drills, access/retention review and owner sign-off. Not a substitute for Phase 2 or Phase 9 acceptance. |

Actual future file lists may expand after review; build changes, if needed, require their own scoped review. Phase 1 acceptance is governed by its phase specification, not completion of this document. The first pilot remains standalone; Kiyoshi interoperability may use documented interfaces later and no dependency on Kiyoshi or all five frameworks is introduced.

## 10. Open owner and engineering decisions

- **OWNER INPUT REQUIRED:** choose workflow, human owner and approver(s), pilot roles, exact records, allowed actions, approval-eligible actions, prohibited actions, and escalation conditions in the [worksheet](../strategy/PHASE_00_OWNER_INPUT_WORKSHEET.md).
- **OWNER INPUT REQUIRED:** approve data access, retention/deletion, evidence storage, baseline definitions and values, and any real integration and credential ownership.
- **Engineering review required:** select supported OS isolation and launcher/broker deployment, trustworthy human authentication, policy administration and audit-sink behavior; prove that compromised adapter code cannot access privileged resources directly.
- **Engineering review required:** define durable replay/approval recovery, time source and external-system idempotency/reconciliation before real irreversible actions; address multi-user/network identity and tenant isolation before network exposure.
- **Unresolved:** current code has no authenticated bridge, per-agent policy, mandatory execution broker, human approval, durable audit or certified framework boundary. The design is not security certification and neither Phase 0 nor Phase 1 is complete.
