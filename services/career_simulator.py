from services.career_engine import recommend_careers

def simulate_career(current_skills, target_role, additional_skills=None):
    additional_skills = additional_skills or []
    skills = list(set(current_skills + additional_skills))

    results = recommend_careers(skills)

    target = next(
        (r for r in results if r["role"] == target_role),
        None
    )

    return target or {}
