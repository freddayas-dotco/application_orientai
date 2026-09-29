"""Dashboard conseiller : connexion par mot de passe (DASHBOARD_PASSWORD) et données agrégées."""

import hashlib
import hmac
import os
import time

from fastapi import APIRouter, Cookie, HTTPException, Response
from pydantic import BaseModel

from sauvegarde import charger_resultats
from scoring import SS_LABELS

router = APIRouter(tags=["dashboard"])

COOKIE_NAME = "orientai_dashboard"
SESSION_SECONDS = 8 * 3600

SS_KEYS = [
    "ss_communication", "ss_esprit_critique", "ss_ethique",
    "ss_intel_emotionnelle", "ss_intel_sociale",
    "ss_mgmt_projet", "ss_mgmt_equipe", "ss_organisation",
]
COLONNES_DASHBOARD = (
    ["date", "prenom", "nom", "classe", "mode"] + SS_KEYS
    + [f"top{i}_{c}" for i in range(1, 4) for c in ("metier", "score", "secteur")]
)


def _password() -> str:
    pwd = os.environ.get("DASHBOARD_PASSWORD", "")
    if not pwd:
        raise HTTPException(503, "DASHBOARD_PASSWORD n'est pas configuré sur le serveur.")
    return pwd


def _sign(expires: int) -> str:
    key = hashlib.sha256(("orientai-dashboard:" + _password()).encode()).digest()
    return hmac.new(key, str(expires).encode(), hashlib.sha256).hexdigest()


def _token_valide(token: str | None) -> bool:
    if not token or "." not in token:
        return False
    expires, sig = token.split(".", 1)
    if not expires.isdigit() or int(expires) < time.time():
        return False
    return hmac.compare_digest(sig, _sign(int(expires)))


class LoginIn(BaseModel):
    password: str


@router.post("/dashboard/login")
def login(data: LoginIn, response: Response):
    if not hmac.compare_digest(data.password.encode(), _password().encode()):
        raise HTTPException(401, "Mot de passe incorrect.")
    expires = int(time.time()) + SESSION_SECONDS
    response.set_cookie(
        COOKIE_NAME, f"{expires}.{_sign(expires)}",
        max_age=SESSION_SECONDS, httponly=True, samesite="strict",
        secure=os.environ.get("COOKIE_SECURE", "0") == "1",
    )
    return {"ok": True}


@router.post("/dashboard/logout")
def logout(response: Response):
    response.delete_cookie(COOKIE_NAME)
    return {"ok": True}


@router.get("/api/dashboard/data")
def dashboard_data(orientai_dashboard: str | None = Cookie(default=None)):
    if not _token_valide(orientai_dashboard):
        raise HTTPException(401, "Authentification requise.")

    df = charger_resultats()
    df = df.reindex(columns=COLONNES_DASHBOARD)
    df = df.astype(object).where(df.notna(), None)
    rows = df.to_dict(orient="records")
    for r in rows:
        for k in SS_KEYS:
            try:
                r[k] = int(float(r[k])) if r[k] not in (None, "") else None
            except (TypeError, ValueError):
                r[k] = None

    return {
        "ss_keys": SS_KEYS,
        "ss_labels": SS_LABELS,
        "rows": rows,
    }
