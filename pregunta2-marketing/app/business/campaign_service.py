import json
import shutil
from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
from app.config import UPLOADS
from app.data.repositories import CampaignRepository


class CampaignService:
    def __init__(self, repository: CampaignRepository):
        self.repository = repository

    async def create(self, company: str, product: str, audience: str, objective: str, photo: UploadFile):
        if not photo.content_type or not photo.content_type.startswith("image/"):
            raise ValueError("El archivo debe ser una imagen")
        suffix = Path(photo.filename or "photo.jpg").suffix.lower() or ".jpg"
        filename = f"{uuid4().hex}{suffix}"
        path = UPLOADS / filename
        with path.open("wb") as output:
            shutil.copyfileobj(photo.file, output)
        scripts = self.propose_scripts(company, product, audience, objective)
        return self.repository.create(
            {
                "company": company.strip(),
                "product": product.strip(),
                "audience": audience.strip(),
                "objective": objective.strip(),
                "original_path": f"uploads/{filename}",
                "scripts": json.dumps(scripts, ensure_ascii=False),
            }
        )

    def propose_scripts(self, company: str, product: str, audience: str, objective: str) -> list[str]:
        return [
            f"Problema y solución: muestra una necesidad cotidiana de {audience}, presenta {product} de {company} como respuesta y cierra con una invitación a {objective}.",
            f"Demostración rápida: inicia con el resultado final, enseña tres beneficios concretos de {product} y termina con la marca {company} y un llamado a {objective}.",
            f"Historia de cliente: una persona de {audience} descubre {product}, experimenta el cambio y recomienda {company} con un cierre orientado a {objective}.",
        ]

    def select(self, campaign_id: int, script_index: int):
        campaign = self.repository.get(campaign_id)
        if not campaign:
            raise ValueError("Campaña inexistente")
        scripts = json.loads(campaign.scripts)
        if script_index not in range(len(scripts)):
            raise ValueError("Guion inexistente")
        self.repository.select_script(campaign, scripts[script_index])
        return campaign

    def list_campaigns(self):
        return self.repository.list_all()

