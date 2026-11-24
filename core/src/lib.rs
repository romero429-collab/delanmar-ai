//! Delanmar core: workforce roster, caller identity and default-deny authorization.
//! Phase 1, Increment 1. See docs/PHASE_01_SECURITY_DESIGN.md.
//! Source of truth: strategy/DELANMAR_AI_WORKFORCE_v1.1.md

use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
use std::io::Read;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Department {
    Communication,
    InternalOperations,
    Executive,
    Project,
}

#[derive(Debug, Clone, Serialize)]
pub struct Agent {
    pub id: &'static str,
    pub name: &'static str,
    pub department: Department,
}

const fn a(id: &'static str, name: &'static str, department: Department) -> Agent {
    Agent { id, name, department }
}

use Department::*;

pub const ROSTER: [Agent; 24] = [
    a("interviewer", "Interviewer", Communication),
    a("receptionist", "Receptionist", Communication),
    a("scheduler", "Scheduler", Communication),
    a("customer_support", "Customer Support", Communication),
    a("sales_pitcher", "Sales Pitcher", Communication),
    a("closer", "Closer", Communication),
    a("cold_lead_caller", "Cold Lead Caller", Communication),
    a("follow_up_caller", "Follow-up Caller", Communication),
    a("data", "Data", InternalOperations),
    a("inventory_tracker", "Inventory Tracker", InternalOperations),
    a("bookkeeping", "Bookkeeping", InternalOperations),
    a("it", "IT", InternalOperations),
    a("compliance", "Compliance", InternalOperations),
    a("quality_assurance", "Quality Assurance", InternalOperations),
    a("market_research", "Market Research", InternalOperations),
    a("trend_analysis", "Trend Analysis", InternalOperations),
    a("security", "Security", InternalOperations),
    a("legal", "Legal", InternalOperations),
    a("human_resources", "Human Resources", InternalOperations),
    a("research", "Research", InternalOperations),
    a("development_based_on_research", "Development Based on Research", InternalOperations),
    a("admin", "Admin", InternalOperations),
    a("executive_personal_assistant", "Executive Personal Assistant", Executive),
    a("project_manager", "Project Manager", Project),
];

/// Version of the request/response contract. Requests with any other version are denied.
pub const PROTOCOL_VERSION: u32 = 1;

/// Actions that can never be `allow` (blueprint section 8). Even if a permission
/// grants one of these as `allow`, the decision is clamped to `approval_required`.
pub const APPROVAL_REQUIRED: [&str; 9] = [
    "transfer_money",
    "issue_payment",
    "change_banking_details",
    "sign_legal_agreement",
    "employment_decision",
    "exceptional_pricing",
    "delete_important_records",
    "change_security_controls",
    "grant_access",
];

/// Stable identity of a caller, established by the Rust core (never by request content).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Principal {
    pub agent_id: String,
}

impl Principal {
    /// Stable string form, e.g. `agent:scheduler`.
    pub fn stable_id(&self) -> String {
        format!("agent:{}", self.agent_id)
    }
}

pub fn is_known_agent(id: &str) -> bool {
    ROSTER.iter().any(|g| g.id == id)
}

