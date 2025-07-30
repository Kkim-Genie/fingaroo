from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings

settings = get_settings()

SQLALCHEMY_DATABASE_URL = (
    "postgresql://"
    f"{settings.SUPABASE_USER}:{settings.SUPABASE_PASSWORD}"
    f"@{settings.SUPABASE_HOST}/postgres"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()