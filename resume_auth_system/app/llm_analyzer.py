import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3-flash-preview")

def generate_resume_insight(skills, ai_skills, strength_score):

    prompt = f"""
    You are an AI hiring assistant.

    A resume analysis system detected:
    Extracted skills: {skills}
    AI-detected skills: {ai_skills}
    Resume Strength Score: {strength_score}%

    Write a short professional summary of the candidate profile.
    Mention strengths and possible skill gaps.
    Keep it under 5 sentences.
    """

    response = model.generate_content(prompt)
    return response.text