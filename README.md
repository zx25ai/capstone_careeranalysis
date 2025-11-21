🧠 Job Role Recommender System
Profile-aware job recommendations + skill-gap analysis + ML pipeline + interactive web UI

This repository contains a complete, end-to-end prototype of a Job Role Recommendation and Skill-Gap Analysis System.
It includes:

🔄 User profile ingestion pipeline

🧠 ML recommendation engine trained on real job role datasets

📊 Skill-gap analysis module

🌐 Responsive React UI

🗄️ PostgreSQL database

🐳 Fully Dockerized architecture

job-role-recommender/
├── README.md
├── docker-compose.yml
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
│
├── ml/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── train.py
│
├── etl/
│   └── ingest_example.py
│
├── db/
│   └── init.sql
│
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── index.html
    └── src/
        ├── main.jsx
        └── App.jsx

        🚀 Getting Started
1. Clone the repository
git clone https://github.com/<your-username>/job-role-recommender.git
cd job-role-recommender

2. Start all services with Docker
docker-compose up --build


Services start at:

Service	URL
Frontend	http://localhost:3000

Backend API	http://localhost:8000

PostgreSQL	localhost:5432
🧠 Architecture Overview
[Frontend (React)]  → calls →  [FastAPI Backend]  →  [ML Models + Skill Gap Engine]
                                              ↘
                                                [PostgreSQL Database]


React UI handles profile creation and visualizes skill gaps
FastAPI backend manages profiles, recommendations & gap calculations
ML service trains and stores job classifier models
PostgreSQL stores profiles, job roles & recommendations history

🧪 Testing the Pipeline
1. Visit the UI
👉 http://localhost:3000

2. Create a profile
Enter your name, email, and skills.

3. Click Get Recommendations
View top 5 recommended job roles + missing skills.

📌 Future Extensions
Semantic embeddings using sentence-transformers
Skill taxonomy + synonym resolution
Personal learning plan generation
Course recommendations (Coursera/LinkedIn API integration)


✅ How to Run the Full System (Local Setup Guide)
1. Prerequisites

Ensure you have installed:

✔ Python 3.10+
✔ Node.js 18+
✔ Docker Desktop
✔ Git
🗂 2. Clone Your Repository
git clone <your-repo-url>
cd job-role-recommender-system

🛢 3. Start PostgreSQL Using Docker

Inside the project root:
docker-compose up -d


This runs:
PostgreSQL @ localhost:5432
pgAdmin @ localhost:8081
With volumes for persistence

To verify PostgreSQL is running:
docker ps

🧠 4. Install & Run the Backend (FastAPI)
➤ Navigate to backend
cd backend

➤ Create virtual environment
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows

➤ Install dependencies
pip install -r requirements.txt

➤ Run database migrations / init script
python init_db.py

➤ (Optional) Ingest sample data
Includes jobs, skills, mappings.

python data_ingestion.py

➤ Train the recommendation model
(This creates model.joblib inside backend/models/.)

python train_model.py

➤ Run FastAPI server
uvicorn main:app --reload


FastAPI now runs at:
👉 http://127.0.0.1:8000

Interactive API docs:
👉 http://127.0.0.1:8000/docs

🎨 5. Run the Frontend (React + Vite)
➤ Open new terminal
cd frontend
npm install
npm run dev


Frontend will run at:
👉 http://localhost:5173

🔗 6. System Flow (End-to-End)
1. User goes to frontend

→ fills profile info, coursework, etc.

2. Frontend sends request to backend
→ /recommendations
→ /skill-gaps
→ /profile

3. Backend loads ML model
→ transforms user skills
→ finds similar job embeddings
→ computes skill gaps
→ responds with JSON

4. Frontend visualizes:
✔ Job role cards
✔ Spider/radar charts
✔ Skill-gap bar chart
✔ Suggested learning path

🧪 7. Test the System
Test API directly:
curl -X POST "http://127.0.0.1:8000/recommend" \
     -H "Content-Type: application/json" \
     -d '{
           "skills": ["python", "sql", "data analysis"]
         }'

Test skill gaps:
curl -X POST "http://127.0.0.1:8000/skill-gaps" \
     -H "Content-Type: application/json" \
     -d '{
           "role": "Data Analyst",
           "skills": ["python", "excel"]
         }'

🚀 8. Optional: Start Everything With One Command
Add this to root Makefile:

run:
	docker-compose up -d
	cd backend && uvicorn main:app --reload


Run:

make run

🎉 You're Done!

You now have a fully functional job-role recommender system with:

ETL pipeline

ML model

FastAPI backend

React frontend

Skill-gap visualization

Dockerized database

Authentication & user accounts
