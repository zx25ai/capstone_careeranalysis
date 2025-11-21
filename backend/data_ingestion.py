"""
Data ingestion using pure SQLAlchemy ORM
No CRUD layer required.
"""

from database import SessionLocal
from models import Skill, Job, User


def seed_skills(db):
    """Insert base skills only if table is empty."""
    existing = db.query(Skill).count()
    if existing > 0:
        print("✔ Skills already exist. Skipping seed.")
        return

    base_skills = [
        "Python",
        "Machine Learning",
        "SQL",
        "Data Visualization",
        "Deep Learning",
        "Project Management",
        "Cloud Computing",
        "NLP",
        "Communication",
    ]

    print("Seeding skills...")

    for name in base_skills:
        db.add(Skill(name=name))

    db.commit()
    print("✔ Skills seeded.")


def seed_jobs(db):
    """Create jobs with related skills."""
    existing = db.query(Job).count()
    if existing > 0:
        print("✔ Jobs already exist. Skipping seed.")
        return

    # Fetch entire skill map
    skills = {s.name: s for s in db.query(Skill).all()}

    jobs = [
        {
            "title": "Data Scientist",
            "description": "Build ML models and analyze datasets.",
            "skill_names": ["Python", "Machine Learning", "SQL", "Deep Learning"],
        },
        {
            "title": "Data Analyst",
            "description": "Work with SQL & dashboards to deliver insights.",
            "skill_names": ["SQL", "Data Visualization", "Communication"],
        },
        {
            "title": "ML Engineer",
            "description": "Deploy machine learning solutions to production.",
            "skill_names": ["Python", "Machine Learning", "Cloud Computing"],
        },
    ]

    print("Seeding jobs...")

    for job in jobs:
        job_obj = Job(
            title=job["title"],
            description=job["description"],
            skills=[skills[name] for name in job["skill_names"]],
        )
        db.add(job_obj)

    db.commit()
    print("✔ Jobs seeded.")


def seed_users(db):
    """Insert sample users."""
    existing = db.query(User).count()
    if existing > 0:
        print("✔ Users already exist. Skipping seed.")
        return

    skills = {s.name: s for s in db.query(Skill).all()}

    users = [
        {
            "name": "Alice",
            "education": "BSc Computer Science",
            "experience": "2 years in data analytics",
            "skill_names": ["Python", "SQL"],
        },
        {
            "name": "Bob",
            "education": "MSc Artificial Intelligence",
            "experience": "1 year ML research",
            "skill_names": ["Python", "Machine Learning"],
        },
    ]

    print("Seeding users...")

    for u in users:
        user_obj = User(
            name=u["name"],
            education=u["education"],
            experience=u["experience"],
            skills=[skills[n] for n in u["skill_names"]],
        )
        db.add(user_obj)

    db.commit()
    print("✔ Users seeded.")


def run_ingestion():
    db = SessionLocal()
    try:
        seed_skills(db)
        seed_jobs(db)
        seed_users(db)
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Running SQLAlchemy-only data ingestion...")
    run_ingestion()
    print("🎉 Data ingestion done.")
