# evaluation_engine.py

from typing import Dict, List
from role_profiles import ROLE_PROFILES, resolve_role_profile


# --------------------------------------------------
# ATS SCORE (GENERIC, ALL DISCIPLINES)
# --------------------------------------------------

def compute_ats_score(sections: Dict[str, str]) -> int:
    """
    Measures resume quality for ATS systems:
    formatting, clarity, quantification, structure.
    """

    score = 100

    # Skills overload
    if len(sections.get("skills", "")) > 900:
        score -= 15

    # Missing experience section
    if not sections.get("experience"):
        score -= 20

    # Missing projects for technical roles
    if not sections.get("projects"):
        score -= 10

    # Poor quantification
    numbers = sum(char.isdigit() for char in " ".join(sections.values()))
    if numbers < 10:
        score -= 10

    # Weak structure
    if not sections.get("education"):
        score -= 5

    return max(score, 40)


# --------------------------------------------------
# ROLE READINESS SCORE (STRICT, DISCIPLINE-SPECIFIC)
# --------------------------------------------------

def compute_role_readiness(
    diagnostics: Dict[str, List[str]],
    base_score: int
) -> int:
    """
    Adjusts score based on role expectations and depth.
    """

    score = base_score

    # Missing core expectations are heavy penalties
    score -= len(diagnostics.get("missing_must_have", [])) * 10

    # Weak signals are lighter penalties
    score -= len(diagnostics.get("weak_signals", [])) * 4

    # Strengths provide small lift
    score += min(len(diagnostics.get("strengths", [])) * 2, 8)

    return max(min(score, 95), 30)


# --------------------------------------------------
# ROLE FIT RECOMMENDATION (KEY DIFFERENTIATOR)
# --------------------------------------------------

def recommend_best_roles(
    resume_text: str
) -> List[str]:
    """
    Determines which roles the resume best aligns with.
    """

    resume_text = resume_text.lower()
    role_scores = {}

    for role, profile in ROLE_PROFILES.items():
        score = 0

        for must in profile["must_have"]:
            if must in resume_text:
                score += 3

        for strong in profile["strong_signals"]:
            if strong in resume_text:
                score += 2

        role_scores[role] = score

    # Sort roles by alignment score
    sorted_roles = sorted(
        role_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [r[0] for r in sorted_roles[:3]]


# --------------------------------------------------
# FINAL EVALUATION WRAPPER
# --------------------------------------------------

def evaluate_resume(
    resume_text: str,
    sections: Dict[str, str],
    diagnostics: Dict[str, List[str]],
    target_role: str
) -> Dict[str, object]:
    """
    Unified evaluation across ALL disciplines.
    """

    ats_score = compute_ats_score(sections)

    role_readiness = compute_role_readiness(
        diagnostics,
        base_score=ats_score
    )

    recommended_roles = recommend_best_roles(resume_text)

    return {
        "ats_score": ats_score,
        "role_readiness_score": role_readiness,
        "recommended_roles": recommended_roles,
        "primary_role": target_role
    }
