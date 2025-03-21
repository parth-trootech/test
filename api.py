from database import async_session, init_db
from sqlalchemy.ext.asyncio import AsyncSession

from api import FastAPI, Depends

app = FastAPI()


# Dependency to get the database session
def get_session() -> AsyncSession:
    return async_session()


# Initialize the database (create tables)
@app.on_event("startup")
async def on_startup():
    await init_db()


# Example endpoint to get users
@app.get("/users/")
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute("SELECT * FROM users")
    users = result.fetchall()
    return {"users": users}
