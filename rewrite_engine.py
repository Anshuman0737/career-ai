# rewrite_engine.py

from typing import Dict, List
from llm_engine import call_llm

SYSTEM_REWRITE = """
You are a professional resume editor.

STRICT RULES:
- Rewrite ONLY based on the user's existing experience.
- Do NOT invent tools, metrics, or responsibilities.
- Do NOT increase seniority.
- Use provided improvement suggestions as guidance.
- Output concise, ATS-safe bullets.
"""


def generate_guided_rewrite(
    existing_bullets: List[str],
    improvement_suggestions: List[Dict[str, object]],
    target_role: str
) -> List[str]:

    if not existing_bullets or not improvement_suggestions:
        return []

    bullets_block = "\n".join(f"- {b}" for b in existing_bullets)
    suggestions_block = "\n".join(
        f"- {s['issue']}: {s['what_to_add']}"
        for s in improvement_suggestions
    )

    prompt = f"""
Target Role:
{target_role}

Existing Resume Bullets:
{bullets_block}

Improvement Guidance:
{suggestions_block}

Task:
Rewrite the bullets to address the guidance safely.
Preserve truth and scope.
"""

    output = call_llm(SYSTEM_REWRITE, prompt, temperature=0.25)

    return [
        line.lstrip("- ").strip()
        for line in output.splitlines()
        if line.strip()
    ]
