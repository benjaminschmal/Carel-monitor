from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class RegisterCurrent(Base):

    __tablename__ = "register_current"

    register = Column(Integer, primary_key=True)

    raw = Column(Integer, nullable=False)

    signed = Column(Integer, nullable=False)

    scaled = Column(Float, nullable=False)

    updated = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class RegisterHistory(Base):

    __tablename__ = "register_history"

    id = Column(Integer, primary_key=True, autoincrement=True)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    register = Column(Integer, index=True, nullable=False)

    raw = Column(Integer, nullable=False)

    signed = Column(Integer, nullable=False)

    scaled = Column(Float, nullable=False)