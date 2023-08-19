from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel
from sqlalchemy import select

from app.core.jwt import sign_jwt, valid_request
from app.core.utils import get_time
from app.db.model import Admin
from app.db.session import get_db

router = APIRouter()


class LoginDto(BaseModel):
    id: str
    password: str


@router.get("/info")
async def info(res: Response, id: int = Depends(valid_request), db=Depends(get_db)):
    if id is None:
        res.status_code = 401
        return {
            "isOk": False,
            "data": "Invalid authentication credentials",
            "timestamp": get_time(),
        }

    user = await db.execute(select(Admin).where(Admin.hospital_id == id))
    user = user.scalar_one_or_none()

    if user is None:
        return {"isOk": False, "data": "User not found", "timestamp": get_time()}

    return {"isOk": True, "data": user, "timestamp": get_time()}


@router.post("/login", status_code=201)
async def login(res: Response, body: LoginDto, db=Depends(get_db)):
    user = await db.execute(select(Admin).where(Admin.id == body.id))
    user = user.scalar_one_or_none()

    if user is None:
        res.status_code = 400
        return {"isOk": False, "data": "User not found", "timestamp": get_time()}
    if user.password != body.password:
        res.status_code = 401
        return {"isOk": False, "data": "Wrong password", "timestamp": get_time()}

    token = sign_jwt(user.hospital_id)
    return {"isOk": True, "data": token, "timestamp": get_time()}
