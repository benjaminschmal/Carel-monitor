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

    @staticmethod
    def _decode(raw):
        signed = raw if raw < 32768 else raw - 65536
        return {
            "raw": raw,
            "signed": signed,
            "scaled": signed / 10,
        }

    def read_register(self, register):
        """Read one CAREL register from the input-register space (FC4)."""
        result = self.client.read_input_registers(
            address=register,
            count=1,
            slave=MODBUS_SLAVE,
        )

        if result.isError():
            raise RuntimeError(result)

        return self._decode(result.registers[0])

    def read_all(self):
        """Read the configured CAREL input-register range (FC4).

        The Dimplex-based controller exposes the useful register space at
        R001...R209. The documented 300xx addresses are kept as documentation
        references; they are not passed directly to the controller.
        """
        registers = {}
        start = REGISTER_START

        while start <= REGISTER_END:
            count = min(125, REGISTER_END - start + 1)

            result = self.client.read_input_registers(
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
