import os
import time
from typing import Optional
from dotenv import load_dotenv

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_EXPIRE_TIME = 60 * 60 * 24 * 30  # 30 days

ALGORITHM = "HS256"
get_bearer_token = HTTPBearer(auto_error=False)


async def valid_request(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
    # db: AsyncSession = Depends(get_db),
) -> str:
    try:
        # _, token = authorization.split(" ")
        if auth is None:
            return None
        token = auth.credentials
        # print("token: ", token)
        # Simulate a database query to find a known token

        payload = jwt.decode(
            token, JWT_SECRET_KEY.encode("utf-8"), algorithms=[ALGORITHM]
        )

        hospital_id = payload.get("sub")
        if hospital_id is None:
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED, detail="sub not found"
            # )
            return None

    except JWTError:
        # print(e)
        return None

    return int(hospital_id)


def sign_jwt(sub) -> str:
    key = JWT_SECRET_KEY.encode("utf-8")
    expire_time = JWT_EXPIRE_TIME

    payload = {
        "sub": str(sub),
        "iat": int(time.time()),
        "exp": int(time.time()) + expire_time,
    }
    token = jwt.encode(payload, key, algorithm="HS256")
    return token
