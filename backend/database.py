# database.py
from sqlalchemy import create_engine, text

# Use environment variables for security
import os

DB_USER = os.getenv("DB_USER", "postgres")     # Adjust to your username
DB_PASS = os.getenv("DB_PASS", "unopsql")     # Adjust to your password
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "dragonFruit")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

# Test connection
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.scalar()
        print(f"✅ Connected to PostgreSQL: {version}")
except Exception as e:
    print(f"❌ Failed to connect: {e}")