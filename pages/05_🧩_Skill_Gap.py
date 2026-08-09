import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from services.skill_gap import analyze_skill_gap

st.title("🧩 Skill Gap Analyzer")

results = st.session_state.get("career_results", [])

if not results:
    st.info("Analyze a resume first.")
    st.stop()

role = st.selectbox("Choose target role", [x["role"] for x in results])
selected = next(x for x in results if x["role"] == role)

current = st.session_state.get("resume_data", {}).get("skills", [])
result = analyze_skill_gap(current, selected["required_skills"])

st.metric("Role Readiness", f"{result['readiness']}%")
st.progress(result["readiness"] / 100)

col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ Matched Skills")
    for skill in result["matched"]:
        st.success(skill.title())

with col2:
    st.subheader("⚠️ Missing Skills")
    for skill in result["missing"]:
        st.warning(skill.title())
