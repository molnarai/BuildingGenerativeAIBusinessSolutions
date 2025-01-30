from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from typing import Generator, Any

# Construct PostgreSQL database URL from environment variables
DATABASE_URL = "postgresql+asyncpg://{u}:{p}@{h}:{o}/{d}".format(
    u = os.getenv("POSTGRES_USER"),
    p = os.getenv("POSTGRES_PASSWORD"),
    h = os.getenv("POSTGRES_HOST"),
    o = os.getenv("POSTGRES_PORT"),
    d = os.getenv("POSTGRES_DB")
)

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
Base = declarative_base()

async def get_db() -> Generator:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)