import os
from pathlib import Path

# ------------------------------------------------------------
# CAREL Controller
# ------------------------------------------------------------

MODBUS_HOST = os.getenv("CAREL_HOST", "127.0.0.1")
MODBUS_PORT = int(os.getenv("CAREL_PORT", "502"))
MODBUS_SLAVE = int(os.getenv("CAREL_SLAVE", "1"))
MODBUS_TIMEOUT = float(os.getenv("CAREL_TIMEOUT", "3"))

REGISTER_START = int(os.getenv("REGISTER_START", "1"))
REGISTER_END = int(os.getenv("REGISTER_END", "209"))

# Dimplex/Weishaupt system operating status (Modbus input register 30006).
# Kept separate from the CAREL Rxxx holding-register scan.
STATUS_REGISTER = int(os.getenv("STATUS_REGISTER", "30006"))

SCAN_INTERVAL = float(os.getenv("SCAN_INTERVAL", "5"))

# ------------------------------------------------------------
# Device information
# ------------------------------------------------------------

DEVICE_MODEL = "Weishaupt WWP S 8 ID"
DEVICE_TECHNOLOGY = "Dimplex Wärmepumpenmanager"

# ------------------------------------------------------------
# Projektpfade
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = Path(os.getenv("DATA_DIR", str(BASE_DIR / "data")))
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_FILE = DATA_DIR / "carel.db"

DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# ------------------------------------------------------------
# Webserver
# ------------------------------------------------------------

WEB_HOST = os.getenv("WEB_HOST", "0.0.0.0")
WEB_PORT = int(os.getenv("WEB_PORT", "8000"))

# ------------------------------------------------------------
# Logging
# ------------------------------------------------------------

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
