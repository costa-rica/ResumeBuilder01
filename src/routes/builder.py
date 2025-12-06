from fastapi import APIRouter, File, UploadFile, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os
import json

from src.utils.file_processing import read_docx, read_prompt_template
from src.utils.llm_client import generate_tailored_resume

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "templates"))

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/submit", response_class=HTMLResponse)
async def submit(
    request: Request,
    resume_file: UploadFile = File(...),
    job_description: str = Form(...),
    model_choice: str = Form(...)
):
    # 1. Read the uploaded file
    if not resume_file.filename.endswith('.docx'):
         # Simple error handling for MVP
         return templates.TemplateResponse("index.html", {
             "request": request,
             "error": "Only .docx files are supported."
         })
    
    try:
        content = await resume_file.read()
        resume_text = read_docx(content)
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
             "error": f"Error reading file: {str(e)}"
        })

    # 2. Read the prompt template
    try:
        prompt_template_resume = read_prompt_template("src/templates/markdown/prompt02.md")
    except Exception as e:
         return templates.TemplateResponse("index.html", {
            "request": request,
             "error": f"Error reading prompt template: {str(e)}"
        })
    # 3. Read the cover letter prompt template
    try:
        prompt_template_cover_letter = read_prompt_template("src/templates/markdown/prompt03.md")
    except Exception as e:
         return templates.TemplateResponse("index.html", {
            "request": request,
             "error": f"Error reading prompt template: {str(e)}"
        })
    # 4. Read the cover letter prompt template
    try:
        prompt_template_scoring_and_improvements = read_prompt_template("src/templates/markdown/prompt03-scoring.md")
    except Exception as e:
         return templates.TemplateResponse("index.html", {
            "request": request,
             "error": f"Error reading prompt template: {str(e)}"
        })

    # 3. Call LLM
    llm_result_resume = generate_tailored_resume(resume_text, job_description, model_choice, prompt_template_resume)
    llm_result_cover_letter = generate_tailored_resume(resume_text, job_description, model_choice, prompt_template_cover_letter)
    llm_result_scoring_and_improvements = generate_tailored_resume(resume_text, job_description, model_choice, prompt_template_scoring_and_improvements)
    llm_result_new_resume_score = generate_tailored_resume(llm_result_resume.get("updated_resume", "No resume generated."), job_description, model_choice, prompt_template_scoring_and_improvements)
    # 4. Render Result Page
    # The result should match the keys expected in result.html
    return templates.TemplateResponse("result.html", {
        "request": request,
        "resume_qualifier_match": f'{llm_result_scoring_and_improvements.get("resume_qualifier_match", "No match generated.")}%',
        "revised_match": f'{llm_result_new_resume_score.get("resume_qualifier_match", "No match generated.")}%',
        "updated_resume": llm_result_resume.get("updated_resume", "No resume generated."),
        "updated_cover_letter": llm_result_cover_letter.get("updated_cover_letter", "No cover letter generated."),
        # "improvements": llm_result_resume.get("improvements_list", [])
        "improvements": llm_result_new_resume_score.get("improvements_list", [])
    })
