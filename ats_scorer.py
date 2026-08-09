import re

def calculate_ats_score(text, target_role=None):
    if not text:
        return 0, []

    score = 0
    suggestions = []
    lower = text.lower()

    if re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text):
        score += 10
    else:
        suggestions.append("Add a professional email address.")

    sections = ["education", "experience", "skills", "projects"]
    section_count = sum(1 for section in sections if section in lower)
    score += min(section_count * 8, 32)

    verbs = [
        "developed", "built", "implemented", "designed",
        "created", "optimized", "deployed", "analyzed"
    ]
    verb_count = sum(lower.count(v) for v in verbs)
    score += min(verb_count * 3, 18)

    numbers = re.findall(r"\b\d+%|\b\d+\+|\b\d+\b", text)

    if len(numbers) >= 3:
        score += 15
    else:
        suggestions.append("Add measurable outcomes to projects or experience.")

    words = len(text.split())

    if 300 <= words <= 900:
        score += 15
    else:
        suggestions.append("Keep the resume concise and relevant.")

    return min(score, 100), suggestions
