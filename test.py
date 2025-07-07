# import requests
# import json

# data = {
#     "name": "John Doe",
#     "email": "john.doe@gmail.com",
#     "phone": "+1 234 567 8901",
#     "summary": "Results-oriented Software Engineer with 5+ years of experience in developing scalable web applications and leading cross-functional teams.",
#     "skills": ["Python", "FastAPI", "JavaScript", "React", "PostgreSQL", "Docker"],
#     "experience": [
#         {
#             "title": "Senior Software Engineer",
#             "company": "TechNova Solutions",
#             "years": "2021 - Present",
#             "description": "Lead a team of 5 developers in building microservices architecture. Improved system performance by 40% and reduced deployment time by 60%."
#         },
#         {
#             "title": "Software Engineer",
#             "company": "DataTech Inc.",
#             "years": "2018 - 2021",
#             "description": "Developed and maintained REST APIs using Python and FastAPI. Collaborated with frontend teams to deliver user-friendly interfaces."
#         }
#     ],
#     "education": [
#         {
#             "degree": "B.Sc. in Computer Science",
#             "institute": "Stanford University",
#             "years": "2014 - 2018",
#             "description": "Graduated with distinction. Specialized in software engineering and data structures."
#         }
#     ]
# }

# try:
#     res = requests.post("http://localhost:8000/generate-resume/", json=data)
    
#     if res.status_code == 200:
#         with open("resume.pdf", "wb") as f:
#             f.write(res.content)
#         print("Resume generated successfully! Check resume.pdf")
#     else:
#         print(f"Error: {res.status_code} - {res.text}")
        
# except requests.exceptions.ConnectionError:
#     print("Error: Could not connect to the server. Make sure FastAPI is running on localhost:8000")
# except Exception as e:
#     print(f"Error: {str(e)}")
import requests
import json

# Replace with your actual Render URL
# BASE_URL = "https://your-app-name.onrender.com"
BASE_URL = 'http://localhost:8000'

data = {
    "name": "John Doe",
    "email": "john.doe@gmail.com",
    "phone": "+1 234 567 8901",
    "summary": "Results-oriented Software Engineer with 5+ years of experience in developing scalable web applications and leading cross-functional teams.",
    "skills": ["Python", "FastAPI", "JavaScript", "React", "PostgreSQL", "Docker"],
    "experience": [
        {
            "title": "Senior Software Engineer",
            "company": "TechNova Solutions",
            "years": "2021 - Present",
            "description": "Lead a team of 5 developers in building microservices architecture. Improved system performance by 40% and reduced deployment time by 60%."
        },
        {
            "title": "Software Engineer",
            "company": "DataTech Inc.",
            "years": "2018 - 2021",
            "description": "Developed and maintained REST APIs using Python and FastAPI. Collaborated with frontend teams to deliver user-friendly interfaces."
        }
    ],
    "education": [
        {
            "degree": "B.Sc. in Computer Science",
            "institute": "Stanford University",
            "years": "2014 - 2018",
            "description": "Graduated with distinction. Specialized in software engineering and data structures."
        }
    ]
}

def test_health_check():
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")

def test_resume_generation():
    try:
        response = requests.post(f"{BASE_URL}/generate-resume/", json=data)
        
        if response.status_code == 200:
            with open("resume_production.pdf", "wb") as f:
                f.write(response.content)
            print("Resume generated successfully from production! Check resume_production.pdf")
        else:
            print(f"Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Resume generation failed: {e}")

if __name__ == "__main__":
    test_health_check()
    test_resume_generation()
