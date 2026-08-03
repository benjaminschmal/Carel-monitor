from pymodbus.client import ModbusTcpClient

from config import (
    MODBUS_HOST,
    MODBUS_PORT,
    MODBUS_SLAVE,
    REGISTER_START,
    REGISTER_END,
)


class ModbusClient:

    def __init__(self):

        self.client = ModbusTcpClient(
            host=MODBUS_HOST,
            port=MODBUS_PORT,
        )

    def connect(self):

        return self.client.connect()

    def disconnect(self):

        self.client.close()

    def read_all(self):

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
                slave=MODBUS_SLAVE,
            )

            if result.isError():
                raise RuntimeError(result)

            for offset, raw in enumerate(result.registers):

                register = start + offset

                signed = raw if raw < 32768 else raw - 65536

                registers[register] = {
                    "raw": raw,
                    "signed": signed,
                    "scaled": signed / 10,
                }

            start += count

        return registers