//! Delanmar core: workforce roster and human-approval policy.
//! Source of truth: strategy/DELANMAR_AI_WORKFORCE_v1.1.md

use serde::{Deserialize, Serialize};

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

/// Actions that always need human approval (blueprint section 8).
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

#[derive(Debug, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum Decision {
    Allowed,
    RequiresHumanApproval,
    UnknownAgent,
}

/// Unknown actions are not auto-allowed: "high-impact actions not covered by an
/// approved policy" require approval, so only explicitly listed routine actions pass.
pub const ROUTINE_ACTIONS: [&str; 6] = [
    "draft_document",
    "read_record",
    "create_task",
    "summarize",
    "send_reminder",
    "update_status",
];

pub fn check_action(agent_id: &str, action: &str) -> Decision {
    if !ROSTER.iter().any(|g| g.id == agent_id) {
        return Decision::UnknownAgent;
    }
    if APPROVAL_REQUIRED.contains(&action) || !ROUTINE_ACTIONS.contains(&action) {
        Decision::RequiresHumanApproval
    } else {
        Decision::Allowed
    }
}

#[derive(Debug, Deserialize)]
#[serde(tag = "op", rename_all = "snake_case")]
pub enum Request {
    ListAgents,
    CheckAction { agent: String, action: String },
}

pub fn handle(line: &str) -> String {
    let out = match serde_json::from_str::<Request>(line) {
        Ok(Request::ListAgents) => serde_json::json!({ "agents": ROSTER }),
        Ok(Request::CheckAction { agent, action }) => {
            serde_json::json!({ "decision": check_action(&agent, &action) })
        }
        Err(e) => serde_json::json!({ "error": e.to_string() }),
    };
    out.to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn roster_matches_blueprint_counts() {
        let n = |d| ROSTER.iter().filter(|g| g.department == d).count();
        assert_eq!(ROSTER.len(), 24);
        assert_eq!(n(Communication), 8);
        assert_eq!(n(InternalOperations), 14);
    }

    #[test]
    fn gates_consequential_and_unknown_actions() {
        assert_eq!(check_action("bookkeeping", "issue_payment"), Decision::RequiresHumanApproval);
        assert_eq!(check_action("scheduler", "something_new"), Decision::RequiresHumanApproval);
        assert_eq!(check_action("scheduler", "create_task"), Decision::Allowed);
        assert_eq!(check_action("nobody", "create_task"), Decision::UnknownAgent);
    }

    #[test]
    fn bridge_rejects_bad_json() {
        assert!(handle("{").contains("error"));
    }
}
