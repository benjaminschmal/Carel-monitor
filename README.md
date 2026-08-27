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

## Current CAREL register mapping

The installed heat pump is a **Weishaupt WWP S 8 ID** with a Dimplex-based heat pump manager. The following CAREL holding registers have now been verified against the live installation and the Dimplex Modbus register documentation.

Only registers with known information are published to Home Assistant via MQTT Discovery.

The current active mapping is maintained in `register_config.py`:

| Register | Name | Unit | Favorite |
|---|---|---|---|
| R001 | Außentemperatur | °C | Yes |
| R002 | Rücklauf | °C | Yes |
| R003 | Warmwasser | °C | Yes |
| R005 | Vorlauf | °C | Yes |
| R006 | Wärmequelleneintritt | °C | No |
| R007 | Wärmequellenaustritt | °C | No |

### Verification

A live read of R001–R007 on the installed WWP S 8 ID returned:

```text
R001 = 18.2 °C  Außentemperatur
R002 = 22.6 °C  Rücklauf
R003 = 40.2 °C  Warmwasser
R004 = -8.8     unbekannt
R005 = 23.6 °C  Vorlauf
R006 = 23.0 °C  Wärmequelleneintritt
R007 = 23.5 °C  Wärmequellenaustritt
```

R004 is intentionally not mapped because its meaning has not yet been established.

Additional registers will be added only after their meaning has been established and, where possible, verified against the installed system.

Unmapped CAREL registers continue to be read and stored by the monitor, but no Home Assistant Discovery entity is created for them.

## Additional Weishaupt / Dimplex register knowledge

The installed **Weishaupt WWP S 8 ID** uses a Dimplex-based heat pump manager. The Dimplex Modbus documentation provides the following temperature register structure, which matches the live CAREL register values observed on the installation:

| Register | Meaning | Unit |
|---:|---|---|
| R001 | Außentemperatur | °C |
| R002 | Rücklauf | °C |
| R003 | Warmwasser | °C |
| R005 | Vorlauf | °C |
| R006 | Wärmequelleneintritt | °C |
| R007 | Wärmequellenaustritt | °C |

The values are represented as tenths of a degree Celsius for these temperature registers.

### SG-Ready investigation

The Weishaupt/Dimplex documentation also identifies SG-Ready-related data points for the heat pump manager. These are documented separately until their exact mapping to the current CAREL register space has been verified:

| Modbus address | Name | Access | Status |
|---:|---|---|---|
| 30006 | Betriebsstatusanzeige | R | documented |
| 35101 | SG-Ready 1 | R | documented |
| 35102 | SG-Ready 2 | R | documented |
| 40001 | Systembetriebsart | R/W | documented |
| 40002 | SollwertPV | R/W | documented |
| 42102 | Warmwasser Push | R/W | documented |
| 42103 | Warmwasser Normal | R/W | documented |
| 42104 | Warmwasser Absenk | R/W | documented |
| 42105 | SG-Ready Anhebung | R/W | documented; availability on the installed system still to be verified |

These addresses are **not automatically equivalent to CAREL Rxxx addresses**. Before any write operation is considered, the relevant data points must be verified on the installed system. The first test will remain read-only for `35101`, `35102` and `30006`.

The detailed investigation is documented in [`docs/weishaupt-wwp-sg-ready.md`](docs/weishaupt-wwp-sg-ready.md).

## MQTT topics

The default MQTT base topic is:

```text
carel/monitor
```

Register values are published below:

```text
carel/monitor/register/001
carel/monitor/register/002
carel/monitor/register/003
carel/monitor/register/005
carel/monitor/register/006
carel/monitor/register/007
```

The payload contains the register information as JSON, for example:

```json
{
  "register": 6,
  "raw": 230,
  "signed": 230,
  "scaled": 23.0
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

The active discovery topics are:

```text
homeassistant/sensor/carel_r001/config
homeassistant/sensor/carel_r002/config
homeassistant/sensor/carel_r003/config
homeassistant/sensor/carel_r005/config
homeassistant/sensor/carel_r006/config
homeassistant/sensor/carel_r007/config
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

## QNAP Container Station – standalone container

The recommended QNAP deployment uses a **standalone Docker container**, not a Container Station Application. This matches the deployment model used by the KACO MQTT Gateway and other standalone containers.

The container uses the published GHCR image:

```text
ghcr.io/benjaminschmal/carel-monitor:latest
```

### Create the container in QNAP Container Station

In Container Station choose **Create Container** and use:

```text
Registry: ghcr.io
Image: ghcr.io/benjaminschmal/carel-monitor:latest
```

Do not create an Application/Compose project.

Configure the container environment variables:

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

Map the web dashboard:

```text
Container port: 8000
```

For persistent SQLite data, map a QNAP folder to:

```text
/app/data
```

For example:

```text
/share/Container/Carel-monitor/data:/app/data
```

Use `restart: unless-stopped` or the corresponding Container Station restart policy.

### QNAP network configuration

The repository intentionally does not contain the QNAP-specific network name, IP address, MAC address or MQTT credentials.

If a fixed container IP is required, configure the QNAP `qnet` network and fixed MAC address directly in Container Station. These values are installation-specific and must not be committed to the public repository.

The deployment architecture is:

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
Standalone container
   └── carel-monitor-1
       ├── Web UI :8000
       └── SQLite /app/data
```

After a new version is pushed to `main`, GitHub Actions creates and publishes a new `latest` image. The QNAP container can then be updated by pulling the latest image and recreating the standalone container with the same configuration.

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
├── docs/
├── app.py
├── config.py
├── database.py
├── main.py
├── mqtt_client.py
├── mqtt_config.py
├── register_config.py
├── requirements.txt
├── Dockerfile
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
- QNAP standalone container deployment: configured
- WWP S 8 ID / Dimplex register mapping: verified for R001–R007 except R004
- SG-Ready Modbus investigation: in progress

## Development notes

The project is developed and tested locally first. The production deployment uses the published Docker image through QNAP Container Station.

Register mappings are intentionally added only when the meaning of a CAREL register is known. This prevents unknown register values from being presented as misleading Home Assistant entities.

Network addresses, MAC addresses, passwords and other private deployment details must remain outside the public repository.
