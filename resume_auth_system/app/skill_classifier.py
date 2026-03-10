# app/skill_classifier.py

skill_categories = {
    "Programming": [
        "python","java","javascript","typescript","c++","c"
    ],

    "Cloud & DevOps": [
        "docker","kubernetes","aws","gcp","azure","jenkins","ci/cd"
    ],

    "Databases": [
        "mysql","mongodb","postgresql","redis","sqlite"
    ],

    "Frontend": [
        "react","vue","angular","html","css"
    ],

    "Backend": [
        "node.js","express","spring","flask","django"
    ]
}


def classify_skills(skills):

    categorized = {category: [] for category in skill_categories}

    for skill in skills:
        s = skill.lower()

        for category, items in skill_categories.items():
            if s in items:
                categorized[category].append(skill)

    return categorized