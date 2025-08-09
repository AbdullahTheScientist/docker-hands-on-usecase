from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request, BackgroundTasks, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict
import os
import uvicorn
from generate_resume import generate_resume, generate_coverletter
import logging
from typing import Dict, Any, Callable
import tempfile
import time
from collections import defaultdict
import uuid

# Import the enhanced models
from pydantic import BaseModel, Field

class PersonalInfo_2(BaseModel):
    template_name : Optional[str] = Field(None, description="name of cover letter template")
    page_size : Optional[str] = Field(None, description="page size for cover letter" )
    name: str = Field(..., description="Full name")
    title: Optional[str] = Field(None, description="Job title or profession")
    phone: Optional[str] = Field(None, description="Phone number")
    email: Optional[str] = Field(None, description="Email address")
    location: Optional[str] = Field(None, description="Location/Address")
    company_name: Optional[str] = Field(None, description="company name")
    hiring_manager_name: Optional[str] = Field(None, description="Manager name")
    paragraph : Optional[list[str]] = Field(None, description="Why are you best fit for this job")

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
    template_name: Optional[str] = Field("modern7", description="Template name")
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

class CoverLetterRequest(BaseModel):
    cover_letter_info : PersonalInfo_2 = Field(..., description="Information for cover letter")

from dotenv import load_dotenv
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Response, Request
from fastapi.middleware.gzip import GZipMiddleware

# Load environment variables
load_dotenv()

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
PORT = int(os.getenv("PORT", 8000))
MAX_REQUEST_SIZE = int(os.getenv("MAX_REQUEST_SIZE", 52428800))  # 50MB default
RATE_LIMIT_CALLS = int(os.getenv("RATE_LIMIT_CALLS", 100))
RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", 60))
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
TEMP_DIR = os.getenv("TEMP_DIR", tempfile.gettempdir())


ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",") if os.getenv("ALLOWED_HOSTS") else []

logger.info(f"Environment: {ENVIRONMENT}")
logger.info(f"Debug mode: {DEBUG}")

logger.info(f"Allowed hosts: {ALLOWED_HOSTS}")

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) ->Response:
        try:
            return await call_next(request)
        except Exception as e:
            logger.info(f"Unhandled exception: {str(e)}", exc_info=True)
            # re raise to let Fast-api handle it
            raise

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""
    async def dispatch(self, request:Request, call_next:Callable) -> Response:
        response = await call_next(request)
        # security headers
        response.headers['X-Content-Type-Options'] = "nosniff"
        response.headers['X-Frame-Options'] = "Deny"
        response.headers['X-XSS-Protection'] = "1; mode=block"
        if ENVIRONMENT == "production":
            response.headers['Strict-Transport-Security'] = "max-age=31536000; includeSubDomains"
        response.headers['Referrer-Policy'] = "strict-origin-when-cross-origin"
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests with timing and response status"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate request ID
        request_id = str(uuid.uuid4())[:8]
        
        # Log request
        start_time = time.time()
        client_ip = request.client.host
        method = request.method
        url = str(request.url)
        
        if DEBUG:
            logger.debug(f"[{request_id}] {method} {url} - IP: {client_ip} - Started")
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            log_level = logging.DEBUG if response.status_code < 400 else logging.INFO
            logger.log(log_level,
                f"[{request_id}] {method} {url} - "
                f"Status: {response.status_code} - "
                f"Duration: {duration:.3f}s - "
                f"IP: {client_ip}"
            )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"[{request_id}] {method} {url} - "
                f"ERROR: {str(e)} - "
                f"Duration: {duration:.3f}s - "
                f"IP: {client_ip}"
            )
            raise


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    """Limit request body size to prevent abuse"""
    
    def __init__(self, app, max_size: int = MAX_REQUEST_SIZE):
        super().__init__(app)
        self.max_size = max_size
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Check content length
        content_length = request.headers.get("content-length")
        if content_length:
            content_length = int(content_length)
            if content_length > self.max_size:
                logger.warning(f"Request too large: {content_length} bytes from {request.client.host}")
                raise HTTPException(
                    status_code=413,
                    detail=f"Request too large. Max size: {self.max_size} bytes"
                )
        
        return await call_next(request)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Global rate limiting middleware"""
    
    def __init__(self, app, calls: int = RATE_LIMIT_CALLS, period: int = RATE_LIMIT_PERIOD):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients = {}
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip rate limiting for health checks in development
        if DEBUG and request.url.path in ["/health", "/test"]:
            return await call_next(request)
            
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean old entries
        if client_ip in self.clients:
            self.clients[client_ip] = [
                timestamp for timestamp in self.clients[client_ip]
                if current_time - timestamp < self.period
            ]
        else:
            self.clients[client_ip] = []
        
        # Check rate limit
        if len(self.clients[client_ip]) >= self.calls:
            logger.warning(f"Rate limit exceeded for {client_ip}")
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Max {self.calls} calls per {self.period} seconds"
            )
        
        # Add current request
        self.clients[client_ip].append(current_time)
        
        return await call_next(request)

class APIMonitoringMiddleware(BaseHTTPMiddleware):
    """Monitor API performance and errors"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        try:
            response = await call_next(request)
            
            # Log metrics
            duration = time.time() - start_time
            endpoint = request.url.path
            method = request.method
            status_code = response.status_code
            
            # Log slow requests
            if duration > 5.0:  # Log requests taking more than 5 seconds
                logger.warning(f"SLOW_REQUEST: {method} {endpoint} {status_code} {duration:.3f}s")
            elif DEBUG:
                logger.debug(f"API_METRIC: {method} {endpoint} {status_code} {duration:.3f}s")
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"API_ERROR: {request.method} {request.url.path} {duration:.3f}s - {str(e)}")
            raise



