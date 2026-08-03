from datetime import datetime

from sqlalchemy.orm import Session

from models import RegisterCurrent
from models import RegisterHistory


class Storage:

    def __init__(self, session: Session):
        self.session = session

    def save_register(
        self,
        register: int,
        raw: int,
        signed: int,
        scaled: float,
    ):

        current = self.session.get(RegisterCurrent, register)

        if current is None:

            current = RegisterCurrent(
                register=register,
                raw=raw,
                signed=signed,
                scaled=scaled,
                updated=datetime.now(),
            )

            self.session.add(current)

        else:

            current.raw = raw
            current.signed = signed
            current.scaled = scaled
            current.updated = datetime.now()

        history = RegisterHistory(
            timestamp=datetime.now(),
            register=register,
            raw=raw,
            signed=signed,
            scaled=scaled,
        )

        self.session.add(history)

    def commit(self):
        self.session.commit()