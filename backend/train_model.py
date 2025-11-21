# backend/train_model.py
import os
import joblib
import json
from sqlalchemy import create_engine, text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://pguser:pgpass@localhost:5432/jobrec")
engine = create_engine(DATABASE_URL)

def load_job_roles():
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT id, title, description, required_skills FROM job_roles")).fetchall()
    return [dict(r) for r in rows]

def build_dataset(rows):
    texts = []
    labels = []
    for r in rows:
        skills = r.get("required_skills") or []
        if isinstance(skills, str):
            try:
                skills = json.loads(skills)
            except:
                skills = [skills]
        combined = f"{r.get('title','')} {r.get('description','')} " + " ".join(skills)
        texts.append(combined)
        labels.append(r["id"])
    return texts, labels

def train_and_save():
    rows = load_job_roles()
    if not rows:
        raise RuntimeError("No job roles found in DB — run init/data_ingestion first.")
    texts, labels = build_dataset(rows)
    vec = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
    X = vec.fit_transform(texts)
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X, labels)
    os.makedirs("models", exist_ok=True)
    joblib.dump(vec, os.path.join("models", "vectorizer.joblib"))
    joblib.dump(clf, os.path.join("models", "clf.joblib"))
    print("Model training complete. Saved to ./models/")

if __name__ == "__main__":
    train_and_save()
