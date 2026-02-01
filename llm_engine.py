# llm_engine.py

import os
from typing import List, Dict
from groq import Groq

# --------------------------------------------------
# LLM CLIENT (SAFE — NO HARD CODED KEYS)
# --------------------------------------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


MODEL_NAME = "llama-3.1-8b-instant"


def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
    """
    Single controlled entry point to the LLM.
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()}
        ],
        temperature=temperature,
        max_tokens=900
    )
    return response.choices[0].message.content.strip()


# --------------------------------------------------
# SYSTEM PROMPTS (STRICT)
# --------------------------------------------------

SYSTEM_RECRUITER = """
You are a senior recruiter and hiring panel reviewer.

STRICT RULES:
- You ONLY explain facts provided by the evaluation system.
- You NEVER invent missing skills, experience, or gaps.
- You NEVER give generic advice.
- You NEVER ask for a resume.
- You NEVER contradict the score.
- You NEVER assume seniority or intent.

Your job is to translate evaluation findings into clear, professional language.
"""

SYSTEM_EDITOR = """
You are an ATS-focused resume editor.

STRICT RULES:
- Improve wording only.
- Preserve meaning, scope, and seniority.
- Do NOT add tools, metrics, ownership, or deployment.
- Do NOT exaggerate or generalize.
- Do NOT merge bullets.
- Output one rewritten bullet per input bullet.
"""


# --------------------------------------------------
# 1️⃣ CROSS-DISCIPLINE REJECTION EXPLANATION
# --------------------------------------------------

def explain_rejection(
    score: int,
    reasons: List[str],
    diagnostics: Dict[str, List[str]],
    target_role: str
) -> str:

    if not reasons:
        return (
            "This resume was not rejected due to ATS or qualification screening. "
            "Any hiring decision at this stage would depend on role fit, team needs, "
            "or competition rather than resume quality."
        )

    reasons_block = "\n".join(f"- {r}" for r in reasons)

    missing_block = (
        ", ".join(diagnostics["missing_must_have"])
        if diagnostics.get("missing_must_have")
        else "None"
    )

    weak_block = (
        ", ".join(diagnostics["weak_signals"])
        if diagnostics.get("weak_signals")
        else "None"
    )

    prompt = f"""
Target Role:
{target_role}

Resume Score:
{score} / 100

Confirmed Rejection Reasons:
{reasons_block}

Missing Core Expectations:
{missing_block}

Weak or Underrepresented Signals:
{weak_block}

Task:
Explain clearly why this resume was rejected.
Do NOT add new reasons.
Do NOT generalize.
Do NOT give advice.
Keep tone professional and direct.
"""

    return call_llm(SYSTEM_RECRUITER, prompt)


# --------------------------------------------------
# 2️⃣ CROSS-DISCIPLINE STRENGTH SUMMARY
# --------------------------------------------------

def summarize_strengths(
    diagnostics: Dict[str, List[str]],
    target_role: str
) -> str:

    strengths = diagnostics.get("strengths", [])

    if not strengths:
        return (
            "The resume does not demonstrate strong differentiating signals "
            "beyond baseline expectations for this role."
        )

    strength_block = "\n".join(f"- {s}" for s in strengths)

    prompt = f"""
Target Role:
{target_role}

Confirmed Strengths:
{strength_block}

Task:
Summarize these strengths in 2–3 professional sentences.
Do not exaggerate.
"""

    return call_llm(SYSTEM_RECRUITER, prompt)


# --------------------------------------------------
# 3️⃣ ATS DIAGNOSTIC EXPLANATION
# --------------------------------------------------

def explain_ats_diagnostics(
    diagnostics: Dict[str, List[str]],
    target_role: str
) -> str:

    missing = diagnostics.get("missing_must_have", [])
    weak = diagnostics.get("weak_signals", [])

    prompt = f"""
Target Role:
{target_role}

Missing Expectations:
{', '.join(missing) if missing else 'None'}

Weak Signals:
{', '.join(weak) if weak else 'None'}

Task:
Explain how these gaps impact ATS and recruiter screening.
Do NOT invent missing tools.
Do NOT provide advice.
"""

    return call_llm(SYSTEM_RECRUITER, prompt)


# --------------------------------------------------
# 4️⃣ SAFE BULLET REWRITE
# --------------------------------------------------

def rewrite_resume_bullets(
    bullets: List[str],
    target_role: str
) -> List[str]:

    if not bullets:
        return []

    bullet_block = "\n".join(f"- {b}" for b in bullets)

    prompt = f"""
Target Role:
{target_role}

Original Bullets:
{bullet_block}

Task:
Rewrite each bullet to improve clarity and ATS alignment ONLY.
Follow all rules strictly.
"""

    output = call_llm(SYSTEM_EDITOR, prompt, temperature=0.25)

    return [
        line.lstrip("- ").strip()
        for line in output.splitlines()
        if line.strip()
    ]
