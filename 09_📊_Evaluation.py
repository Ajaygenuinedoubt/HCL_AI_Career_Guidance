
import streamlit as st
import json
import re
from pathlib import Path
import sys


# ============================================================
# PATH
# ============================================================

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CareerPilot AI - Evaluation",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# HELPERS
# ============================================================

def safe_list(value):
    """Convert a value into a list."""

    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    if isinstance(value, str):

        if not value.strip():
            return []

        return [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]

    return [value]


def safe_text(value):
    """Convert any value into readable text."""

    if value is None:
        return ""

    if isinstance(value, (dict, list)):

        try:
            return json.dumps(
                value,
                ensure_ascii=False,
            )

        except Exception:
            return str(value)

    return str(value)


def calculate_profile_score(profile):
    """Calculate profile completeness."""

    if not isinstance(profile, dict):
        return 0

    important_fields = [
        "name",
        "branch",
        "year",
        "skills",
        "projects",
        "career_interest",
        "experience_level",
        "location",
    ]

    completed = 0

    for field in important_fields:

        value = profile.get(field)

        if isinstance(value, list):

            if len(value) > 0:
                completed += 1

        elif value is not None:

            if str(value).strip():
                completed += 1

    return round(
        completed / len(important_fields) * 100
    )


def calculate_resume_score(resume_data, resume_text):
    """Estimate resume data completeness."""

    score = 0

    if resume_text:
        score += 30

    if isinstance(resume_data, dict):

        if resume_data.get("skills"):
            score += 20

        if resume_data.get("education"):
            score += 10

        if resume_data.get("experience"):
            score += 15

        if resume_data.get("projects"):
            score += 15

        if resume_data.get("summary"):
            score += 10

    return min(score, 100)


def calculate_skill_gap_score(skill_gaps):
    """
    Estimate skill-gap analysis coverage.

    A generated skill-gap list means the analyzer
    has identified actionable gaps.
    """

    gaps = safe_list(skill_gaps)

    if not gaps:
        return 0

    if len(gaps) >= 8:
        return 100

    return min(
        40 + len(gaps) * 7,
        95,
    )


def extract_ats_score():
    """
    Try multiple session-state keys because different
    versions of CareerPilot may store the ATS result
    differently.
    """

    possible_keys = [
        "ats_score",
        "resume_ats_score",
        "ats_result",
    ]

    for key in possible_keys:

        value = st.session_state.get(key)

        if value is None:
            continue

        if isinstance(value, dict):

            for score_key in [
                "score",
                "ats_score",
                "overall_score",
            ]:

                if score_key in value:

                    try:
                        return float(
                            value[score_key]
                        )

                    except Exception:
                        pass

        try:
            return float(value)

        except Exception:
            pass

    return None


def extract_interview_score():
    """Get latest mock interview score."""

    possible_keys = [
        "interview_score",
        "last_interview_score",
        "mock_interview_score",
    ]

    for key in possible_keys:

        value = st.session_state.get(key)

        if value is None:
            continue

        try:
            return float(value)

        except Exception:
            pass

    # Try interview history

    history = st.session_state.get(
        "interview_history",
        [],
    )

    if isinstance(history, list) and history:

        scores = []

        for item in history:

            if isinstance(item, dict):

                score = item.get("score")

                if score is not None:

                    try:
                        scores.append(
                            float(score)
                        )

                    except Exception:
                        pass

        if scores:
            return round(
                sum(scores) / len(scores),
                1,
            )

    return None


def calculate_overall(
    profile_score,
    resume_score,
    skill_gap_score,
    ats_score,
    interview_score,
):
    """Calculate overall career readiness."""

    scores = []

    # Profile
    scores.append(profile_score)

    # Resume
    scores.append(resume_score)

    # Skill gap
    if skill_gap_score > 0:
        scores.append(skill_gap_score)

    # ATS
    if ats_score is not None:
        scores.append(
            max(
                0,
                min(
                    ats_score,
                    100,
                ),
            )
        )

    # Interview
    if interview_score is not None:
        scores.append(
            max(
                0,
                min(
                    interview_score,
                    100,
                ),
            )
        )

    if not scores:
        return 0

    return round(
        sum(scores) / len(scores)
    )


def readiness_label(score):

    if score >= 85:
        return "🚀 Highly Ready"

    if score >= 70:
        return "🟢 Job Preparation Ready"

    if score >= 50:
        return "🟡 Needs Improvement"

    if score >= 30:
        return "🟠 Early Preparation"

    return "🔴 Profile Incomplete"


def score_status(score):

    if score >= 80:
        return "🟢 Strong"

    if score >= 60:
        return "🟡 Moderate"

    return "🔴 Needs Work"


# ============================================================
# HEADER
# ============================================================

st.title("📊 Evaluation & Responsible AI")

