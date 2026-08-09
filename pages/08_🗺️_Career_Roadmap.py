
import streamlit as st
import sys

from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(
    __file__
).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:

    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )


# ============================================================
# SERVICE
# ============================================================

from services.roadmap_generator import (
    generate_roadmap
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Career Roadmap | CareerPilot AI",
    page_icon="🗺️",
    layout="wide",
)


# ============================================================
# HEADER
# ============================================================

st.title(
    "🗺️ Personalized Career Roadmap"
)

st.write(
    """
    Build a personalized learning journey based on
    your target career, current skills, resume,
    skill gaps and available learning time.
    """
)


# ============================================================
# USER PROFILE
# ============================================================

profile = st.session_state.get(
    "profile",
    {}
)

resume_text = st.session_state.get(
    "resume_text",
    ""
)

resume_data = st.session_state.get(
    "resume_data",
    {}
)

skill_gaps = st.session_state.get(
    "skill_gap",
    []
)


# ============================================================
# CAREER OPTIONS
# ============================================================

career_options = [
    "AI Engineer",
    "Machine Learning Engineer",
    "Data Scientist",
    "Data Analyst",
    "Software Engineer",
    "Python Developer",
    "Backend Developer",
    "Frontend Developer",
    "Full Stack Developer",
    "Cloud Engineer",
    "DevOps Engineer",
    "Data Engineer",
    "Cybersecurity Analyst",
    "Business Analyst",
]


# ============================================================
# EXISTING PROFILE CAREER
# ============================================================

profile_interest = profile.get(
    "career_interest",
    profile.get(
        "target_role",
        "",
    ),
)


default_index = 0

if profile_interest:

    for i, career in enumerate(
        career_options
    ):

        if career.lower() == str(
            profile_interest
        ).lower():

            default_index = i
            break


# ============================================================
# TARGET CAREER
# ============================================================

career_interest = st.selectbox(
    "🎯 What career do you want to pursue?",
    career_options,
    index=default_index,
)


# ============================================================
# CUSTOM CAREER
# ============================================================

custom_career = st.text_input(
    "Or enter another career",
    placeholder=(
        "Example: Generative AI Engineer"
    ),
)

if custom_career.strip():

    career_interest = custom_career.strip()


# ============================================================
# PROFILE PREVIEW
# ============================================================

with st.expander(
    "👤 View information used for personalization"
):

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "**Branch:**",
            profile.get(
                "branch",
                "Not provided",
            ),
        )

        st.write(
            "**Year:**",
            profile.get(
                "year",
                "Not provided",
            ),
        )

        st.write(
            "**Experience:**",
            profile.get(
                "experience_level",
                "Not provided",
            ),
        )

    with col2:

        st.write(
            "**Current Skills:**"
        )

        current_skills = profile.get(
            "skills",
            resume_data.get(
                "skills",
                [],
            ),
        )

        if isinstance(
            current_skills,
            list,
        ):

            st.write(
                ", ".join(
                    map(
                        str,
                        current_skills
                    )
                )
            )

        else:

            st.write(
                current_skills
            )

        st.write(
            "**Skill Gaps:**"
        )

        if skill_gaps:

            st.write(
                ", ".join(
                    map(
                        str,
                        skill_gaps[:15]
                    )
                )
            )

        else:

            st.write(
                "No skill gaps available."
            )


# ============================================================
# LEARNING SETTINGS
# ============================================================

st.markdown(
    "### ⚙️ Learning Preferences"
)

col1, col2 = st.columns(2)

with col1:

    hours = st.slider(
        "⏱️ Hours available per week",
        min_value=3,
        max_value=30,
        value=10,
        step=1,
    )


with col2:

    duration = st.selectbox(
        "📅 Roadmap duration",
        [4, 8, 12, 16, 24],
        index=2,
        format_func=lambda x:
            f"{x} weeks",
    )


# ============================================================
# GENERATE
# ============================================================

st.divider()

