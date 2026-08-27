import time

from config import SCAN_INTERVAL
from mqtt_client import MqttClient
from mqtt_config import MqttConfig

from core.modbus_client import ModbusClient
from core.storage import Storage


class Scanner:

    def __init__(self):
        self.client = ModbusClient()
        self.storage = Storage()
        self.mqtt = MqttClient(MqttConfig.from_environment())
        self.last = {}

    def run(self):
        if not self.client.connect():
            raise RuntimeError("Keine Verbindung.")

        print("✅ Verbunden")

        if self.mqtt.config.enabled:
            if self.mqtt.connect():
                print("📡 MQTT verbunden")
            else:
                print("⚠️ MQTT nicht verfügbar – Scanner läuft weiter")

        try:
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

                    if self.mqtt.connected:
                        self.mqtt.publish_register(register, value)

                    print(f"R{register:03d} = {value['scaled']:.1f}")
                    changed += 1

                if changed:
                    self.storage.commit()

                time.sleep(SCAN_INTERVAL)

        finally:
            self.mqtt.disconnect()
            self.client.disconnect()
