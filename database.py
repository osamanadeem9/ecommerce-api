import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv(
    "PG_DATABASE_URL", "postgresql://user:password@localhost:5432/database_name"
)
SECRET_KEY = os.getenv("SECRET_KEY")
print(f"DATABASE URL: {DATABASE_URL} {SECRET_KEY}")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
