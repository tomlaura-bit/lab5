from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.data.models import Asset, Campaign


class CampaignRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, value: dict) -> Campaign:
        campaign = Campaign(**value)
        self.session.add(campaign)
        self.session.commit()
        self.session.refresh(campaign)
        return campaign

    def get(self, campaign_id: int) -> Campaign | None:
        query = select(Campaign).where(Campaign.id == campaign_id).options(joinedload(Campaign.assets))
        return self.session.scalars(query).unique().first()

    def list_all(self) -> list[Campaign]:
        query = select(Campaign).options(joinedload(Campaign.assets)).order_by(Campaign.created_at.desc())
        return list(self.session.scalars(query).unique().all())

    def select_script(self, campaign: Campaign, script: str) -> None:
        campaign.selected_script = script
        campaign.status = "SELECCIONADO"
        self.session.commit()

    def add_assets(self, campaign: Campaign, values: list[dict]) -> None:
        self.session.add_all(Asset(campaign_id=campaign.id, **value) for value in values)
        campaign.status = "GENERADO"
        self.session.commit()

    def publish(self, campaign: Campaign, social_id: str) -> None:
        campaign.social_id = social_id
        campaign.status = "PUBLICADO"
        self.session.commit()

