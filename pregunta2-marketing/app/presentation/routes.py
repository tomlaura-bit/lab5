import json
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.business.campaign_service import CampaignService
from app.business.media_service import MediaService
from app.business.social_service import SocialService
from app.data.database import SessionLocal
from app.data.repositories import CampaignRepository


router = APIRouter()
templates = Jinja2Templates(directory="app/presentation/templates")
templates.env.filters["from_json"] = json.loads


def get_session():
    with SessionLocal() as session:
        yield session


@router.get("/", response_class=HTMLResponse)
def home(request: Request, session: Session = Depends(get_session)):
    campaigns = CampaignService(CampaignRepository(session)).list_campaigns()
    return templates.TemplateResponse(request, "index.html", {"campaigns": campaigns})


@router.post("/campaigns")
async def create_campaign(
    company: str = Form(...),
    product: str = Form(...),
    audience: str = Form(...),
    objective: str = Form(...),
    photo: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    try:
        campaign = await CampaignService(CampaignRepository(session)).create(company, product, audience, objective, photo)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return RedirectResponse(f"/campaigns/{campaign.id}", status_code=303)


@router.get("/campaigns/{campaign_id}", response_class=HTMLResponse)
def campaign_detail(campaign_id: int, request: Request, session: Session = Depends(get_session)):
    campaign = CampaignRepository(session).get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaña inexistente")
    return templates.TemplateResponse(request, "detail.html", {"campaign": campaign, "scripts": json.loads(campaign.scripts)})


@router.post("/campaigns/{campaign_id}/select")
def select_script(campaign_id: int, script_index: int = Form(...), session: Session = Depends(get_session)):
    try:
        CampaignService(CampaignRepository(session)).select(campaign_id, script_index)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return RedirectResponse(f"/campaigns/{campaign_id}", status_code=303)


@router.post("/campaigns/{campaign_id}/generate")
def generate(campaign_id: int, session: Session = Depends(get_session)):
    try:
        MediaService(CampaignRepository(session)).generate(campaign_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return RedirectResponse(f"/campaigns/{campaign_id}", status_code=303)


@router.post("/campaigns/{campaign_id}/publish")
async def publish(campaign_id: int, session: Session = Depends(get_session)):
    try:
        await SocialService(CampaignRepository(session)).publish(campaign_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return RedirectResponse(f"/campaigns/{campaign_id}", status_code=303)


@router.get("/health")
def health():
    return {"status": "ok"}

