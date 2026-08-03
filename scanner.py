import time

from database import SessionLocal, init_database

from core.modbus_client import CarelClient
from core.storage import Storage

from config import SCAN_INTERVAL


class CarelScanner:

    def __init__(self):

        init_database()

        self.session = SessionLocal()

        self.storage = Storage(self.session)

        self.client = CarelClient()

        self.last_values = {}

    def run(self):

        if not self.client.connect():
            print("❌ Keine Verbindung zum CAREL.")
            return

        print("✅ Verbunden")

        try:

            while True:

                registers = self.client.read_registers()

                changes = 0

                for register, value in registers.items():

                    raw = value["raw"]

                    if self.last_values.get(register) == raw:
                        continue

                    self.last_values[register] = raw

                    self.storage.save_register(
                        register=register,
                        raw=raw,
                        signed=value["signed"],
                        scaled=value["scaled"],
                    )

                    print(
                        f"R{register:03d}: "
                        f"{value['scaled']:.1f}"
                    )

                    changes += 1

                if changes:
                    self.storage.commit()

                time.sleep(SCAN_INTERVAL)

        finally:

            self.client.disconnect()


if __name__ == "__main__":

    scanner = CarelScanner()

    scanner.run()