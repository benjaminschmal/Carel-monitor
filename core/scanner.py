import time

from config import SCAN_INTERVAL

from core.modbus_client import ModbusClient
from core.storage import Storage


class Scanner:

    def __init__(self):

        self.client = ModbusClient()

        self.storage = Storage()

        self.last = {}

    def run(self):

        if not self.client.connect():

            raise RuntimeError(
                "Keine Verbindung."
            )

        print("✅ Verbunden")

        while True:

            registers = self.client.read_all()

            changed = 0

            for register, value in registers.items():

                raw = value["raw"]

                if self.last.get(register) == raw:

                    continue

                self.last[register] = raw

                self.storage.save(

                    register,

                    raw,

                    value["signed"],

                    value["scaled"],

                )

                print(

                    f"R{register:03d} = "

                    f"{value['scaled']:.1f}"

                )

                changed += 1

            if changed:

                self.storage.commit()

            time.sleep(SCAN_INTERVAL)