from uuid import uuid4
import httpx
from app.config import INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_GRAPH_VERSION, INSTAGRAM_USER_ID, PUBLIC_BASE_URL, SOCIAL_MODE
from app.data.repositories import CampaignRepository


class SocialService:
    def __init__(self, repository: CampaignRepository):
        self.repository = repository

    async def publish(self, campaign_id: int):
        campaign = self.repository.get(campaign_id)
        if not campaign or not campaign.assets:
            raise ValueError("Debe generar los recursos")
        image = next((asset for asset in campaign.assets if asset.kind == "IMAGE"), None)
        if SOCIAL_MODE == "simulation":
            social_id = f"sim-{uuid4().hex[:12]}"
        else:
            if not INSTAGRAM_USER_ID or not INSTAGRAM_ACCESS_TOKEN or not image:
                raise ValueError("Faltan credenciales de Instagram")
            create_url = f"https://graph.facebook.com/{INSTAGRAM_GRAPH_VERSION}/{INSTAGRAM_USER_ID}/media"
            image_url = f"{PUBLIC_BASE_URL}/assets/{image.path}"
            async with httpx.AsyncClient(timeout=30) as client:
                creation = await client.post(
                    create_url,
                    data={"image_url": image_url, "caption": campaign.selected_script, "access_token": INSTAGRAM_ACCESS_TOKEN},
                )
                creation.raise_for_status()
                publish = await client.post(
                    f"https://graph.facebook.com/{INSTAGRAM_GRAPH_VERSION}/{INSTAGRAM_USER_ID}/media_publish",
                    data={"creation_id": creation.json()["id"], "access_token": INSTAGRAM_ACCESS_TOKEN},
                )
                publish.raise_for_status()
                social_id = publish.json()["id"]
        self.repository.publish(campaign, social_id)
        return self.repository.get(campaign.id)

