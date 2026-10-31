from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import GENERATED, UPLOADS
from app.data.database import Base, engine
from app.presentation.routes import router


UPLOADS.mkdir(parents=True, exist_ok=True)
GENERATED.mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Marketing Studio", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/presentation/static"), name="static")
app.mount("/assets", StaticFiles(directory="storage"), name="assets")
app.include_router(router)

