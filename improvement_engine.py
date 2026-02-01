# improvement_engine.py

from typing import Dict, List
from role_profiles import resolve_role_profile


# --------------------------------------------------
# IMPROVEMENT TEMPLATES (RESEARCH-ALIGNED)
# --------------------------------------------------

IMPROVEMENT_LIBRARY = {

    # ---------- ML / AI ----------
    "model training": {
        "section": "Projects / Experience",
        "what_to_add": "Explicitly describe how the model was trained.",
        "how_to_word": [
            "Trained a [model type] using [dataset description], optimizing for [objective].",
            "Implemented training pipelines with appropriate loss functions and optimization strategies."
        ]
    },

    "evaluation metrics": {
        "section": "Projects",
        "what_to_add": "Clarify how model performance was evaluated.",
        "how_to_word": [
            "Evaluated model performance using metrics such as accuracy, precision, recall, and F1-score.",
            "Measured performance on a held-out validation set to assess generalization."
        ]
    },

    "data preprocessing": {
        "section": "Projects / Experience",
        "what_to_add": "Describe data cleaning and feature preparation steps.",
        "how_to_word": [
            "Preprocessed raw data by handling missing values, normalization, and feature extraction.",
            "Applied domain-specific preprocessing techniques to improve model input quality."
        ]
    },

    "error analysis": {
        "section": "Projects",
        "what_to_add": "Mention analysis of failure cases or errors.",
        "how_to_word": [
            "Performed error analysis to identify common misclassification patterns.",
            "Reviewed failure cases to guide model refinement."
        ]
    },

    "baseline comparison": {
        "section": "Projects",
        "what_to_add": "Compare model results against a baseline.",
        "how_to_word": [
            "Compared model performance against baseline approaches to validate improvements.",
            "Benchmarked results against simpler models to justify architectural choices."
        ]
    },

    "monitoring": {
        "section": "Experience",
        "what_to_add": "Explain how models or systems were monitored post-deployment.",
        "how_to_word": [
            "Implemented logging and monitoring to track system performance over time.",
            "Monitored key metrics to ensure system reliability and performance stability."
        ]
    },

    # ---------- SOFTWARE / ENGINEERING ----------
    "system design": {
        "section": "Experience / Projects",
        "what_to_add": "Show architectural decision-making.",
        "how_to_word": [
            "Designed modular system architecture to support scalability and maintainability.",
            "Defined service boundaries and data flow for backend systems."
        ]
    },

    "scalability": {
        "section": "Experience",
        "what_to_add": "Explain how systems handled growth or load.",
        "how_to_word": [
            "Optimized system components to handle increased load efficiently.",
            "Improved system scalability through caching, async processing, or load balancing."
        ]
    },

    "testing": {
        "section": "Experience",
        "what_to_add": "Demonstrate validation and quality assurance.",
        "how_to_word": [
            "Implemented unit and integration tests to ensure system reliability.",
            "Used automated testing to catch regressions during development."
        ]
    },

    # ---------- PRODUCT / BUSINESS ----------
    "metrics": {
        "section": "Experience",
        "what_to_add": "Tie work to measurable outcomes.",
        "how_to_word": [
            "Defined and tracked key metrics to evaluate feature success.",
            "Used data-driven insights to inform decision-making."
        ]
    },

    "stakeholder communication": {
        "section": "Experience",
        "what_to_add": "Show cross-functional collaboration.",
        "how_to_word": [
            "Collaborated with cross-functional stakeholders to gather requirements.",
            "Communicated project progress and trade-offs to non-technical teams."
        ]
    }
}


# --------------------------------------------------
# CORE IMPROVEMENT ENGINE
# --------------------------------------------------

def generate_improvements(
    diagnostics: Dict[str, List[str]],
    target_role: str
) -> List[Dict[str, object]]:
    """
    Generates precise, safe improvement suggestions.
    """

    profile = resolve_role_profile(target_role)
    suggestions = []

    # Missing must-have signals
    for missing in diagnostics.get("missing_must_have", []):
        if missing in IMPROVEMENT_LIBRARY:
            entry = IMPROVEMENT_LIBRARY[missing]
            suggestions.append({
                "issue": f"Missing or unclear: {missing}",
                "section_to_update": entry["section"],
                "what_to_add": entry["what_to_add"],
                "example_wording": entry["how_to_word"]
            })

    # Weak signals
    for weak in diagnostics.get("weak_signals", []):
        if weak in IMPROVEMENT_LIBRARY:
            entry = IMPROVEMENT_LIBRARY[weak]
            suggestions.append({
                "issue": f"Weakly represented: {weak}",
                "section_to_update": entry["section"],
                "what_to_add": entry["what_to_add"],
                "example_wording": entry["how_to_word"]
            })

    return suggestions
