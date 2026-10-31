from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.business.match_service import MatchService
from app.business.prediction_service import PredictionService
from app.data.database import SessionLocal
from app.data.repositories import MatchRepository, PredictionRepository


router = APIRouter()
templates = Jinja2Templates(directory="app/presentation/templates")


def get_session():
    with SessionLocal() as session:
        yield session


@router.get("/", response_class=HTMLResponse)
def home(request: Request, session: Session = Depends(get_session)):
    matches = MatchService(MatchRepository(session)).list_matches()
    predictions = PredictionService(MatchRepository(session), PredictionRepository(session)).list_predictions()
    return templates.TemplateResponse(request, "index.html", {"matches": matches, "predictions": predictions})


@router.post("/predictions")
def create_prediction(
    match_id: int = Form(...),
    participant: str = Form(...),
    result: str = Form(...),
    home_score: int = Form(...),
    away_score: int = Form(...),
    session: Session = Depends(get_session),
):
    try:
        PredictionService(MatchRepository(session), PredictionRepository(session)).register(
            match_id, participant, result, home_score, away_score
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return RedirectResponse("/#predictions", status_code=303)


@router.get("/api/matches")
def api_matches(session: Session = Depends(get_session)):
    matches = MatchService(MatchRepository(session)).list_matches()
    return [
        {
            "id": match.id,
            "home_team": match.home_team,
            "away_team": match.away_team,
            "kickoff": match.kickoff.isoformat(),
            "venue": match.venue,
        }
        for match in matches
    ]


@router.get("/api/predictions")
def api_predictions(session: Session = Depends(get_session)):
    predictions = PredictionService(MatchRepository(session), PredictionRepository(session)).list_predictions()
    return [
        {
            "id": item.id,
            "match": f"{item.match.home_team} vs {item.match.away_team}",
            "participant": item.participant,
            "result": item.result,
            "score": f"{item.home_score}-{item.away_score}",
        }
        for item in predictions
    ]

@router.get("/health")
def health():
    return {"status": "ok"}

