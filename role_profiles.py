# role_profiles.py

ROLE_PROFILES = {

    "software_engineer": {
        "must_have": [
            "data structures",
            "algorithms",
            "problem solving",
            "programming"
        ],
        "strong_signals": [
            "system design",
            "scalability",
            "performance optimization",
            "testing"
        ],
        "red_flags": [
            "only coursework projects",
            "no production or applied work",
            "tool listing without usage"
        ]
    },

    "machine_learning_engineer": {
        "must_have": [
            "model training",
            "evaluation metrics",
            "data preprocessing"
        ],
        "strong_signals": [
            "deployment",
            "error analysis",
            "baseline comparison",
            "monitoring"
        ],
        "red_flags": [
            "accuracy without context",
            "no dataset description",
            "no evaluation methodology"
        ]
    },

    "data_scientist": {
        "must_have": [
            "data analysis",
            "statistics",
            "visualization"
        ],
        "strong_signals": [
            "business insights",
            "hypothesis testing",
            "experimentation"
        ],
        "red_flags": [
            "models without interpretation",
            "no impact metrics"
        ]
    },

    "backend_engineer": {
        "must_have": [
            "api development",
            "databases",
            "backend frameworks"
        ],
        "strong_signals": [
            "scalability",
            "security",
            "distributed systems"
        ],
        "red_flags": [
            "crud-only work",
            "no performance considerations"
        ]
    },

    "frontend_engineer": {
        "must_have": [
            "ui development",
            "javascript",
            "frontend frameworks"
        ],
        "strong_signals": [
            "performance optimization",
            "accessibility",
            "state management"
        ],
        "red_flags": [
            "design-only focus",
            "no interaction logic"
        ]
    },

    "product_manager": {
        "must_have": [
            "requirements gathering",
            "stakeholder communication",
            "roadmapping"
        ],
        "strong_signals": [
            "user research",
            "metrics",
            "prioritization frameworks"
        ],
        "red_flags": [
            "only coordination",
            "no ownership evidence"
        ]
    },

    "business_analyst": {
        "must_have": [
            "data interpretation",
            "requirements analysis",
            "reporting"
        ],
        "strong_signals": [
            "process optimization",
            "decision support"
        ],
        "red_flags": [
            "tool usage without insights"
        ]
    },

    "cybersecurity_engineer": {
        "must_have": [
            "security principles",
            "risk assessment",
            "network fundamentals"
        ],
        "strong_signals": [
            "incident response",
            "threat modeling",
            "compliance"
        ],
        "red_flags": [
            "certs without practice",
            "theory-only exposure"
        ]
    },

    "mechanical_engineer": {
        "must_have": [
            "design principles",
            "manufacturing processes"
        ],
        "strong_signals": [
            "cad tools",
            "simulation",
            "optimization"
        ],
        "red_flags": [
            "no applied projects"
        ]
    },

    "electrical_engineer": {
        "must_have": [
            "circuit analysis",
            "signal fundamentals"
        ],
        "strong_signals": [
            "embedded systems",
            "hardware testing"
        ],
        "red_flags": [
            "theory without implementation"
        ]
    },

    "generic": {
        "must_have": [],
        "strong_signals": [],
        "red_flags": []
    }
}


def resolve_role_profile(target_role: str):
    """
    Maps arbitrary role names to known profiles.
    """
    role = target_role.lower()

    if "machine learning" in role or "ml" in role:
        return ROLE_PROFILES["machine_learning_engineer"]
    if "data scientist" in role:
        return ROLE_PROFILES["data_scientist"]
    if "backend" in role:
        return ROLE_PROFILES["backend_engineer"]
    if "frontend" in role:
        return ROLE_PROFILES["frontend_engineer"]
    if "product" in role:
        return ROLE_PROFILES["product_manager"]
    if "business analyst" in role:
        return ROLE_PROFILES["business_analyst"]
    if "security" in role:
        return ROLE_PROFILES["cybersecurity_engineer"]
    if "software" in role or "developer" in role:
        return ROLE_PROFILES["software_engineer"]

    return ROLE_PROFILES["generic"]
