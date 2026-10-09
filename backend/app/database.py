import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger("uvicorn")

# Default to local SQLite for fast, offline-first execution.
# To use Supabase or another PostgreSQL instance, set DATABASE_URL environment variable.
DEFAULT_SQLITE_URL = "sqlite:///./attendance.db"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)

def get_engine():
    if DATABASE_URL.startswith("sqlite"):
        return create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    
    # Try PostgreSQL or remote database with timeout
    try:
        eng = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args={"connect_timeout": 5})
        with eng.connect():
            pass
        print(f"[DB] Connected to remote database.")
        return eng
    except Exception as e:
        print(f"[DB Warning] Could not connect to {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL}: {e}")
        print("[DB Notice] Falling back to local SQLite database (attendance.db).")
        return create_engine(DEFAULT_SQLITE_URL, connect_args={"check_same_thread": False})

# Create the SQLAlchemy engine
engine = get_engine()

# Create a session maker to talk to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our database models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()