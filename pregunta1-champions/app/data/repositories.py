from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.data.models import Match, Prediction


class MatchRepository:
    def __init__(self, session: Session):
        self.session = session

    def count(self) -> int:
        return len(self.session.scalars(select(Match)).all())

    def save_many(self, values: list[dict]) -> None:
        known = set(self.session.scalars(select(Match.external_id)).all())
        self.session.add_all(Match(**value) for value in values if value["external_id"] not in known)
        self.session.commit()

    def list_all(self) -> list[Match]:
        return list(self.session.scalars(select(Match).order_by(Match.kickoff)).all())

    def get(self, match_id: int) -> Match | None:
        return self.session.get(Match, match_id)


class PredictionRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, value: dict) -> Prediction:
        prediction = Prediction(**value)
        self.session.add(prediction)
        self.session.commit()
        self.session.refresh(prediction)
        return prediction

    def list_all(self) -> list[Prediction]:
        query = select(Prediction).options(joinedload(Prediction.match)).order_by(Prediction.created_at.desc())
        return list(self.session.scalars(query).all())

