
import os
import json
import re

from dotenv import load_dotenv

load_dotenv()


def _clean_json(text: str) -> str:
    """
    Remove markdown code fences and extract JSON.
    """

    text = text.strip()

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"^```\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    # Try to extract JSON array
    start = text.find("[")

    end = text.rfind("]")

    if start != -1 and end != -1:

        text = text[start:end + 1]

    return text.strip()


def generate_roadmap(
    career_interest,
    profile=None,
    resume_text="",
    skill_gaps=None,
    hours_per_week=10,
    duration_weeks=12,
):
    """
    Generate a personalized career roadmap using Groq.

    The roadmap is personalized using:

    - Career interest
    - Engineering branch
    - Academic year
    - Current skills
    - Projects
    - Resume
    - Skill gaps
    - Weekly learning availability
    """

    api_key = os.getenv(
        "GROQ_API_KEY",
        "",
    ).strip()

    if not api_key:

        return {
            "error": (
                "GROQ_API_KEY is not configured. "
                "Add it to your .env file."
            ),
            "roadmap": [],
        }

    if not career_interest:

        return {
            "error": (
                "Please select your target career."
            ),
            "roadmap": [],
        }

    profile = profile or {}

    skill_gaps = skill_gaps or []

    # --------------------------------------------------------
    # Extract profile information
    # --------------------------------------------------------

    branch = profile.get(
        "branch",
        "Not provided",
    )

    year = profile.get(
        "year",
        "Not provided",
    )

    current_skills = profile.get(
        "skills",
        [],
    )

    projects = profile.get(
        "projects",
        [],
    )

    experience_level = profile.get(
        "experience_level",
        "Beginner",
    )

    preferred_language = profile.get(
        "preferred_language",
        "English",
    )

    location = profile.get(
        "location",
        "Not provided",
    )

    # Convert lists into readable strings
    if isinstance(current_skills, list):

        current_skills_text = ", ".join(
            map(str, current_skills)
        )

    else:

        current_skills_text = str(
            current_skills
        )

    if isinstance(projects, list):

        projects_text = ", ".join(
            map(str, projects)
        )

    else:

        projects_text = str(
            projects
        )

    if isinstance(skill_gaps, list):

        gaps_text = ", ".join(
            map(str, skill_gaps)
        )

    else:

        gaps_text = str(
            skill_gaps
        )

    # Keep resume reasonably small
    resume_text = (
        resume_text[:8000]
        if resume_text
        else "No resume uploaded."
    )

    # --------------------------------------------------------
    # Groq
    # --------------------------------------------------------

    try:

        from groq import Groq

        client = Groq(
            api_key=api_key
        )

        prompt = f"""
You are CareerPilot AI, an expert career mentor
for engineering students and early-career professionals.

Create a highly personalized career roadmap.

IMPORTANT:
Do NOT generate a generic roadmap.
The roadmap must be based on the user's actual
career interest, profile, resume, skills and gaps.

==================================================
TARGET CAREER
==================================================

{career_interest}

==================================================
STUDENT PROFILE
==================================================

Engineering Branch:
{branch}

Academic Year:
{year}

Experience Level:
{experience_level}

Location:
{location}

Preferred Learning Language:
{preferred_language}

==================================================
CURRENT SKILLS
==================================================

{current_skills_text}

==================================================
PROJECT EXPERIENCE
==================================================

{projects_text}

==================================================
SKILL GAPS
==================================================

{gaps_text}

==================================================
RESUME
==================================================

{resume_text}

==================================================
LEARNING AVAILABILITY
==================================================

Hours per week:
{hours_per_week}

Roadmap duration:
{duration_weeks} weeks

==================================================
ROADMAP REQUIREMENTS
==================================================

Create a practical {duration_weeks}-week roadmap.

The roadmap must:

1. Start from the user's current level.

2. Prioritize skills required for:
   {career_interest}

3. Do not recommend skills the user
   already clearly knows unless they need
   advanced depth.

4. Prioritize the identified skill gaps.

5. Include practical hands-on learning.

6. Include projects that are relevant to
   the target career.

7. Include interview preparation.

8. Include portfolio/GitHub preparation.

9. Include measurable weekly outcomes.

10. Consider the user's available
    {hours_per_week} hours per week.

11. Gradually increase difficulty.

12. Include checkpoints to measure progress.

13. If the target career appears too advanced
    for the current profile, create a realistic
    bridge path rather than rejecting the goal.

14. Recommend an alternate career only if there
    is a significant mismatch between the profile
    and the target career.

15. Avoid guaranteeing jobs, internships,
    salaries or selection.

==================================================
ROADMAP STRUCTURE
==================================================

Return ONLY valid JSON.

Each week must contain:

{{
    "week": 1,
    "phase": "Foundation",
    "title": "Specific title",
    "skill": "Main skill",
    "objective": "What the candidate should achieve",
    "topics": [
        "topic 1",
        "topic 2",
        "topic 3"
    ],
    "tasks": [
        "specific task 1",
        "specific task 2",
        "specific task 3"
    ],
    "project": "Practical project or None",
    "deliverable": "What the candidate should produce",
    "hours": 8,
    "resources": [
        "Recommended resource type 1",
        "Recommended resource type 2"
    ],
    "interview_prep": "Interview preparation task",
    "checkpoint": "How the candidate can verify progress"
}}

Generate one object for every week.

Use approximately {hours_per_week} hours
per week.

Make the roadmap specific to:

{career_interest}

Do not return explanations outside JSON.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a personalized AI "
                        "career mentor. Return valid JSON only."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.7,
            max_tokens=8000,
        )

        text = response.choices[0].message.content

        cleaned = _clean_json(text)

        roadmap = json.loads(
            cleaned
        )

        if not isinstance(
            roadmap,
            list,
        ):

            raise ValueError(
                "Groq returned an invalid roadmap format."
            )

        return {
            "error": None,
            "roadmap": roadmap,
        }

    except json.JSONDecodeError as exc:

        return {
            "error": (
                "AI returned an invalid roadmap format. "
                f"Details: {exc}"
            ),
            "roadmap": [],
        }

    except Exception as exc:

        return {
            "error": (
                f"Groq roadmap generation failed: {exc}"
            ),
            "roadmap": [],
        }
