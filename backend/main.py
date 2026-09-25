"""
FastAPI Backend Application
Resume Parsing and Job Description Skill Matching Using NLP
"""

import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from services.pdf_extractor import extract_text_from_pdf, PDFExtractionError
from services.resume_parser import resume_parser_instance
from services.jd_parser import jd_parser_instance
from services.similarity import compare_skills
from services.skill_extractor import skill_extractor_instance

app = FastAPI(
    title="ResumeIQ API",
    description="Resume Parsing and Job Description Skill Matching",
    version="1.0.0"
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local student dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10MB limit


@app.get("/api/health")
def health_check():
    """Returns backend status and available dictionary size."""
    return {
        "status": "healthy",
        "service": "ResumeIQ NLP Backend",
        "total_skills_in_dictionary": len(skill_extractor_instance.skills_data)
    }


@app.get("/api/skills")
def get_supported_skills():
    """Returns list of supported skills and categories in the dictionary."""
    return {
        "skills": skill_extractor_instance.skills_data,
        "count": len(skill_extractor_instance.skills_data)
    }


@app.post("/api/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    """
    Parses an uploaded PDF resume, extracts structured fields and skills.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file was selected."
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Please upload a PDF file (.pdf)."
        )

    try:
        content = await file.read()
        if len(content) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds the 10MB limit."
            )

        extracted_text, page_count = extract_text_from_pdf(content)
        parsed_resume = resume_parser_instance.parse(extracted_text)

        return {
            "success": True,
            "filename": file.filename,
            "page_count": page_count,
            "data": parsed_resume
        }

    except PDFExtractionError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected parsing error: {str(e)}")


@app.post("/api/analyze")
async def analyze_resume_and_jd(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Full pipeline analysis:
    1. Extract text from PDF resume.
    2. Extract entities and skills from resume.
    3. Clean and extract skills from Job Description.
    4. Compute Skill Overlap (matching, missing, additional).
    """
    # Validation 1: Resume file
    if not resume.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No resume file was uploaded."
        )

    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Please upload a PDF resume."
        )

    # Validation 2: Job description
    clean_jd_raw = job_description.strip()
    if not clean_jd_raw:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description cannot be empty. Please paste the job requirements."
        )

    if len(clean_jd_raw) < 15:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The job description is too short. Please provide a more detailed job description."
        )

    try:
        # Step 1: Read PDF
        pdf_bytes = await resume.read()
        if len(pdf_bytes) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Resume file exceeds the 10MB limit."
            )

        resume_text, page_count = extract_text_from_pdf(pdf_bytes)

        # Step 2: Parse Resume
        parsed_resume = resume_parser_instance.parse(resume_text)

        # Step 3: Parse Job Description
        parsed_jd = jd_parser_instance.parse(clean_jd_raw)

        # Step 4: Compare Skills
        skill_comparison = compare_skills(
            resume_skills=parsed_resume["skill_names"],
            jd_skills=parsed_jd["skill_names"]
        )

        return {
            "success": True,
            "filename": resume.filename,
            "page_count": page_count,
            "resume_info": {
                "name": parsed_resume["name"],
                "email": parsed_resume["email"],
                "phone": parsed_resume["phone"],
                "education": parsed_resume["education"],
                "experience": parsed_resume["experience"],
                "projects": parsed_resume["projects"],
                "certifications": parsed_resume["certifications"],
                "skills": parsed_resume["skills"],
                "skill_names": parsed_resume["skill_names"],
                "sections_detected": parsed_resume["sections_detected"]
            },
            "jd_info": {
                "skills": parsed_jd["skills"],
                "skill_names": parsed_jd["skill_names"],
                "word_count": parsed_jd["word_count"]
            },
            "skill_comparison": skill_comparison,
            "nlp_pipeline_steps": [
                {"step": 1, "title": "PDF Ingestion", "desc": "Extracted plain text across pages using PyMuPDF (fitz)"},
                {"step": 2, "title": "Text Preprocessing", "desc": "Whitespace normalization, special character handling, and tokenization"},
                {"step": 3, "title": "Entity & Section Extraction", "desc": "Rule-based identification of contact details and key resume sections"},
                {"step": 4, "title": "Controlled Skill Extraction", "desc": "Dictionary-driven regex pattern matching with canonical alias normalization"},
                {"step": 5, "title": "Skill Overlap Comparison", "desc": "Set algebra (intersection & difference) to categorize matching, missing, & additional skills"}
            ]
        }

    except PDFExtractionError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis pipeline error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
