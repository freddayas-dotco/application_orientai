"""
OrientAI — Module de sauvegarde des résultats élèves
Sauvegarde dans Google Sheets (cloud) + CSV local en backup
"""

import csv
import os
from datetime import datetime
import pandas as pd

# ── Configuration Google Sheets ───────────────────────────────────────────────
GOOGLE_SHEET_ID = os.environ.get("GOOGLE_SHEET_ID", "1-clYEeefpu5Hx9Cl2Tp-4R1AVRsbACcLZtJVvFPrdZc")

# Chemin vers le fichier de credentials Google (fallback local)
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "google_credentials.json")


def _get_credentials(scopes):
    """Retourne les credentials Google depuis st.secrets (cloud) ou le fichier JSON (local)."""
    from google.oauth2.service_account import Credentials

    # Priorité 1 : st.secrets (Streamlit Cloud)
    try:
        import streamlit as st
        if "gcp_service_account" in st.secrets:
            info = dict(st.secrets["gcp_service_account"])
            return Credentials.from_service_account_info(info, scopes=scopes)
    except Exception:
        pass

    # Priorité 2 : fichier JSON local
    if os.path.exists(CREDENTIALS_FILE):
        return Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)

    return None


def _get_sheet_id():
    """Retourne l'ID du Google Sheet depuis st.secrets ou la variable d'environnement."""
    try:
        import streamlit as st
        return st.secrets.get("GOOGLE_SHEET_ID", GOOGLE_SHEET_ID)
    except Exception:
        return GOOGLE_SHEET_ID

# Nom de l'onglet dans le Google Sheet
SHEET_TAB = "Résultats"
SHEET_TAB_ENQUETE = "Enquête"

# ── Fallback CSV local ────────────────────────────────────────────────────────
RESULTATS_FILE = "data/resultats.csv"
ENQUETE_FILE = "data/enquete.csv"

COLONNES = [
    "date", "prenom", "nom", "classe", "mode",
    "mbti", "mbti_desc",
    "ss_communication", "ss_esprit_critique", "ss_ethique",
    "ss_intel_emotionnelle", "ss_intel_sociale",
    "ss_mgmt_projet", "ss_mgmt_equipe", "ss_organisation",
    "top1_metier", "top1_score", "top1_secteur",
    "top2_metier", "top2_score", "top2_secteur",
    "top3_metier", "top3_score", "top3_secteur",
]

COLONNES_ENQUETE = [
    "date", "prenom", "nom", "classe", "mode",
    "enquete_pertinence", "enquete_surprise", "enquete_profil", "enquete_utilite",
    "enquete_suggestions",
]


def _get_gsheet():
    """Retourne la feuille Google Sheets ou None si non disponible."""
    try:
        import gspread

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = _get_credentials(scopes)
        if creds is None:
            return None

        client = gspread.authorize(creds)
        sh = client.open_by_key(_get_sheet_id())

        try:
            worksheet = sh.worksheet(SHEET_TAB)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sh.add_worksheet(title=SHEET_TAB, rows=1000, cols=30)
            worksheet.append_row(COLONNES)

        # Ajouter l'en-tête si la feuille est vide
        if worksheet.row_count == 0 or worksheet.cell(1, 1).value != "date":
            worksheet.insert_row(COLONNES, 1)

        return worksheet

    except Exception as e:
        print(f"⚠️ Google Sheets non disponible : {e}")
        return None


def init_fichier():
    """Crée le fichier CSV local s'il n'existe pas."""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(RESULTATS_FILE):
        with open(RESULTATS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=COLONNES)
            writer.writeheader()


def _build_row(prenom, nom, classe, mode, profile, top_metiers):
    """Construit le dictionnaire de données à sauvegarder."""
    ss = profile["ss"]
    top3 = top_metiers[:3]

    row = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "prenom": prenom,
        "nom": nom,
        "classe": classe or "",
        "mode": mode,
        "mbti": profile.get("mbti", ""),
        "mbti_desc": profile.get("mbti_desc", ""),
        "ss_communication": ss[0],
        "ss_esprit_critique": ss[1],
        "ss_ethique": ss[2],
        "ss_intel_emotionnelle": ss[3],
        "ss_intel_sociale": ss[4],
        "ss_mgmt_projet": ss[5],
        "ss_mgmt_equipe": ss[6],
        "ss_organisation": ss[7],
    }

    for i, m in enumerate(top3, 1):
        row[f"top{i}_metier"] = m.get("metier", "")
        row[f"top{i}_score"] = m.get("score", 0)
        row[f"top{i}_secteur"] = m.get("secteur", "")

    for i in range(len(top3) + 1, 4):
        row[f"top{i}_metier"] = ""
        row[f"top{i}_score"] = ""
        row[f"top{i}_secteur"] = ""

    return row


