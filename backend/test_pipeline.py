"""
Script to generate a sample resume PDF and test the entire backend pipeline.
"""
import fitz  # PyMuPDF
import os
import sys

# Add backend directory to sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from services.pdf_extractor import extract_text_from_pdf
from services.resume_parser import resume_parser_instance
from services.jd_parser import jd_parser_instance
from services.similarity import compare_skills

def create_sample_pdf(output_path: str):
    doc = fitz.open()
    page = doc.new_page()
    
    text = """Alex Johnson
Email: alex.johnson@example.com | Phone: +1 (555) 234-5678
GitHub: github.com/alexjohnson | LinkedIn: linkedin.com/in/alexjohnson

EDUCATION
Bachelor of Science in Computer Science
State University, 2020 - 2024
GPA: 3.8 / 4.0

TECHNICAL SKILLS
Languages: Python, JavaScript, TypeScript, C++, SQL, HTML, CSS
Frameworks & Libraries: React, Node.js, Express.js, FastAPI, Flask, Pandas, NumPy, Scikit-learn
Databases: PostgreSQL, MongoDB, MySQL
Tools & Cloud: Git, GitHub, Docker, AWS, Linux

EXPERIENCE
Software Engineering Intern - CloudTech Solutions (June 2023 - Dec 2023)
• Developed responsive web applications using React and Node.js with REST APIs
• Optimized database queries in PostgreSQL, improving query response time by 25%
• Built machine learning pipelines using Python, Pandas, and Scikit-learn for text classification
• Containerized backend microservices using Docker and deployed on AWS EC2

PROJECTS
ResumeIQ - NLP Resume & Job Description Analyzer
• Built an NLP application to parse resumes using PyMuPDF and calculate TF-IDF cosine similarity
• Implemented rule-based skill extraction with a controlled skill dictionary
• Developed interactive frontend using React and Vite with clean UI components

E-Commerce Storefront
• Built full-stack web application with React, Express.js, and MongoDB
• Integrated secure payment gateway and RESTful API endpoints

CERTIFICATIONS
• AWS Certified Cloud Practitioner
• Coursera Deep Learning Specialization
"""
    # Insert text into PDF page
    rect = fitz.Rect(50, 50, 550, 750)
    page.insert_textbox(rect, text, fontsize=10.5, fontname="helv", align=0)
    doc.save(output_path)
    doc.close()
    print(f"Sample PDF created at {output_path}")

if __name__ == "__main__":
    sample_pdf_path = os.path.join(backend_dir, "sample_resume.pdf")
    create_sample_pdf(sample_pdf_path)

    # Read and test
    with open(sample_pdf_path, "rb") as f:
        pdf_bytes = f.read()

    extracted_text, page_count = extract_text_from_pdf(pdf_bytes)
    print(f"\n--- Extracted {page_count} page(s) ---")
    
    parsed_resume = resume_parser_instance.parse(extracted_text)
    print("\n--- Parsed Resume ---")
    print(f"Name: {parsed_resume['name']}")
    print(f"Email: {parsed_resume['email']}")
    print(f"Phone: {parsed_resume['phone']}")
    print(f"Skills Found ({len(parsed_resume['skill_names'])}): {parsed_resume['skill_names']}")
    print(f"Education: {parsed_resume['education'][:60]}...")
    print(f"Experience: {parsed_resume['experience'][:60]}...")
    print(f"Projects: {parsed_resume['projects'][:60]}...")
    print(f"Certifications: {parsed_resume['certifications'][:60]}...")

    # Sample Job Description
    sample_jd = """
    We are looking for a Full Stack Python / React Developer to join our engineering team.
    
    Requirements:
    • Strong proficiency in Python, JavaScript, and TypeScript
    • Experience building modern web frontends using React and CSS
    • Backend experience with FastAPI or Django and building REST APIs
    • Experience with relational databases like PostgreSQL or MySQL
    • Familiarity with Docker, Git, and cloud services such as AWS or Azure
    • Knowledge of Machine Learning, Scikit-learn, or NLP is a plus
    • Excellent problem-solving skills
    """

    parsed_jd = jd_parser_instance.parse(sample_jd)
    print("\n--- Parsed Job Description ---")
    print(f"JD Skills ({len(parsed_jd['skill_names'])}): {parsed_jd['skill_names']}")

    # Comparison
    comparison = compare_skills(parsed_resume['skill_names'], parsed_jd['skill_names'])
    print("\n--- Skill Comparison ---")
    print(f"Matching Skills ({comparison['matching_count']}): {comparison['matching_skills']}")
    print(f"Missing Skills ({comparison['missing_count']}): {comparison['missing_skills']}")
    print(f"Additional Skills ({comparison['additional_count']}): {comparison['additional_skills']}")
    print(f"Skill Overlap: {comparison['skill_overlap_percentage']}%")
