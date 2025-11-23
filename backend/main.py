from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from sqlalchemy import create_engine, text
from fastapi.middleware.cors import CORSMiddleware
import os
import joblib
import json

app = FastAPI(title="Job Role Recommender API")

# Enable CORS BEFORE routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Load ML model
MODEL_PATH = "./models"
try:
    clf = joblib.load(f"{MODEL_PATH}/clf.joblib")
except:
    clf = None


# -----------------------------
# Pydantic Profile schema
# -----------------------------
class Profile(BaseModel):
    name: str
    email: str
    summary: str = ""
    education: Dict[str, Any] = {}
    coursework: List[str] = []
    skills: List[str] = []


# -----------------------------
# Create Profile
# -----------------------------
@app.post("/profiles")
def create_profile(profile: Profile):
    with engine.begin() as conn:
        res = conn.execute(
            text("""
                INSERT INTO users (name, email, summary, education, coursework, skills)
                VALUES (:name, :email, :summary, :education, :coursework, :skills)
                RETURNING id
            """),
            {
                "name": profile.name,
                "email": profile.email,
                "summary": profile.summary,
                "education": json.dumps(profile.education),
                "coursework": json.dumps(profile.coursework),
                "skills": json.dumps(profile.skills),
            },
        )
        uid = res.scalar()

    return {"status": "ok", "user_id": uid}


# -----------------------------
# Get Job Roles
# -----------------------------
@app.get("/job_roles")
def get_job_roles():
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT id, title, description, required_skills, seniority FROM job_roles")
        ).fetchall()
    return [dict(r) for r in rows]


# -----------------------------
# Recommendation Endpoint
# -----------------------------
@app.get("/recommend/{user_id}")
def recommend(user_id: int):

    # Fetch user + job roles in one connection
    with engine.connect() as conn:
        user = conn.execute(
            text("SELECT * FROM users WHERE id = :id"),
            {"id": user_id},
        ).fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        job_roles = conn.execute(
            text("SELECT id, title, required_skills FROM job_roles")
        ).fetchall()

    user_skills = set(json.loads(user["skills"] or "[]"))
    recs = []

    for jr in job_roles:
        req = set(json.loads(jr["required_skills"] or "[]"))

        overlap = len(req & user_skills)
        score = overlap / max(1, len(req))
        missing = list(req - user_skills)

        recs.append(
            {
                "job_role_id": jr["id"],
                "title": jr["title"],
                "score": score,
                "missing_skills": missing,
            }
        )

    recs = sorted(recs, key=lambda x: x["score"], reverse=True)

    # Save top 5 recommendations
    with engine.begin() as conn:
        for r in recs[:5]:
            conn.execute(
                text("""
                    INSERT INTO recommendations (user_id, job_role_id, score, gap_summary)
                    VALUES (:u, :j, :s, :g)
                """),
                {
                    "u": user_id,
                    "j": r["job_role_id"],
                    "s": r["score"],
                    "g": json.dumps(r["missing_skills"]),
                },
            )

    return {"recommendations": recs[:5]}


# -----------------------------
# Gap Analysis
# -----------------------------
@app.get("/gap/{user_id}/{job_role_id}")
def gap(user_id: int, job_role_id: int):
    with engine.connect() as conn:
        user = conn.execute(
            text("SELECT skills FROM users WHERE id = :id"),
            {"id": user_id},
        ).fetchone()

        job = conn.execute(
            text("SELECT required_skills FROM job_roles WHERE id = :id"),
            {"id": job_role_id},
        ).fetchone()

    if not user or not job:
        raise HTTPException(status_code=404, detail="Not found")

    user_skills = set(json.loads(user["skills"] or "[]"))
    req_skills = set(json.loads(job["required_skills"] or "[]"))

    missing = list(req_skills - user_skills)
    overlap = list(req_skills & user_skills)

    plan = [{"skill": s, "priority": "high"} for s in missing]

    return {"missing": missing, "overlap": overlap, "plan": plan}
