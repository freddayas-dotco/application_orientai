import pandas as pd
import streamlit as st
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LYCEE_FILE = os.path.join(BASE_DIR, "Questionnaire_v5_Lycee_Adulte_48q.xlsx")
COLLEGE_FILE = os.path.join(BASE_DIR, "Questionnaire_v5_College_48q.xlsx")

SS_CATEGORIES = {
    "Communication": 0, "Esprit critique": 1, "Ethique": 2,
    "Intelligence émotionnelle": 3, "Intelligence sociale": 4,
    "Management de projet": 5, "Management et gestion d'équipe": 6,
    "Organisation": 7
}

MBTI_DIMS = {
    "Energie (E-extraverti ou I-Introverti)": "EI",
    "Recueil d'information ou perception (S-sensation ou N-intuition)": "SN",
    "Prise de décision (T-pensée ou F-sentiment)": "TF",
    "Mode d'action ou style de vie (J-Organisation ou P-perception)": "JP",
}

def parse_mbti_dim(text):
    if pd.isna(text) or not str(text).strip(): return None
    t = str(text).strip()
    for key, val in MBTI_DIMS.items():
        if key in t or t in key: return val
    if "E-" in t or "extraverti" in t.lower(): return "EI"
    if "S-" in t or "sensation" in t.lower(): return "SN"
    if "T-" in t or "pensée" in t.lower(): return "TF"
    if "J-" in t or "Organisation" in t: return "JP"
    return None

def parse_scoring(best_answer_col):
    val = str(best_answer_col).strip().upper() if not pd.isna(best_answer_col) else "A"
    return "normal" if val in ("A", "B") else "inverse"

@st.cache_data
def load_questionnaire(profil="lycee"):
    """Charge le questionnaire correspondant (lycée/adulte ou collège)."""
    file_path = COLLEGE_FILE if profil == "college" else LYCEE_FILE
    sheet_name = "Questionnaire "  # ← les deux fichiers ont un espace à la fin
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=1)
        questions = []
        for i, row in df.iterrows():
            q_text = row.iloc[6] if pd.notna(row.iloc[6]) else ""
            if not str(q_text).strip() or str(q_text).strip() == "Question": continue
            
            cat = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
            mbti_text = str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else ""
            opt_a = str(row.iloc[7]).strip() if pd.notna(row.iloc[7]) else ""
            opt_b = str(row.iloc[8]).strip() if pd.notna(row.iloc[8]) else ""
            opt_c = str(row.iloc[9]).strip() if pd.notna(row.iloc[9]) else ""
            opt_d = str(row.iloc[10]).strip() if pd.notna(row.iloc[10]) else ""
            best = row.iloc[11]
            sous_cat = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ""
            
            ss_idx = SS_CATEGORIES.get(cat)
            mbti_dim = parse_mbti_dim(mbti_text)
            
            if not q_text or ss_idx is None: continue
            
            questions.append({
                "id": len(questions),
                "q": q_text,
                "options": [opt_a, opt_b, opt_c, opt_d],
                "ss_idx": ss_idx,
                "cat_name": cat,
                "sous_cat": sous_cat,
                "mbti_dim": mbti_dim,
                "scoring": parse_scoring(best)
            })
            
        return questions
    except Exception as e:
        st.error(f"Erreur chargement questionnaire ({profil}) : {e}")
        return []