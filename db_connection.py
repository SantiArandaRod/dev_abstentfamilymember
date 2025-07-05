from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRESQL_ADDON_USER = os.getenv('POSTGRESQL_ADDON_USER')
POSTGRESQL_ADDON_PASSWORD = os.getenv('POSTGRESQL_ADDON_PASSWORD')
POSTGRESQL_ADDON_HOST = os.getenv('POSTGRESQL_ADDON_HOST')
POSTGRESQL_ADDON_PORT = os.getenv('POSTGRESQL_ADDON_PORT')
POSTGRESQL_ADDON_DB = os.getenv('POSTGRESQL_ADDON_DB')

if POSTGRESQL_ADDON_PORT is None:
    raise ValueError("POSTGRESQL_ADDON_PORT environment variable is not set.")
CLEVER_DB= (
    f"postgresql+asyncpg://{POSTGRESQL_ADDON_USER}:"
    f"{POSTGRESQL_ADDON_PASSWORD}@"
    f"{POSTGRESQL_ADDON_HOST}:"
    f"{POSTGRESQL_ADDON_PORT}/"
    f"{POSTGRESQL_ADDON_DB}"
)
engine : AsyncEngine = create_async_engine(CLEVER_DB, echo=True)
AsyncSession = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
async def get_session():
    async with AsyncSession() as session:
        yield session