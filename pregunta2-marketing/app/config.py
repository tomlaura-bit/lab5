import os
from pathlib import Path


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./marketing.db")
SOCIAL_MODE = os.getenv("SOCIAL_MODE", "simulation")
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "http://localhost:8002").rstrip("/")
INSTAGRAM_USER_ID = os.getenv("INSTAGRAM_USER_ID", "")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
INSTAGRAM_GRAPH_VERSION = os.getenv("INSTAGRAM_GRAPH_VERSION", "v26.0")
STORAGE = Path(os.getenv("STORAGE", "storage"))
UPLOADS = STORAGE / "uploads"
GENERATED = STORAGE / "generated"

