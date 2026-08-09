def optimize_resume(resume_data, confirmed_skills):
    # Only optimize skills the candidate explicitly confirms.
    optimized = dict(resume_data)
    skills = set(optimized.get("skills", []))

    for skill in confirmed_skills:
        skills.add(skill.lower().strip())

    optimized["skills"] = sorted(skills)
    return optimized
