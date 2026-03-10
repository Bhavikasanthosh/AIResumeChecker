import re
import spacy

# Load spaCy for precision Entity Recognition
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# --- PROFILE EXTRACTION (Module 1) ---

    
    doc = nlp(text[:300]) # Scan the header of the resume
    for ent in doc.ents:
        # A valid name is a PERSON entity, not in the blacklist, and usually 2+ words
        name_candidate = ent.text.strip()
        if (ent.label_ == "PERSON" and 
            name_candidate.upper() not in skill_blacklist and 
            len(name_candidate.split()) >= 2):
            return name_candidate
            
    # Fallback: If AI is confused, take the first non-empty line that isn't a skill
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for line in lines[:3]:
        if line.upper() not in skill_blacklist and len(line.split()) >= 2:
            return line
            
    return "Candidate Name Not Detected"

def extract_email(text):
    """Regex for standard email extraction."""
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else "Not found"

def extract_phone(text):
    """Regex for international and local phone formats."""
    match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    return match.group(0) if match else "Not found"

def extract_github(text):
    """Extracts GitHub profile handle for Module 2."""
    match = re.search(r'github\.com/([\w-]+)', text)
    return match.group(1) if match else "Not found"

def extract_linkedin(text):
    """Extracts LinkedIn profile handle for Module 3."""
    match = re.search(r'linkedin\.com/in/([\w-]+)', text)
    return match.group(1) if match else "Not found"

# --- CAREER TIMELINE PARSING (Module 1 & 3) ---

def extract_section(text, start_keyword, end_keywords):
    """Isolates the Experience section even with non-standard headers."""
    lines = text.split('\n')
    start_index = -1
    # Fuzzy matching for common experience headers
    possible_headers = [start_keyword, "WORK HISTORY", "PROFESSIONAL EXPERIENCE", "EMPLOYMENT", "BACKGROUND"]
    
    for i, line in enumerate(lines):
        if any(header in line.upper() for header in possible_headers):
            start_index = i
            break
            
    if start_index == -1: return "Not found"
        
    content = []
    for line in lines[start_index + 1:]:
        # Stop if we hit the next major section (e.g., EDUCATION)
        if any(key in line.upper() for key in end_keywords) and len(line.split()) < 4:
            break
        content.append(line)
    return "\n".join(content)

def extract_structured_experience(experience_text):
    """
    Requirement: Extract Company, Role, and Timeline.
    Uses a 'Lookback Heuristic' to find company names above dates.
    """
    if not experience_text or experience_text == "Not found": return []

    structured = []
    lines = [l.strip() for l in experience_text.split('\n') if l.strip()]
    
    # Advanced date regex for formats like '09/2022 - Present' or '2020 to 2023'
    date_pattern = re.compile(r'(\d{2}/\d{4}|\d{4}|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*(-|–|to|—)\s*(\d{2}/\d{4}|\d{4}|Present)', re.I)

    for i, line in enumerate(lines):
        date_match = date_pattern.search(line)
        if date_match:
            duration = date_match.group(0)
            
            # Logic: Company/Role are typically 1-2 lines ABOVE the date
            potential_role = lines[i-1] if i > 0 else "Role Detected"
            potential_company = lines[i-2] if i > 1 else (lines[i-1] if i > 0 else "Independent")

            # Final Cleanup: Remove long description sentences from being labeled as companies
            if len(potential_company.split()) > 7 or "." in potential_company:
                company = "Project / Freelance"
            else:
                company = potential_company

            structured.append({
                "company": company,
                "role": potential_role[:40], # Cap length to keep UI clean
                "years": duration
            })
            
    return structured