from fastapi import APIRouter
from sqlalchemy import select

from database import SessionLocal
from models import RegisterCurrent

from register_config import REGISTER_MAP

router = APIRouter()


@router.get("/api/status")
def status():

    return {
        "status": "online"
    }


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

                "name": config.get(
                    "name",
                    f"R{row.register:03d}"
                ),

                "unit": config.get(
                    "unit",
                    ""
                ),

                "favorite": config.get(
                    "favorite",
                    False
                ),

                "raw": row.raw,

                "signed": row.signed,

                "scaled": row.scaled,

                "updated": row.updated.isoformat()

            })

        registers.sort(
            key=lambda r: r["register"]
        )

        return registers

    finally:

        session.close()