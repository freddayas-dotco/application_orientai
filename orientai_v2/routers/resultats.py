"""API résultats : calcul du profil soft skills, matching métiers, sauvegarde, filtres."""

import os
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Literal

import pandas as pd
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field, field_validator

from donnees_rapport import MAPPING_QUESTIONS, SS_RAPPORT_NOMS
from matching import NIVEAUX_ETUDES, compute_matching, niveau_etudes, split_secteurs
from routers.questionnaire import get_questions
from sauvegarde import sauvegarder, sauvegarder_reponses_brutes
from scoring import SS_LABELS, SS_TEXT, compute_profile

router = APIRouter(prefix="/api", tags=["resultats"])

METIERS_CSV = Path(os.environ.get(
    "METIERS_CSV",
    Path(__file__).resolve().parents[2] / "orientai_claude" / "data" / "metiers_v52_final.csv",
))

# Valeur de « mode » enregistrée dans Google Sheets (compatibilité avec les données v1)
MODE_SAUVEGARDE = {"eleve": "lycee", "adulte": "adulte"}


@lru_cache(maxsize=1)
def load_metiers() -> pd.DataFrame:
    return pd.read_csv(METIERS_CSV, sep=";", encoding="utf-8-sig")


class ReponsesIn(BaseModel):
    answers: list[int | None] = Field(min_length=48, max_length=48)
    prenom: str = Field("", max_length=100)
    nom: str = Field("", max_length=100)
    classe: str = Field("", max_length=150)
    mode: Literal["eleve", "adulte"] = "eleve"

    @field_validator("answers")
    @classmethod
    def check_answers(cls, v):
        if any(a is not None and not 0 <= a <= 3 for a in v):
            raise ValueError("Chaque réponse doit valoir 0 (A), 1 (B), 2 (C) ou 3 (D).")
        return v


def _analyse(answers: list[int], questions: list[dict]) -> list[dict]:
    """Pour chaque soft skill : ce que révèle chaque réponse (textes du rapport v5.2)."""
    analyse = [{"nom": SS_RAPPORT_NOMS[i], "items": []} for i in range(8)]
    for (sous_comp, _ss_nom, textes), q, ans in zip(MAPPING_QUESTIONS, questions, answers):
        analyse[q["ss"]]["items"].append({"sous_competence": sous_comp, "texte": textes["ABCD"[ans]]})
    return analyse


def _calcul(data: ReponsesIn):
    profile = compute_profile(data.answers, get_questions(data.mode))
    metiers = compute_matching(profile, load_metiers(), limit=None)
    return profile, metiers


@router.post("/resultats")
def resultats(data: ReponsesIn):
    if any(a is None for a in data.answers):
        raise HTTPException(422, "Toutes les questions doivent avoir une réponse.")
    profile, metiers = _calcul(data)
    return {
        "profil": [
            {"label": label, "niveau": niveau, "texte": SS_TEXT[niveau]}
            for label, niveau in zip(SS_LABELS, profile["ss"])
        ],
        "ss": profile["ss"],
        "analyse": _analyse(data.answers, get_questions(data.mode)),
        # Liste complète triée : le client filtre (secteur / niveau) puis affiche le top 10
        "metiers": metiers,
    }


@router.post("/sauvegarde")
def sauvegarde(data: ReponsesIn):
    if not data.prenom.strip() or not data.nom.strip():
        raise HTTPException(422, "Le prénom et le nom sont requis pour sauvegarder.")
    # Recalcul côté serveur : on ne fait pas confiance à un score envoyé par le client
    profile, metiers = _calcul(data)
    mode = MODE_SAUVEGARDE[data.mode]
    google_ok, csv_ok = sauvegarder(data.prenom.strip(), data.nom.strip(), data.classe.strip(),
                                    mode, profile, metiers[:3])
    brutes_google_ok, brutes_csv_ok = sauvegarder_reponses_brutes(
        data.prenom.strip(), data.nom.strip(), data.classe.strip(), mode, data.answers)
    if not (google_ok or csv_ok):
        raise HTTPException(500, "La sauvegarde a échoué.")
    return {
        "google_ok": google_ok and brutes_google_ok,
        "csv_ok": csv_ok and brutes_csv_ok,
    }


@router.get("/metiers/filtres")
def filtres():
    df = load_metiers()
    secteurs = sorted({s for v in df["Secteur(s) activité"].dropna() for s in split_secteurs(v)})
    presents = {niveau_etudes(str(d)) for d in df["Diplômes"].fillna("")}
    return {
        "secteurs": secteurs,
        "niveaux_etudes": [n for n in NIVEAUX_ETUDES if n in presents],
    }


def _normaliser(texte: str) -> str:
    """Minuscules sans accents, pour une recherche tolérante (« ingenieur » trouve « Ingénieur »)."""
    decompose = unicodedata.normalize("NFKD", texte.lower())
    return "".join(c for c in decompose if not unicodedata.combining(c))


def _texte(value) -> str:
    return "" if pd.isna(value) else str(value).strip()


@lru_cache(maxsize=1)
def catalogue_metiers() -> list[dict]:
    """Fiches métiers dédupliquées et triées par nom, avec secteurs et niveau d'études normalisés."""
    fiches, vus = [], set()
    for row in load_metiers().to_dict(orient="records"):
        metier = _texte(row.get("Métier"))
        cle = metier.lower()
        if not metier or cle in vus:
            continue
        vus.add(cle)
        diplomes = _texte(row.get("Diplômes"))
        fiches.append({
            "metier": metier,
            "secteurs": split_secteurs(row.get("Secteur(s) activité")),
            "domaine": _texte(row.get("Domaine")),
            "niveau": _texte(row.get("Niveau")),
            "niveau_etudes": niveau_etudes(diplomes),
            "diplomes": diplomes,
            "salaire": _texte(row.get("Salaire")),
            "descriptif": _texte(row.get("Descriptif")),
            "_recherche": _normaliser(metier),
        })
    return sorted(fiches, key=lambda f: f["_recherche"])


@router.get("/metiers/search")
def recherche_metiers(
    q: str = Query("", max_length=100),
    secteur: str = Query("", max_length=200),
    niveau: str = Query("", max_length=50),
    limit: int = Query(60, ge=1, le=2000),
):
    mots = _normaliser(q).split()
    resultats = [
        f for f in catalogue_metiers()
        if all(m in f["_recherche"] for m in mots)
        and (not secteur or secteur in f["secteurs"])
        and (not niveau or f["niveau_etudes"] == niveau)
    ]
    return {
        "total": len(resultats),
        "metiers": [{k: v for k, v in f.items() if not k.startswith("_")} for f in resultats[:limit]],
    }
