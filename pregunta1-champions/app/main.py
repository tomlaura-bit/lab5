from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.business.match_service import MatchService
from app.data.database import Base, SessionLocal, engine
from app.data.repositories import MatchRepository
from app.presentation.routes import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        await MatchService(MatchRepository(session)).synchronize()
    yield


app = FastAPI(title="Champions Predictions", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/presentation/static"), name="static")
app.include_router(router)

