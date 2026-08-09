import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from services.resume_parser import parse_resume
from services.career_engine import recommend_careers
from services.ats_scorer import calculate_ats_score

st.title("📄 Resume AI")

uploaded = st.file_uploader("Upload your resume", type=["pdf", "docx"])

if uploaded:
    try:
        resume = parse_resume(uploaded.read(), uploaded.name)
        st.session_state.resume_data = resume
        st.session_state.resume_text = resume["text"]

        ats, suggestions = calculate_ats_score(resume["text"])
        st.session_state.ats_score = ats

        c1, c2 = st.columns(2)
        c1.metric("Skills Found", len(resume["skills"]))
        c2.metric("ATS Score", f"{ats}/100")

        st.subheader("🧠 Detected Skills")
        st.write(", ".join(x.title() for x in resume["skills"]) or "No known skills detected.")

        st.subheader("🎯 Recommended Careers")

        results = recommend_careers(resume["skills"])
        st.session_state.career_results = results

        for result in results[:5]:
            with st.container(border=True):
                st.markdown(f"### {result['role']}")
                st.write(f"**Fit: {result['score']}%**")
                st.progress(result["score"] / 100)

                if result["missing_skills"]:
                    st.warning("Skills to improve: " + ", ".join(result["missing_skills"]))
                else:
                    st.success("Strong skill match.")

        if suggestions:
            st.subheader("⚡ Resume Improvements")
            for suggestion in suggestions:
                st.write("• " + suggestion)

    except Exception as exc:
        st.error(f"Resume processing failed: {exc}")
