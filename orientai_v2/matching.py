"""
OrientAI v2 — Module de matching
Score de compatibilité profil soft skills ↔ métiers (repris de scoring.compute_matching v1,
sans MBTI) + niveau d'études normalisé déduit de la colonne « Diplômes ».
"""

import re

from scoring import SS_COLS, SS_FROM_TEXT

# Niveaux d'études normalisés, du plus accessible au plus long
NIVEAUX_ETUDES = [
    "Sans diplôme",
    "CAP / BEP",
    "Bac",
    "Bac+2",
    "Bac+3",
    "Bac+5",
    "Bac+8 et plus",
    "Variable",
]

_NIVEAU_PATTERNS = [
    ("Sans diplôme", r"aucun dipl|pas de dipl"),
    ("CAP / BEP", r"\bCAPA?\b|\bBEPA?\b"),
    ("Bac", r"\bbac\b(?!\s*\+)|\bBPREA\b|\bBPJEPS\b|brevet professionnel"),
    ("Bac+2", r"bac\s*\+\s*2|\bBTSA?\b|\bDUT\b|\bBUT\b|\bDEUST\b"),
    ("Bac+3", r"bac\s*\+\s*3|\blicence\b(?! pilote)|\bbachelor"),
    ("Bac+5", r"bac\s*\+\s*[45]|\bmaster\b|ingénieur|école de commerce|grande école"),
    ("Bac+8 et plus", r"bac\s*\+\s*(?:[6-9]|1\d)|doctorat"),
]


def niveau_etudes(diplomes: str) -> str:
    """Niveau d'études minimal requis : le premier niveau cité dans le texte « Diplômes »."""
    best, best_pos = "Variable", None
    for label, pattern in _NIVEAU_PATTERNS:
        m = re.search(pattern, diplomes, flags=re.IGNORECASE)
        if m and (best_pos is None or m.start() < best_pos):
            best, best_pos = label, m.start()
    return best


def split_secteurs(value) -> list[str]:
    return [s.strip() for s in str(value or "").split(";") if s.strip() and s.strip() != "nan"]


def compute_matching(profile: dict, df_metiers, limit: int | None = 30) -> list[dict]:
    """
    Calcule le score de compatibilité entre le profil et chaque métier.

    Args:
        profile: résultat de compute_profile()
        df_metiers: DataFrame pandas des métiers
        limit: nombre max de métiers retournés (None = tous)

    Returns:
        Liste de dicts triée par score décroissant, dédupliquée
    """
    user_ss = profile["ss"]

    results = []
    for _, row in df_metiers.iterrows():
        ss_score = 0
        for i, col in enumerate(SS_COLS):
            job_val = SS_FROM_TEXT.get(str(row.get(col, "Nécessaire")), 2)
            diff = abs(user_ss[i] - job_val)
            if diff == 0:
                ss_score += 3
            elif diff == 1:
                ss_score += 1.5
        score = round((ss_score / (8 * 3)) * 100)

        diplomes = str(row.get("Diplômes", ""))
        results.append({
            "metier": str(row.get("Métier", "")),
            "secteur": str(row.get("Secteur(s) activité", "")),
            "secteurs": split_secteurs(row.get("Secteur(s) activité")),
            "domaine": str(row.get("Domaine", "")),
            "niveau": str(row.get("Niveau", "")),
            "niveau_etudes": niveau_etudes(diplomes),
            "salaire": str(row.get("Salaire", "")),
            "descriptif": str(row.get("Descriptif", "")),
            "diplomes": diplomes,
            "score": score,
            # Niveau requis par le métier (« Peu nécessaire » / « Nécessaire » / « Absolument nécessaire »)
            "soft_skills": {
                col: row.get(col) if row.get(col) in SS_FROM_TEXT else "" for col in SS_COLS
            },
        })

    # Tri + déduplication + limite
    seen = set()
    top = []
    for r in sorted(results, key=lambda x: -x["score"]):
        key = r["metier"].lower().strip()
        if key not in seen:
            seen.add(key)
            top.append(r)
        if limit is not None and len(top) >= limit:
            break

    return top
