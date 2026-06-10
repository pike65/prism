from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DB_DIR = Path(__file__).resolve().parent
STORAGE_DIR = DB_DIR / "storage"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_URL = f"sqlite:///{STORAGE_DIR}/prism.db"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
