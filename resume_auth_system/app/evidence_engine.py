from sentence_transformers import util
from app.ai_skill_detector import model # Re-using BERT from Module 1

# --- MODULE 1 & 2: Skill Strength Logic ---
def analyze_skill_strength(skills, repos):
    """
    Analyzes how many times a skill appears in GitHub repos.
    """
    evidence = {}
    for skill in skills:
        # Check if skill is in repo description or matches the primary language
        count = sum(1 for repo in repos if skill.lower() in (repo['description'] or "").lower() 
                    or skill.lower() == (repo['language'] or "").lower())
        evidence[skill] = {
            "count": count,
            "level": "Strong" if count >= 3 else "Medium" if count >= 1 else "None"
        }
    return evidence

# --- MODULE 2: GitHub AI Match Score ---
def calculate_github_match_score(resume_skills, github_repos):
    """
    Calculates semantic similarity between resume skills and GitHub metadata.
    Requirement: Sentence-BERT
    """
    if not resume_skills or not github_repos:
        return 0.0

    repo_texts = []
    for repo in github_repos:
        # Combine name, description, and topics for context
        text = f"{repo['name']} {repo['description']} {' '.join(repo.get('topics', []))} {repo.get('language', '')}"
        repo_texts.append(text.lower())
    
    combined_github = " ".join(repo_texts)
    skill_text = " ".join(resume_skills).lower()
    
    # AI Task: Cosine Similarity
    emb1 = model.encode(skill_text, convert_to_tensor=True)
    emb2 = model.encode(combined_github, convert_to_tensor=True)
    
    score = util.cos_sim(emb1, emb2)
    return float(score[0][0])

# --- MODULE 3: LinkedIn Consistency Score ---
def calculate_linkedin_consistency(resume_exp, linkedin_exp):
    """
    Compares Resume Timeline vs LinkedIn Timeline.
    Requirement: Similarity scoring using Sentence-BERT
    """
    if not resume_exp or not linkedin_exp:
        return 1.0 # Default to 100% if no LinkedIn data provided to compare

    scores = []
    for r_job in resume_exp:
        match_found = False
        for l_job in linkedin_exp:
            # Compare Company Names semantically
            emb_r = model.encode(r_job['company'].lower(), convert_to_tensor=True)
            emb_l = model.encode(l_job['company'].lower(), convert_to_tensor=True)
            company_sim = float(util.cos_sim(emb_r, emb_l))

            # If companies match (>0.8), check title and dates
            if company_sim > 0.8:
                match_found = True
                emb_role_r = model.encode(r_job['role'].lower(), convert_to_tensor=True)
                emb_role_l = model.encode(l_job['role'].lower(), convert_to_tensor=True)
                role_sim = float(util.cos_sim(emb_role_r, emb_role_l))
                
                job_score = (company_sim + role_sim) / 2
                
                # Penalty if years/dates don't match
                if r_job['years'] != l_job['years']:
                    job_score *= 0.8
                
                scores.append(job_score)
                break
        
        if not match_found:
            scores.append(0.3) # Heavy penalty for missing jobs

    return sum(scores) / len(scores) if scores else 0.0