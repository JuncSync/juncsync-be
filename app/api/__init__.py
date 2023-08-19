from fastapi import APIRouter
from app.api.admin import router as admin_router
from app.api.bed import router as bed_router

router = APIRouter()
router.include_router(admin_router, prefix="/admin", tags=["admin"])
router.include_router(bed_router, prefix="/bed", tags=["bed"])


@router.get("/")
def health_check():
    return "OK"
