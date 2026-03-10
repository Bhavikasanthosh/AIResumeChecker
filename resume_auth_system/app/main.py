from parser import extract_text_from_pdf
from skill_extractor import extract_skills
import re


def extract_email(text: str):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else "Not found"


def extract_phone(text: str):
    match = re.search(r'(\+?\d[\d\s\-]{8,}\d)', text)
    return match.group(0) if match else "Not found"


def extract_name(text: str):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines[0] if lines else "Not found"


def main():
    pdf_path = "../resumes/bhavikas cv.pdf"

    extracted_text = extract_text_from_pdf(pdf_path)

    if not extracted_text:
        print("No text extracted from resume.")
        return

    name = extract_name(extracted_text)
    email = extract_email(extracted_text)
    phone = extract_phone(extracted_text)
    skills = extract_skills(extracted_text)

    print("\n===== BASIC RESUME INFO =====\n")
    print("Name :", name)
    print("Email:", email)
    print("Phone:", phone)

    print("\n===== EXTRACTED SKILLS =====\n")
    print(skills)

    print("\n===== RESUME PREVIEW =====\n")
    print(extracted_text[:1500])


if __name__ == "__main__":
    main()