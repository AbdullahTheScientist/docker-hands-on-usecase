from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import FileResponse
import os
import uvicorn

from generate_resume import generate_resume

app = FastAPI(title="Resume Generator API", version="1.0.0")

# ---- Pydantic Models ----
class Experience(BaseModel):
    title: str
    company: str
    years: str
    description: str

class Education(BaseModel):
    degree: str
    institute: str
    years: str
    description: str

class ResumeRequest(BaseModel):
    name: str
    email: str
    phone: str
    summary: str
    skills: List[str]
    experience: List[Experience]
    education: List[Education]

# ---- Health Check Endpoint ----
@app.get("/")
def health_check():
    return {"message": "Resume Generator API is running!", "status": "healthy"}

# ---- POST Endpoint to generate resume ----
@app.post("/generate-resume/")
def create_resume(data: ResumeRequest):
    try:
        # Convert Pydantic model to dict
        resume_data = data.dict()
        
        # Generate resume PDF
        pdf_path = generate_resume(resume_data)
        
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"{resume_data['name']}_resume.pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume generation failed: {str(e)}")

# For local development
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)