def recommend_projects(missing_skills, projects):
    missing = {x.lower() for x in missing_skills}
    results = []

    for project in projects:
        skills = {x.lower() for x in project.get("skills", [])}
        overlap = missing & skills

        if overlap:
            results.append({
                **project,
                "gap_coverage": len(overlap)
            })

    return sorted(results, key=lambda x: x["gap_coverage"], reverse=True)
