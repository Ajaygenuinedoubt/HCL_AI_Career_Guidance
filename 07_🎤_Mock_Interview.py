
import streamlit as st
import sys
from pathlib import Path

# ============================================================
# PATH
# ============================================================

sys.path.append(
    str(
        Path(__file__).resolve().parents[1]
    )
)

from services.interview.question_generator import (
    generate_question,
)

from services.interview.answer_evaluator import (
    evaluate_answer,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Mock Interview | CareerPilot AI",
    page_icon="🎤",
    layout="wide",
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "interview_started": False,
    "question_number": 1,
    "current_question": None,
    "current_answer": "",
    "answer_submitted": False,
    "evaluation": None,
    "previous_questions": [],
    "interview_score": 0,
    "questions_answered": 0,
    "selected_role": "AI Engineer",
    "difficulty": "Medium",
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HEADER
# ============================================================

st.title("🎤 AI Mock Interview")

st.write(
    "Practice realistic role-specific interviews "
    "powered by Groq AI."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Interview Setup")

    role = st.selectbox(
        "Select Target Role",
        [
            "AI Engineer",
            "ML Engineer",
            "Data Scientist",
            "Data Analyst",
            "Software Engineer",
            "Python Developer",
            "Data Engineer",
            "Backend Developer",
        ],
        key="selected_role",
    )

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Easy",
            "Medium",
            "Hard",
            "Mixed",
        ],
        key="difficulty",
    )

    st.divider()

    st.caption(
        "Questions are generated dynamically "
        "for the selected role."
    )


# ============================================================
# USER CONTEXT
# ============================================================

profile = st.session_state.get(
    "profile",
    {},
)

resume_text = st.session_state.get(
    "resume_text",
    "",
)


# ============================================================
# START INTERVIEW
# ============================================================

