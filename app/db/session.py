import os
from typing import AsyncIterable
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

load_dotenv()
engine = create_async_engine(
    os.getenv("DATABASE_URL"), pool_size=20, echo=False, pool_pre_ping=True
)


async def get_db() -> AsyncIterable[AsyncSession]:
    sess = AsyncSession(bind=engine)
    try:
        yield sess
    finally:
        await sess.close()
