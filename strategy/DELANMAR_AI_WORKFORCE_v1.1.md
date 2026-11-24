# Delanmar AI Workforce Blueprint v1.1

**Status:** Initial operating blueprint  
**Workforce size:** 24 specialized agents  
**Operating model:** Human-led, AI-assisted, coordinated specialist workforce

## 1. Purpose

Delanmar AI is designed as an interoperable business workforce—not a collection of unrelated chatbots. Each agent has a defined mission, scope, permitted tools, expected inputs and outputs, escalation rules, and performance measures.

The initial implementation supports Delanmar's own operations. The architecture should remain configurable so successful workflows can later be adapted to other small businesses.

## 2. Workforce composition

| Group | Count | Purpose |
|---|---:|---|
| Communication Department | 8 | Customer-facing communication and relationship workflows |
| Internal Operations Department | 14 | Business administration, research, controls, and technical support |
| Executive Personal Assistant | 1 | Supports the human executive and coordinates executive information |
| Project Manager | 1 | Plans and tracks defined projects and deliverables |
| **Total** | **24** | **Specialized agents** |

The **Business Operations Director** is a coordinating management role, not a twenty-fifth specialist agent. It oversees ongoing business operations and coordinates work across departments.

## 3. Communication Department — 8 agents

1. **Interviewer** — gathers customer requirements, clarifies needs, and captures structured intake information.
2. **Receptionist** — receives and routes inquiries, provides approved general information, and directs requests to the appropriate workflow.
3. **Scheduler** — coordinates appointments, availability, confirmations, and reminders within approved scheduling rules.
4. **Customer Support** — handles routine questions, service updates, and issue triage; escalates unresolved or sensitive cases.
5. **Sales Pitcher** — explains approved services and presents relevant value propositions without making unauthorized promises.
6. **Closer** — supports the final stages of a sales conversation and records customer decisions; cannot independently approve exceptional terms.
7. **Cold Lead Caller** — conducts approved outreach to prospective customers, follows contact rules, and records outcomes.
8. **Follow-up Caller** — contacts customers and leads after defined events, tracks responses, and routes next steps.

All outbound communication must follow applicable consent, privacy, telemarketing, and do-not-contact requirements. Agents must identify themselves appropriately and must not misrepresent themselves as human employees.

## 4. Internal Operations Department — 14 agents

1. **Data** — maintains structured data, performs approved data entry and validation, and supports reporting.
2. **Inventory Tracker** — monitors supplies, equipment, stock levels, and reorder thresholds.
3. **Bookkeeping** — organizes transactions and supporting records, prepares reconciliations and reports, and flags anomalies. Human review remains required for accounting judgments, payments, and filings.
4. **IT** — supports systems, accounts, devices, troubleshooting, and technical documentation within granted access.
5. **Compliance** — tracks applicable requirements, maintains checklists, and flags potential compliance issues; it does not replace qualified professional advice.
6. **Quality Assurance** — checks work against defined standards, acceptance criteria, and customer requirements.
7. **Market Research** — gathers and summarizes market, customer, competitor, and industry information with source references.
8. **Trend Analysis** — identifies patterns in business and market data and distinguishes evidence from hypotheses.
9. **Security** — monitors operational security practices, access, incidents, and risk signals; sensitive actions require authorization.
10. **Legal** — organizes legal information, drafts materials for qualified review, and flags issues; it does not act as legal counsel or independently bind the business.
11. **Human Resources** — supports recruiting administration, onboarding materials, role records, and HR workflows. Employment decisions and sensitive personnel actions remain human-led.
12. **Research** — conducts assigned research and produces traceable findings.
13. **Development Based on Research** — turns approved research findings into proposed improvements, prototypes, or development tasks.
14. **Admin** — supports records, document organization, routine administration, and internal coordination.

## 5. Executive and management roles

### Human Executive / Owner

The human owner retains strategic direction, business accountability, and final authority. The owner approves budgets, business commitments, exceptional pricing or terms, sensitive personnel decisions, legal commitments, and other consequential actions.

### Executive Personal Assistant — specialist agent

The Executive Personal Assistant supports the owner directly. Responsibilities include:

- Preparing and organizing documents, reports, proposals, and presentations.
- Drafting correspondence for review and coordinating approved communications.
- Preparing meeting agendas, notes, summaries, and action lists.
- Tracking executive priorities, deadlines, reminders, and pending decisions.
- Relaying instructions and decisions to the appropriate roles.
- Maintaining organized executive records and decision history.
- Coordinating information between the owner and business functions.

The assistant is an information and coordination role. It does not acquire independent authority to make business decisions or approve commitments.

### Business Operations Director — coordinating role

The Business Operations Director coordinates ongoing business operations across the Communication and Internal Operations departments. It translates approved business priorities into operational direction, resolves routine coordination conflicts, monitors operational health, and escalates matters outside its authority.

### Project Manager — specialist agent

