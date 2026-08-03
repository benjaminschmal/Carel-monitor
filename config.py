from pathlib import Path

# ------------------------------------------------------------
# CAREL Controller
# ------------------------------------------------------------

MODBUS_HOST = "192.168.1.195"
MODBUS_PORT = 502
MODBUS_SLAVE = 1

REGISTER_START = 2
REGISTER_END = 209

SCAN_INTERVAL = 5  # Sekunden

# ------------------------------------------------------------
# Projektpfade
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_FILE = DATA_DIR / "carel.db"

DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# ------------------------------------------------------------
# Webserver
# ------------------------------------------------------------

WEB_HOST = "0.0.0.0"
WEB_PORT = 8000

# ------------------------------------------------------------
# Logging
# ------------------------------------------------------------

LOG_LEVEL = "INFO"