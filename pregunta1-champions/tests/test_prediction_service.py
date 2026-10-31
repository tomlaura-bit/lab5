from types import SimpleNamespace
import pytest
from app.business.prediction_service import PredictionService


class Matches:
    def get(self, match_id):
        return SimpleNamespace(id=match_id) if match_id == 1 else None


class Predictions:
    def save(self, value):
        return value

    def list_all(self):
        return []


def test_registers_consistent_prediction():
    value = PredictionService(Matches(), Predictions()).register(1, "Ana", "LOCAL", 2, 1)
    assert value["participant"] == "Ana"


def test_rejects_inconsistent_result():
    with pytest.raises(ValueError):
        PredictionService(Matches(), Predictions()).register(1, "Ana", "EMPATE", 2, 1)
