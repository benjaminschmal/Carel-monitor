# CAREL Monitor

[![Docker Build](https://github.com/benjaminschmal/Carel-monitor/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/benjaminschmal/Carel-monitor/actions/workflows/docker-publish.yml)

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
- Docker deployment
- GitHub Actions Docker image build
- GitHub Container Registry (GHCR) publishing

The monitor has been tested against a real CAREL controller and deployed successfully on a QNAP NAS.

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

- `LOG_LEVEL`

The actual network addresses, MAC addresses and credentials are not stored in the repository.

## Local development

Install the Python dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Copy the example configuration and adjust it for your environment:

```bash
cp .env.example .env
```

Set the required CAREL and MQTT values in `.env`, then start the complete application:

```bash
python3 main.py
```

The dashboard is available on:

```text
http://localhost:8000
```

## Docker image

Build the image locally:

```bash
docker build -t carel-monitor:latest .
```

The container exposes the web dashboard on port `8000`.

## Docker Image via GitHub Container Registry

The repository automatically builds and publishes the Docker image using **GitHub Actions** whenever changes are pushed to the `main` branch.

The published image is available at:

```text
ghcr.io/benjaminschmal/carel-monitor:latest
```

A second image tag containing the Git commit SHA is also published for reproducible deployments.

The workflow is located at:

```text
.github/workflows/docker-publish.yml
```

The **Docker Build** badge at the top of this README shows the current status of this workflow. It is green when the latest workflow run succeeded and red when the build or publishing failed.

## QNAP Container Station – Application deployment

The recommended QNAP deployment uses a **Container Station Application** based on the repository's `compose.yaml` file. This is intentionally different from creating a single standalone container.

The application uses the published GHCR image:

```text
ghcr.io/benjaminschmal/carel-monitor:latest
```

The Compose configuration is stored in:

```text
compose.yaml
```

It defines:

- Application service: `carel-monitor`
- Container name: `carel-monitor-1`
- Web dashboard: `8000:8000`
- Persistent SQLite data: `./data:/app/data`
- Automatic restart: `unless-stopped`
- Container healthcheck
- All CAREL, MQTT and web configuration as environment variables

### Create the Application in QNAP Container Station

In Container Station, create a new **Application** and use the repository's `compose.yaml` as the application definition.

The image is pulled from GHCR; the QNAP does not need to build the Docker image locally.

Before starting the application, set the installation-specific values for:

```text
CAREL_HOST
CAREL_PORT
CAREL_SLAVE
CAREL_TIMEOUT
REGISTER_START
REGISTER_END
SCAN_INTERVAL

MQTT_HOST
MQTT_PORT
MQTT_USERNAME
MQTT_PASSWORD
MQTT_BASE_TOPIC

WEB_HOST
WEB_PORT
LOG_LEVEL
```

The persistent data directory is mapped to `/app/data` so the SQLite database survives application/container recreation.

### QNAP network configuration

The repository intentionally does not contain the QNAP-specific network name, IP address, MAC address or MQTT credentials.

If a fixed container IP is required, configure the QNAP `qnet` network and the fixed MAC address in Container Station for the application/container. These values are installation-specific and must not be committed to the public repository.

The application architecture is:

```text
GitHub repository
       ↓
GitHub Actions
       ↓
Docker image build
       ↓
GitHub Container Registry (GHCR)
       ↓
QNAP Container Station
       ↓
Application
   └── carel-monitor-1
       ├── Web UI :8000
       └── SQLite /app/data
```

After a new version is pushed to `main`, GitHub Actions creates and publishes a new `latest` image. The QNAP Application can then be updated by pulling the latest image and recreating the service with the same application configuration.

## Security

Do not expose the web interface or MQTT broker directly to the Internet. Never commit credentials, MAC addresses or other private deployment details to the public repository.

## Project structure

```text
Carel-monitor/
├── core/
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
├── compose.yaml
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
- Docker image: working
- GitHub Actions / GHCR publishing: configured
- QNAP Container Station Application deployment: configured

## Development notes

The project is developed and tested locally first. The production deployment uses the published Docker image through QNAP Container Station.

Register mappings are intentionally added only when the meaning of a CAREL register is known. This prevents unknown register values from being presented as misleading Home Assistant entities.

Network addresses, MAC addresses, passwords and other private deployment details must remain outside the public repository.