def sauvegarder(prenom: str, nom: str, classe: str, mode: str,
                profile: dict, top_metiers: list):
    """
    Sauvegarde dans Google Sheets ET dans le CSV local.
    Retourne (google_ok, csv_ok).
    """
    row = _build_row(prenom, nom, classe, mode, profile, top_metiers)
    row_values = [str(row[col]) for col in COLONNES]

    google_ok = False
    csv_ok = False

    # ── Google Sheets ─────────────────────────────────────────────────────────
    try:
        worksheet = _get_gsheet()
        if worksheet:
            worksheet.append_row(row_values)
            google_ok = True
    except Exception as e:
        print(f"⚠️ Erreur Google Sheets : {e}")

    # ── CSV local (toujours, en backup) ──────────────────────────────────────
    try:
        init_fichier()
        with open(RESULTATS_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=COLONNES)
            writer.writerow(row)
        csv_ok = True
    except Exception as e:
        print(f"⚠️ Erreur CSV : {e}")

    return google_ok, csv_ok


def charger_resultats() -> pd.DataFrame:
    """
    Charge depuis Google Sheets en priorité, sinon depuis le CSV local.
    """
    try:
        worksheet = _get_gsheet()
        if worksheet:
            data = worksheet.get_all_records()
            if data:
                return pd.DataFrame(data)
    except Exception as e:
        print(f"⚠️ Impossible de lire Google Sheets : {e}")

    init_fichier()
    try:
        return pd.read_csv(RESULTATS_FILE, encoding="utf-8")
    except Exception:
        return pd.DataFrame(columns=COLONNES)


def effacer_resultats():
    """Efface le CSV local (ne touche pas Google Sheets)."""
    if os.path.exists(RESULTATS_FILE):
        os.remove(RESULTATS_FILE)
    init_fichier()


# ── Enquête de satisfaction ───────────────────────────────────────────────────

def _get_gsheet_enquete():
    """Retourne la feuille 'Enquête' Google Sheets ou None si non disponible."""
    try:
        import gspread

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = _get_credentials(scopes)
        if creds is None:
            return None

        client = gspread.authorize(creds)
        sh = client.open_by_key(_get_sheet_id())

        try:
            worksheet = sh.worksheet(SHEET_TAB_ENQUETE)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sh.add_worksheet(title=SHEET_TAB_ENQUETE, rows=1000, cols=10)
            worksheet.append_row(COLONNES_ENQUETE)

        if worksheet.row_count == 0 or worksheet.cell(1, 1).value != "date":
            worksheet.insert_row(COLONNES_ENQUETE, 1)

        return worksheet

    except Exception as e:
        print(f"⚠️ Google Sheets (Enquête) non disponible : {e}")
        return None


def sauvegarder_enquete(prenom: str, nom: str, classe: str, mode: str,
                        pertinence: str, surprise: str, profil: str, utilite: str,
                        suggestions: str = ""):
    """
    Sauvegarde les réponses à l'enquête dans l'onglet 'Enquête' du Google Sheet
    et dans un CSV local data/enquete.csv.
    Retourne (google_ok, csv_ok).
    """
    row = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "prenom": prenom,
        "nom": nom,
        "classe": classe or "",
        "mode": mode,
        "enquete_pertinence": pertinence,
        "enquete_surprise": surprise,
        "enquete_profil": profil,
        "enquete_utilite": utilite,
        "enquete_suggestions": suggestions,
    }
    row_values = [str(row[col]) for col in COLONNES_ENQUETE]

    google_ok = False
    csv_ok = False

    try:
        worksheet = _get_gsheet_enquete()
        if worksheet:
            worksheet.append_row(row_values)
            google_ok = True
    except Exception as e:
        print(f"⚠️ Erreur Google Sheets (enquête) : {e}")

    try:
        os.makedirs("data", exist_ok=True)
        file_exists = os.path.exists(ENQUETE_FILE)
        with open(ENQUETE_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=COLONNES_ENQUETE)
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)
        csv_ok = True
    except Exception as e:
        print(f"⚠️ Erreur CSV enquête : {e}")

    return google_ok, csv_ok


def charger_enquete() -> pd.DataFrame:
    """
    Charge les réponses enquête depuis Google Sheets en priorité, sinon depuis le CSV local.
    """
    try:
        worksheet = _get_gsheet_enquete()
        if worksheet:
            data = worksheet.get_all_records()
            if data:
                return pd.DataFrame(data)
    except Exception as e:
        print(f"⚠️ Impossible de lire Google Sheets (enquête) : {e}")

    if os.path.exists(ENQUETE_FILE):
        try:
            return pd.read_csv(ENQUETE_FILE, encoding="utf-8")
        except Exception:
            pass

    return pd.DataFrame(columns=COLONNES_ENQUETE)
