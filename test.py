
# import requests
# import json
# import base64
# import os

# BASE_URL = 'http://localhost:8000'

# def load_profile_image(image_path="5-min.jpg"):
#     """Load and encode profile image to base64"""
#     try:
#         if os.path.exists(image_path):
#             with open(image_path, "rb") as image_file:
#                 base64_image = base64.b64encode(image_file.read()).decode('utf-8')
#                 print(f"Profile image loaded from: {image_path}")
#                 return base64_image
#         else:
#             print(f"Warning: Profile image not found at {image_path}")
#             return None
#     except Exception as e:
#         print(f"Error loading profile image: {e}")
#         return None
# profile_image_base64 = load_profile_image("6.jpg")


# data ={
#     # "template_name": "modern7",
#     "personal_info": {
#         "name": "Ava jdksjdks",
#         "title": "Senior Grapgner",
#         "phone": "(415) 555-0199",
#         "email": "ava@example.com",
#         "github": "www.github.com",
#         "location": "San Francisco, CA",
#         "linkedin": "https://linkedin.com/in/avamartinezdesign",
#         "website": "https://avamartinezdesign.com"
#     },
#      "custom_links": [
#     {
#       "name": "Dribbble",
#       "url": "https://dribbble.com/ava"
#     },
#     {
#       "name": "Portfolio",
#       "url": "https://avaportfolio.com"
#     },
#     {
#       "name": "Dribbble",
#       "url": "https://dribbble.com/ava"
#     },
#     {
#       "name": "Dribbble",
#       "url": "https://dribbble.com/ava"
#     },
#     {
#       "name": "Dribbble",
#       "url": "https://dribbble.com/ava"
#     },
#     {
#       "name": "Dribbble",
#       "url": "https://dribbble.com/ava"
#     }
#   ],
#     "professional_summary": "Led the branding and visual identity for 20+ clients across tech, fashion, and hospitality industries.",
#     # "page_size": "A4",
#     "work_experience": [
#         {
#         "company": "Lime & Co. Creative Agency",
#         "position": "Senior Graphic Designer",
#         "start_date": "2018-06-01",
#         "end_date": "Present",
#         "description": 
#             """Led the branding and visual identity for 20+ clients across tech. fashion, and hospitality industries. fashion, and hospitality industries. fashion, and hospitality industries fashion, and hospitality industries."""
#             # "Designed marketing materials including brochures, social media graphics, and infographics that boosted engagement by 35%.",
#             # "Collaborated with copywriters, photographers, and developers to deliver cohesive marketing campaigns."
        
