import requests
import json

BASE_URL = "http://localhost:8000"  # Change to your URL

BASE_URL = "https://docker-hands-on-usecase.onrender.com" 
# Test 1: Enhance Summary
def quick_test_enhance_summary():
    data = {
        "text": "I am a developer with experience in Python and web development."
    }
    response = requests.post(f"{BASE_URL}/enhance_summary", json=data)
    print("Enhance Summary Response:")
    print(json.dumps(response.json(), indent=2))

# Test 2: Enhance Experience  
def quick_test_enhance_experience():
    data = {
        "text": "Worked as software engineer. Built applications and fixed bugs."
    }
    response = requests.post(f"{BASE_URL}/enhance_experience", json=data)
    print("Enhance Experience Response:")
    print(json.dumps(response.json(), indent=2))

# Test 3: Enhance Project
def quick_test_enhance_project():
    data = {
        "text": "Built a web app using React and Node.js with database integration."
    }
    response = requests.post(f"{BASE_URL}/enhance_project", json=data)
    print("Enhance Project Response:")
    print(json.dumps(response.json(), indent=2))

# Test 4: Analyze Resume with PDF
def test_with_pdf():
    # You'll need to have a PDF file
    job_description = """
ob description
Welcome to Warner Bros. Discovery… the stuff dreams are made of.

Who We Are…

When we say, “the stuff dreams are made of,” we’re not just referring to the world of wizards, dragons and superheroes, or even to the wonders of Planet Earth. Behind WBD’s vast portfolio of iconic content and beloved brands, are the storytellers bringing our characters to life, the creators bringing them to your living rooms and the dreamers creating what’s next…

From brilliant creatives, to technology trailblazers, across the globe, WBD offers career defining opportunities, thoughtfully curated benefits, and the tools to explore and grow into your best selves. Here you are supported, here you are celebrated, here you can thrive.

Sr. Data Scientist – Job description

Meet our team:

The Data & Analytics organization is at the forefront of developing and maintaining frameworks, tools, and data products vital to WBD, including flagship streaming product Max and non-streaming products such as Films Group, Sports, News and overall WBD eco-system. Our mission is to foster unified analytics and drive data-driven use cases by leveraging a robust multi-tenant platform and semantic layer. We are committed to delivering innovative solutions that empower teams across the company to catalyze subscriber growth, amplify engagement, and execute timely, informed decisions, ensuring our continued success in an ever-evolving digital landscape.

Roles & Responsibilities:
• The role will focus on building out machine learning solutions for WBD’s Data and Analytics organization. Primary focus will be on unlocking machine learning opportunitiesand building foundational machine learning training and inference pipelines at scale.
• You have a deep understanding of different types of data, metrics and KPIs. You will lead by example and define the best practices, will set high standards for the entire team and for the rest of the organization. You have a successful track record for ambitious projects across cross-functional teams. You are passionate and results oriented. You strive for technical excellence and are very hands-on. Your co-workers love working with you. You have built respect in your career through concrete accomplishments.
• Build cutting-edge capabilities utilizing machine learning and data science (e.g., large language models, computer vision models, advanced ad & content targeting, etc.)
• Lead data science and model development techniques for the team.
• Leverage industry best practices and tools to continually improve teams' ability to build machine learning models.

What to Bring:
• BA/BS in statistics, mathematics, economics, industrial engineering, or other quantitative discipline is required. Masters/PhD is a plus
• 4+ years of experience building data science/statistical models (Multivariate regression, Time Series Model, XGBoost, Causal inference etc.)
• Strong understanding of modern ML approaches (GBDT, CNN, LSTM, GRU, HRNN, transformers, siamese neural networks, variational auto-encoders, ...).
• Experience with Deep Learning,NLP, LLMs, Reinforcement Learning, Causal Inference. Good knowledge of ML tools and frameworks (TensorFlow, Keras, pyTorch, scikit-learn, Spark,...).
• Proficiency in programming languages such as Python or R.
• Familiarity with real-world ML systems (configuration, data collection, data verification, feature extraction, resource and process management, analytics, training, serving, validation, experimentation, monitoring).
• Good understanding of operating machine learning solutions at scale, covering the end-to-end ML workflow.
• Strong interpersonal skills with the ability to motivate, collaborate and influence
• Ability to deliver on multiple projects and meet tight deadlines
• Ability to effectively influence and commu
"""
    
    with open("sample_resume.pdf", "rb") as f:
        files = {"resume": f}
        data = {"job_description": job_description}
        response = requests.post(f"{BASE_URL}/analyze-resume", files=files, data=data)
    
    print("Resume Analysis Response:")
    print(json.dumps(response.json(), indent=2))

# Test 5: Simple Health Check
def quick_health_check():
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:")
    print(json.dumps(response.json(), indent=2))
import time
# Run quick tests
if __name__ == "__main__":
    print("Running Quick Tests...")
    
    try:
        quick_health_check()
        print("\n" + "-"*50 + "\n")
        
        quick_test_enhance_summary()
        print("\n" + "-"*50 + "\n")
        time.sleep(6)
        quick_test_enhance_experience()
        print("\n" + "-"*50 + "\n")
        time.sleep(6)
        # quick_test_enhance_project()
        test_with_pdf()
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure your FastAPI server is running!")