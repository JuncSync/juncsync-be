from fastapi import APIRouter
from app.api.admin import router as admin_router
from app.api.bed import router as bed_router
from app.api.patient import router as patient_router
from app.api.hospital import router as hospital_router

router = APIRouter()
router.include_router(admin_router, prefix="/admin", tags=["admin"])
router.include_router(bed_router, prefix="/bed", tags=["bed"])
router.include_router(patient_router, prefix="/patient", tags=["patient"])
router.include_router(hospital_router, prefix="/hospital", tags=["hospital"])


@router.get("/")
def health_check():
    return "OK"