if not st.session_state.interview_started:

    st.subheader(
        "🚀 Ready for your interview?"
    )

    st.info(
        """
        **How it works**

        1. Select your target role.
        2. Start the interview.
        3. AI generates a random role-specific question.
        4. Submit your answer.
        5. AI evaluates your answer.
        6. See your score and best answer.
        7. Continue to the next question.
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Questions",
            "Dynamic",
        )

    with col2:
        st.metric(
            "AI Evaluation",
            "100 Points",
        )

    with col3:
        st.metric(
            "Difficulty",
            difficulty,
        )

    if st.button(
        "🚀 Start Interview",
        type="primary",
        use_container_width=True,
    ):

        st.session_state.interview_started = True

        st.session_state.question_number = 1

        st.session_state.current_question = None

        st.session_state.current_answer = ""

        st.session_state.answer_submitted = False

        st.session_state.evaluation = None

        st.session_state.previous_questions = []

        st.session_state.interview_score = 0

        st.session_state.questions_answered = 0

        st.rerun()


# ============================================================
# INTERVIEW
# ============================================================

if st.session_state.interview_started:

    # --------------------------------------------------------
    # TOP INFORMATION
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Role",
            role,
        )

    with col2:
        st.metric(
            "Question",
            st.session_state.question_number,
        )

    with col3:
        st.metric(
            "Answered",
            st.session_state.questions_answered,
        )

    with col4:

        if st.session_state.questions_answered:

            average = (
                st.session_state.interview_score
                /
                st.session_state.questions_answered
            )

            st.metric(
                "Average Score",
                f"{average:.0f}/100",
            )

        else:

            st.metric(
                "Average Score",
                "0/100",
            )

    st.divider()

    # --------------------------------------------------------
    # GENERATE QUESTION
    # --------------------------------------------------------

    if (
        st.session_state.current_question
        is None
    ):

        effective_difficulty = difficulty

        if difficulty == "Mixed":

            import random

            effective_difficulty = random.choice(
                [
                    "Easy",
                    "Medium",
                    "Hard",
                ]
            )

        with st.spinner(
            "🤖 Generating a new interview question..."
        ):

            question_data = generate_question(

                role=role,

                question_number=(
                    st.session_state.question_number
                ),

                difficulty=effective_difficulty,

                previous_questions=(
                    st.session_state.previous_questions
                ),

                profile=profile,

                resume_text=resume_text,
            )

        if question_data.get("error"):

            st.error(
                question_data["error"]
            )

            st.stop()

        st.session_state.current_question = (
            question_data
        )

        st.session_state.answer_submitted = False

        st.session_state.evaluation = None

        st.session_state.current_answer = ""

        st.rerun()

    # --------------------------------------------------------
    # CURRENT QUESTION
    # --------------------------------------------------------

    question_data = (
        st.session_state.current_question
    )

    question = question_data.get(
        "question",
        "",
    )

    category = question_data.get(
        "category",
        "Technical",
    )

    topic = question_data.get(
        "topic",
        "",
    )

    question_difficulty = question_data.get(
        "difficulty",
        difficulty,
    )

    st.markdown(
        f"### Question {st.session_state.question_number}"
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.caption(
            f"📚 Category: **{category}**"
        )

    with c2:
        st.caption(
            f"🎯 Topic: **{topic}**"
        )

    with c3:
        st.caption(
            f"🔥 Difficulty: **{question_difficulty}**"
        )

    st.info(
        question
    )

    # --------------------------------------------------------
    # ANSWER
    # --------------------------------------------------------

    if not st.session_state.answer_submitted:

        answer = st.text_area(
            "✍️ Your Answer",
            height=220,
            placeholder=(
                "Explain your answer as if "
                "you are speaking to an interviewer..."
            ),
            key="answer_input",
        )

        if st.button(
            "✅ Submit Answer",
            type="primary",
            use_container_width=True,
        ):

            if not answer.strip():

                st.warning(
                    "Please enter your answer."
                )

            else:

                with st.spinner(
                    "🤖 AI is evaluating your answer..."
                ):

                    result = evaluate_answer(

                        question=question,

                        answer=answer,

                        role=role,

                        category=category,

                        expected_points=(
                            question_data.get(
                                "expected_points",
                                [],
                            )
                        ),
                    )

                if result.get("error"):

                    st.error(
                        result["error"]
                    )

                else:

                    st.session_state.current_answer = (
                        answer
                    )

                    st.session_state.evaluation = (
                        result
                    )

                    st.session_state.answer_submitted = (
                        True
                    )

                    st.session_state.questions_answered += 1

                    st.session_state.interview_score += (
                        result.get(
                            "score",
                            0,
                        )
                    )

                    # Store question so next one
                    # won't repeat it.
                    st.session_state.previous_questions.append(
                        question
                    )

                    st.rerun()

    # --------------------------------------------------------
    # EVALUATION
    # --------------------------------------------------------

    if st.session_state.answer_submitted:

        result = (
            st.session_state.evaluation
        )

        st.divider()

        st.subheader(
            "📊 AI Evaluation"
        )

        score = result.get(
            "score",
            0,
        )

        rating = result.get(
            "rating",
            "Needs Improvement",
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Answer Score",
                f"{score}/100",
            )

        with col2:

            st.metric(
                "Rating",
                rating,
            )

        # ----------------------------------------------------
        # FEEDBACK
        # ----------------------------------------------------

        st.markdown(
            "### 💬 Interviewer Feedback"
        )

        st.write(
            result.get(
                "feedback",
                "",
            )
        )

        # ----------------------------------------------------
        # STRENGTHS
        # ----------------------------------------------------

        strengths = result.get(
            "strengths",
            [],
        )

        if strengths:

            st.markdown(
                "### ✅ What You Did Well"
            )

            for item in strengths:

                st.success(
                    str(item)
                )

        # ----------------------------------------------------
        # MISSING POINTS
        # ----------------------------------------------------

        missing_points = result.get(
            "missing_points",
            [],
        )

        if missing_points:

            st.markdown(
                "### ⚠️ Missing Points"
            )

            for item in missing_points:

                st.warning(
                    str(item)
                )

        # ----------------------------------------------------
        # IMPROVEMENTS
        # ----------------------------------------------------

        improvements = result.get(
            "improvements",
            [],
        )

        if improvements:

            st.markdown(
                "### 🛠️ How to Improve"
            )

            for item in improvements:

                st.info(
                    str(item)
                )

        # ----------------------------------------------------
        # BEST ANSWER
        # ----------------------------------------------------

        best_answer = result.get(
            "best_answer",
            "",
        )

        if best_answer:

            with st.expander(
                "💡 See a Strong Interview Answer",
                expanded=True,
            ):

                st.write(
                    best_answer
                )

        st.divider()

        # ----------------------------------------------------
        # NEXT QUESTION
        # ----------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "➡️ Next Question",
                type="primary",
                use_container_width=True,
            ):

                st.session_state.question_number += 1

                st.session_state.current_question = None

                st.session_state.current_answer = ""

                st.session_state.answer_submitted = False

                st.session_state.evaluation = None

                st.rerun()

        with col2:

            if st.button(
                "🛑 End Interview",
                use_container_width=True,
            ):

                st.session_state.interview_started = False

                st.session_state.current_question = None

                st.session_state.evaluation = None

                st.rerun()