if st.button(
    "🚀 Generate My Personalized Roadmap",
    type="primary",
    use_container_width=True,
):

    if not career_interest:

        st.warning(
            "Please select a career first."
        )

    else:

        with st.spinner(
            "🤖 CareerPilot AI is analyzing your profile..."
        ):

            result = generate_roadmap(
                career_interest=career_interest,
                profile=profile,
                resume_text=resume_text,
                skill_gaps=skill_gaps,
                hours_per_week=hours,
                duration_weeks=duration,
            )


        if result["error"]:

            st.error(
                result["error"]
            )

        else:

            st.session_state[
                "generated_roadmap"
            ] = result["roadmap"]

            st.session_state[
                "roadmap_career"
            ] = career_interest

            st.success(
                "🎉 Your personalized roadmap is ready!"
            )


# ============================================================
# DISPLAY ROADMAP
# ============================================================

roadmap = st.session_state.get(
    "generated_roadmap",
    []
)

if roadmap:

    roadmap_career = st.session_state.get(
        "roadmap_career",
        career_interest,
    )

    st.divider()

    st.markdown(
        f"## 🎯 Your {roadmap_career} Journey"
    )

    total_hours = sum(
        int(item.get("hours", 0))
        for item in roadmap
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Roadmap Duration",
            f"{len(roadmap)} weeks",
        )

    with col2:

        st.metric(
            "Total Learning",
            f"{total_hours} hours",
        )

    with col3:

        st.metric(
            "Target Career",
            roadmap_career,
        )


    # ========================================================
    # WEEKLY ROADMAP
    # ========================================================

    for item in roadmap:

        week = item.get(
            "week",
            "?",
        )

        phase = item.get(
            "phase",
            "Learning",
        )

        title = item.get(
            "title",
            "Career Development",
        )

        skill = item.get(
            "skill",
            "",
        )

        objective = item.get(
            "objective",
            "",
        )

        topics = item.get(
            "topics",
            [],
        )

        tasks = item.get(
            "tasks",
            [],
        )

        project = item.get(
            "project",
            "None",
        )

        deliverable = item.get(
            "deliverable",
            "",
        )

        week_hours = item.get(
            "hours",
            0,
        )

        resources = item.get(
            "resources",
            [],
        )

        interview = item.get(
            "interview_prep",
            "",
        )

        checkpoint = item.get(
            "checkpoint",
            "",
        )


        with st.container(
            border=True
        ):

            st.markdown(
                f"### Week {week}: {title}"
            )

            st.caption(
                f"🎯 {phase}  •  "
                f"⏱️ {week_hours} hours  •  "
                f"🧠 Focus: {skill}"
            )

            if objective:

                st.write(
                    f"**Objective:** {objective}"
                )


            # ------------------------------------------------
            # Topics
            # ------------------------------------------------

            if topics:

                st.markdown(
                    "**📚 Topics to Learn**"
                )

                for topic in topics:

                    st.write(
                        f"• {topic}"
                    )


            # ------------------------------------------------
            # Tasks
            # ------------------------------------------------

            if tasks:

                st.markdown(
                    "**⚡ Action Plan**"
                )

                for task in tasks:

                    st.write(
                        f"☐ {task}"
                    )


            # ------------------------------------------------
            # Project
            # ------------------------------------------------

            if project and project.lower() != "none":

                st.markdown(
                    "**🛠️ Practical Project**"
                )

                st.info(
                    project
                )


            # ------------------------------------------------
            # Deliverable
            # ------------------------------------------------

            if deliverable:

                st.markdown(
                    "**📦 Weekly Deliverable**"
                )

                st.success(
                    deliverable
                )


            # ------------------------------------------------
            # Resources
            # ------------------------------------------------

            if resources:

                st.markdown(
                    "**🔗 Suggested Resources**"
                )

                for resource in resources:

                    st.write(
                        f"• {resource}"
                    )


            # ------------------------------------------------
            # Interview
            # ------------------------------------------------

            if interview:

                st.markdown(
                    "**🎤 Interview Preparation**"
                )

                st.write(
                    interview
                )


            # ------------------------------------------------
            # Checkpoint
            # ------------------------------------------------

            if checkpoint:

                st.markdown(
                    "**✅ Progress Checkpoint**"
                )

                st.write(
                    checkpoint
                )


# ============================================================
# NO ROADMAP
# ============================================================

else:

    st.info(
        """
        👆 Select your target career and click
        **Generate My Personalized Roadmap**.

        CareerPilot will consider your profile,
        resume, existing skills, skill gaps and
        available time before creating the roadmap.
        """
    )

