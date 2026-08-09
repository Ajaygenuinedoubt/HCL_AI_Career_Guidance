

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
# SERVICES
# ============================================================

from services.chatbot.chatbot import ask

from services.voice.speech_to_text import (
    transcribe_audio,
)

from services.voice.text_to_speech import (
    text_to_speech,
)


# ============================================================
# PAGE
# ============================================================

st.title("💬 Career Copilot")

st.caption(
    "Ask CareerPilot about your resume, skills, "
    "career path, roadmap, interviews or projects."
)


# ============================================================
# USER CONTEXT
# ============================================================

profile = st.session_state.get(
    "profile",
    {}
)

resume_text = st.session_state.get(
    "resume_text",
    ""
)


def build_context():

    return f"""
You are CareerPilot AI, a career guidance assistant.

Student Profile:
{profile}

Resume:
{resume_text[:12000]}

Use the student's profile and resume to provide
personalized career guidance.

Do not guarantee jobs, internships, salaries
or selection outcomes.
"""


# ============================================================
# TEXT CHAT
# ============================================================

st.subheader("💬 Ask by Text")

question = st.chat_input(
    "Ask your career question..."
)

if question:

    with st.chat_message(
        "user"
    ):

        st.write(question)

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "🤖 Thinking..."
        ):

            try:

                response = ask(
                    question,
                    build_context(),
                )

                st.write(response)

            except Exception as exc:

                response = ""

                st.error(
                    f"AI response error: {exc}"
                )


# ============================================================
# VOICE SECTION
# ============================================================

st.divider()

st.subheader(
    "🎙️ Ask CareerPilot by Voice"
)

st.caption(
    "Speak your question and CareerPilot will "
    "answer in the same language."
)


# ============================================================
# LANGUAGE
# ============================================================

language_options = {
    "🇮🇳 English": "en-IN",
    "🇮🇳 Hindi / Hinglish": "hi-IN",
    "🇮🇳 Odia": "od-IN",
    "🇮🇳 Bengali": "bn-IN",
    "🇮🇳 Tamil": "ta-IN",
    "🇮🇳 Telugu": "te-IN",
    "🇮🇳 Kannada": "kn-IN",
    "🇮🇳 Marathi": "mr-IN",
    "🇮🇳 Gujarati": "gu-IN",
    "🇮🇳 Punjabi": "pa-IN",
    "🇮🇳 Malayalam": "ml-IN",
}

selected_language = st.selectbox(
    "Select your spoken language",
    list(language_options.keys()),
)

language_code = language_options[
    selected_language
]


# ============================================================
# AUDIO INPUT
# ============================================================

audio_input = st.audio_input(
    "🎤 Click here and record your question"
)


# ============================================================
# PROCESS AUDIO
# ============================================================

if audio_input:

    # --------------------------------------------------------
    # Show recorded audio
    # --------------------------------------------------------

    st.audio(
        audio_input,
        format="audio/wav",
    )

    # --------------------------------------------------------
    # Process
    # --------------------------------------------------------

    with st.spinner(
        "🎧 Understanding your voice..."
    ):

        try:

            # IMPORTANT:
            # transcribe_audio() accepts UploadedFile
            # directly and converts it internally.

            transcript, detected_language = (
                transcribe_audio(
                    audio_input,
                    language_code,
                )
            )

        except Exception as exc:

            transcript = ""
            detected_language = language_code

            st.error(
                f"Voice processing error: {exc}"
            )

    # --------------------------------------------------------
    # Transcript
    # --------------------------------------------------------

    if transcript:

        st.success(
            f"🎙️ You said: {transcript}"
        )

        # ----------------------------------------------------
        # AI RESPONSE
        # ----------------------------------------------------

        with st.spinner(
            "🤖 Preparing your personalized answer..."
        ):

            try:

                response = ask(
                    transcript,
                    build_context(),
                )

                st.markdown(
                    "### 🤖 CareerPilot AI"
                )

                st.write(response)

            except Exception as exc:

                response = ""

                st.error(
                    f"AI response error: {exc}"
                )

        # ----------------------------------------------------
        # TEXT TO SPEECH
        # ----------------------------------------------------

        if response:

            with st.spinner(
                "🔊 Generating voice response..."
            ):

                try:

                    audio_response = text_to_speech(
                        response,
                        detected_language,
                    )

                    if audio_response:

                        st.audio(
                            audio_response,
                            format="audio/wav",
                        )

                    else:

                        st.warning(
                            "Sarvam did not return audio."
                        )

                except Exception as exc:

                    st.warning(
                        "Voice response unavailable: "
                        f"{exc}"
                    )

    else:

        st.warning(
            "I couldn't understand the audio. "
            "Please speak clearly and try again."
        )

