# Delanmar OpenWorks Pilot Setup

**Status:** Proposed pilot plan (business track; engineering track: [BUILD_ROADMAP.md](../BUILD_ROADMAP.md))  
**Pilot environment:** Delanmar  
**Purpose:** Build, test, measure, and document a practical AI-assisted small-business operating model.

## 1. Executive summary

Delanmar will serve as the first real-world environment for developing and validating a coordinated AI workforce. The pilot will begin with a limited number of practical workflows, establish baseline measurements, introduce agents in controlled phases, and record outcomes.

The purpose is twofold:

1. Improve Delanmar's own business operations through useful, accountable automation.
2. Create a documented, reusable implementation model that can support future small-business deployments and an OpenWorks application or partnership discussion.

This document describes Delanmar's preparation and pilot plan. It does not imply OpenWorks acceptance, funding, endorsement, or program eligibility.

## 2. Pilot objectives

- Reduce avoidable administrative work and repetitive manual steps.
- Improve response consistency and follow-through.
- Make customer intake, scheduling, documentation, and internal coordination more reliable.
- Test how specialized agents collaborate and hand off work.
- Keep humans in control of consequential decisions.
- Measure actual results rather than relying on assumed productivity gains.
- Produce reusable templates, workflow documentation, and a credible case study.

## 3. Scope and workforce

The planned workforce contains 24 specialized agents:

- 8 Communication agents.
- 14 Internal Operations agents.
- 1 Executive Personal Assistant.
- 1 Project Manager.

The Business Operations Director is a coordinating role, not an additional specialist agent. The human owner/executive retains final authority.

The pilot should not attempt to deploy all 24 agents at once. Start with the smallest useful set for a clearly defined workflow, validate it, and expand only when the controls and results justify doing so.

See [DELANMAR_AI_WORKFORCE_v1.1.md](DELANMAR_AI_WORKFORCE_v1.1.md) for role definitions and authority boundaries.

## 4. Recommended pilot workflow

**AI-assisted customer intake, service preparation, scheduling, and follow-up**

A first end-to-end workflow can include:

1. Receive and classify an incoming inquiry.
2. Collect required customer and job details.
3. Organize the information into a structured service request.
4. Prepare an estimate using owner-approved service descriptions and pricing rules.
5. Draft a customer response or proposal for review where required.
6. Coordinate scheduling after customer agreement.
7. Check relevant inventory, equipment, or resource needs.
8. Track task completion and quality checks.
9. Organize transaction and service records.
10. Conduct approved follow-up and capture customer feedback.

Begin with intake, document preparation, and follow-up if those are the easiest safe workflows to validate. Add estimates, scheduling integrations, and financial workflows only after policies and permissions are defined.

## 5. Phased implementation

### Phase 0 — Define the baseline and boundaries

- Document Delanmar's current services and operating procedures.
- Select one pilot workflow and define its start and end points.
- Record current handling time, response time, rework, missed follow-ups, and other relevant baseline measures.
- Identify data that may be used, data that must remain restricted, and retention requirements.
- Define which actions agents may perform, which require review, and which are prohibited.
- Establish a human owner for each workflow.

**Exit criteria:** A written workflow map, baseline measurement plan, recorded baseline values with measurement definitions, collection period and data sources before automation begins, permission plan, and named human approver.

### Phase 1 — Establish the foundation

- Set up the shared business knowledge base and approved source documents.
- Define customer, lead, task, project, and service-request records.
- Establish agent identities and least-privilege permissions.
- Configure logging, audit history, backup, and recovery practices.
- Define secure integration credentials and secrets handling.
- Create a process for correcting inaccurate records and reporting incidents.

**Exit criteria:** Test records can be created, accessed only by authorized roles, audited, and recovered.

### Phase 2 — Configure the executive and operations layer

- Configure the Executive Personal Assistant for drafting, records, reminders, and executive summaries.
- Define the Business Operations Director's routine coordination scope.
- Establish escalation routes to the human owner.
- Test that neither role can independently approve restricted actions.

