# backend/data_ingestion.py
import os
import json
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://pguser:pgpass@localhost:5432/jobrec")
engine = create_engine(DATABASE_URL)

def insert_job(title, description, skills, seniority="mid"):
    skills_json = json.dumps(skills)
    with engine.begin() as conn:
        conn.execute(
            text("""
            INSERT INTO job_roles (title, description, required_skills, seniority)
            VALUES (:title, :description, :skills::jsonb, :seniority)
            """),
            {"title": title, "description": description, "skills": skills_json, "seniority": seniority}
        )

def insert_sample_jobs():
    jobs = [
        ("Data Scientist", "Build models and analyze data end-to-end", ["python","pandas","ml","statistics"], "mid"),
        ("Product Manager", "Define product features and strategy; work with stakeholders", ["product management","roadmapping","stakeholder mgmt"], "senior"),
        ("Data Engineer", "Build data pipelines and ETL infrastructure", ["sql","airflow","spark","python"], "mid"),
        ("Machine Learning Engineer", "Productionise ML models and pipelines", ["python","ml","docker","model-serving"], "mid"),
        ("Business Analyst", "Translate business requirements to analytics", ["sql","excel","data visualization","stakeholder mgmt"], "junior"),
    ]
    for title, desc, skills, seniority in jobs:
        insert_job(title, desc, skills, seniority)
    print("Sample jobs inserted.")

def insert_sample_user():
    with engine.begin() as conn:
        conn.execute(
            text("""
            INSERT INTO users (name, email, summary, education, coursework, skills)
            VALUES (:name, :email, :summary, :education::jsonb, :coursework::jsonb, :skills::jsonb)
            ON CONFLICT (email) DO NOTHING
            """),
            {
                "name": "Alice Example",
                "email": "alice@example.com",
                "summary": "MSc Computer Science, interested in data and ML.",
                "education": json.dumps({"degree":"MSc Computer Science","institution":"Example University"}),
                "coursework": json.dumps(["machine learning","databases","distributed systems"]),
                "skills": json.dumps(["python","sql","pandas"])
            }
        )
    print("Sample user inserted (if not exist).")

if __name__ == "__main__":
    insert_sample_jobs()
    insert_sample_user()
