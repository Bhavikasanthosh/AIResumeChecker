def extract_skills(text: str) -> list:
    skill_keywords = [
        "python", "java", "sql", "machine learning", "deep learning",
        "tensorflow", "pytorch", "pandas", "numpy", "excel",
        "power bi", "tableau", "docker", "kubernetes", "aws",
        "gcp", "azure", "fastapi", "flask", "django", "react",
        "node.js", "mongodb", "postgresql", "git", "linux"
    ]

    text_lower = text.lower()
    found_skills = []

    for skill in skill_keywords:
        if skill in text_lower:
            found_skills.append(skill)

    return sorted(list(set(found_skills)))