**Exit criteria:** Executive information and routine operational requests can be routed correctly, with authority boundaries enforced.

### Phase 3 — Add project coordination

- Configure the Project Manager for a defined pilot project.
- Create tasks, dependencies, milestones, and acceptance criteria.
- Test assignments, blocker reporting, status summaries, and deliverable checks.
- Confirm that project coordination cannot override approved budget or business policy.

**Exit criteria:** The pilot project can be tracked from approved objective through verified deliverables.

### Phase 4 — Deploy selected Communication agents

Prioritize the agents needed for the chosen workflow, potentially Receptionist, Interviewer, Customer Support, Scheduler, and Follow-up Caller.

- Use approved scripts, service information, and response boundaries.
- Test handoffs and incomplete or ambiguous customer requests.
- Require review for unusual requests and customer commitments.
- Apply appropriate consent and contact rules to outbound communication.

**Exit criteria:** Test cases are handled consistently, escalations work, and no unauthorized promises or communications occur.

### Phase 5 — Add selected Internal Operations agents

Prioritize Data, Admin, Quality Assurance, Inventory Tracker, and Bookkeeping support as appropriate to the pilot.

- Validate data accuracy and record provenance.
- Test inventory thresholds and exception handling.
- Use QA checklists and explicit completion criteria.
- Keep payments, filings, accounting judgments, and other consequential financial actions under human control.

**Exit criteria:** Internal records and checks are accurate enough for supervised operational use.

### Phase 6 — Integration and controlled testing

- Test the complete workflow from initial inquiry through follow-up.
- Test normal, incomplete, duplicate, conflicting, and exceptional requests.
- Verify permission enforcement and approval gates.
- Test outages, retries, recovery, and human handoff.
- Record defects, severity, owner, corrective action, and retest result.

**Exit criteria:** Critical defects are resolved; unresolved limitations are documented; the human owner approves the limited pilot launch.

### Phase 7 — Run the pilot and evaluate

- Run the workflow with defined limits and human oversight.
- Review logs and exceptions regularly.
- Compare actual results to the baseline.
- Interview users or customers where appropriate and permitted.
- Document what improved, what did not, and what remains manual.

**Exit criteria:** A results report supported by actual records and a decision to expand, revise, pause, or stop.

### Phase 8 — Package reusable templates

- Separate reusable agent instructions from Delanmar-specific business data.
- Document configuration steps, integration requirements, permission patterns, and costs.
- Create sample workflows and test cases using synthetic or properly anonymized data.
- Record known limitations and conditions where human expertise is necessary.

**Exit criteria:** A repeatable small-business implementation package that another operator can evaluate without access to Delanmar's private records.

## 6. Measurement plan

Capture a baseline before automation. Use the same definitions before and after implementation.

| Measure | Definition |
|---|---|
| Time per inquiry | Elapsed staff time spent handling an inquiry |
| First response time | Time from inquiry receipt to first response |
| Completion rate | Share of eligible requests completed through the defined workflow |
| Follow-up completion | Share of required follow-ups completed on time |
| Rework rate | Share of cases requiring correction or repeated work |
| Data accuracy | Share of sampled records meeting defined accuracy checks |
| Escalation rate | Share of cases routed to a human for review |
| Customer feedback | Structured feedback collected with appropriate consent |
| Cost per completed workflow | Measured operating cost divided by completed cases |

For each metric, record the measurement period, sample size, data source, exclusions, and calculation method. Report both improvements and regressions. Do not claim savings, accuracy, or customer outcomes until supported by measured results.

## 7. Human oversight and risk controls

The pilot must preserve human authority over consequential decisions.

Require human approval before:

- Payments, transfers, refunds outside approved rules, or changes to financial account details.
- Signing agreements or accepting binding legal terms.
- Exceptional pricing, discounts, scope changes, or unapproved customer commitments.
- Sensitive employment or personnel decisions.
- Granting access, changing security controls, or deleting important records.
- Any high-impact action not explicitly covered by a reviewed policy.

