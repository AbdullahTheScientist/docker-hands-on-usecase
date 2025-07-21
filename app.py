from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict
import os
import uvicorn
from generate_resume import generate_resume

# Import the enhanced models
from pydantic import BaseModel, Field

# Personal Information Model
class PersonalInfo(BaseModel):
    name: str = Field(..., description="Full name")
    title: Optional[str] = Field(None, description="Job title or profession")
    phone: Optional[str] = Field(None, description="Phone number")
    email: Optional[str] = Field(None, description="Email address")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    location: Optional[str] = Field(None, description="Location/Address")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    website: Optional[str] = Field(None, description="Personal website URL")

class Custom_link(BaseModel):
    name: Optional[str] = Field(None, description="Link name")
    url: Optional[str] = Field(None, description='url')

# Work Experience Model
class WorkExperience(BaseModel):
    company: str = Field(..., description="Company name")
    position: str = Field(..., description="Job position/title")
    start_date: str = Field(..., description="Start date")
    end_date: Optional[str] = Field(None, description="End date (None if current)")
    description: Optional[str] = Field(None, description="Job description bullet points")

# Education Model
class Education(BaseModel):
    institution: str = Field(..., description="Educational institution")
    degree: str = Field(..., description="Degree obtained")
    start_date: Optional[str] = Field(None, description="Start date")
    end_date: Optional[str] = Field(None, description="End date")

# Academic Projects Model
class AcademicProject(BaseModel):
    title: str = Field(..., description="Project title")
    date: str = Field(..., description="Project date")
    technologies: Optional[str] = Field(None, description="Technologies used")
    # description: Optional[List[str]] = Field(None, description="Project description")
    description: Optional[str] = Field(None, description="Job description bullet points")
    links: Optional[Dict[str, str]] = Field(None, description="Project links")

# Certifications Model
class Certification(BaseModel):
    name: str = Field(..., description="Certification name")
    issuer: str = Field(..., description="Issuing organization")
    date: str = Field(..., description="Date obtained")
    credential_id: Optional[str] = Field(None, description="Credential ID")
    url: Optional[str] = Field(None, description="Certificate URL")
    description: Optional[str] = Field(None, description="Job description bullet points")
    # description: Optional[List[str]] = Field(None, description="Certification description")

# Publications Model
class Publication(BaseModel):
    title: str = Field(..., description="Publication title")
    authors: str = Field(..., description="Authors")
    journal: str = Field(..., description="Journal or publication venue")
    date: str = Field(..., description="Publication date")
    url: Optional[str] = Field(None, description="Publication URL")
    # description: Optional[List[str]] = Field(None, description="Publication description")
    description: Optional[str] = Field(None, description="Job description bullet points")

# Referees Model
class Referee(BaseModel):
    name: str = Field(..., description="Reference name")
    position: str = Field(..., description="Reference position")
    organization: Optional[str] = Field(None, description="Organization")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    relationship: Optional[str] = Field(None, description="Relationship to applicant")

# Custom Text
# class CustomText(BaseModel):
#     title: str = Field(..., description="Title of custom section")
#     description: Optional[str] = Field(None, description="Description of Custom section")

class Link(BaseModel):
    name: Optional[str] = Field(..., description="Display name of the link (e.g., Facebook, LinkedIn)")
    url: Optional[str] = Field(None, description="URL of the link")

class CustomText(BaseModel):
    title: str = Field(..., description="Title of custom section")
    description: Optional[str] = Field(None, description="Description of the custom section")
    link: Optional[Link] = Field(None, description="Optional link with name and URL")

# Main Resume Request Model
class ResumeRequest(BaseModel):
    # template_name: Optional[str] = Field("modern7", description="Template name")
    personal_info: PersonalInfo = Field(..., description="Personal information")
    photo: Optional[str] = Field(None, description="Base64-encoded image string")  # ✅ Add this line

    custom_links: Optional[list[Custom_link]] = Field(None, description="custom_links")
    professional_summary: Optional[str] = Field(None, description="Professional summary")
    page_size: Optional[str] = Field("A4", description="Page size")
    work_experience: Optional[List[WorkExperience]] = Field(None, description="Work experience")
    education: Optional[List[Education]] = Field(None, description="Education")
    skills: Optional[List[str]] = Field(None, description="Skills list")
    academic_projects: Optional[List[AcademicProject]] = Field(None, description="Academic projects")
    certifications: Optional[List[Certification]] = Field(None, description="Certifications")
    publications: Optional[List[Publication]] = Field(None, description="Publications")
    hobbies: Optional[List[str]] = Field(None, description="Hobbies and interests")
    languages: Optional[List[str]] = Field(None, description="Languages")
    referees: Optional[List[Referee]] = Field(None, description="References")
    custom_text: Optional[list[CustomText]] = Field(None, description= "custom text")

