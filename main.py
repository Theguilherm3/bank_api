# to run use: uv run uvicorn main:app
from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.base import Base
from db.session import engine
from routes.accounts import router as accounts_router
from routes.transactions import router as transactions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    import models.accounts  # noqa: F401
    import models.transactions  # noqa: F401

    Base.metadata.create_all(bind=engine)

    # aplicacao roda no yield
    yield


app = FastAPI(title="API Bancária - v0.1", lifespan=lifespan)


@app.get("/health")
def health():
    return {"ok": True, "status": "running"}


app.include_router(transactions_router, tags=["transactions"])
app.include_router(accounts_router, tags=["Accounts"])
