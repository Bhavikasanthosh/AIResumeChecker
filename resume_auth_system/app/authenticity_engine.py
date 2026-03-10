def calculate_resume_strength(email, phone, linkedin, github, total_skills, skill_evidence):
    score = 0
    
    # 1. Contact completeness (20%)
    if email != "Not found": score += 10
    if phone != "Not found": score += 10
    
    # 2. Professional Links (30%)
    if linkedin != "Not found": score += 15
    if github != "Not found": score += 15
    
    # 3. Skill breadth (20%)
    if total_skills >= 15: score += 20
    elif total_skills >= 8: score += 15
    elif total_skills >= 4: score += 10
    elif total_skills > 0: score += 5
    
    # 4. Project Evidence (30%)
    verified_skills = sum(1 for v in skill_evidence.values() if v["count"] > 0)
    if verified_skills >= 4: score += 30
    elif verified_skills >= 2: score += 20
    elif verified_skills == 1: score += 10
    
    return min(score, 100)