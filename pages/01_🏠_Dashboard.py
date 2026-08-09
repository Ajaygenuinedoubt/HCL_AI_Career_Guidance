import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CareerPilot AI | Dashboard",
    page_icon="🚀",
    layout="wide",
)

# ============================================================
# SESSION STATE
# ============================================================

if "profile" not in st.session_state:
    st.session_state.profile = {}

if "resume_data" not in st.session_state:
    st.session_state.resume_data = {}

if "skill_gap" not in st.session_state:
    st.session_state.skill_gap = []

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .dashboard-title {
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .dashboard-subtitle {
        color: #94a3b8;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .metric-card {
        padding: 20px;
        border-radius: 16px;
        background: linear-gradient(
            135deg,
            rgba(30,41,59,0.95),
            rgba(15,23,42,0.95)
        );
        border: 1px solid rgba(148,163,184,0.15);
        min-height: 130px;
    }

    .metric-title {
        color: #94a3b8;
        font-size: 14px;
        font-weight: 600;
    }

    .metric-value {
        font-size: 30px;
        font-weight: 800;
        margin-top: 8px;
    }

    .metric-desc {
        color: #64748b;
        font-size: 12px;
        margin-top: 5px;
    }

    .role-card {
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(148,163,184,0.15);
        background: rgba(15,23,42,0.8);
        margin-bottom: 12px;
    }

    .role-name {
        font-size: 21px;
        font-weight: 750;
    }

    .role-level {
        color: #94a3b8;
        font-size: 13px;
    }

    .skill-pill {
        display: inline-block;
        padding: 6px 10px;
        margin: 3px;
        border-radius: 20px;
        background: rgba(59,130,246,0.12);
        color: #60a5fa;
        font-size: 12px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 750;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .action-card {
        padding: 16px;
        border-radius: 14px;
        background: rgba(30,41,59,0.65);
        border-left: 4px solid #6366f1;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HEADER
# ============================================================

profile = st.session_state.get("profile", {})
resume_data = st.session_state.get("resume_data", {})
skill_gap = st.session_state.get("skill_gap", [])

st.markdown(
    '<div class="dashboard-title">🚀 Career Intelligence Dashboard</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="dashboard-subtitle">
    Your personalized career readiness, skill intelligence and next-step recommendations.
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# PROFILE EXTRACTION
# ============================================================

branch = str(
    profile.get("branch", "Not specified")
)

year = str(
    profile.get("year", "Not specified")
)

career_interest = str(
    profile.get(
        "career_interest",
        profile.get(
            "target_role",
            "AI Engineer"
        )
    )
)

profile_skills = profile.get("skills", [])

resume_skills = resume_data.get("skills", [])

# Make sure skills are lists

if not isinstance(profile_skills, list):
    profile_skills = []

if not isinstance(resume_skills, list):
    resume_skills = []

# Combine skills

all_skills = list(
    dict.fromkeys(
        [
            str(skill).strip()
            for skill in profile_skills + resume_skills
            if str(skill).strip()
        ]
    )
)

# ============================================================
# CAREER ROLE DATABASE
# ============================================================

ROLE_DATABASE = {

    "AI Engineer": {
        "level": "Intermediate → Advanced",
        "skills": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "LLM",
            "RAG",
            "APIs",
            "SQL",
            "Git",
        ],
    },

    "ML Engineer": {
        "level": "Intermediate → Advanced",
        "skills": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "Scikit-learn",
            "Pandas",
            "SQL",
            "Docker",
            "Git",
        ],
    },

    "Data Scientist": {
        "level": "Intermediate",
        "skills": [
            "Python",
            "Statistics",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "SQL",
            "Data Visualization",
        ],
    },

    "Data Analyst": {
        "level": "Beginner → Intermediate",
        "skills": [
            "SQL",
            "Excel",
            "Power BI",
            "Python",
            "Pandas",
            "Statistics",
            "Data Visualization",
        ],
    },

    "Software Engineer": {
        "level": "Beginner → Advanced",
        "skills": [
            "Python",
            "Java",
            "C++",
            "Data Structures",
            "Algorithms",
            "SQL",
            "Git",
            "APIs",
        ],
    },

    "AI/ML Analyst": {
        "level": "Beginner → Intermediate",
        "skills": [
            "Python",
            "SQL",
            "Machine Learning",
            "Statistics",
            "Pandas",
            "Data Visualization",
            "LLM",
        ],
    },

    "Cloud Data Engineer": {
        "level": "Intermediate",
        "skills": [
            "Python",
            "SQL",
            "ETL",
            "Cloud",
            "Azure",
            "AWS",
            "Databricks",
            "Git",
        ],
    },

    "Generative AI Engineer": {
        "level": "Intermediate → Advanced",
        "skills": [
            "Python",
            "LLM",
            "RAG",
            "LangChain",
            "Embeddings",
            "Vector Database",
            "APIs",
            "Git",
        ],
    },
}

# ============================================================
# SKILL NORMALIZATION
# ============================================================

def normalize_skill(skill):

    return (
        str(skill)
        .lower()
        .strip()
        .replace("-", " ")
        .replace("_", " ")
    )


normalized_user_skills = {
    normalize_skill(skill)
    for skill in all_skills
}

# ============================================================
# ROLE RECOMMENDATION ENGINE
# ============================================================

recommendations = []

for role, data in ROLE_DATABASE.items():

    required_skills = data["skills"]

    matched = []

    missing = []

    for skill in required_skills:

        if normalize_skill(skill) in normalized_user_skills:

            matched.append(skill)

        else:

            missing.append(skill)

    fit_score = int(
        (len(matched) / len(required_skills)) * 100
    )

    # Career interest bonus

    interest_bonus = 0

    if career_interest:

        interest_words = set(
            normalize_skill(career_interest).split()
        )

        role_words = set(
            normalize_skill(role).split()
        )

        if interest_words.intersection(role_words):

            interest_bonus = 10

    final_score = min(
        100,
        fit_score + interest_bonus
    )

    recommendations.append(
        {
            "role": role,
            "score": final_score,
            "matched": matched,
            "missing": missing,
            "level": data["level"],
        }
    )

# Sort highest first

recommendations.sort(
    key=lambda x: x["score"],
    reverse=True
)

# ============================================================
# TOP RECOMMENDATION
# ============================================================

top_role = recommendations[0]

# ============================================================
# CALCULATE DASHBOARD METRICS
# ============================================================

career_fit = top_role["score"]

skill_readiness = int(
    min(
        100,
        (
            len(all_skills)
            /
            max(
                len(ROLE_DATABASE[top_role["role"]]["skills"]),
                1
            )
        )
        * 100
    )
)

# ATS score from Resume AI if available

ats_score = resume_data.get(
    "ats_score",
    resume_data.get(
        "score",
        None
    )
)

if ats_score is None:
    ats_score = 0

try:
    ats_score = int(float(ats_score))
except:
    ats_score = 0

# Readiness combines career + skills + ATS

if ats_score > 0:

    readiness = int(
        (
            career_fit
            +
            skill_readiness
            +
            ats_score
        ) / 3
    )

else:

    readiness = int(
        (
            career_fit
            +
            skill_readiness
        ) / 2
    )

# ============================================================
# METRIC CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">
                🎯 TOP CAREER FIT
            </div>
            <div class="metric-value">
                {career_fit}%
            </div>
            <div class="metric-desc">
                {top_role["role"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">
                🧠 SKILL READINESS
            </div>
            <div class="metric-value">
                {skill_readiness}%
            </div>
            <div class="metric-desc">
                Based on current skills
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">
                📄 ATS SCORE
            </div>
            <div class="metric-value">
                {ats_score}%
            </div>
            <div class="metric-desc">
                Resume compatibility
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c4:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">
                🚀 READINESS
            </div>
            <div class="metric-value">
                {readiness}%
            </div>
            <div class="metric-desc">
                Overall career readiness
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# CAREER RECOMMENDATION
# ============================================================

st.markdown(
    '<div class="section-title">🎯 AI Career Recommendations</div>',
    unsafe_allow_html=True,
)

st.caption(
    "Recommendations are based on the skills available in your profile/resume and are indicative, not job guarantees."
)

# ============================================================
# TOP 5 ROLES
# ============================================================

for index, item in enumerate(
    recommendations[:5]
):

    role = item["role"]

    score = item["score"]

    matched = item["matched"]

    missing = item["missing"]

    level = item["level"]

    col1, col2 = st.columns(
        [4, 1]
    )

    with col1:

        st.markdown(
            f"""
            <div class="role-card">

            <div class="role-name">
                {index + 1}. {role}
            </div>

            <div class="role-level">
                Recommended level: {level}
            </div>

            <br>

            <b>Career Fit</b>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.progress(
            score / 100
        )

        m1, m2 = st.columns(2)

        with m1:

            st.success(
                f"✓ Matching skills: {len(matched)}"
            )

        with m2:

            st.warning(
                f"⚠ Missing skills: {len(missing)}"
            )

        if matched:

            st.write(
                "**Your matching skills:**"
            )

            st.markdown(
                " ".join(
                    [
                        f"`{skill}`"
                        for skill in matched
                    ]
                )
            )

        if missing:

            st.write(
                "**Skills to develop:**"
            )

            st.markdown(
                " ".join(
                    [
                        f"`{skill}`"
                        for skill in missing[:6]
                    ]
                )
            )

    with col2:

        st.metric(
            "Fit",
            f"{score}%"
        )

# ============================================================
# SKILL INTELLIGENCE
# ============================================================

st.markdown(
    '<div class="section-title">🧠 Skill Intelligence</div>',
    unsafe_allow_html=True,
)

if all_skills:

    # Create approximate proficiency levels.
    # Replace this later with actual skill levels
    # from the profile form.

    skill_levels = []

    for skill in all_skills[:15]:

        skill_levels.append(
            {
                "Skill": skill,
                "Level": np.random.randint(
                    45,
                    91
                ),
            }
        )

    skill_df = pd.DataFrame(
        skill_levels
    )

    st.bar_chart(
        skill_df.set_index("Skill")
    )

else:

    st.info(
        "No skills found yet. Complete your Career Profile or upload a resume."
    )

# ============================================================
# SKILL GAP
# ============================================================

st.markdown(
    '<div class="section-title">🧩 Priority Skill Gaps</div>',
    unsafe_allow_html=True,
)

priority_gaps = top_role["missing"]

if priority_gaps:

    gap_cols = st.columns(
        min(
            len(priority_gaps[:6]),
            3
        )
    )

    for i, skill in enumerate(
        priority_gaps[:6]
    ):

        with gap_cols[
            i % len(gap_cols)
        ]:

            st.warning(
                f"⚠️ {skill}"
            )

else:

    st.success(
        "🎉 Your current skills strongly match the selected career path."
    )

# ============================================================
# PERSONALIZED NEXT STEPS
# ============================================================

st.markdown(
    '<div class="section-title">🚀 Your Next Best Actions</div>',
    unsafe_allow_html=True,
)

actions = []

if not profile:

    actions.append(
        "Complete your Career Profile to improve personalization."
    )

if not resume_data:

    actions.append(
        "Upload your resume to calculate ATS score and perform resume-based skill analysis."
    )

if priority_gaps:

    actions.append(
        f"Start learning **{priority_gaps[0]}** because it is one of the key gaps for {top_role['role']}."
    )

if ats_score < 70:

    actions.append(
        "Optimize your resume for ATS keywords, measurable achievements and role-specific skills."
    )

if career_fit < 60:

    actions.append(
        f"Your current profile has a significant gap for {top_role['role']}. Consider the bridge skills before targeting advanced roles."
    )

actions.append(
    f"Build a practical project aligned with **{top_role['role']}** and add it to your portfolio."
)

actions.append(
    "Take a mock interview to measure your technical and communication readiness."
)

for i, action in enumerate(
    actions[:6]
):

    st.markdown(
        f"""
        <div class="action-card">
            <b>Step {i + 1}</b><br>
            {action}
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# CAREER JOURNEY
# ============================================================

st.markdown(
    '<div class="section-title">🗺️ Career Journey</div>',
    unsafe_allow_html=True,
)

journey = pd.DataFrame(
    {
        "Stage": [
            "Profile",
            "Resume",
            "Skills",
            "Projects",
            "Interview",
            "Ready",
        ],
        "Score": [
            100 if profile else 20,
            100 if resume_data else 20,
            skill_readiness,
            min(
                100,
                skill_readiness + 10
            ),
            40,
            readiness,
        ],
    }
)

st.line_chart(
    journey.set_index("Stage")
)

# ============================================================
# PROFILE SUMMARY
# ============================================================

st.markdown(
    '<div class="section-title">👤 Profile Snapshot</div>',
    unsafe_allow_html=True,
)

p1, p2, p3, p4 = st.columns(4)

p1.metric(
    "Branch",
    branch
)

p2.metric(
    "Academic Year",
    year
)

p3.metric(
    "Current Skills",
    len(all_skills)
)

p4.metric(
    "Recommended Role",
    top_role["role"]
)

# ============================================================
# DISCLAIMER
# ============================================================

st.divider()

st.caption(
    """
    ⚠️ CareerPilot AI provides guidance based on the information supplied by the user
    and prepared career/skill data. Recommendations are indicative and do not guarantee
    employment, internships, salary, selection or eligibility.
    """
)
