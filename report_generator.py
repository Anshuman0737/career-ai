# report_generator.py

from typing import Dict
from resume_parser import extract_text_from_pdf
from analyzer import split_into_sections, score_resume
from llm_engine import (
    explain_rejection,
    summarize_strengths,
    explain_ats_diagnostics,
    rewrite_resume_bullets
)
from improvement_engine import generate_improvements
from evaluation_engine import evaluate_resume


def generate_final_report(
    pdf_path: str,
    target_role: str
) -> Dict[str, object]:

    # ---------------------------------
    # 1️⃣ Parse resume
    # ---------------------------------
    resume_text = extract_text_from_pdf(pdf_path)
    sections = split_into_sections(resume_text)

    # ---------------------------------
    # 2️⃣ Deterministic analysis
    # ---------------------------------
    score, reasons, diagnostics = score_resume(
        resume_text=resume_text,
        sections=sections,
        target_role=target_role
    )

    # ---------------------------------
    # 3️⃣ Dual scoring + role fit
    # ---------------------------------
    evaluation = evaluate_resume(
        resume_text=resume_text,
        sections=sections,
        diagnostics=diagnostics,
        target_role=target_role
    )

    # ---------------------------------
    # 4️⃣ LLM explanations (constrained)
    # ---------------------------------
    rejection_explanation = explain_rejection(
        score=score,
        reasons=reasons,
        diagnostics=diagnostics,
        target_role=target_role
    )

    strengths_summary = summarize_strengths(
        diagnostics=diagnostics,
        target_role=target_role
    )

    ats_diagnostics = explain_ats_diagnostics(
        diagnostics=diagnostics,
        target_role=target_role
    )

    # ---------------------------------
    # 5️⃣ Improvement suggestions
    # ---------------------------------
    improvements = generate_improvements(
        diagnostics=diagnostics,
        target_role=target_role
    )

    # ---------------------------------
    # 6️⃣ Bullet rewrite (safe)
    # ---------------------------------
    raw_projects = sections.get("projects", "")
    project_bullets = [
        b.strip()
        for b in raw_projects.split("–")
        if len(b.strip()) > 40
    ][:4]

    rewritten_bullets = (
        rewrite_resume_bullets(project_bullets, target_role)
        if project_bullets
        else ["No bullet rewrite required — project bullets are already ATS-aligned."]
    )

    # ---------------------------------
    # 7️⃣ Final report
    # ---------------------------------
    return {
        "target_role": target_role,

        # Scores
        "ats_score": evaluation["ats_score"],
        "role_readiness_score": evaluation["role_readiness_score"],

        # Fit
        "recommended_roles": evaluation["recommended_roles"],

        # Explanations
        "rejection_explanation": rejection_explanation,
        "strengths_summary": strengths_summary,
        "ats_diagnostics": ats_diagnostics,

        # Gaps
        "missing_core_expectations": diagnostics["missing_must_have"],
        "weak_signals": diagnostics["weak_signals"],

        # Improvements
        "how_to_improve": improvements,

        # Rewrites
        "sample_bullet_rewrites": rewritten_bullets
    }


# ---------------------------------
# 🧪 LOCAL TEST
# ---------------------------------
if __name__ == "__main__":

    report = generate_final_report(
        pdf_path="sample_resume.pdf",
        target_role="Machine Learning Engineer"
    )

    print("\n================ FINAL REPORT ================\n")
    for k, v in report.items():
        print(f"\n--- {k.upper()} ---")
        print(v)
