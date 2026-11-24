# Increment 2 — Trusted Workload Identity Deployment Boundary Proposal

**Status: recovered design proposal; architectural direction approved, implementation
not authorized or deployment-verified.** This reconstructs the reviewed document
from the conversation because the previous local commit was unavailable. The
proposed boundary is single-host only. Network and multi-tenant deployment are
unsupported. No production permissions, business workloads, approvals,
resource-scoped grants or execution broker are authorized by this document.
This is not Phase 1 acceptance, production readiness or independent certification.
The approved identity-boundary direction does not select a VM host or approve a
long-term local-first or hybrid product architecture.

## Increment 1 milestone and evidence

PR [#7](https://github.com/romero429-collab/delanmar-ai/pull/7) was merged on
2026-11-24 as fail-closed Increment 1 hardening. Its final PR head
`baff0183817593f7a8e1bb1ebceb7eb7de380ac4` is distinct from merge commit
`1e037b4023a1dced2a4405fe6dfa7c0051f732cf`. The latter is not a tested SHA in
the evidence below.

The [verification record on main at the merge commit](https://github.com/romero429-collab/delanmar-ai/blob/1e037b4023a1dced2a4405fe6dfa7c0051f732cf/docs/ARCHITECTURE.md)
and the [PR finalization comment](https://github.com/romero429-collab/delanmar-ai/pull/7#issuecomment-7144301348)
report these results; they are historical reports, not tests run for this
documentation change:

| Tested revision | Reported results |
|---|---|
| Original PR head `f30c6c96303045c5e62538b3733d8c573fbe8f7b` | 15 Rust unit tests, locked Rust build and 18 Python tests passed before subsequent changes. |
| Final PR head `baff0183817593f7a8e1bb1ebceb7eb7de380ac4` | The PR finalization comment reports 15 Rust and 21 Python tests, locked build and formatting passed. The main verification document separately records these commands against code commit `7248e15b5415e8ad81da126c361eeccd49aacdd9`; the final head's subsequent change was documentation only. |

The main verification document records Linux 7.0.0-1017-azure x86_64,
Rust/Cargo 1.100.0 and Python 3.12.3, the exact commands, a Bazel timeout and
CodeQL's absence of Python or Rust alerts for `7248e15b...`. The Linux
descendant test observed children inheriting bridge pipes survive timeout and
close; it cleaned them up explicitly. The evidence does not establish a
trusted identity boundary or independent security approval.

At merged main, the production executable has no trusted caller authentication
and denies all calls; production grants remain empty. Resource and context
fields are validated but not enforced as policy scopes. Framework guards are
voluntary; approvals, execution enforcement, process-tree containment and
independent security review are incomplete. An `approval_required` decision is
not an approval or permission to execute. The earlier inherited caller
assertion was removed, not made trustworthy.

## Scope and trust model

The proposed boundary authenticates the **workload instance** presenting a
local connection and maps it to one agent; it does not prove that the agent's
code is benign or enforce control of external effects. Future implementation
requires an explicit migration of the existing subprocess contract; it must
not silently fall back to caller-supplied identity assertions.

The trusted computing base includes the Linux host and kernel, host
administrator, service manager, trusted launcher, Rust authorization service,
protected configuration and their executable/dependency supply chain. For the
proposed cloud VM, it also includes Google Cloud infrastructure and
administrators, hypervisor and project IAM. Administrators control
installation, accounts and host isolation. Workloads, frameworks, model output,
request fields and ordinary local users are untrusted. The service is an
authorization decision point, not an execution broker.

## Proposed architecture

1. A privileged service manager starts a trusted launcher and a Rust service
   under separate, non-workload identities. Their executables, parent
   directories, configuration, working directories and environment are
   administrator-controlled and not writable by workloads or ordinary users.
   The launcher uses fixed, verified executable and configuration paths, not
   workload-provided paths or environment variables.
2. For the initial prototype, an administrator provisions dedicated host
   workload accounts and UIDs in advance, with one active instance per UID,
   including simultaneous instances of the same agent. The launcher selects
   only from the protected provisioned inventory; workloads cannot choose an
   account or agent mapping. These accounts are non-interactive and not shared
   with humans, daemons or other workloads. Dynamic allocation and UID reuse
   are deferred until lifecycle and cleanup behavior is independently verified.
   A protected registry binds the UID and a fresh instance/generation
   identifier to exactly one known agent. Agent IDs and request claims are not
   credentials.
3. Before executing untrusted code, the launcher creates a supervised process
   group/cgroup, establishes isolation and registers the instance through a
   protected control channel. The Rust service authenticates the launcher's
   dedicated OS identity using kernel peer credentials on the control
   connection, not a caller-supplied claim. The launcher's account, executable,
   configuration, control socket and all parent directories are protected by
   administrator-controlled ownership, permissions and isolation; workloads
   and ordinary users cannot access the endpoint or register, replace or revoke
   mappings. The service validates peer identity on every control connection.
   A same-UID attacker would be indistinguishable, so the launcher's UID must
   itself be exclusive and inaccessible to untrusted processes. The service
   uses an immutable or atomically published registry snapshot and accepts a
   mapping only after its validation and acknowledgement. Workloads cannot
   write, replace, or indirectly direct updates to the registry.
4. A workload connects to a protected filesystem Unix-domain stream socket.
   The Rust service obtains Linux `SO_PEERCRED` on each accepted connection,
   resolves the kernel-reported UID against the active registry, and binds that
   connection to the resulting instance and agent. Unknown, ambiguous,
   inactive or revoked UIDs are rejected. Any agent field in a request is only
   a claim and must match the bound agent; it never selects the principal.
5. On stop, crash, revocation or service restart, the supervisor invalidates
   the instance and its connections and stops the entire workload cgroup.
   Restart requires a new registration and fresh instance generation; no
   in-flight decision or cached binding survives by assumption. In the initial
   prototype the stopped account remains quarantined, not reused.

The launcher is trusted because of the protected host setup, not because a
process calls itself a launcher. The precise deployment, account allocation
and isolation mechanisms require implementation review.

## Laboratory choice and long-term direction

Windows remains the primary development and administration workstation. A
hybrid product with a local-first security core and optional cloud resources is
a **proposal**, not an owner decision. The Fedora VM is a laboratory host, not
a permanent product dependency; a cloud or physical deployment would need its
own boundary review and verification. WSL2 may support ordinary development,
but is not automatically equivalent to the isolated VM laboratory.

Compare these candidates before selecting a laboratory. Neither candidate has
been provisioned or approved by this comparison.

| Area | Local VM on Windows | Google Cloud VM |
|---|---|---|
| Trust boundary | Depends on the Windows host, hypervisor, their administrators and configuration as well as the guest. Host compromise can compromise the laboratory. | Depends on Google Cloud, hypervisor, project IAM and administrators as well as the guest. A cloud VM is not inherently a stronger boundary. |
| Feasibility | The owner's Windows edition, hardware virtualization, memory, disk, host security, hypervisor support and capacity are unknown. Verify them before selection; no hypervisor is selected. | The candidate size, region, image availability, account permissions and quotas must be verified. |
| Administration | A protected local console or tightly restricted host-to-guest SSH are candidates; select and verify the host and guest access controls. Avoid exposing SSH to the LAN. | No external IP; proposed IAP-only SSH with OS Login, least-privilege IAM and MFA where available. Compatibility must be established for the chosen image. |
| Updates and workload egress | A reviewed update-only route or verified offline package transfer is needed. A host-only network does not by itself prove workload egress is blocked. | IAP provides inbound access, not updates. Select and price filtered outbound access; Cloud NAT alone does not filter destinations. |
| Cost and operation | No cloud VM charge, but local electricity, hardware capacity, licenses, backup and any supporting services remain unpriced. | Compute, disk and supporting network services incur charges; an itemized estimate is still required. |

For either option, isolate the laboratory from business systems, do not expose
application services, and verify host-enforced restrictions rather than relying
on the workload's cooperation. The test scope is one Rust authorization service
and two synthetic workloads under separate UIDs, with local Unix-domain sockets
and kernel peer credentials. No customer data, business grants or privileged
workload execution is permitted. The host administration and trusted launcher
may require administrative privilege; that is distinct from granting privilege
to the workloads.

## Initial Fedora Cloud VM candidate

The proposed initial test platform is a dedicated, terminal-only Fedora Cloud
VM on Google Cloud Compute Engine, using systemd, cgroups and SELinux enforcing.
The host runs synthetic workloads only. No cloud resource provisioning or
runtime implementation is authorized. The proposed sizing is `e2-standard-2`
(2 vCPUs, 8 GiB), a 40 GiB standard persistent boot disk with Google-managed
encryption, and `us-central1-a`; availability and current prices require
verification. This is a candidate, not an approved deployment.

The exact Fedora Cloud Base x86_64 release and image remain **unselected**.
Before provisioning, verify publisher and provenance, support status,
guest-agent and OS Login compatibility, SELinux configuration and kernel
features. Fedora CoreOS is not a drop-in substitute: Google's
[OS Login documentation](https://cloud.google.com/compute/docs/oslogin/set-up-oslogin)
excludes it. If the requirements cannot be established together, stop for
review. After provisioning, verify the actual kernel, systemd, SELinux and
guest settings rather than assuming the image's intended configuration.

Proposed access has no external VM IP, uses least-privilege IAM, OS Login and
MFA where available, and permits administrative SSH through IAP TCP forwarding
only. Scope the firewall to this VM, TCP 22 and IAP's IPv4 source range
`35.235.240.0/20`; remove or disable broad SSH ingress. IAP is not outbound
internet access. An approved filtering proxy for documented update, package
and required Google API destinations is still to be selected, priced and
reviewed; Cloud NAT alone does not filter destinations. Deny other workload
egress and do not expose application services publicly.

Prefer no attached VM service account, subject to confirming the
administration workflow. Do not put cloud or administrative credentials in
workload environments, metadata or ordinary configuration. Verify host-enforced
workload restrictions on metadata access without breaking required guest
administration. Configure a human-reviewed profile specifying exact account
ownership, cgroup and service units, filesystem and socket permissions/ACLs,
mount views, `/proc`, ptrace, capabilities, namespaces, `no_new_privs`,
SELinux policy and descriptor inheritance. Startup must fail if required
controls cannot be established. No generic Linux compatibility is claimed.

Target approximately $25/month, with $50/month as the maximum, including
proxy and networking costs. Prior compute and disk estimates are unverified and
exclude proxy, network, snapshots, logging, taxes and other charges. Verify
regional prices and the full cost before provisioning; disks and snapshots can
incur charges while stopped. Set a budget and alert thresholds first; alerts
are notifications, not a hard cap. Any automated shutdown is subject to
separate review and testing.

Separate provisioning approval is required after image, access, networking and
budget gates are resolved. Runtime implementation needs a further separate
approval. VM evidence applies only to the tested configuration, not to future
physical hardware; independently review and verify any migration.

## Decision and gate record

This is a pre-provisioning review, not evidence that the planned controls
operate. A human owner must select the laboratory and explicitly decide whether
to adopt hybrid/local-first as the long-term direction. Until then both remain
open. No independent reviewer has approved the boundary in this record.

| Gate | State and evidence needed before provisioning |
|---|---|
| Environment | **Open.** Record the chosen host and hypervisor or cloud project/region, supported Fedora release, exact image identifier and provenance, signed checksum verification method, and expected kernel, systemd and SELinux configuration. Confirm host capacity or cloud availability and image compatibility. |
| Trust boundary | **Open.** Obtain independent review of the protected launcher, service, UID inventory and registry, socket and filesystem permissions, process/IPC isolation, descriptor handling and lifecycle/revocation design below. Identify the reviewer and unresolved risks; neither a design nor `SO_PEERCRED` alone proves enforcement. |
| Access and egress | **Open.** Specify the Windows administration path and recovery access, authenticated administrators, firewall rules and update destinations. Demonstrate in the design how workload traffic is denied even when the host can update. For cloud, verify IAP, OS Login, image guest support, IAM, service-account choice and filtered outbound path together. For local, document host-only or other network topology and how it avoids LAN exposure and unintended forwarding. |
| Budget | **Open.** Record dated, sourced prices and usage assumptions for the selected candidate, all supporting services and taxes, plus budget owner approval. Complete the estimate below and confirm it is at or below $50/month; approximately $25 is the target. An alert is not a spending cap. |
| Evidence and approval | **Open.** Record the selected configuration, decision owner, independent reviewer, evidence location, known limitations and explicit provisioning approval. Runtime implementation requires a separate explicit approval; neither approval closes Phase 1 or approves production security. |

Pre-provisioning checks establish that a specific configuration is feasible and
reviewed; they cannot establish actual enforcement. After separately approved
provisioning, record the installed image and artifact hashes, kernel, systemd,
SELinux enforcing state, account and socket settings, network paths and
administrative access, then verify them on the actual VM. Runtime-dependent
adversarial tests below can only follow separate runtime authorization and
implementation. A mismatch or failed control stops the experiment for review,
not an automatic exception.

### Cost worksheet

The amounts are deliberately **unverified**, not zero. Capture the date,
currency, source, region, machine and disk SKUs, hours/month, storage and
network usage, and pricing assumptions for each selected option. Include
one-time setup costs separately and disclose uncertainty.

| Cost component | Local VM | Cloud VM |
|---|---|---|
| Compute / host capacity | Incremental hardware, licensing and electricity: not estimated | VM size and running hours: not estimated |
| Storage and recovery | Disk capacity, backup and replacement: not estimated | Boot disk, snapshots and backup, including stopped VM storage: not estimated |
| Access, filtering and networking | Network and update-transfer/supporting service costs: not estimated | IAP, filtering proxy, NAT if needed, addresses, data processing and egress: not estimated |
| Operations | Monitoring, logs and other supporting services: not estimated | Monitoring, logs and other supporting services: not estimated |
| Taxes and fees | Not estimated | Not estimated |
| Total monthly and one-time cost | Unknown; budget gate open | Unknown; budget gate open |

## Socket, credentials and isolation evaluation

Unix-domain sockets and `SO_PEERCRED` avoid a caller-supplied bearer identity and
provide kernel-originated connection credentials. Filesystem socket access
permissions are a first filter, not an agent identity check. The proposal uses
an administrator-owned, non-workload-writable runtime directory (including
all parent components) and a launcher-created workload socket restricted to a
dedicated client group, for example directory mode `0711` and socket mode
`0660`. Only registered workload UIDs receive the client group; unregistered
group members still fail registry lookup. Ownership, modes, ACLs, mount view,
socket type and actual access must be checked before activation. The service
receives only the intended listening descriptor from the trusted launcher;
workloads cannot replace the socket or its directory. Stale paths may be
removed only after verifying their ownership and that no live service owns
them. Abstract sockets lack filesystem permission checks and are not proposed.
The separate control socket is restricted to the launcher and service identities
and checked independently; workload socket group access does not grant control
access.

The service and workload UIDs must be interpreted consistently in the host's
initial user namespace. This proposal excludes workload-created user namespaces
and credential-changing capabilities; it requires verification that namespace
translation, supplementary groups, setuid executables, capabilities and
`no_new_privs` cannot produce an accepted foreign UID. A PID reported by
`SO_PEERCRED` is diagnostic, not a durable identity: PIDs recycle. Credentials
are captured at connection establishment; do not assume they are refreshed for
each message or identify the current holder of a transferred descriptor.
Service authentication to clients relies on the protected socket path and
trusted mount view, not on an untrusted path or environment variable.

Distinct UIDs distinguish different workload instances only if the host
actually reserves them. A hostile process with the **same UID** is
indistinguishable by `SO_PEERCRED` and can use that instance's identity. Thus
the host must prevent unrelated processes from acquiring an allocated UID,
including through login, sudo, account provisioning, setuid, capabilities,
namespace mappings and service-manager configuration. All code already running
under one workload UID is within that workload's compromise scope: neither
same-UID process attribution nor isolation of mutually hostile code inside one
workload is claimed. If exclusive UID ownership cannot be established, startup
must fail rather than treating same-user credentials as authentication.

Isolation must also prevent cross-workload access to process state, descriptors
and IPC endpoints: restrict `/proc`, ptrace, signals, shared files, shared
memory and Unix sockets using host-enforced controls, separate writable
directories and appropriate namespaces/LSM policy as reviewed. Clear
supplementary groups and capabilities except for the explicitly needed client
group; restrict network and unrelated IPC. `SO_PEERCRED` alone does not prevent
a connected descriptor being transferred or a compromised workload proxying
requests for another party. Do not pass client or control descriptors between
workloads; enforce IPC restrictions and reject unexpected ancillary descriptor
passing on the service protocol. A compromised instance can nevertheless
exercise its own identity, and deliberate collusion or covert channels are not
claimed to be fully preventable by peer credentials.

## Lifecycle, reuse and fail-closed behavior

The launcher closes all unintended descriptors before workload execution, uses
close-on-exec by default, and explicitly allowlists only descriptors needed by
each child. Neither the service listener, launcher control channel, other
workloads' connections nor inherited binding pipes reach untrusted workloads.
Workload children stay in the same supervised instance and share its identity;
they cannot launch a different agent identity. The service must not treat a
workload-created bridge or inherited binding as authoritative.

Registry updates and connection admission/revocation must be serialized so
that a connection cannot be admitted using a stale mapping during a change.
Revocation blocks subsequent authorization decisions, closes existing
connections and invalidates pending requests; a request must still be
associated with an active instance at decision time. **Previously returned
decisions cannot reliably be retracted.** Without a future enforcement
mechanism at execution, a workload may use a stale allow after revocation;
this increment cannot prevent that execution or its external effects.

UID reuse is excluded from the initial prototype. If independently verified
lifecycle and cleanup procedures later permit reuse, first revoke the mapping,
terminate and reap the complete old cgroup, close and drain old connections and
pending work, verify no process or accessible descriptor retains that UID's
authority, and remove old writable state. Quarantine the UID if any step is
uncertain. Only then may a new generation be registered; on reboot, discard all
old registrations and connections and reconcile process/account state before
allocation. Since `SO_PEERCRED` supplies no generation, a generation number
alone cannot make unsafe UID reuse safe.

Start the service and validate its binary, configuration, policy availability,
socket and registry/control channel before launching workloads. Publish a
mapping and receive service acknowledgement before allowing workload code to
run. Any failed validation, duplicate UID or agent mapping ambiguity, missing
control acknowledgement, isolation failure, peer-credential error, unknown
peer, malformed request or unavailable policy prevents admission or yields
deny; no unbound or default identity is substituted. Loss of the service,
control channel or registry integrity stops new admissions, invalidates active
sessions, and causes the supervisor to stop affected workloads. Timeouts,
EOF, malformed/mismatched responses and uncertain outcomes must not be treated
as permission. Recovery starts from validated state and fresh registrations,
not cached allows. `approval_required` is not an allow. These are requirements
for future behavior, not claims about the existing bridge.

## Threats, assumptions and limits

The design targets a malicious workload or ordinary local user attempting to
claim another agent, connect as an unregistered UID, tamper with mapping or
socket state, steal a descriptor, survive restart, or exploit UID/PID reuse.
It assumes correct kernel isolation, exclusive UID provisioning, protected
service/launcher configuration, and a trusted administrator and supply chain.
Host root, kernel compromise, a malicious administrator, an attacker with
launcher/service privileges, and physical host compromise are outside the
boundary. Denial of service, kernel vulnerabilities, resource exhaustion,
side channels and covert collusion require separate controls and are not
eliminated by this design.

Identity authentication establishes who connects; it does not make that
workload trustworthy. An authenticated workload can request unauthorized
actions, run its own code, and attempt direct access to resources. Authorization
produces a decision; it does not itself enforce the decision at execution.
Controlling external side effects requires a separately reviewed future
enforcement mechanism and restrictions on direct resource access. Until then,
a Rust decision is not a system-wide execution guarantee and no business
operation is made safe by this proposal. There is no network transport, remote
identity, tenant isolation, approval workflow, durable audit, resource-scoped
authorization or privileged tool execution in this proposal. Use synthetic
workloads and resources only.

## Deployment-level adversarial verification requirements

These are **future test requirements**, not results. Run on the actual proposed
Linux deployment with at least two simultaneously live workloads A and B using
distinct UIDs and synthetic agents/actions. Use isolated test-only policy
fixtures that can distinguish A and B; never add business grants. A successful
test must verify both the service's observed principal/decision and the absence
of an unintended synthetic effect, where applicable. A rejected connection,
explicit deny, or timeout followed by no effect is failure-closed; an
`approval_required` response is not a successful allow. A previously returned
allow can still be acted on by a workload; demonstrate and record that
limitation rather than claiming revocation prevents its use.

| Scenario | Measurable pass criterion |
|---|---|
| Baseline and claim spoofing | Each workload is mapped to its registered agent; 100% of A's requests claiming B are denied, and a test-only B grant never applies to A. |
| Unknown and same-user processes | An unregistered UID and an ordinary user cannot obtain a principal. Attempt to spawn an unrelated process under B's UID via each configured account, privilege and namespace path; every attempt is blocked. If one runs as B, record boundary failure, not a successful peer-credential test. |
| Mapping and endpoint tampering | Attempts by A and an ordinary user to modify or replace registry, control channel, socket, parent directories or service binary fail; no request is attributed to a forged mapping or endpoint. Include stale socket and bad ACL cases. |
| Launcher control | Workloads and ordinary users cannot connect as the launcher, register, replace or revoke a mapping, or modify its executable, account, configuration or IPC endpoint. Wrong or unavailable control peer credentials prevent registration. |
| Process and descriptor theft | A cannot inspect or duplicate B's or the service's descriptors, ptrace or signal B, or access B's private IPC/state. Inspect inherited descriptors in each child; no listener, control channel or other workload connection is present. Attempt `SCM_RIGHTS` and cross-workload forwarding; no usable cross-instance channel is established under the configured isolation. |
| Lifecycle and reuse | Stop/revoke B while connected and with requests in flight: no subsequent decision uses B's old binding. Initial UID reuse is refused. Future reuse testing must include surviving children and retained descriptors, and demonstrate refusal until cleanup and that old connections never become the new generation. Repeat across service and host restart. Test previously returned decisions separately and record that this boundary cannot retract them. |
| Failure injection | Independently break credential lookup, registry validation, mapping acknowledgement, policy availability, isolation setup, socket creation, service/control-channel availability and response delivery. For every case, no workload starts unbound and no affected request produces an allow or synthetic effect. |
| Namespace and concurrency | Exercise configured namespace, capability, setuid and supplementary-group escape attempts and race connect/request against revoke/re-register. No foreign UID is accepted and no stale or ambiguous mapping produces an allow. Repeat races under load and report iteration counts. |
| Local VM baseline, if selected | Verify actual Windows host and hypervisor, guest image and configuration, administrative access, update path and workload egress restrictions. Verify that the VM and its management interfaces are not unintentionally exposed to the LAN. |
| Cloud baseline | Verify the actual image, IAM and OS Login, IAP-only ingress, proxy and egress restrictions, SELinux, accounts, protected files and sockets, descriptor inheritance and cgroup settings. Record failures; intended settings alone are not evidence. |

For each run record the repository revision and artifact hashes, Linux/kernel
and service-manager versions, UID/group and namespace layout, socket and
directory ownership/modes/ACLs, isolation and cgroup settings, registry
generation, test fixture, commands or reproducible procedure, attacker and
victim identities, timestamps, iteration counts, expected and actual
principal/decision/effect, logs, failures, cleanup and reviewer. Protect and
redact evidence; do not capture secrets. Retain failures and limitations, not
just passing logs. Independent review must assess whether the tested settings
match the deployment and whether the same-UID and descriptor-transfer
assumptions were actually enforced. Passing these tests would support only the
tested identity boundary, not Phase 1 acceptance or production readiness.

## Open design questions for human review

- Which supported Fedora Cloud image, kernel, systemd configuration and
  SELinux profile will be selected, and how will they be independently verified?
- Does the owner adopt hybrid/local-first, and which local or cloud laboratory
  meets the gates given the actual Windows workstation and available budget?
- Can OS Login and IAP work with that image and no attached service account?
  Which approved outbound proxy, destinations, regional prices and budget controls
  fit within the $25 target and $50 maximum?
- Who provisions and administers the dedicated accounts and protected mapping?
  What evidence would eventually justify UID reuse and crash recovery?
- What exact privileged control protocol, registry consistency/revocation
  semantics and client/server lifecycle will be specified and audited?
- Which IPC, filesystem, `/proc` and network restrictions are enforceable for
  the intended frameworks without undermining the identity assumptions?
- How will the existing bridge be migrated without a compatibility fallback
  that bypasses the proposed service?
- Where will deployment evidence be retained, and who independently reviews it?
