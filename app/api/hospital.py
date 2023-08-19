from fastapi import APIRouter, Depends, Response
from sqlalchemy import select

from app.core.utils import get_time
from app.db.model import Bed, Hospital
from app.db.session import get_db

router = APIRouter()


@router.get("", status_code=200)
async def get_all(res: Response, db=Depends(get_db)):
    hospitals = await db.execute(select(Hospital))
    hospitals = hospitals.scalars().all()

    for hospital in hospitals:
        tot_bed = await db.execute(select(Bed).where(Bed.hospital_id == hospital.id))
        empty_bed = await db.execute(
            select(Bed)
            .where(Bed.hospital_id == hospital.id)
            .where(Bed.patient_id == None)
        )

        hospital.bed_count = len(tot_bed.scalars().all())
        hospital.empty_bed_count = len(empty_bed.scalars().all())

    return {"isOk": True, "data": hospitals, "timestamp": get_time()}