st.caption(
    "CareerPilot AI evaluates the completeness of your "
    "career profile, resume, skills and preparation progress."
)


# ============================================================
# LOAD SESSION DATA
# ============================================================

profile = st.session_state.get(
    "profile",
    {},
)

resume_text = st.session_state.get(
    "resume_text",
    "",
)

resume_data = st.session_state.get(
    "resume_data",
    {},
)

skill_gaps = st.session_state.get(
    "skill_gap",
    [],
)

career_interest = st.session_state.get(
    "career_interest",
    "",
)

# Some applications store career interest
# inside profile.

if not career_interest and isinstance(profile, dict):

    career_interest = profile.get(
        "career_interest",
        profile.get(
            "target_role",
            "",
        ),
    )


# ============================================================
# CALCULATE METRICS
# ============================================================

profile_score = calculate_profile_score(
    profile
)

resume_score = calculate_resume_score(
    resume_data,
    resume_text,
)

skill_gap_score = calculate_skill_gap_score(
    skill_gaps
)

ats_score = extract_ats_score()

interview_score = extract_interview_score()

overall_score = calculate_overall(
    profile_score,
    resume_score,
    skill_gap_score,
    ats_score,
    interview_score,
)


# ============================================================
# OVERALL READINESS
# ============================================================

st.subheader("🎯 Career Readiness")

col1, col2, col3 = st.columns(
    [1, 1, 1]
)

with col1:

    st.metric(
        "Overall Readiness",
        f"{overall_score}/100",
    )

with col2:

    st.metric(
        "Status",
        readiness_label(
            overall_score
        ),
    )

with col3:

    if career_interest:

        st.metric(
            "Target Career",
            career_interest,
        )

    else:

        st.metric(
            "Target Career",
            "Not Set",
        )


st.progress(
    overall_score / 100
)


# ============================================================
# PROFILE + RESUME METRICS
# ============================================================

st.subheader("👤 Candidate Evaluation")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Profile Completeness",
        f"{profile_score}%",
    )

    st.caption(
        score_status(profile_score)
    )

with c2:

    st.metric(
        "Resume Completeness",
        f"{resume_score}%",
    )

    st.caption(
        score_status(resume_score)
    )

with c3:

    if ats_score is not None:

        st.metric(
            "ATS Score",
            f"{ats_score:.0f}/100",
        )

        st.caption(
            score_status(ats_score)
        )

    else:

        st.metric(
            "ATS Score",
            "Not Available",
        )

        st.caption(
            "Analyze your resume first"
        )

with c4:

    if interview_score is not None:

        st.metric(
            "Interview Score",
            f"{interview_score:.0f}/100",
        )

        st.caption(
            score_status(
                interview_score
            )
        )

    else:

        st.metric(
            "Interview Score",
            "Not Available",
        )

        st.caption(
            "Complete a mock interview"
        )


# ============================================================
# SKILL GAP
# ============================================================

st.subheader("🧩 Skill Gap Evaluation")

gap_list = safe_list(
    skill_gaps
)

if gap_list:

    st.success(
        f"CareerPilot identified "
        f"{len(gap_list)} potential skill gaps."
    )

    cols = st.columns(3)

    for index, gap in enumerate(
        gap_list
    ):

        with cols[index % 3]:

            st.markdown(
                f"""
                <div style="
                    padding:12px;
                    margin:5px 0;
                    border-radius:10px;
                    border:1px solid #ddd;
                    background:#fafafa;
                ">
                    🔹 <b>{safe_text(gap)}</b>
                </div>
                """,
                unsafe_allow_html=True,
            )

else:

    st.info(
        "Upload a resume or complete your "
        "career profile to generate skill-gap analysis."
    )


# ============================================================
# PROFILE INFORMATION
# ============================================================

st.subheader("📋 Profile Evaluation")

if isinstance(profile, dict) and profile:

    profile_columns = st.columns(2)

    with profile_columns[0]:

        branch = profile.get(
            "branch",
            "Not provided",
        )

        year = profile.get(
            "year",
            "Not provided",
        )

        experience = profile.get(
            "experience_level",
            "Not provided",
        )

        st.write(
            f"**Engineering Branch:** {branch}"
        )

        st.write(
            f"**Academic Year:** {year}"
        )

        st.write(
            f"**Experience Level:** {experience}"
        )

    with profile_columns[1]:

        skills = safe_list(
            profile.get(
                "skills",
                [],
            )
        )

        projects = safe_list(
            profile.get(
                "projects",
                [],
            )
        )

        st.write(
            f"**Skills:** "
            f"{', '.join(map(str, skills))}"
            if skills
            else "**Skills:** Not provided"
        )

        st.write(
            f"**Projects:** "
            f"{', '.join(map(str, projects))}"
            if projects
            else "**Projects:** Not provided"
        )

else:

    st.warning(
        "No candidate profile found. "
        "Complete the Career Profile page first."
    )


