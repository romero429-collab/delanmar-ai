# Phase 0 — Owner Input Worksheet

**Status:** Preparation only; Phase 0 is not accepted. Complete and review with the human owner before automation. Do not enter real customer information in this repository. See the [Phase 0 acceptance criteria](../phases/PHASE_00_BASELINE_BOUNDARIES.md) and [pilot plan](DELANMAR_OPENWORKS_PILOT_SETUP.md).

Use **OWNER INPUT REQUIRED** for each unanswered item. Proposed entries are not decisions or permissions. Store any sensitive completed worksheet and evidence in an owner-approved location with appropriate access controls, not in this repository.

## 1. Select and bound the workflow

The [pilot plan](DELANMAR_OPENWORKS_PILOT_SETUP.md#4-recommended-pilot-workflow) suggests customer intake, service preparation, scheduling, and follow-up. Start by considering only intake organization, document preparation, and follow-up preparation as the smallest safe subset. This is a suggestion, not an approved workflow. Estimates, payments, external scheduling, outbound calls, and customer commitments are not assumed approved.

| Decision | Owner input |
|---|---|
| Selected workflow, service and intended outcome | OWNER INPUT REQUIRED |
| Trigger and start point | OWNER INPUT REQUIRED |
| End point and completion criteria | OWNER INPUT REQUIRED |
| Channels, systems and locations in scope | OWNER INPUT REQUIRED |
| Included steps and handoffs | OWNER INPUT REQUIRED |
| Explicit exclusions and manual fallback | OWNER INPUT REQUIRED |
| Pilot limits, stop conditions and human launch decision | OWNER INPUT REQUIRED |

## 2. Current process and accountability

For each current step, document the actual process, not the desired automated process. Add rows as needed.

| Step and sequence | Trigger, input and output | Manual work, system and handoff | Human responsible | Pain points and exceptions |
|---|---|---|---|---|
| OWNER INPUT REQUIRED | OWNER INPUT REQUIRED | OWNER INPUT REQUIRED | OWNER INPUT REQUIRED | OWNER INPUT REQUIRED |

| Decision | Owner input |
|---|---|
| Named human workflow owner and backup | OWNER INPUT REQUIRED |
| Named human approver(s), approval points and escalation route | OWNER INPUT REQUIRED |
| Required agent roles and why each is needed | OWNER INPUT REQUIRED |
| Human responsibilities for review, corrections and customer handoff | OWNER INPUT REQUIRED |

## 3. Data and boundaries

| Decision | Owner input |
|---|---|
| Approved data sources, record types, purpose and access by role | OWNER INPUT REQUIRED |
| Restricted information and prohibited sources or uses | OWNER INPUT REQUIRED |
| Data minimization, test data and separation from business-specific information | OWNER INPUT REQUIRED |
| Retention periods, responsible owner and applicable requirements | OWNER INPUT REQUIRED |
| Deletion triggers, process, authorization and exceptions | OWNER INPUT REQUIRED |
| Approved location for measurements and evidence | OWNER INPUT REQUIRED |

## 4. Action and approval plan

List specific action, resource and context combinations. An empty cell grants no permission. Resolve overlaps conservatively; the owner must review the plan and representative permitted and prohibited actions. This worksheet does not implement enforcement.

| Agent or human role | Action, resource and context | Allowed / approval required / prohibited | Approver and escalation condition | Rationale or open decision |
|---|---|---|---|---|
| OWNER INPUT REQUIRED | OWNER INPUT REQUIRED | OWNER INPUT REQUIRED | OWNER INPUT REQUIRED | OWNER INPUT REQUIRED |

In particular, record explicit decisions about estimates, payments, external scheduling, outbound calls and customer commitments rather than treating preparation as permission to execute them. See the [proposed security design](../docs/PHASE_01_SECURITY_DESIGN.md).

## 5. Baseline measurements

Collect and record actual baseline values **before automation begins**. The definitions below are starting points, not established procedures; the owner must specify the eligible population, exact numerator, denominator, units, timing and rules. Use the same definitions for comparisons, document changes, and report limitations and regressions. Do not invent values or insert customer data.

| Measure | Starting definition to refine | Baseline value and unit |
|---|---|---|
| Time per inquiry | Staff time spent handling an inquiry | OWNER INPUT REQUIRED |
| First response time | Time from inquiry receipt to first response | OWNER INPUT REQUIRED |
| Completion rate | Completed eligible requests / eligible requests | OWNER INPUT REQUIRED |
| Follow-up completion | Required follow-ups completed on time / required follow-ups | OWNER INPUT REQUIRED |
| Rework rate | Cases requiring correction or repeated work / eligible cases | OWNER INPUT REQUIRED |
| Data accuracy | Sampled records meeting defined accuracy checks / sampled records | OWNER INPUT REQUIRED |
| Escalation rate | Cases routed to a human for review / eligible cases | OWNER INPUT REQUIRED |
| Cost per completed workflow | Included operating cost / completed cases | OWNER INPUT REQUIRED |

Complete one row per metric, identifying evidence without including private records here.

| Metric | Final definition, numerator / denominator and units | Source and evidence location | Collection period and time zone | Population, sample size and selection | Exclusions / missing data | Calculation and aggregation method | Responsible reviewer |
|---|---|---|---|---|---|---|---|
| OWNER INPUT REQUIRED | OWNER INPUT REQUIRED | OWNER INPUT REQUIRED | OWNER INPUT REQUIRED | OWNER INPUT REQUIRED | OWNER INPUT REQUIRED | OWNER INPUT REQUIRED | OWNER INPUT REQUIRED |

For time measures specify working versus elapsed time, start/stop events and aggregation; for accuracy define checks and sampling; for cost define included costs and allocation. If a denominator is zero or data is unavailable, record the result as unavailable and explain rather than inventing a value. Record the measurement method and limitations before comparing later results.

## 6. Exclusions, decisions and review

| Item | Owner input |
|---|---|
| Pilot exclusions and dependencies | OWNER INPUT REQUIRED |
| Unresolved decisions, risk, decision owner and due date | OWNER INPUT REQUIRED |
| Evidence of baseline, permission-plan and workflow review | OWNER INPUT REQUIRED |
| Human owner / approver, decision and date | OWNER INPUT REQUIRED |

Completion of this worksheet alone does not accept Phase 0, authorize automation, or establish that any security control exists. Use the [phase acceptance standard](../PHASE_ACCEPTANCE_STANDARD.md) to record review and evidence.
