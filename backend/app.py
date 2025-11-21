from fastapi import FastAPI
from database import init_db
from pydantic import BaseModel
import joblib
import json
import os

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

MODEL_PATH = "models/recommendation_model.pkl"
SKILL_MAP_PATH = "models/skill_map.json"

model = joblib.load(MODEL_PATH)
skill_map = json.load(open(SKILL_MAP_PATH, "r"))

class Profile(BaseModel):
    education: str
    coursework: list[str]
    skills: list[str]

@app.get("/")
def health():
    return {"status": "backend running"}

@app.post("/recommend")
def recommend(profile: Profile):
    # Very simple scoring for prototype purposes
    user_skills = set(profile.skills)

    scored = []
    for role, role_skills in skill_map.items():
        role_skills = set(role_skills)
        score = len(user_skills & role_skills)
        missing = list(role_skills - user_skills)
        scored.append({
            "role": role,
            "match_score": score,
            "missing_skills": missing
        })

    scored = sorted(scored, key=lambda x: x["match_score"], reverse=True)
    return {"recommendations": scored[:5]}
