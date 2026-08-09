import pandas as pd

ROLES_PATH = "data/processed/roles.csv"

def load_roles():
    return pd.read_csv(ROLES_PATH)

def calculate_match(user_skills, required_skills):
    user = {s.lower().strip() for s in user_skills}
    required = {s.lower().strip() for s in required_skills}

    if not required:
        return 0

    return round(len(user & required) / len(required) * 100)

def recommend_careers(user_skills):
    roles = load_roles()
    results = []

    for _, row in roles.iterrows():
        required = [x.strip() for x in row["skills"].split(";")]
        score = calculate_match(user_skills, required)

        missing = [
            skill for skill in required
            if skill.lower() not in {x.lower() for x in user_skills}
        ]

        results.append({
            "role": row["role"],
            "description": row["description"],
            "score": score,
            "required_skills": required,
            "missing_skills": missing,
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)
