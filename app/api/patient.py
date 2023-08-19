from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel
from sqlalchemy import select, update

from app.core.jwt import valid_request
from app.core.utils import get_time
from app.db.model import Patient
from app.db.session import get_db

router = APIRouter()


@router.get("")
async def get_all(
    res: Response, hospital_id: int = Depends(valid_request), db=Depends(get_db)
):
    if hospital_id is None:
        res.status_code = 401
        return {
            "isOk": False,
            "data": "Invalid authentication credentials",
            "timestamp": get_time(),
        }

    print("id: ", hospital_id)
    patients = await db.execute(
        select(Patient).where(Patient.hospital_id == hospital_id)
    )
    patients = patients.scalars().all()

    return {"isOk": True, "data": patients, "timestamp": get_time()}


class PatientInfo(BaseModel):
    name: str
    gender: str
    diagnosis: str
    birth_year: int
    birth_month: int
    birth_day: int


@router.put("/edit/{patient_id}", status_code=201)
async def bed_in(
    res: Response,
    body: PatientInfo,
    patient_id: str,
    hospital_id: int = Depends(valid_request),
    db=Depends(get_db),
):
    if hospital_id is None:
        res.status_code = 401
        return {
            "isOk": False,
            "data": "Invalid authentication credentials",
            "timestamp": get_time(),
        }

    patient = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = patient.scalar_one_or_none()

    if patient is None:
        res.status_code = 400
        return {"isOk": False, "data": "Patient not found", "timestamp": get_time()}
    if patient.hospital_id != hospital_id:
        res.status_code = 403
        return {"isOk": False, "data": "Wrong hospital", "timestamp": get_time()}

    await db.execute(
        update(Patient)
        .where(Patient.id == patient_id)
        .values(
            name=body.name,
            gender=body.gender,
            diagnosis=body.diagnosis,
            birth_year=body.birth_year,
            birth_month=body.birth_month,
            birth_day=body.birth_day,
        )
    )

    await db.commit()
    await db.refresh(patient)

    return {
        "isOk": True,
        "data": {"patient": patient},
        "timestamp": get_time(),
    }


@router.get("/search/{keyword}")
async def search_patient(
    res: Response,
    keyword: str,
    hospital_id: int = Depends(valid_request),
    db=Depends(get_db),
):
    if hospital_id is None:
        res.status_code = 401
        return {
            "isOk": False,
            "data": "Invalid authentication credentials",
            "timestamp": get_time(),
        }

    patients = await db.execute(
        select(Patient).filter(Patient.name.like(f"%{keyword}%"))
    )
    patients = patients.scalars().all()

    return {
        "isOk": True,
        "data": patients,
        "timestamp": get_time(),
    }
