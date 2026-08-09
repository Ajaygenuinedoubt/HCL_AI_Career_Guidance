import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from services.career_engine import recommend_careers

st.title("🎯 Career Explorer")

profile = st.session_state.get("profile", {})
resume = st.session_state.get("resume_data", {})

skills = list(set(
    profile.get("skills", []) +
    resume.get("skills", [])
))

if not skills:
    st.warning("Complete your profile or upload a resume first.")
    st.stop()

for result in recommend_careers(skills):
    with st.container(border=True):
        st.subheader(result["role"])
        st.progress(result["score"] / 100)
        st.write(f"**Career Fit: {result['score']}%**")
        st.write(result["description"])

        if result["missing_skills"]:
            st.warning("Missing: " + ", ".join(result["missing_skills"]))
        else:
            st.success("Strong alignment.")