#         }
#         # {
#         # "company": "Lime & Co. Creative Agency",
#         # "position": "Senior Graphic Designer",
#         # "start_date": "2018-06-01",
#         # "end_date": "Present",
#         # "description": [
#         #     "Managed full design cycle from concept to final delivery independently. Managed full design cycle from concept to final delivery independently. Managed full design cycle from concept to final delivery independently.",
#         #     "Led the branding and visual identity for 20+ clients across tech, fashion, and hospitality industries. Led the branding and visual identity for 20+ clients across tech, fashion, and hospitality industries.",
#         #     "Designed marketing materials including brochures, social media graphics, and infographics that boosted engagement by 35%.",
#         #     "Collaborated with copywriters, photographers, and developers to deliver cohesive marketing campaigns."
#         # ]
#         # },
#         # {
#         # "company": "Freelance",
#         # "position": "Graphic Designer",
#         # "start_date": "2015-01-01",
#         # "end_date": "2018-05-01",
#         # "description": [
#         #     "Worked with small businesses to create logos., packaging, and promotional materials.",
#         #     "Built long-term relationships with over a dozen clients through reliable service and high-quality design.",
#         #     "Managed full design cycle from concept to final delivery independently. Managed full design cycle from concept to final delivery independently. Managed full design cycle from concept to final delivery independently.",
#         #                 "Worked with small businesses to create logos., packaging, and promotional materials.",
#         #     "Built long-term relationships with over a dozen clients through reliable service and high-quality design.",
#         #     "Managed full design cycle from concept to final delivery independently.",
#         #                 "Worked with small businesses to create logos., packaging, and promotional materials.",
#         #     "Built long-term relationships with over a dozen clients through reliable service and high-quality design.",
#         #     "Managed full design cycle from concept to final delivery independently.",
#         #                 "Worked with small businesses to create logos., packaging, and promotional materials.",
#         #     "Built long-term relationships with over a dozen clients through reliable service and high-quality design.",
#         #     "Managed full design cycle from concept to final delivery independently.",
#         #                 "Worked with small businesses to create logos., packaging, and promotional materials.",
#         #     "Built long-term relationships with over a dozen clients through reliable service and high-quality design.",
#         #     "Managed full design cycle from concept to final delivery independently.",
#         #                 "Worked with small businesses to create logos., packaging, and promotional materials.",
#         #     "Built long-term relationships with over a dozen clients through reliable service and high-quality design.",
#         #     "Managed full design cycle from concept to final delivery independently."
#         # ]
#         # }
#     ],
#     "education": [
#         {
#         "institution": "California College of the Arts",
#         "degree": "Bachelor of Fine Arts",
#         "start_date": "2010-08-01",
#         "end_date": "2014-05-01"
#         }
#     ],
#     "skills": [
#         "Adobe",
#         "Brand Identity Design",
#         "Adobe Creative Suite",
#         "Adobe",
#         "Brand Identity Design",
#         "Adobe Creative Suite",
#         "Adobe",
#         "Brand Identity Design",
#         "Adobe Creative Suite",
#     ],
#     "academic_projects": [
#         {
#         "title": "Branding for Local Farmers Market",
#         "date": "Fall 2013",
#         "technologies": "Illustrator, InDesign, Photoshop",
#         "description": [
#             "Created a visual identity system including logo, signage, and promotional posters.",
#             "Received campus-wide recognition and used in real-world local market."
#         ],
#         "links": {
#             "Portfolio": "https://avamartinezdesign.com/farmers-market"
#         }
#         }
#     ],
#     "certifications": [
#         {
#         "name": "Adobe Certified Expert (ACE)",
#         "issuer": "Adobe",
#         "date": "2021-11-01",
#         "credential_id": "ACE-987654",
#         "url": "https://adobe.com/",
#         "description": [
#             "Validated advanced proficiency in Adobe Photoshop and Illustrator.",
#             "Demonstrated excellence in digital imaging and design workflows."
#         ]
#         },
#         {
#         "name": "Graphic Design Specialization",
#         "issuer": "Coursera | CalArts",
#         "date": "2020-04-01",
#         "credential_id": "CALARTS-GDS-456789",
#         "url": "https://coursera.org/graphicdesign",
#         "description": [
#             "Completed series covering fundamentals of graphic design, typography, and composition.",
#             "Produced real-world projects under the mentorship of CalArts professors."
#         ]
#         }
#     ],
#     "publications": [
#         {
#         "title": "Minimalist Branding in the Digital Age",
#         "authors": "Martinez, A.",
#         "journal": "Design Week",
#         "date": "2022-08-01",
#         "url": "https://designweek.com/minimalist-branding",
#         "description": [
#             "Explored the impact of minimalist aesthetics in modern branding.",
#             "Featured case studies and tips for new designers."
#         ]
#         }
#     ],
#     "hobbies": [
#         "Digital illustration",
#         "Photography",
#         "Poster collecting",
#         "Travel sketching",
#         "Calligraphy"
#     ],
#     "languages": [
#         "English",
#         "French",
#         "jdskjd",
#         "jdskjd",
#         "jdskjd",
#         "jdskjd"
#     ],
#     "referees": [
#         {
#         "name": "Elena Roberts",
#         "position": "Creative Director",
#         "organization": "Lime & Co. Creative Agency",
#         "email": "elena.roberts@example.com",
#         "phone": "(415) 555-0222",
#         "relationship": "Direct Supervisor"
#         }
#     ],
#     "custom_text": [{
#         "title": "Design Philosophy",
#         "description": "kjsakj sakska kajskajska. Completed series covering fundamentals of graphic design, typography, and composition.Completed series covering fundamentals of graphic design, typography, and composition.Completed series covering fundamentals of graphic design, typography, and composition. "
#     }],
#     }

#     # Add profile picture if available
# if profile_image_base64:
#     data["photo"] = profile_image_base64

# def test_health_check():
#     try:
#         response = requests.get(f"{BASE_URL}/")
#         print(f"Health check: {response.status_code} - {response.json()}")
#     except Exception as e:
#         print(f"Health check failed: {e}")

# def test_resume_generation():
#     try:
#         response = requests.post(f"{BASE_URL}/generate-resume/", json=data)
        
#         if response.status_code == 200:
#             with open("resume_production.pdf", "wb") as f:
#                 f.write(response.content)
#             print("Resume generated successfully from production! Check resume_production.pdf")
#         else:
#             print(f"Error: {response.status_code} - {response.text}")
            
#     except Exception as e:
#         print(f"Resume generation failed: {e}")

# if __name__ == "__main__":
#     test_health_check()
#     test_resume_generation()



import requests
import json
import base64
import os

BASE_URL = 'http://localhost:8000'

