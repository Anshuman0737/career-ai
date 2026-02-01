# analyzer.py

import re
from typing import Dict, List, Tuple
from role_profiles import resolve_role_profile


# -------------------------------------------------
# SECTION SPLITTING (ATS STYLE)
# -------------------------------------------------

SECTION_HEADERS = [
    "skills",
    "experience",
    "projects",
    "education",
    "certifications"
]


def split_into_sections(text: str) -> Dict[str, str]:
    text = text.lower()
    sections = {"header": ""}
    current = "header"

    lines = re.split(r"\n", text)

    for line in lines:
        clean = line.strip()
        if not clean:
            continue

        header_found = False
        for h in SECTION_HEADERS:
            if h in clean:
                current = h
                sections[current] = ""
                header_found = True
                break

        if not header_found:
            sections[current] += clean + " "

    return sections


# -------------------------------------------------
# IMPLICIT SIGNAL MAP (CRITICAL FIX)
# -------------------------------------------------

IMPLICIT_SIGNAL_MAP = {
    # ML core
    "model training": [
        "trained", "training", "cnn", "lstm", "bert",
        "fine-tuned", "fine tuned", "fit model"
    ],
    "evaluation metrics": [
        "accuracy", "precision", "recall", "f1",
        "%", "auc", "latency"
    ],
    "data preprocessing": [
        "preprocess", "pre-processing", "feature extraction",
        "normalization", "tokenization", "cleaned data"
    ],
    # ML depth
    "deployment": [
        "api", "fastapi", "flask", "lambda", "serverless",
        "tflite", "inference", "production"
    ],
    "baseline comparison": [
        "baseline", "compared", "improved over", "outperformed"
    ],
    "error analysis": [
        "error analysis", "failure cases", "misclassification"
    ],
    "monitoring": [
        "monitoring", "logging", "metrics tracking"
    ]
}


def has_implicit_signal(text: str, signal: str) -> bool:
    text = text.lower()
    keywords = IMPLICIT_SIGNAL_MAP.get(signal, [])
    return any(k in text for k in keywords)


# -------------------------------------------------
# CORE SCORING ENGINE (FIXED)
# -------------------------------------------------

def score_resume(
    resume_text: str,
    sections: Dict[str, str],
    target_role: str
) -> Tuple[int, List[str], Dict[str, List[str]]]:

    profile = resolve_role_profile(target_role)

    must_have = profile["must_have"]
    strong_signals = profile["strong_signals"]

    score = 100
    reasons = []

    diagnostics = {
        "missing_must_have": [],
        "weak_signals": [],
        "strengths": []
    }

    full_text = resume_text.lower()

    # -----------------------------
    # MUST-HAVE SIGNALS (SEMANTIC)
    # -----------------------------
    for item in must_have:
        if item in full_text or has_implicit_signal(full_text, item):
            diagnostics["strengths"].append(item)
        else:
            diagnostics["missing_must_have"].append(item)
            score -= 12

    if diagnostics["missing_must_have"]:
        reasons.append(
            "Core role expectations are present only partially or lack clear framing."
        )

    # -----------------------------
    # STRONG SIGNALS (OPTIONAL DEPTH)
    # -----------------------------
    for signal in strong_signals:
        if signal in full_text or has_implicit_signal(full_text, signal):
            diagnostics["strengths"].append(signal)
        else:
            diagnostics["weak_signals"].append(signal)

    if diagnostics["weak_signals"]:
        score -= min(len(diagnostics["weak_signals"]) * 4, 16)
        reasons.append(
            "Advanced role signals are present but not explicitly articulated."
        )

    # -----------------------------
    # UNIVERSAL ATS RULES
    # -----------------------------
    if len(sections.get("skills", "")) > 800:
        score -= 8
        reasons.append("Skills section is overloaded and may dilute ATS signals.")

    if "projects" in sections and len(sections["projects"].split()) < 120:
        score -= 6
        reasons.append("Projects could benefit from deeper applied context.")

    # -----------------------------
    # HARD GUARDRAIL
    # -----------------------------
    if reasons and score > 85:
        score = 78

    score = max(score, 0)

    return score, reasons, diagnostics
