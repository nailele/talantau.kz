
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from talantau.auth.routes import router
from talantau.config import BASE_DIR
from talantau.db.base import Base, engine

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)
app.include_router(router)

HTML_FILE = BASE_DIR / "landing.html"
@app.get("/", response_class=HTMLResponse)
async def read_landing():
    return HTML_FILE.read_text(encoding="utf-8")
