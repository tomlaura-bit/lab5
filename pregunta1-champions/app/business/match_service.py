from datetime import datetime
import httpx
from app.config import MATCHES_API_URL
from app.data.repositories import MatchRepository


class MatchService:
    def __init__(self, repository: MatchRepository):
        self.repository = repository

    async def synchronize(self) -> int:
        if self.repository.count() > 0:
            return 0
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(MATCHES_API_URL)
            response.raise_for_status()
        values = [
            {
                "external_id": item["id"],
                "home_team": item["home_team"],
                "away_team": item["away_team"],
                "kickoff": datetime.fromisoformat(item["kickoff"]),
                "venue": item["venue"],
            }
            for item in response.json()
        ]
        self.repository.save_many(values)
        return len(values)

    def list_matches(self):
        return self.repository.list_all()

