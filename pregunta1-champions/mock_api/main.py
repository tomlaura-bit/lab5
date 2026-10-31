import json
from pathlib import Path
from fastapi import FastAPI


app = FastAPI(title="Champions Mock API")


@app.get("/matches")
def matches():
    return json.loads(Path("matches.json").read_text(encoding="utf-8"))


@app.get("/health")
def health():
    return {"status": "ok"}

