
import requests
import json
import base64
from datetime import datetime
import os

BASE_URL = 'http://localhost:8000'
# BASE_URL = 'https://docker-hands-on-usecase.onrender.com'
data = {
    "cover_letter_info": {
        "template_name": "08",
        "page_size":"letter",
        "name": "Muhammad Abdullah",
        'date': datetime.now().strftime("%B %d, %Y"),
        "title": "Senior Grapgner",
        "phone": "(415) 555-0199",
        "email": "ava@example.com",
        "location": "San Francisco, CA",
        "company_name": "devsinc",
        "hiring_manager_name": "harry",
        "paragraph": ["Hi, jira we brought you here today. I've fixed the date issue by reverting to the JavaScript approach for the default date, which is more universally supported. However, if you're using a server-side environment where JavaScript won't execute during PDF generation, you have a few options:", "Hi, jira we brought you here today. Ive fixed the date issue by reverting to the JavaScript approach for the default date, which is more universally supported. However, if youre using a server-side environment where JavaScript wont execute during PDF generation, you have a few options:",]
    }}

def test_health_check():
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")

def test_resume_generation():
    try:
        response = requests.post(f"{BASE_URL}/generate-cover-letter/", json=data)
        
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