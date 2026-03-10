from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import logic for Modules 1, 2, and 3
from app.github_verifier import extract_username, fetch_repositories
from app.parser import extract_text_from_pdf
from app.skill_extractor import extract_skills
from app.skill_classifier import classify_skills
from app.ai_skill_detector import detect_ai_skills
from app.evidence_engine import (
    analyze_skill_strength, 
    calculate_github_match_score, 
    calculate_linkedin_consistency
)
from app.authenticity_engine import calculate_resume_strength
from app.llm_analyzer import generate_resume_insight
from app.utils import (
    extract_email, extract_phone, extract_name, extract_github,
    extract_linkedin, extract_section, extract_structured_experience
)

# This is the "app" variable Uvicorn is looking for
app = FastAPI(title="AI Resume Authenticity System")

# Master's Project CORS - Essential for fixing "Failed to Fetch"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze")
async def analyze_resume(
    file: UploadFile = File(...), 
    linkedin_text: str = Form("") 
):
    # 1. Process PDF
    file_bytes = await file.read()
    class BytesReader:
        def read(self): return file_bytes
        
    extracted_text = extract_text_from_pdf(BytesReader()) 
    if not extracted_text:
        return {"error": "Could not extract text from the PDF."}

    # 2. Extract Profile Info (Module 1)
    name = extract_name(extracted_text)
    email = extract_email(extracted_text)
    phone = extract_phone(extracted_text)
    github_link = extract_github(extracted_text)
    linkedin_link = extract_linkedin(extracted_text)

    # 3. Extract Work Experience (Module 1 & 3)
    experience_raw = extract_section(
        extracted_text, 
        "EXPERIENCE", 
        ["PROJECTS", "SKILLS", "EDUCATION", "CERTIFICATIONS", "LANGUAGES", "AWARDS"]
    )
    # Convert text block to structured objects for the Career Timeline
    resume_exp = extract_structured_experience(experience_raw)

    # 4. Extract Skills (Module 1)
    skills = extract_skills(extracted_text)
    ai_skills = detect_ai_skills(extracted_text)
    categorized_skills = classify_skills(skills)
    all_skills = list(set(skills + ai_skills))

    # 5. GitHub Skill Match (Module 2)
    repos = []
    github_match_score = 0.0
    if github_link != "Not found":
        username = extract_username(github_link)
        if username:
            repos = fetch_repositories(username)
            github_match_score = calculate_github_match_score(all_skills, repos)

    # 6. LinkedIn Career Validation (Module 3)
    linkedin_exp = extract_structured_experience(linkedin_text) if linkedin_text else []
    linkedin_consistency = calculate_linkedin_consistency(resume_exp, linkedin_exp)

    # 7. Final Scoring & AI Summary
    skill_evidence = analyze_skill_strength(all_skills, repos)
    strength_score = calculate_resume_strength(
        email, phone, linkedin_link, github_link, len(all_skills), skill_evidence
    )
    ai_summary = generate_resume_insight(skills, ai_skills, strength_score)

    return {
        "profile": {"name": name, "email": email, "phone": phone},
        "links": {"github": github_link, "linkedin": linkedin_link},
        "skills": {
            "categorized": categorized_skills,
            "total_count": len(all_skills)
        },
        "experience": resume_exp, # This populates your "Career Timeline"
        "github_match_score": round(github_match_score, 2),
        "linkedin_consistency": round(linkedin_consistency, 2),
        "strength_score": strength_score,
        "ai_summary": ai_summary,
        "github_repos": repos[:6]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)