/// Authentication failure. Always results in deny.
#[derive(Debug, PartialEq, Eq)]
pub enum AuthError {
    Unavailable(String),
    Invalid(String),
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
struct CallerBinding {
    version: u32,
    agent: String,
}

/// Establish the caller from a binding written by the trusted launcher onto a private
/// inherited channel (an inherited pipe/socket the launcher created). The identity is
/// never read from the environment or from request content.
pub fn authenticate_binding(mut channel: impl Read) -> Result<Principal, AuthError> {
    let mut buf = String::new();
    channel
        .by_ref()
        .take(4096)
        .read_to_string(&mut buf)
        .map_err(|e| AuthError::Unavailable(e.to_string()))?;
    let b: CallerBinding =
        serde_json::from_str(buf.trim()).map_err(|e| AuthError::Invalid(e.to_string()))?;
    if b.version != PROTOCOL_VERSION {
        return Err(AuthError::Invalid("unsupported binding version".into()));
    }
    if !is_known_agent(&b.agent) {
        return Err(AuthError::Invalid("unknown agent".into()));
    }
    Ok(Principal { agent_id: b.agent })
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Effect {
    Allow,
    ApprovalRequired,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Permission {
    pub action: String,
    pub effect: Effect,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum Decision {
    Allow,
    Deny,
    ApprovalRequired,
}

/// Individually assigned per-agent permissions. Anything not listed is denied.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PolicyTable {
    grants: BTreeMap<String, Vec<Permission>>,
}

impl PolicyTable {
    /// Production policy: every agent has an explicit, empty permission set.
    /// No business permissions are granted until the owner worksheet establishes them.
    pub fn production() -> Self {
        let grants = ROSTER.iter().map(|g| (g.id.to_string(), Vec::new())).collect();
        PolicyTable { grants }
    }

    /// Build a table from explicit assignments. Fails if any agent is unknown.
    pub fn from_assignments(
        assignments: Vec<(&str, Vec<Permission>)>,
    ) -> Result<Self, String> {
        let mut t = Self::production();
        for (agent, perms) in assignments {
            if !is_known_agent(agent) {
                return Err(format!("unknown agent in policy: {agent}"));
            }
            t.grants.insert(agent.to_string(), perms);
        }
        Ok(t)
    }

    pub fn authorize(&self, who: &Principal, action: &str) -> (Decision, &'static str) {
        let Some(perms) = self.grants.get(&who.agent_id) else {
            return (Decision::Deny, "unknown_agent");
        };
        match perms.iter().find(|p| p.action == action) {
            None => (Decision::Deny, "no_permission"),
            Some(p) => match p.effect {
                Effect::ApprovalRequired => (Decision::ApprovalRequired, "approval_required"),
                Effect::Allow if APPROVAL_REQUIRED.contains(&action) => {
                    (Decision::ApprovalRequired, "approval_required")
                }
                Effect::Allow => (Decision::Allow, "permitted"),
            },
        }
    }
}

/// The authorization service: an authenticated caller plus a policy. If either is
/// unavailable, every authorization request is denied (fail closed).
pub struct Core {
    caller: Result<Principal, AuthError>,
    policy: Result<PolicyTable, String>,
}

#[derive(Debug, Deserialize)]
#[serde(tag = "op", rename_all = "snake_case", deny_unknown_fields)]
enum Op {
    ListAgents,
    /// `agent` is a claim only; it must match the authenticated caller.
    Authorize { agent: String, action: String },
}

#[derive(Debug, Deserialize)]
struct Envelope {
    version: u32,
    #[serde(flatten)]
    op: Op,
}

fn deny(reason: &str) -> serde_json::Value {
    serde_json::json!({ "version": PROTOCOL_VERSION, "decision": Decision::Deny, "reason": reason })
}

impl Core {
    pub fn new(caller: Result<Principal, AuthError>, policy: Result<PolicyTable, String>) -> Self {
        Core { caller, policy }
    }

    pub fn handle(&self, line: &str) -> String {
        let env = match serde_json::from_str::<Envelope>(line) {
            Ok(e) => e,
            Err(_) => return deny("malformed_request").to_string(),
        };
        if env.version != PROTOCOL_VERSION {
            return deny("unsupported_version").to_string();
        }
        let Ok(who) = &self.caller else {
            return deny("caller_not_authenticated").to_string();
        };
        let out = match env.op {
            Op::ListAgents => serde_json::json!({ "version": PROTOCOL_VERSION, "agents": ROSTER }),
            Op::Authorize { agent, action } => {
                if agent != who.agent_id {
                    deny("caller_mismatch")
                } else if action.is_empty() {
                    deny("malformed_request")
                } else {
                    match &self.policy {
                        Err(_) => deny("authorization_unavailable"),
                        Ok(p) => {
                            let (d, reason) = p.authorize(who, &action);
                            serde_json::json!({
                                "version": PROTOCOL_VERSION,
                                "decision": d,
                                "reason": reason,
                                "principal": who.stable_id(),
                                "action": action,
                            })
                        }
                    }
                }
            }
        };
        out.to_string()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // TEST FIXTURE ONLY: not real business permissions.
    fn fixture() -> PolicyTable {
        PolicyTable::from_assignments(vec![
            (
                "scheduler",
                vec![Permission { action: "fixture_read".into(), effect: Effect::Allow }],
            ),
            (
                "bookkeeping",
                vec![
                    Permission { action: "issue_payment".into(), effect: Effect::Allow },
                    Permission { action: "fixture_review".into(), effect: Effect::ApprovalRequired },
                ],
            ),
        ])
        .unwrap()
    }

    fn core_as(agent: &str) -> Core {
        Core::new(Ok(Principal { agent_id: agent.into() }), Ok(fixture()))
    }

    fn req(c: &Core, agent: &str, action: &str) -> serde_json::Value {
        let line = serde_json::json!({"version":1,"op":"authorize","agent":agent,"action":action});
        serde_json::from_str(&c.handle(&line.to_string())).unwrap()
    }

    #[test]
    fn roster_matches_blueprint_counts() {
        let n = |d| ROSTER.iter().filter(|g| g.department == d).count();
        assert_eq!(ROSTER.len(), 24);
        assert_eq!(n(Communication), 8);
        assert_eq!(n(InternalOperations), 14);
    }

    #[test]
    fn production_policy_grants_nothing() {
        let p = PolicyTable::production();
        for g in ROSTER.iter() {
            let who = Principal { agent_id: g.id.into() };
            assert_eq!(p.authorize(&who, "create_task").0, Decision::Deny);
            assert_eq!(p.authorize(&who, "issue_payment").0, Decision::Deny);
        }
    }

    #[test]
    fn allow_deny_and_approval_required() {
        let c = core_as("scheduler");
        assert_eq!(req(&c, "scheduler", "fixture_read")["decision"], "allow");
        assert_eq!(req(&c, "scheduler", "fixture_review")["decision"], "deny");
        assert_eq!(req(&c, "scheduler", "unlisted")["decision"], "deny");
        let b = core_as("bookkeeping");
        assert_eq!(req(&b, "bookkeeping", "fixture_review")["decision"], "approval_required");
    }

    #[test]
    fn permissions_are_per_agent() {
        let c = core_as("bookkeeping");
        assert_eq!(req(&c, "bookkeeping", "fixture_read")["decision"], "deny");
    }

    #[test]
    fn approval_required_actions_never_allow() {
        let c = core_as("bookkeeping");
        assert_eq!(req(&c, "bookkeeping", "issue_payment")["decision"], "approval_required");
    }

    #[test]
    fn claimed_agent_must_match_authenticated_caller() {
        let c = core_as("scheduler");
        let r = req(&c, "bookkeeping", "issue_payment");
        assert_eq!(r["decision"], "deny");
        assert_eq!(r["reason"], "caller_mismatch");
        assert_eq!(req(&c, "nobody", "fixture_read")["decision"], "deny");
    }

    #[test]
    fn malformed_requests_denied() {
        let c = core_as("scheduler");
        for line in [
            "{",
            "{}",
            r#"{"version":1,"op":"authorize","agent":"scheduler"}"#,
            r#"{"version":1,"op":"authorize","agent":"scheduler","action":""}"#,
            r#"{"version":1,"op":"authorize","agent":"scheduler","action":"x","extra":1}"#,
            r#"{"op":"authorize","agent":"scheduler","action":"fixture_read"}"#,
        ] {
            let v: serde_json::Value = serde_json::from_str(&c.handle(line)).unwrap();
            assert_eq!(v["decision"], "deny", "{line}");
        }
    }

    #[test]
    fn unsupported_version_denied() {
        let c = core_as("scheduler");
        let v: serde_json::Value = serde_json::from_str(
            &c.handle(r#"{"version":2,"op":"authorize","agent":"scheduler","action":"fixture_read"}"#),
        )
        .unwrap();
        assert_eq!(v["reason"], "unsupported_version");
    }

    #[test]
    fn unauthenticated_caller_denied() {
        let c = Core::new(Err(AuthError::Unavailable("no channel".into())), Ok(fixture()));
        assert_eq!(req(&c, "scheduler", "fixture_read")["decision"], "deny");
    }

    #[test]
    fn authorization_service_failure_denies() {
        let c = Core::new(
            Ok(Principal { agent_id: "scheduler".into() }),
            Err("policy load failed".into()),
        );
        let r = req(&c, "scheduler", "fixture_read");
        assert_eq!(r["decision"], "deny");
        assert_eq!(r["reason"], "authorization_unavailable");
    }

    #[test]
    fn policy_with_unknown_agent_rejected() {
        assert!(PolicyTable::from_assignments(vec![("ghost", vec![])]).is_err());
    }

    #[test]
    fn binding_authentication() {
        let ok = authenticate_binding(&br#"{"version":1,"agent":"admin"}"#[..]).unwrap();
        assert_eq!(ok.stable_id(), "agent:admin");
        for bad in [
            &br#"{"version":1,"agent":"ghost"}"#[..],
            &br#"{"version":9,"agent":"admin"}"#[..],
            &b"garbage"[..],
            &b""[..],
        ] {
            assert!(authenticate_binding(bad).is_err());
        }
    }
}