app = FastAPI(
    title="Enhanced Resume Generator API", 
    version="2.0.0",
    description="A comprehensive resume generator supporting multiple sections and formats"
)

# Rate limit records for dependency-based rate limiting
rate_limit_records = defaultdict(float)
# 1. Error handling (should be first/outermost)
app.add_middleware(ErrorHandlingMiddleware)

# 2. Security headers
app.add_middleware(SecurityHeadersMiddleware)

# 3. Request logging
app.add_middleware(RequestLoggingMiddleware)

# 4. API monitoring
app.add_middleware(APIMonitoringMiddleware)

# 5. Request size limiting
app.add_middleware(RequestSizeLimitMiddleware, max_size=MAX_REQUEST_SIZE)

# 6. Global rate limiting (optional - uncomment if you want global rate limiting)
app.add_middleware(RateLimitMiddleware, calls=RATE_LIMIT_CALLS, period=RATE_LIMIT_PERIOD)

# 7. GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request bodies
class TextRequest(BaseModel):
    text: str


# Dependency for rate limiting (keeping your existing approach)
async def rate_limiter(request: Request):
    client_ip = request.client.host
    current_time = time.time()

    if current_time - rate_limit_records[client_ip] < 5:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    rate_limit_records[client_ip] = current_time
    if DEBUG:
        logger.debug(f"Request from {client_ip} allowed at {current_time}")

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
def create_resume(data: ResumeRequest, dep=Depends(rate_limiter)):
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

@app.post("/generate-cover-letter/")
def create_resume(data: CoverLetterRequest):
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
        pdf_path = generate_coverletter(clean_data)
        
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


@app.post("/enhance_experience")
async def enhance_experience(request: TextRequest, dep=Depends(rate_limiter)):
    """Enhance professional experience description"""
    try:
        logger.info("Experience enhancement requested")
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text field cannot be empty")
        
        result = enhance_professional_experience(request.text)
        logger.info("Experience enhancement completed successfully")
        return {"enhanced_experience": result}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enhancing experience: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/enhance_summary")
async def enhance_summary(request: TextRequest, dep=Depends(rate_limiter)):
    """Enhance profile summary"""
    try:
        logger.info("Summary enhancement requested")
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text field cannot be empty")
        
        result = enhance_profile_summary(request.text)
        logger.info("Summary enhancement completed successfully")
        return {"enhanced_summary": result}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enhancing summary: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/enhance_project")
async def enhance_project(request: TextRequest, dep=Depends(rate_limiter)):
    """Enhance project description"""
    try:
        logger.info("Project enhancement requested")
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text field cannot be empty")
        
        result = enhance_project_description(request.text)
        logger.info("Project enhancement completed successfully")
        return {"enhanced_project_description": result}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enhancing project: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post('/analyze-resume')
async def analyze_resume_api(
    resume: UploadFile = File(..., description="Resume file to analyze"),
    job_description: str = Form(..., description="Job description to compare against"), dep=Depends(rate_limiter)
):
    # if resume.content_type != "application/pdf":
    #     raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    """Analyze a resume against a job description"""
    logger.info("Resume analysis requested")
    
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is empty")
    
    try:
        # Read the uploaded file
        resume_content = await resume.read()
        logger.info(f"Resume file read, size: {len(resume_content)} bytes")
        
        # Analyze resume against job description
        result = analyze_resume_against_jd(resume_content, job_description)
        logger.info("Resume analysis completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error occurred during analyzing resume: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))



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