# BASE_URL = 'https://docker-hands-on-usecase.onrender.com'

def load_profile_image(image_path="5-min.jpg"):
    """Load and encode profile image to base64"""
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                print(f"Profile image loaded from: {image_path}")
                return base64_image
        else:
            print(f"Warning: Profile image not found at {image_path}")
            return None
    except Exception as e:
        print(f"Error loading profile image: {e}")
        return None

profile_image_base64 = load_profile_image("5.jpg")

data = {
    "template_name": "prof1",
    "personal_info": {
        "name": "Ava jdksjdks",
        "title": "Senior Grapgner",
        "phone": "(415) 555-0199",
        "email": "ava@example.com",
        "github": "www.github.com",
        "location": "San Francisco, CA",
        "linkedin": "https://linkedin.com/in/avamartinezdesign",
        "website": "https://avamartinezdesign.com"
    },
    "custom_links": [
        {
            "name": "Dribbble",
            "url": "https://dribbble.com/ava"
        }],
    "professional_summary": "Led the branding and visual identity for 20+ clients across tech, fashion, and hospitality industries. Led the branding and visual identity for 20+ clients across tech, fashion, and hospitality industries.Led the branding and visual identity for 20+ clients across tech, fashion, and hospitality industries.Led the branding and visual identity for 20+ clients across tech, fashion, and hospitality industries.Led the branding and visual identity for 20+ clients across tech, fashion, and hospitality industries.Led the branding and visual identity for 20+ clients across tech, fashion, and hospitality industries.Led the branding and visual identity for 20+ clients across tech, fashion, and hospitality industries.",
    "page_size": "letter",
    "work_experience": [
        {
            "company": "Lime & Co. Creative Agency",
            "position": "Senior Graphic Designer",
            "start_date": "2018-06-01",
            "end_date": "Present",
            "description": 
                """Led the branding and visual identity for 20+ clients across tech. fashion, and hospitality industries. fashion, and hospitality industries. fashion, and hospitality industries fashion, and hospitality industries. Led the branding and visual identity for 20+ clients across tech. fashion, and hospitality industries. fashion, and hospitality industries. fashion, and hospitality industries fashion, and hospitality industries."""
        }
    ],
    "education": [
        {

            "institution": "California College of the ArtsCalifornia College of the Arts",
            "degree": "Bachelor of Fine Arts",
            "start_date": "2010-08-01",
            "end_date": "2014-05-01"
        }
    ],
    "skills": [
        "Adobe",
        "Brand Identity Design",
        "Adobe Creative Suite",
        "Adobe",
        "Brand Identity Design"
    ],
    "academic_projects": [
        {
            "title": "Branding for Local Farmers Market",
            "date": "Fall 2013",
            "technologies": "Illustrator, InDesign, Photoshop",
            "description": """
                Created a visual identity system including logo, signage, and promotional posters. Received campus-wide recognition and used in real-world local market.
            """,
            "links": {
                "Portfolio": "https://avamartinezdesign.com/farmers-market"
            }
        }
    ],
    "certifications": [
        {
            "name": "Adobe Certified Expert (ACE)",
            "issuer": "Adobe",
            "date": "2021-11-01",
            "credential_id": "ACE-987654",
            "url": "https://adobe.com/",
            "description": """
                Created a visual identity system including logo, signage, and promotional posters. Received campus-wide recognition and used in real-world local market.
            """
        }
    ],
    "publications": [
        {
            "title": "Minimalist Branding in the Digital Age",
            "authors": "Martinez, A.",
            "journal": "Design Week",
            "date": "2022-08-01",
            "url": "https://designweek.com/minimalist-branding",
            "description": """
                Created a visual identity system including logo, signage, and promotional posters. Received campus-wide recognition and used in real-world local market.
            """
        }
    ],
    "hobbies": [
        "Digital illustration",
        "Photography",
        "Poster collecting",
        "Travel sketching",
        "Calligraphy"
    ],
    "languages": [
        "English",
        "French",
       
    ],
    "referees": [
        {
            "name": "Elena Roberts",
            "position": "Creative Director",
            "organization": "Lime & Co. Creative Agency",
            "email": "elena.roberts@example.com",
            "phone": "(415) 555-0222",
            "relationship": "Direct Supervisor"
        }
    ],
  "custom_text": [
    {
      "title": "Social Links",
      "description": "Here are my social and professional profiles. Here are my social and professional profiles.Here are my social and professional profiles.Here are my social and professional profiles.",
      "link": {
        "name": "LinkedIn",
        "url": "https://linkedin.com/in/yourname"
      }}
  ],
}

# Add profile picture if available
if profile_image_base64:
    data["photo"] = profile_image_base64


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