import os
from dataclasses import dataclass


@dataclass(frozen=True)
class MqttConfig:
    host: str | None
    port: int
    username: str | None
    password: str | None
    base_topic: str

    @property
    def enabled(self) -> bool:
        return bool(self.host)

    @classmethod
    def from_environment(cls) -> "MqttConfig":
        return cls(
            host=os.getenv("MQTT_HOST"),
            port=int(os.getenv("MQTT_PORT", "1883")),
            username=os.getenv("MQTT_USERNAME"),
            password=os.getenv("MQTT_PASSWORD"),
            base_topic=os.getenv("MQTT_BASE_TOPIC", "carel/monitor"),
        )
