from sentence_transformers import SentenceTransformer, util

# Load lightweight semantic model
model = SentenceTransformer("all-MiniLM-L6-v2")


# master skill list
skill_bank = [
    "Python",
    "Java",
    "JavaScript",
    "Docker",
    "Kubernetes",
    "Microservices",
    "REST APIs",
    "Machine Learning",
    "Deep Learning",
    "Data Analysis",
    "SQL",
    "MongoDB",
    "React",
    "Node.js",
    "Cloud Computing",
    "AWS",
    "GCP",
    "CI/CD",
]


# convert skills to embeddings once
skill_embeddings = model.encode(skill_bank, convert_to_tensor=True)


def detect_ai_skills(resume_text):

    # embed resume
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)

    # similarity between resume and skills
    similarities = util.cos_sim(resume_embedding, skill_embeddings)[0]

    detected = []

    for i, score in enumerate(similarities):

        if score > 0.35:   # similarity threshold
            detected.append(skill_bank[i])

    return detected