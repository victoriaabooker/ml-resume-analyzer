from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .models import ResumeRequest, ScoreResponse, FeedbackResponse
from .resume_parser import score_resume, generate_feedback

app = FastAPI(
    title="Resume Analyzer API",
    description="NLP-based resume analyzer for keyword alignment and suggestion generation.",
    version="1.0.0",
)

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_model=dict)
def root():
    return {"status": "ok", "message": "Resume Analyzer API running"}

@app.get("/form", response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/analyze", response_model=ScoreResponse)
def analyze_resume(payload: ResumeRequest):
    results = score_resume(payload.resume_text, payload.job_description)
    return {
        "match_score": results["match_score"],
        "top_missing_keywords": results["missing_keywords"],
        "extracted_skills": results["resume_skills"],
    }

@app.post("/feedback", response_model=FeedbackResponse)
def feedback(payload: ResumeRequest):
    results = score_resume(payload.resume_text, payload.job_description)
    suggestions = generate_feedback(results)
    return {
        "message": "Resume feedback generated.",
        "suggestions": suggestions
    }