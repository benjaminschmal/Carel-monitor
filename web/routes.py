from fastapi import APIRouter
from sqlalchemy import select

from config import DEVICE_MODEL, DEVICE_TECHNOLOGY, MODBUS_HOST, MODBUS_PORT, MODBUS_SLAVE
from database import SessionLocal
from models import RegisterCurrent

from register_config import REGISTER_MAP

router = APIRouter()

_system_status = {
    "register": 30006,
    "raw": None,
    "mode": "Nicht verfügbar",
}

STATUS_MODES = {
    2: "Normalbetrieb",
}


def set_system_status(status: dict) -> None:
    raw = status.get("raw")
    _system_status["raw"] = raw
    _system_status["mode"] = STATUS_MODES.get(raw, f"Status {raw}" if raw is not None else "Nicht verfügbar")


@router.get("/api/status")
def status():
    return {"status": "online"}


@router.get("/api/device")
def device():
    return {
        "model": DEVICE_MODEL,
        "technology": DEVICE_TECHNOLOGY,
        "host": MODBUS_HOST,
        "port": MODBUS_PORT,
        "slave": MODBUS_SLAVE,
    }


@router.get("/api/system")
def system():
    return _system_status


@router.get("/api/registers")
def registers():

    session = SessionLocal()

    try:

        result = session.execute(
            select(RegisterCurrent)
        )

        registers = []

        for row in result.scalars():

            config = REGISTER_MAP.get(row.register, {})

            registers.append({
                "register": row.register,
                "name": config.get("name", f"R{row.register:03d}"),
                "unit": config.get("unit", ""),
                "favorite": config.get("favorite", False),
                "raw": row.raw,
                "signed": row.signed,
                "scaled": row.scaled,
                "updated": row.updated.isoformat(),
            })

        registers.sort(key=lambda r: r["register"])

        return registers

    finally:
        session.close()
