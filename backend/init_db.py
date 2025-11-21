# backend/init_db.py
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://pguser:pgpass@localhost:5432/jobrec")
INIT_SQL_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "init.sql")

def wait_for_db(engine, timeout=60):
    start = time.time()
    while True:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except OperationalError:
            if time.time() - start > timeout:
                raise
            print("Waiting for database... retrying in 2s")
            time.sleep(2)

def run_init():
    engine = create_engine(DATABASE_URL)
    print("Waiting for DB...")
    wait_for_db(engine)
    print("DB available. Running init SQL if present.")
    if os.path.exists(INIT_SQL_PATH):
        sql = open(INIT_SQL_PATH, "r", encoding="utf-8").read()
        with engine.begin() as conn:
            conn.execute(text(sql))
        print(f"Executed {INIT_SQL_PATH}")
    else:
        print("No init.sql found at", INIT_SQL_PATH)
        # Optionally create tables programmatically if you prefer

if __name__ == "__main__":
    run_init()
