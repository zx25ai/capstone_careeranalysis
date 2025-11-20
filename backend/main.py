from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from sqlalchemy import create_engine, text
import os
import joblib


DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)


app = FastAPI(title='Job Role Recommender API')


# Load models (trained by ml service) from /app/models
MODEL_PATH = './models'
try:
clf = joblib.load(f'{MODEL_PATH}/clf.joblib')
emb_model = None
except Exception as e:
clf = None


class Profile(BaseModel):
name: str
email: str
summary: str = ''
education: Dict[str, Any] = {}
coursework: List[str] = []
skills: List[str] = []


@app.post('/profiles')
def create_profile(profile: Profile):
with engine.begin() as conn:
res = conn.execute(text("INSERT INTO users (name,email,summary,education,coursework,skills) VALUES (:name,:email,:summary,:education,:coursework,:skills) RETURNING id"),
{"name":profile.name, "email":profile.email, "summary":profile.summary, "education":profile.education, "coursework":profile.coursework, "skills":profile.skills})
uid = res.scalar()
return {"status":"ok","user_id":uid}


@app.get('/job_roles')
def get_job_roles():
with engine.connect() as conn:
rows = conn.execute(text('SELECT id, title, description, required_skills, seniority FROM job_roles')).fetchall()
return [dict(r) for r in rows]


@app.get('/recommend/{user_id}')
def recommend(user_id: int):
# simple flow: load user, featurize, call classifier, compute top N, compute gap
with engine.connect() as conn:
user = conn.execute(text('SELECT * FROM users WHERE id=:id'),{"id":user_id}).fetchone()
if not user:
raise HTTPException(status_code=404, detail='User not found')
user_skills = user['skills'] or []
job_roles = conn.execute(text('SELECT id, title, required_skills FROM job_roles')).fetchall()


# If clf is available, use it. Otherwise fall back to simple vector overlap scoring.
recs = []
for jr in job_roles:
req = jr['required_skills'] or []
# score = overlap / len(req)
overlap = len(set(map(str.lower, req)).intersection(set(map(str.lower,user_skills))))
score = overlap / max(1,len(req))
missing = list(set(req) - set(user_skills))
recs.append({"job_role_id": jr['id'], "title": jr['title'], "score": score, "missing_skills": missing})


recs = sorted(recs, key=lambda x: x['score'], reverse=True)
# Save top 5 recommendations
with engine.begin() as conn:
for r in recs[:5]:
conn.execute(text('INSERT INTO recommendations (user_id, job_role_id, score, gap_summary) VALUES (:u,:j,:s,:g)'),
{"u":user_id, "j":r['job_role_id'], "s":r['score'], "g":r['missing_skills']})
return {"recommendations": recs[:5]}


@app.get('/gap/{user_id}/{job_role_id}')
def gap(user_id: int, job_role_id: int):
with engine.connect() as conn:
user = conn.execute(text('SELECT skills FROM users WHERE id=:id'),{"id":user_id}).fetchone()
job = conn.execute(text('SELECT required_skills FROM job_roles WHERE id=:id'),{"id":job_role_id}).fetchone()
if not user or not job:
raise HTTPException(status_code=404, detail='Not found')
user_skills = set(user['skills'] or [])
req_skills = set(job['required_skills'] or [])
missing = list(req_skills - user_skills)
overlap = list(req_skills & user_skills)
# simple priority: if missing skill in coursework or education -> lower priority
plan = []
for s in missing:
plan.append({"skill": s, "priority": "high"})
return {"missing": missing, "overlap": overlap, "plan": plan}
