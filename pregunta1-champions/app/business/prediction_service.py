from app.data.repositories import MatchRepository, PredictionRepository


class PredictionService:
    def __init__(self, matches: MatchRepository, predictions: PredictionRepository):
        self.matches = matches
        self.predictions = predictions

    def register(self, match_id: int, participant: str, result: str, home_score: int, away_score: int):
        if not self.matches.get(match_id):
            raise ValueError("Partido inexistente")
        if result not in {"LOCAL", "VISITA", "EMPATE"}:
            raise ValueError("Resultado inválido")
        if not participant.strip() or home_score < 0 or away_score < 0:
            raise ValueError("Datos inválidos")
        expected = "EMPATE" if home_score == away_score else "LOCAL" if home_score > away_score else "VISITA"
        if result != expected:
            raise ValueError("El resultado no coincide con el marcador")
        return self.predictions.save(
            {
                "match_id": match_id,
                "participant": participant.strip(),
                "result": result,
                "home_score": home_score,
                "away_score": away_score,
            }
        )

    def list_predictions(self):
        return self.predictions.list_all()

