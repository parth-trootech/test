from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from api import FastAPI

DATABASE_URL = "postgresql+asyncpg://your_user:your_password@localhost/your_db_name"

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session maker
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


# Function to initialize the database
async def init_db():
    # Create all tables
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(SQLModel.metadata.create_all)

# DATABASE_URL = "postgresql+asyncpg://your_user:your_password@localhost/your_db_name"
