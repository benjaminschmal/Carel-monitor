from datetime import datetime

from database import SessionLocal
from models import RegisterCurrent
from models import RegisterHistory


class Storage:

    def __init__(self):

        self.session = SessionLocal()

    def save(self, register, raw, signed, scaled):

        current = self.session.get(
            RegisterCurrent,
            register,
        )

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

        self.session.add(

            RegisterHistory(

                timestamp=datetime.now(),

                register=register,

                raw=raw,

                signed=signed,

                scaled=scaled,

            )

        )

    def commit(self):

        self.session.commit()