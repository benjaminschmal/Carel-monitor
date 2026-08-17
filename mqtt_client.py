import json
import logging
from typing import Any

import paho.mqtt.client as mqtt

from mqtt_config import MqttConfig


logger = logging.getLogger(__name__)


class MqttClient:

    def __init__(self, config: MqttConfig):
        self.config = config
        self.connected = False

        self._client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id="carel-monitor",
        )

        if config.username:
            self._client.username_pw_set(
                config.username,
                config.password,
            )

        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect

    def _on_connect(
        self,
        client: mqtt.Client,
        userdata: Any,
        flags: Any,
        reason_code: Any,
        properties: Any,
    ) -> None:
        if reason_code == 0:
            self.connected = True
            logger.info(
                "Connected to MQTT broker %s:%s",
                self.config.host,
                self.config.port,
            )
            self.publish_status("online")
        else:
            self.connected = False
            logger.error("MQTT connection failed: %s", reason_code)

    def _on_disconnect(
        self,
        client: mqtt.Client,
        userdata: Any,
        disconnect_flags: Any,
        reason_code: Any,
        properties: Any,
    ) -> None:
        self.connected = False
        logger.info("Disconnected from MQTT broker: %s", reason_code)

    def connect(self) -> bool:
        if not self.config.enabled:
            return False

        try:
            self._client.connect(
                self.config.host,
                self.config.port,
                10,
            )
            self._client.loop_start()
            return True
        except Exception:
            logger.exception("Could not connect to MQTT broker")
            return False

    def publish(
        self,
        topic: str,
        payload: str,
        retain: bool = False,
    ) -> bool:
        if not self.connected:
            return False

        try:
            result = self._client.publish(
                topic,
                payload,
                qos=0,
                retain=retain,
            )
            return result.rc == mqtt.MQTT_ERR_SUCCESS
        except Exception:
            logger.exception("MQTT publish failed: %s", topic)
            return False

    def publish_status(self, status: str) -> bool:
        return self.publish(
            f"{self.config.base_topic}/status",
            status,
            retain=True,
        )

    def publish_register(
        self,
        register: int,
        value: dict,
    ) -> bool:
        payload = json.dumps(
            {
                "register": register,
                **value,
            },
            separators=(",", ":"),
        )

        return self.publish(
            f"{self.config.base_topic}/register/{register:03d}",
            payload,
            retain=True,
        )

    def disconnect(self) -> None:
        if not self.config.enabled:
            return

        try:
            if self.connected:
                self.publish_status("offline")
            self._client.loop_stop()
            self._client.disconnect()
        finally:
            self.connected = False
