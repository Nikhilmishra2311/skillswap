from sqlmodel import create_engine, Session
from app.core.config import DATABASE_URL

# Create engine (connection to DB)
engine = create_engine(DATABASE_URL, echo=True)

# Dependency for DB session
def get_session():
    with Session(engine) as session:
        yield session