Additional controls:

- Apply least-privilege permissions and separate test from production data.
- Use synthetic data for early testing wherever practical.
- Protect customer information and define retention and deletion procedures.
- Keep audit logs for important actions, approvals, and handoffs.
- Make uncertainty and source information visible to reviewers.
- Provide a human fallback for every customer-facing workflow.
- Review applicable privacy, consumer protection, accessibility, labor, and communications requirements before deployment.

## 8. OpenWorks preparation

Prepare an accurate application and demonstration package that explains:

1. The business problem Delanmar is addressing.
2. The target users and small-business context.
3. The proposed agent workforce and human oversight model.
4. The first workflow selected for the pilot.
5. The implementation phases and technical approach.
6. Baseline and outcome measurement methods.
7. Privacy, security, and safety controls.
8. What has been built, what has been tested, and what remains planned.
9. Evidence of community or small-business value, where available.
10. Lessons learned and how the model could be reused.

Use the current official OpenAI OpenWorks materials and application instructions to confirm program requirements, eligibility, deadlines, and any financial or partnership terms before submitting. Do not rely on unofficial summaries or assume that an application guarantees acceptance or funding.

Official starting points (verify current availability and instructions before use):

- [OpenAI OpenWorks](https://openai.com/openworks/)
- [OpenWorks Partner application](https://openai.com/form/openworks-partner/)
- [OpenWorks Business application](https://openai.com/form/openworks-business/)

## 9. Demonstration package

The pilot should produce a concise, evidence-based demonstration containing:

- A diagram of the workflow and agent handoffs.
- A short demonstration using synthetic or approved data.
- The workforce and permission model.
- Before-and-after metrics with dates and sample sizes.
- Examples of human approval and escalation.
- A list of known limitations and unresolved risks.
- A reusable setup guide for another small business.

Clearly distinguish working features from mockups, planned features, and future integrations.

## 10. Initial 30-day action plan

### Week 1 — Select and document

- Choose the first Delanmar workflow.
- Map current steps and identify pain points.
- Define the baseline metrics and human approver.
- Gather approved service descriptions, policies, and templates.

### Week 2 — Build the minimum foundation

- Set up shared records and a small approved knowledge base.
- Define roles, permissions, and audit requirements.
- Configure a limited Executive Personal Assistant workflow.
- Prepare test cases using synthetic data.

### Week 3 — Prototype and test

- Configure the first customer-intake and document-preparation steps.
- Add controlled handoffs to scheduling or follow-up as appropriate.
- Test edge cases, approvals, and human fallback.
- Correct defects and document limitations.

### Week 4 — Supervised pilot review

- Run a limited pilot only after the owner approves readiness.
- Review actual logs, exceptions, and measured outcomes.
- Compare results with the baseline.
- Decide whether to expand, revise, pause, or stop.
- Update the OpenWorks evidence package with verified findings.

The 30-day schedule is a planning target, not a promise that every phase or agent will be production-ready within that period.

## 11. Decisions to make before launch

- Which Delanmar service or workflow is the first pilot?
- Which communication channels and business systems are in scope?
- What data may agents access, and for how long?
- Which actions are permitted automatically, and which require approval?
- Who reviews exceptions and how quickly?
- What baseline period and sample size are adequate?
- What budget and operating-cost limits apply?

## 12. Pilot completion standard

The pilot is ready to be presented as a validated case study only when there is evidence of:

- A defined and documented workflow.
- Tested role permissions and human approval gates.
- Successful handling of representative test cases.
- A supervised operational run.
- Measured outcomes compared with a baseline.
- Documented failures, limitations, and corrective actions.
- A clear separation between demonstrated capabilities and future plans.

**Guiding principle:** Build something useful for Delanmar first, measure it honestly, and turn proven workflows into reusable tools for other small businesses.
