def analyze_skill_gap(current_skills, required_skills):
    current = {x.lower().strip() for x in current_skills}
    required = {x.lower().strip() for x in required_skills}

    matched = sorted(current & required)
    missing = sorted(required - current)

    readiness = round(len(matched) / len(required) * 100) if required else 0

    return {
        "matched": matched,
        "missing": missing,
        "readiness": readiness,
    }
