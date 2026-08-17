# CAREL Monitor

CAREL monitoring service for reading controller values via **Modbus TCP**, storing the values locally and publishing selected values via **MQTT**.

The project also publishes **Home Assistant MQTT Discovery** configuration so mapped CAREL values appear automatically as sensors in Home Assistant.

## Features

- Modbus TCP connection to a CAREL controller
- Register scanning with configurable register range
- Signed 16-bit value handling
- Configurable scaling of register values
- Current values and historical values stored in SQLite
- Web dashboard with register overview
- Configurable register mapping and names
- MQTT publishing of changed register values
- MQTT availability status (`online` / `offline`)
- Home Assistant MQTT Discovery
- Discovery only for registers that are explicitly mapped
- Environment-based configuration
- Docker-ready deployment

The monitor has been tested against a real CAREL controller.

## Current register mapping

Only registers with known information are published to Home Assistant via MQTT Discovery.

The current mapping is maintained in `register_config.py`:

| Register | Name | Unit |
|---|---|---|
| R002 | Vorlauf | °C |
| R003 | Rücklauf | °C |
| R006 | Außentemperatur | °C |

Additional registers can be added to the mapping when their meaning is known.

Unmapped registers continue to be read and stored by the monitor, but no Home Assistant Discovery entity is created for them.

## MQTT topics

The default MQTT base topic is:

```text
carel/monitor
```

Register values are published below:

```text
carel/monitor/register/002
carel/monitor/register/003
carel/monitor/register/006
```

The payload contains the register information as JSON, for example:

```json
{
  "register": 6,
  "raw": 122,
  "signed": 122,
  "scaled": 12.2
}
```

Availability is published to:

```text
carel/monitor/status
```

with the values:

```text
online
offline
```

## Home Assistant

The MQTT integration must already be configured in Home Assistant and connected to the same MQTT broker used by the CAREL Monitor.

No YAML sensor definitions are required.

When the monitor connects to MQTT, it publishes retained Home Assistant MQTT Discovery configuration for the registers defined in `register_config.py`.

Discovery topics use the following structure:

```text
homeassistant/sensor/carel_r002/config
homeassistant/sensor/carel_r003/config
homeassistant/sensor/carel_r006/config
```

The sensors use the CAREL Monitor device and the MQTT availability topic automatically.

For temperature values (`°C`), Home Assistant receives the appropriate temperature device class and measurement state class.

## Configuration

The CAREL controller connection is configured via environment variables:

- `CAREL_HOST`
- `CAREL_PORT`
- `CAREL_SLAVE`
- `CAREL_TIMEOUT`
- `REGISTER_START`
- `REGISTER_END`
- `SCAN_INTERVAL`

MQTT is configured via:

- `MQTT_HOST`
- `MQTT_PORT`
- `MQTT_USERNAME`
- `MQTT_PASSWORD`
- `MQTT_BASE_TOPIC`

Webserver configuration:

- `WEB_HOST`
- `WEB_PORT`

Other configuration:

- `DATA_DIR`
- `LOG_LEVEL`

The actual network addresses and credentials are not stored in the repository.

## Local development

Install the Python dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Set the CAREL controller address:

```bash
export CAREL_HOST=192.168.1.x
```

Set MQTT configuration if MQTT should be enabled:

```bash
export MQTT_HOST=192.168.1.x
export MQTT_PORT=1883
export MQTT_USERNAME=mqtt
export MQTT_PASSWORD=<password>
```

Start the complete application:

```bash
python3 main.py
```

The application starts the web dashboard and the CAREL scanner together.

The dashboard is available on:

```text
http://localhost:8000
```

## Docker

The project is prepared for Docker deployment.

The container runs the same `main.py` entry point used during local development, so the web dashboard and CAREL scanner run together.

The SQLite data directory should be mounted as a persistent volume so historical data survives container recreation.

Example runtime configuration:

```text
CAREL_HOST=192.168.1.x
CAREL_PORT=502
CAREL_SLAVE=1
CAREL_TIMEOUT=3
SCAN_INTERVAL=5

MQTT_HOST=192.168.1.x
MQTT_PORT=1883
MQTT_USERNAME=mqtt
MQTT_PASSWORD=<password>
MQTT_BASE_TOPIC=carel/monitor
```

Do not commit real passwords, private network details or other credentials to the repository.

## Project structure

```text
Carel-monitor/
├── core/
│   ├── modbus_client.py
│   ├── scanner.py
│   └── storage.py
├── static/
├── templates/
├── test/
├── data/
├── app.py
├── config.py
├── database.py
├── main.py
├── mqtt_client.py
├── mqtt_config.py
├── register_config.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Status

Current implementation status:

- Modbus TCP: working
- Register scanning: working
- SQLite storage: working
- Web dashboard: working
- MQTT publishing: working
- Home Assistant MQTT Discovery: working
- Docker deployment: prepared, not yet validated on the QNAP

## Development notes

The project is developed and tested locally first. Deployment to the QNAP is performed separately using Docker.

Register mappings are intentionally added only when the meaning of a CAREL register is known. This prevents unknown register values from being presented as misleading Home Assistant entities.
