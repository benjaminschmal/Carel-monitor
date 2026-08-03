from pymodbus.client import ModbusTcpClient

from config import (
    MODBUS_HOST,
    MODBUS_PORT,
    MODBUS_UNIT_ID,
    REGISTER_START,
    REGISTER_END,
)


class CarelClient:

    def __init__(self):

        self.client = ModbusTcpClient(
            host=MODBUS_HOST,
            port=MODBUS_PORT,
        )

    def connect(self):

        return self.client.connect()

    def disconnect(self):

        self.client.close()

    def read_registers(self):

        registers = {}

        start = REGISTER_START

        while start <= REGISTER_END:

            count = min(
                125,
                REGISTER_END - start + 1,
            )

            result = self.client.read_holding_registers(
                address=start,
                count=count,
                slave=MODBUS_UNIT_ID,
            )

            if result.isError():
                raise RuntimeError(result)

            for offset, value in enumerate(result.registers):

                register = start + offset

                signed = value if value < 32768 else value - 65536

                scaled = signed / 10

                registers[register] = {
                    "raw": value,
                    "signed": signed,
                    "scaled": scaled,
                }

            start += count

        return registers