app = FastAPI(
    title="Enhanced Resume Generator API", 
    version="2.0.0",
    description="A comprehensive resume generator supporting multiple sections and formats"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Health Check Endpoint ----
@app.get("/")
def health_check():
    return {
        "message": "Enhanced Resume Generator API is running!", 
        "status": "healthy",
        "version": "2.0.0",
        "supported_sections": [
            "personal_info", "professional_summary", "work_experience", 
            "education", "skills", "academic_projects", "certifications", 
            "publications", "hobbies", "languages", "referees"
        ]
    }

# ---- POST Endpoint to generate resume ----
@app.post("/generate-resume/")
def create_resume(data: ResumeRequest):
    try:
        # Convert Pydantic model to dict
        resume_data = data.model_dump()
        
        # Clean the data (remove None values and empty lists)
        clean_data = {}
        for key, value in resume_data.items():
            if value is not None:
                if isinstance(value, list) and len(value) == 0:
                    continue
                clean_data[key] = value
        
        # Generate resume PDF
        pdf_path = generate_resume(clean_data)
        
        # Create a clean filename
        name = clean_data.get('personal_info', {}).get('name', 'Resume')
        clean_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{clean_name.replace(' ', '_')}_resume.pdf"
        
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=filename,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume generation failed: {str(e)}")

# ---- GET Endpoint to get sample data format ----
@app.get("/sample-data")
def get_sample_data():
    """Returns sample data format for testing"""
    return {
        "template_name": "modern7",
        "personal_info": {
            "name": "John Doe",
            "title": "Software Engineer",
            "phone": "(555) 123-4567",
            "email": "john.doe@example.com",
            "github": "https://github.com/johndoe",
            "location": "San Francisco, CA",
            "linkedin": "https://linkedin.com/in/johndoe",
            "website": "https://johndoe.dev"
        },
        "professional_summary": "Experienced software engineer with 5+ years of experience in full-stack development.",
        "page_size": "A4",
        "work_experience": [
            {
                "company": "Tech Corp",
                "position": "Senior Software Engineer",
                "start_date": "2020-01-01",
                "end_date": "Present",
                "description": [
                    "Led development of microservices architecture",
                    "Mentored junior developers",
                    "Improved system performance by 40%"
                ]
            }
        ],
        "education": [
            {
                "institution": "University of Technology",
                "degree": "Bachelor of Science in Computer Science",
                "start_date": "2014-09-01",
                "end_date": "2018-05-01"
            }
        ],
        "skills": [
            "Python", "JavaScript", "React", "Node.js", "Docker", "AWS"
        ],
        "academic_projects": [
            {
                "title": "E-commerce Platform",
                "date": "Spring 2018",
                "technologies": "React, Node.js, MongoDB",
                "description": [
                    "Built full-stack e-commerce platform",
                    "Implemented payment processing"
                ],
                "links": {
                    "GitHub": "https://github.com/johndoe/ecommerce",
                    "Demo": "https://demo.example.com"
                }
            }
        ],
        "certifications": [
            {
                "name": "AWS Solutions Architect",
                "issuer": "Amazon Web Services",
                "date": "2021-03-15",
                "credential_id": "AWS-SAA-123456",
                "url": "https://aws.amazon.com/verification",
                "description": [
                    "Validated expertise in AWS cloud architecture",
                    "Demonstrated proficiency in designing scalable systems"
                ]
            }
        ],
        "publications": [
            {
                "title": "Microservices Best Practices",
                "authors": "Doe, J.",
                "journal": "Tech Weekly",
                "date": "2022-06-01",
                "url": "https://techweekly.com/microservices",
                "description": [
                    "Explored patterns for microservices architecture",
                    "Provided practical implementation guidelines"
                ]
            }
        ],
        "hobbies": [
            "Photography", "Hiking", "Open Source Contribution", "Chess"
        ],
        "languages": [
            "English", "Spanish", "German"
        ],
        "referees": [
            {
                "name": "Jane Smith",
                "position": "Engineering Manager",
                "organization": "Tech Corp",
                "email": "jane.smith@techcorp.com",
                "phone": "(555) 987-6543",
                "relationship": "Direct Supervisor"
            }
        ],
        "custom_text":[{
        "title": "Design Philosophy",
        "content": [
            "I believe great design should be both beautiful and functional. My approach combines aesthetic excellence with strategic thinking to create visual solutions that not only look stunning but also achieve business objectives.",
            "Collaboration is at the heart of my design process. I work closely with clients to understand their vision and translate it into compelling visual narratives that resonate with their target audience."
        ]
    }],
    }

# For local development
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
