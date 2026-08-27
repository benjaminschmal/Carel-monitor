from pymodbus.client import ModbusTcpClient

from config import (
    MODBUS_HOST,
    MODBUS_PORT,
    MODBUS_SLAVE,
    REGISTER_START,
    REGISTER_END,
    STATUS_REGISTER,
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

    @staticmethod
    def _decode(raw):
        signed = raw if raw < 32768 else raw - 65536
        return {
            "raw": raw,
            "signed": signed,
            "scaled": signed / 10,
        }

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
                registers[register] = self._decode(raw)

            start += count

        return registers

    def read_status(self):
        """Read Dimplex/Weishaupt operating status from input register 30006."""
        address = STATUS_REGISTER - 30001

        result = self.client.read_input_registers(
            address=address,
            count=1,
            slave=MODBUS_SLAVE,
        )

        if result.isError():
            raise RuntimeError(result)

        raw = result.registers[0]

        return {
            "register": STATUS_REGISTER,
            "raw": raw,
            "value": raw,
        }
