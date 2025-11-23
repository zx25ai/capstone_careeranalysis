"""
Data ingestion for SQLAlchemy ORM models (no CRUD layer).
Seeds Skills, JobRoles, and Users safely.
"""
from database import SessionLocal, engine, Base
Base.metadata.create_all(bind=engine)
from models import Skill, JobRole, User


# ==============================
# SKILLS
# ==============================

def seed_skills(db):
    if db.query(Skill).count() > 0:
        print("✔ Skills already exist. Skipping.")
        return

    skill_names = [
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
    for name in skill_names:
        db.add(Skill(name=name))

    db.commit()
    print("✔ Skills seeded.")


# ==============================
# JOB ROLES
# ==============================

def seed_job_roles(db):
    if db.query(JobRole).count() > 0:
        print("✔ Job roles already exist. Skipping.")
        return

    skills = {s.name: s for s in db.query(Skill).all()}

    job_roles = [
        {
            "name": "Data Scientist",
            "description": "Build ML models and perform advanced data analysis.",
            "skill_names": ["Python", "Machine Learning", "SQL", "Deep Learning"],
        },
        {
            "name": "Data Analyst",
            "description": "Use SQL and dashboards to derive insights.",
            "skill_names": ["SQL", "Data Visualization", "Communication"],
        },
        {
            "name": "ML Engineer",
            "description": "Deploy and scale ML models in production.",
            "skill_names": ["Python", "Machine Learning", "Cloud Computing"],
        },
    ]

    print("Seeding job roles...")
    for role in job_roles:
        jr = JobRole(
            name=role["name"],
            description=role["description"],
            skills=[skills[n] for n in role["skill_names"]],
        )
        db.add(jr)

    db.commit()
    print("✔ Job roles seeded.")


# ==============================
# USERS
# ==============================

def seed_users(db):
    if db.query(User).count() > 0:
        print("✔ Users already exist. Skipping.")
        return

    skills = {s.name: s for s in db.query(Skill).all()}

    users = [
        {
            "name": "Alice",
            "education": "BSc Computer Science",
            "experience": "2 years in data analytics",
            "email": "alice_chien@gmeal.com",
            "skill_names": ["Python", "SQL"],
        },
        {
            "name": "Bob",
            "education": "MSc Artificial Intelligence",
            "experience": "1 year in ML research",
            "email": "bob_fagot@gmeal.com",
            "skill_names": ["Python", "Machine Learning"],
        },
    ]

    print("Seeding users...")
    for u in users:
        user = User(
            name=u["name"],
            education=u["education"],
            experience=u["experience"],
            email=u["email"],
            skills=[skills[n] for n in u["skill_names"]],
        )
        db.add(user)

    db.commit()
    print("✔ Users seeded.")


# ==============================
# MAIN EXECUTION
# ==============================

def run_ingestion():
    db = SessionLocal()
    try:
        seed_skills(db)
        seed_job_roles(db)
        seed_users(db)
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Running SQLAlchemy ORM data ingestion...")
    run_ingestion()
    print("🎉 Data ingestion complete!")
