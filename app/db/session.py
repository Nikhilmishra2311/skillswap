from sqlmodel import create_engine, Session
from app.core.config import settings

# Create engine (connection to DB)
engine = create_engine(settings.DATABASE_URL, echo=True)

# Dependency for DB session
def get_session():
    with Session(engine) as session:
        yield session