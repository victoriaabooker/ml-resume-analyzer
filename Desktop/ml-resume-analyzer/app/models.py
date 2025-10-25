from pydantic import BaseModel
from typing import List, Dict

class ResumeRequest(BaseModel):
    job_description: str
    resume_text: str

class ScoreResponse(BaseModel):
    match_score: float
    top_missing_keywords: List[str]
    extracted_skills: List[str]

class FeedbackResponse(BaseModel):
    message: str
    suggestions: Dict[str, str]