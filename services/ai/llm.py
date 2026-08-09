import os
from typing import Optional

from dotenv import load_dotenv
from sarvamai import SarvamAI


load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "").strip()

# IMPORTANT
# Your API is rejecting sarvam-30b.
MODEL = "sarvam-105b"

_client: Optional[SarvamAI] = None


def get_client() -> SarvamAI:
    global _client

    if not SARVAM_API_KEY:
        raise RuntimeError(
            "SARVAM_API_KEY is missing from .env"
        )

    if _client is None:
        _client = SarvamAI(
            api_subscription_key=SARVAM_API_KEY
        )

    return _client


def detect_language(text: str) -> str:

    if not text or not text.strip():
        return "en-IN"

    try:
        client = get_client()

        response = client.text.identify_language(
            input=text.strip()[:1000]
        )

        language_code = getattr(
            response,
            "language_code",
            None
        )

        return language_code or "en-IN"

    except Exception as exc:
        print(f"Language detection error: {exc}")
        return "en-IN"


def generate(
    prompt: str,
    language_code: Optional[str] = None,
) -> str:

    if not prompt or not prompt.strip():
        return "Please provide a question."

    try:

        client = get_client()

        if not language_code:
            language_code = detect_language(prompt)

        system_prompt = f"""
You are CareerPilot AI.

You are a career guidance assistant for
Tier-2 and Tier-3 engineering students.

USER LANGUAGE:
{language_code}

LANGUAGE RULES:

1. Reply in the same language as the user.
2. If the user speaks Hindi, respond in Hindi.
3. If the user speaks Hinglish, respond naturally in Hinglish.
4. If the user speaks Tamil, respond in Tamil.
5. If the user speaks Telugu, respond in Telugu.
6. If the user speaks Kannada, respond in Kannada.
7. If the user speaks English, respond in English.
8. Preserve natural code-mixing.
9. Do not unnecessarily translate technical terms.

CAREER RULES:

- Personalize advice using the user's profile.
- Use resume information when available.
- Identify missing skills.
- Explain why a role is recommended.
- Suggest realistic projects.
- Suggest learning paths.
- Give approximate learning timelines.
- Suggest alternative roles if appropriate.
- Never guarantee a job.
- Never guarantee an internship.
- Never guarantee salary or placement.
- Never invent user experience or skills.

STYLE:

Be practical, friendly, concise and actionable.
"""

        response = client.chat.completions(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
            reasoning_effort=None,
            max_tokens=2000,
        )

        if not response:
            return "Sarvam did not return a response."

        if not response.choices:
            return "Sarvam returned no response choices."

        answer = response.choices[0].message.content

        if not answer:
            return "Sarvam returned an empty response."

        return answer.strip()

    except Exception as exc:

        print(
            "SARVAM CHAT ERROR:",
            repr(exc)
        )

        return (
            "AI service error.\n\n"
            f"Details: {exc}"
        )
