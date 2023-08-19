import datetime
import time
from fastapi import APIRouter, Depends, Response
import pytz
from sqlalchemy import select, update
from uuid import uuid4

from app.core.jwt import valid_request
from app.core.utils import get_time
from app.db.model import Bed, Patient
from app.db.session import get_db

router = APIRouter()


@router.get("")
async def get_all(res: Response, id: int = Depends(valid_request), db=Depends(get_db)):
    if id is None:
        res.status_code = 401
        return {
            "isOk": False,
            "data": "Invalid authentication credentials",
            "timestamp": get_time(),
        }

    print("id: ", id)
    beds = await db.execute(select(Bed).where(Bed.hospital_id == id))
    beds = beds.scalars().all()

    return {"isOk": True, "data": beds, "timestamp": get_time()}


@router.post("/in/{bed_id}", status_code=201)
async def bed_in(
    res: Response, bed_id: int, id: int = Depends(valid_request), db=Depends(get_db)
):
    if id is None:
        res.status_code = 401
        return {
            "isOk": False,
            "data": "Invalid authentication credentials",
            "timestamp": get_time(),
        }

    bed = await db.execute(select(Bed).where(Bed.id == bed_id))
    bed = bed.scalar_one_or_none()

    if bed is None:
        return {"isOk": False, "data": "Bed not found", "timestamp": get_time()}
    if bed.hospital_id != id:
        res.status_code = 403
        return {"isOk": False, "data": "Wrong hospital", "timestamp": get_time()}
    if bed.patient_id is not None:
        res.status_code = 400
        return {"isOk": False, "data": "Bed is not empty", "timestamp": get_time()}

    patient = Patient(id=str(uuid4())[:8], hospital_id=id)
    db.add(patient)

    await db.execute(update(Bed).where(Bed.id == bed_id).values(patient_id=patient.id))

    await db.commit()
    await db.refresh(bed)
    await db.refresh(patient)

    return {
        "isOk": True,
        "data": {"bed": bed, "patient": patient},
        "timestamp": get_time(),
    }


@router.post("/out/{bed_id}", status_code=201)
async def bed_out(
    res: Response, bed_id: int, id: int = Depends(valid_request), db=Depends(get_db)
):
    if id is None:
        res.status_code = 401
        return {
            "isOk": False,
            "data": "Invalid authentication credentials",
            "timestamp": get_time(),
        }

    bed = await db.execute(select(Bed).where(Bed.id == bed_id))
    bed = bed.scalar_one_or_none()

    if bed is None:
        return {"isOk": False, "data": "Bed not found", "timestamp": get_time()}
    if bed.hospital_id != id:
        res.status_code = 403
        return {"isOk": False, "data": "Wrong hospital", "timestamp": get_time()}
    if bed.patient_id is None:
        res.status_code = 400
        return {"isOk": False, "data": "Bed is empty", "timestamp": get_time()}

    current_time_with_tz = datetime.datetime.now(pytz.utc)
    await db.execute(
        update(Patient)
        .where(Patient.id == bed.patient_id)
        .values(deleted_at=current_time_with_tz)
    )
    await db.execute(update(Bed).where(Bed.id == bed_id).values(patient_id=None))

    await db.commit()
    await db.refresh(bed)

    return {"isOk": True, "data": bed, "timestamp": get_time()}
