from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import declarative_base


Base = declarative_base()


class RegisterCurrent(Base):
    """
    Enthält immer den aktuellsten Wert eines Registers.
    """

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
    """
    Historie aller Änderungen.
    """

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


class RegisterInfo(Base):
    """
    Beschreibung eines Registers.
    Wird später automatisch oder manuell gepflegt.
    """

    __tablename__ = "register_info"

    register = Column(Integer, primary_key=True)

    name = Column(String(100))

    unit = Column(String(20))

    description = Column(String(500))