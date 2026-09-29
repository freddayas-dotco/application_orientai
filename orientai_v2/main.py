"""
OrientAI v2 — Application FastAPI
Lancement : uvicorn main:app --reload   (depuis le dossier orientai_v2/)
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.gzip import GZipMiddleware  # noqa: E402
from fastapi.responses import FileResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402

from routers import dashboard, questionnaire, resultats  # noqa: E402

STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="OrientAI v2", docs_url="/api/docs" if os.environ.get("ORIENTAI_DOCS") else None)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.middleware("http")
async def static_no_cache(request, call_next):
    # Force le navigateur à revalider JS/CSS (ETag) : sinon un ancien app.js en cache
    # tourne avec le nouveau HTML et casse les pages après une mise à jour.
    response = await call_next(request)
    if request.url.path.startswith("/static/"):
        response.headers["Cache-Control"] = "no-cache"
    return response

app.include_router(questionnaire.router)
app.include_router(resultats.router)
app.include_router(dashboard.router)


def _page(name: str) -> FileResponse:
    return FileResponse(STATIC_DIR / name, headers={"Cache-Control": "no-cache"})


@app.get("/", include_in_schema=False)
def index():
    return _page("index.html")


@app.get("/espace", include_in_schema=False)
def page_espace():
    return _page("espace.html")


@app.get("/explorateur", include_in_schema=False)
def page_explorateur():
    return _page("explorateur.html")


@app.get("/questionnaire", include_in_schema=False)
def page_questionnaire():
    return _page("questionnaire.html")


@app.get("/resultats", include_in_schema=False)
def page_resultats():
    return _page("resultats.html")


@app.get("/dashboard", include_in_schema=False)
def page_dashboard():
    return _page("dashboard.html")


@app.get("/api/health", include_in_schema=False)
def health():
    return {"ok": True}