The Project Manager manages defined projects rather than all continuous business operations. Responsibilities include:

- Breaking approved objectives into tasks, dependencies, and milestones.
- Assigning or recommending task ownership among agents.
- Tracking progress, deadlines, blockers, and deliverables.
- Coordinating cross-department project work.
- Verifying deliverables against acceptance criteria.
- Producing concise project status reports and escalating risks.

The Project Manager cannot change business priorities, approve unbudgeted spending, or make commitments beyond delegated authority.

## 6. Coordination and authority model

The normal coordination path is:

**Human Executive / Owner → Executive Personal Assistant (executive interface) → Business Operations Director (ongoing operations) → departments and agents.**

For defined projects, the **Project Manager** coordinates assigned tasks across departments under an approved objective and scope.

This is a coordination model, not a rigid chain that prevents direct collaboration. The Executive Personal Assistant can communicate directly with the owner; department agents can collaborate on shared workflows; and the Project Manager can coordinate directly with task owners. Authority remains limited by each role's permissions.

| Role | Primary authority |
|---|---|
| Human Executive / Owner | Final strategic and consequential business decisions |
| Executive Personal Assistant | Organize, draft, remind, relay, and coordinate executive information |
| Business Operations Director | Coordinate routine ongoing operations within approved policies |
| Project Manager | Coordinate approved project scope, tasks, milestones, and reporting |
| Department agents | Execute assigned tasks within their specific permissions |

## 7. Shared infrastructure

The workforce should use shared infrastructure rather than isolated agent memory:

- **Business knowledge base:** approved policies, service descriptions, procedures, and reference material.
- **Customer and lead records:** structured records with access limited by role and purpose.
- **Document repository:** proposals, estimates, work orders, reports, correspondence, and templates.
- **Operational database:** tasks, schedules, inventory, projects, and workflow status.
- **Identity and permissions:** unique agent identities and least-privilege access.
- **Audit history:** records of important actions, approvals, data changes, and handoffs.
- **Integration layer:** controlled interfaces to communication, calendar, accounting, storage, and other approved systems.
- **Escalation channel:** clear routing to the responsible human decision-maker.

Each agent specification should define: identity, mission, scope, inputs, outputs, tools, permissions, communication protocol, escalation conditions, and performance metrics.

## 8. Safety, permissions, and human approval

Use least-privilege access: agents receive only the data and tools needed for their assigned work.

Human approval is required before:

- Transferring money, issuing payments, or changing banking details.
- Signing or accepting legal agreements or making binding legal commitments.
- Making sensitive employment or HR decisions.
- Accepting exceptional pricing, changing contractual terms, or promising unapproved deliverables.
- Deleting important records, changing security controls, or granting access.
- Taking other high-impact actions that are not explicitly covered by a reviewed and approved policy.

Agents may prepare recommendations, drafts, calculations, and supporting evidence. They must clearly label uncertainty, avoid fabricating facts, and preserve an approval trail. Human review does not remove the need for privacy, security, legal, or regulatory compliance.

## 9. Example customer workflow

A possible service-request workflow:

1. Receptionist receives and classifies the inquiry.
2. Interviewer gathers the customer's needs and required details.
3. The appropriate operations role prepares an estimate using approved pricing rules; unusual cases are escalated.
4. Sales Pitcher explains the proposed service.
5. Closer records the customer's decision, subject to approval rules.
6. Scheduler coordinates the appointment or service window.
7. Inventory Tracker checks relevant supplies or equipment.
8. Quality Assurance checks completion against the agreed requirements.
9. Bookkeeping organizes the transaction records for review.
10. Follow-up Caller requests feedback and records any next steps.

The workflow is illustrative. Actual routing, estimates, pricing, and service commitments must be configured to Delanmar's real services and approved procedures.

## 10. Implementation sequence

1. Define business data, shared records, identity, permissions, and audit requirements.
2. Configure the Executive Personal Assistant and Business Operations Director.
3. Establish project tracking and configure the Project Manager.
4. Implement the highest-value Communication workflows.
5. Implement the Internal Operations workflows in priority order.
6. Test handoffs, permissions, error handling, escalation, and human approvals.
7. Run a controlled pilot and measure results against a baseline.
8. Document reusable templates and lessons learned.

## 11. Reuse and Kiyoshi compatibility

Delanmar is the first deployment, not the only intended use. Keep business-specific policies and data separate from reusable agent definitions. Prefer documented APIs, portable data formats, and replaceable integrations.

The initial system should operate independently. It may later interoperate with Kiyoshi AI OS and related projects through documented interfaces, without making the Delanmar pilot dependent on Kiyoshi being complete.

## 12. Versioning and change control

This document is the v1.1 workforce baseline. Changes to agent count, roles, authority, or safety rules should be recorded with a rationale and version update. Pilot evidence should inform revisions; proposed capabilities must not be described as implemented until tested.
