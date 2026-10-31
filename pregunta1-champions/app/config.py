import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./champions.db")
MATCHES_API_URL = os.getenv("MATCHES_API_URL", "http://localhost:8101/matches")

