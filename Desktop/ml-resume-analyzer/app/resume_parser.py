import re
from .skills_db import SKILL_KEYWORDS

def extract_skills(text: str):
    text = text.lower()
    found = [skill for skill in SKILL_KEYWORDS if skill.lower() in text]
    return list(set(found))

def score_resume(resume_text: str, job_description: str):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    overlap = set(resume_skills).intersection(job_skills)
    missing = set(job_skills) - set(resume_skills)

    match_score = (len(overlap) / len(job_skills)) * 100 if job_skills else 0

    return {
        "match_score": round(match_score, 2),
        "missing_keywords": list(missing),
        "resume_skills": resume_skills
    }

def generate_feedback(results):
    feedback = {}
    if results["match_score"] >= 80:
        feedback["overall"] = "Your resume aligns very well with the job description!"
    elif results["match_score"] >= 50:
        feedback["overall"] = "Your resume is a decent match, but you could improve it."
    else:
        feedback["overall"] = "Your resume needs stronger alignment with the job description."

    if results["missing_keywords"]:
        feedback["missing"] = (
            f"Consider adding these keywords: {', '.join(results['missing_keywords'])}."
        )

    return feedback