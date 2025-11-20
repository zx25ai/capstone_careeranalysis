import os
import joblib
from sqlalchemy import create_engine, text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Load job roles
with engine.connect() as conn:
    rows = conn.execute(text("SELECT * FROM job_roles")).fetchall()

texts = []
labels = []

for r in rows:
    combined = f"{r['title']} {r['description']} " + " ".join(r['required_skills'])
    texts.append(combined)
    labels.append(r["id"])

vec = TfidfVectorizer(max_features=5000)
X = vec.fit_transform(texts)

clf = LogisticRegression(max_iter=1000)
clf.fit(X, labels)

os.makedirs("models", exist_ok=True)
joblib.dump(vec, "models/vectorizer.joblib")
joblib.dump(clf, "models/clf.joblib")

print("Training complete — models saved to /models")
