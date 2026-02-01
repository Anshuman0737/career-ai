# app.py

import streamlit as st
import tempfile
import os

from report_generator import generate_final_report

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Career AI – Resume Intelligence",
    layout="wide"
)

st.title("🚀 Career AI – Resume Intelligence Engine")
st.caption("ATS score • Role readiness • What to fix • How to fix it")

st.divider()

# ---------------------------------
# INPUTS
# ---------------------------------
uploaded_file = st.file_uploader(
    "Upload your resume (PDF only)",
    type=["pdf"]
)

target_role = st.text_input(
    "Target Role (e.g. Machine Learning Engineer, Backend Engineer, Product Manager)",
    placeholder="Machine Learning Engineer"
)

analyze_btn = st.button("Analyze Resume")

# ---------------------------------
# PROCESS
# ---------------------------------
if analyze_btn:

    if not uploaded_file or not target_role:
        st.error("Please upload a resume and enter a target role.")
        st.stop()

    with st.spinner("Analyzing resume..."):

        # Save uploaded PDF temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        try:
            report = generate_final_report(
                pdf_path=tmp_path,
                target_role=target_role
            )
        finally:
            os.remove(tmp_path)

    st.success("Analysis complete")
    st.divider()

    # ---------------------------------
    # SCORES
    # ---------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.metric("ATS Score", report["ats_score"])

    with col2:
        st.metric("Role Readiness Score", report["role_readiness_score"])

    st.divider()

    # ---------------------------------
    # ROLE FIT
    # ---------------------------------
    st.subheader("🎯 Best Fit Roles")
    st.write(", ".join(report["recommended_roles"]))

    st.divider()

    # ---------------------------------
    # EXPLANATIONS
    # ---------------------------------
    st.subheader("❌ Why You May Be Rejected")
    st.write(report["rejection_explanation"])

    st.subheader("✅ Strengths Detected")
    st.write(report["strengths_summary"])

    st.subheader("⚠️ ATS Diagnostics")
    st.write(report["ats_diagnostics"])

    st.divider()

    # ---------------------------------
    # GAPS
    # ---------------------------------
    st.subheader("📉 Missing Core Expectations")
    if report["missing_core_expectations"]:
        st.write(", ".join(report["missing_core_expectations"]))
    else:
        st.write("None")

    st.subheader("📉 Weak Signals")
    if report["weak_signals"]:
        st.write(", ".join(report["weak_signals"]))
    else:
        st.write("None")

    st.divider()

    # ---------------------------------
    # IMPROVEMENTS
    # ---------------------------------
    st.subheader("🛠️ How to Improve (What + Where + How)")

    if report["how_to_improve"]:
        for item in report["how_to_improve"]:
            with st.expander(item["issue"]):
                st.write(f"**Section to update:** {item['section_to_update']}")
                st.write(f"**What to add:** {item['what_to_add']}")
                st.write("**Safe example wording:**")
                for ex in item["example_wording"]:
                    st.markdown(f"- {ex}")
    else:
        st.write("No critical improvements required.")

    st.divider()

    # ---------------------------------
    # REWRITES
    # ---------------------------------
    st.subheader("✍️ Sample Bullet Rewrites")
    for b in report["sample_bullet_rewrites"]:
        st.markdown(f"- {b}")
