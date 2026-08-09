def build_profile(data):
    return {
        "name": data.get("name", ""),
        "branch": data.get("branch", ""),
        "year": data.get("year", ""),
        "interests": data.get("interests", []),
        "skills": data.get("skills", []),
        "hours": data.get("hours", 2),
        "location": data.get("location", ""),
    }
