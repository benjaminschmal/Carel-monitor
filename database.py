from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_FILE
from models import Base

DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def init_database():
    """
    Erstellt alle Tabellen, falls sie noch nicht existieren.
    """
    Base.metadata.create_all(bind=engine)