from generate_resume import generate_resume

data = {
    "name": "John Doe",
    "email": "john.doe@gmail.com",
    "phone": "+1 234 567 8901",
    "summary": "Results-oriented Software Engineer with 5+ years of experience in designing, developing, and maintaining scalable web applications. Passionate about building high-quality software and learning new technologies.",
    "skills": ["Python", "FastAPI", "JavaScript", "React", "Docker", "SQL", "Git", "REST APIs"],
    "experience": [
        {
            "title": "Senior Software Engineer",
            "company": "TechNova Solutions",
            "years": "2021 - Present",
            "description": "Lead a team of 5 developers to build a high-availability e-commerce API with FastAPI and PostgreSQL. Improved backend performance by 35%."
        },
        {
            "title": "Software Engineer",
            "company": "CodeCraft Inc.",
            "years": "2018 - 2021",
            "description": "Developed and maintained full-stack applications using Django and React. Contributed to CI/CD pipelines and Docker-based deployments."
        }
    ],
    "education": [
        {
            "degree": "B.Sc. in Computer Science",
            "institute": "Stanford University",
            "years": "2014 - 2018",
            "description": "Graduated with distinction. Specialized in software systems and machine learning."
        }
    ]
}

generate_resume(data)