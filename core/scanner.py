import time

from config import SCAN_INTERVAL
from mqtt_client import MqttClient
from mqtt_config import MqttConfig

from core.modbus_client import ModbusClient
from core.storage import Storage
from web.routes import set_system_status


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

        mqtt_enabled = self.mqtt.config.enabled

        if mqtt_enabled:
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

                    print(
                        f"R{register:03d} = "
                        f"{value['scaled']:.1f}"
                    )

                    changed += 1

                if changed:
                    self.storage.commit()

                # Read Dimplex/Weishaupt operating status separately from
                # the CAREL Rxxx holding-register range.
                try:
                    system_status = self.client.read_status()
                    set_system_status(system_status)
                except Exception as exc:
                    print(f"⚠️ Betriebsstatus 30006 nicht lesbar: {exc}")

                time.sleep(SCAN_INTERVAL)

        finally:
            self.mqtt.disconnect()
            self.client.disconnect()
