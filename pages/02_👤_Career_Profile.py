
import streamlit as st


st.title("👤 Career Profile")

st.markdown(
    """
    ### Build your Career With CareerPilot 🚀

    Tell CareerPilot about your education, skills, interests,
    preferences and goals. This information will be used across
    the career recommendation, skill-gap, roadmap and interview modules.
    """
)


# ---------------------------------------------------------
# IMPORTANT:
# Do NOT use key="profile" for any widget.
# "profile" is reserved for the final structured profile.
# ---------------------------------------------------------

with st.form("career_profile_form"):

    st.subheader("🎓 Education")

    name = st.text_input(
        "Full Name",
        key="profile_name",
        placeholder="Enter your name"
    )

    branch = st.selectbox(
        "Engineering Branch",
        [
            "Computer Science",
            "Artificial Intelligence",
            "Artificial Intelligence & Machine Learning",
            "Information Technology",
            "Electronics & Communication",
            "Electrical Engineering",
            "Mechanical Engineering",
            "Civil Engineering",
            "Other"
        ],
        key="profile_branch"
    )

    year = st.selectbox(
        "Current Year",
        [
            "1st Year",
            "2nd Year",
            "3rd Year",
            "4th Year",
            "Graduate"
        ],
        key="profile_year"
    )

    cgpa = st.number_input(
        "CGPA",
        min_value=0.0,
        max_value=10.0,
        value=7.0,
        step=0.1,
        key="profile_cgpa"
    )

    st.divider()

    st.subheader("💻 Technical Skills")

    skills_text = st.text_area(
        "Current Skills",
        placeholder=(
            "Python, SQL, Machine Learning, "
            "Power BI, React, Docker..."
        ),
        key="profile_skills"
    )

    project_experience = st.text_area(
        "Projects / Experience",
        placeholder=(
            "Describe your major projects, internships "
            "or practical experience..."
        ),
        key="profile_projects"
    )

    st.divider()

    st.subheader("🎯 Career Preferences")

    interests = st.multiselect(
        "Career Interests",
        [
            "AI / Machine Learning",
            "Data Science",
            "Data Analytics",
            "Software Development",
            "Data Engineering",
            "Cloud Computing",
            "Cybersecurity",
            "Generative AI",
            "DevOps",
            "Product / Business"
        ],
        key="profile_interests"
    )

    preferred_roles = st.multiselect(
        "Preferred Roles",
        [
            "AI Engineer",
            "ML Engineer",
            "Data Scientist",
            "Data Analyst",
            "Software Engineer",
            "Data Engineer",
            "Cloud Engineer",
            "GenAI Engineer"
        ],
        key="profile_roles"
    )

    preferred_location = st.text_input(
        "Preferred Work Location",
        placeholder="Gurugram, Bangalore, Hyderabad, Remote...",
        key="profile_location"
    )

    work_mode = st.selectbox(
        "Preferred Work Mode",
        [
            "Any",
            "On-site",
            "Hybrid",
            "Remote"
        ],
        key="profile_work_mode"
    )

    st.divider()

    st.subheader("📚 Learning Preferences")

    learning_hours = st.slider(
        "Available learning hours per day",
        min_value=1,
        max_value=10,
        value=2,
        key="profile_learning_hours"
    )

    language = st.selectbox(
        "Preferred Guidance Language",
        [
            "English",
            "Hinglish",
            "Hindi",
            "Tamil",
            "Kannada",
            "Telugu",
            "Bengali"
        ],
        key="profile_language"
    )

    career_goal = st.text_area(
        "What is your career goal?",
        placeholder=(
            "Example: I want to become an AI Engineer "
            "within the next 6 months."
        ),
        key="profile_goal"
    )

    submitted = st.form_submit_button(
        "🚀 Build My Career Profile",
        use_container_width=True
    )


# ---------------------------------------------------------
# SAVE PROFILE
# ---------------------------------------------------------

if submitted:

    parsed_skills = [
        skill.strip()
        for skill in skills_text.split(",")
        if skill.strip()
    ]

    profile = {
        "name": name,
        "branch": branch,
        "year": year,
        "cgpa": cgpa,

        "skills": parsed_skills,

        "projects": project_experience,

        "interests": interests,

        "preferred_roles": preferred_roles,

        "location": preferred_location,

        "work_mode": work_mode,

        "learning_hours": learning_hours,

        "language": language,

        "career_goal": career_goal
    }

    # Safe because no widget uses key="profile"
    st.session_state["profile"] = profile

    st.success(
        "🎉 Your Career Digital Twin has been created!"
    )

    st.balloons()


# ---------------------------------------------------------
# DISPLAY SAVED PROFILE
# ---------------------------------------------------------

profile = st.session_state.get(
    "profile"
)


if profile:

    st.divider()

    st.subheader("✅ Your Career Profile")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Branch",
            profile.get("branch", "—")
        )

    with col2:

        st.metric(
            "Year",
            profile.get("year", "—")
        )

    with col3:

        st.metric(
            "Learning Hours",
            f"{profile.get('learning_hours', 0)} hrs/day"
        )


    st.markdown("### 💻 Skills")

    if profile.get("skills"):

        st.write(
            " • ".join(
                skill.title()
                for skill in profile["skills"]
            )
        )

    else:

        st.info(
            "No technical skills added yet."
        )


    st.markdown("### 🎯 Career Interests")

    if profile.get("interests"):

        for interest in profile["interests"]:

            st.write(
                f"• {interest}"
            )

    else:

        st.info(
            "No career interests selected."
        )


    st.markdown("### 🗺️ Career Goal")

    st.write(
        profile.get(
            "career_goal",
            "No career goal provided."
        )
    )