# ============================================================
# RESUME STATUS
# ============================================================

st.subheader("📄 Resume Evaluation")

if resume_text:

    st.success(
        "✅ Resume uploaded and available "
        "for AI analysis."
    )

    st.write(
        f"Resume text extracted: "
        f"**{len(resume_text):,} characters**"
    )

    if isinstance(resume_data, dict):

        extracted_skills = safe_list(
            resume_data.get(
                "skills",
                [],
            )
        )

        if extracted_skills:

            st.write(
                "**Detected Skills:**"
            )

            st.write(
                ", ".join(
                    map(
                        str,
                        extracted_skills,
                    )
                )
            )

else:

    st.info(
        "📄 No resume uploaded yet."
    )


# ============================================================
# RECOMMENDATIONS
# ============================================================

st.subheader("💡 Personalized Improvements")

improvements = []

if profile_score < 70:

    improvements.append(
        "Complete more fields in your Career Profile."
    )

if resume_score < 70:

    improvements.append(
        "Upload a complete resume with projects, "
        "skills and experience."
    )

if not gap_list:

    improvements.append(
        "Run Skill Gap Analysis to identify "
        "missing skills for your target role."
    )

if ats_score is None:

    improvements.append(
        "Run the ATS Resume Scanner to evaluate "
        "resume compatibility."
    )

elif ats_score < 70:

    improvements.append(
        "Optimize your resume to improve its ATS score."
    )

if interview_score is None:

    improvements.append(
        "Complete a Mock Interview to measure "
        "your interview readiness."
    )

elif interview_score < 70:

    improvements.append(
        "Practice more mock interviews and review "
        "the AI feedback."
    )

if not career_interest:

    improvements.append(
        "Select a target career so CareerPilot can "
        "personalize your roadmap."
    )


if improvements:

    for item in improvements:

        st.warning(
            f"➡️ {item}"
        )

else:

    st.success(
        "🎉 Your CareerPilot profile is well prepared. "
        "Continue improving your skills and interview readiness."
    )


# ============================================================
# RESPONSIBLE AI
# ============================================================

st.divider()

st.subheader(
    "🛡️ Responsible AI Checklist"
)

st.caption(
    "These checks define how CareerPilot should "
    "use AI recommendations responsibly."
)

responsible_items = [
    (
        "No job or internship guarantees",
        True,
    ),
    (
        "No fabricated resume skills",
        True,
    ),
    (
        "Career recommendations are guidance, "
        "not official eligibility decisions",
        True,
    ),
    (
        "Recommendations should be grounded "
        "in available profile/resume data",
        True,
    ),
    (
        "Mock/anonymized student profiles only",
        True,
    ),
    (
        "User feedback should be captured",
        True,
    ),
    (
        "Recommendation quality should be evaluated",
        True,
    ),
    (
        "AI should disclose uncertainty when information "
        "is insufficient",
        True,
    ),
]

for item, default in responsible_items:

    st.checkbox(
        item,
        value=default,
        key=f"rai_{hash(item)}",
    )


# ============================================================
# EVALUATION METRICS
# ============================================================

st.subheader(
    "📈 System Evaluation Metrics"
)

c1, c2, c3 = st.columns(3)

with c1:

    if resume_text:

        grounding_score = 90

        st.metric(
            "Resume Grounding",
            f"{grounding_score}%",
        )

        st.caption(
            "Resume context available to AI"
        )

    else:

        st.metric(
            "Resume Grounding",
            "N/A",
        )

with c2:

    if career_interest:

        recommendation_score = min(
            95,
            profile_score + 10,
        )

        st.metric(
            "Recommendation Coverage",
            f"{recommendation_score}%",
        )

        st.caption(
            "Profile + target career available"
        )

    else:

        st.metric(
            "Recommendation Coverage",
            "N/A",
        )

with c3:

    if gap_list:

        gap_accuracy = min(
            95,
            50 + len(gap_list) * 5,
        )

        st.metric(
            "Skill Gap Coverage",
            f"{gap_accuracy}%",
        )

        st.caption(
            "Potential gaps identified"
        )

    else:

        st.metric(
            "Skill Gap Coverage",
            "N/A",
        )


# ============================================================
# DATA STATUS
# ============================================================

with st.expander(
    "🔍 Debug / Data Status"
):

    st.write(
        "Session state currently available:"
    )

    st.write(
        list(
            st.session_state.keys()
        )
    )

    st.write(
        "Profile:"
    )

    st.json(
        profile
        if isinstance(
            profile,
            dict,
        )
        else {}
    )

    st.write(
        "Resume data:"
    )

    st.json(
        resume_data
        if isinstance(
            resume_data,
            dict,
        )
        else {}
    )

    st.write(
        "Skill gaps:"
    )

    st.write(
        gap_list
    )

