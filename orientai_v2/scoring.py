"""
OrientAI v2 — Module de scoring
Calcule le profil soft skills à partir des réponses au questionnaire.
"""

SS_LABELS = [
    "Communication",
    "Esprit critique",
    "Éthique",
    "Intel. émotionnelle",
    "Intel. sociale",
    "Mgmt de projet",
    "Mgmt d'équipe",
    "Organisation",
]

SS_COLS = [
    "Communication",
    "Esprit critique",
    "Éthique",
    "Intel. émotionnelle",
    "Intel. sociale",
    "Mgmt de projet",
    "Mgmt d'équipe",
    "Organisation",
]

SS_TEXT = {1: "Peu nécessaire", 2: "Nécessaire", 3: "Absolument nécessaire"}
SS_FROM_TEXT = {v: k for k, v in SS_TEXT.items()}


def compute_profile(answers: list[int], questions: list[dict]) -> dict:
    """
    Calcule le profil soft skills à partir des réponses.

    Args:
        answers: liste de 48 entiers (0=A, 1=B, 2=C, 3=D), None si sans réponse
        questions: liste des 48 questions (voir questionnaire.py)

    Returns:
        dict avec 'ss' (liste 8 valeurs 1-3), 'ss_raw' (scores bruts), 'ss_max'
    """
    ss_raw = [0] * 8
    ss_max = [0] * 8

    for qi, q in enumerate(questions):
        ans = answers[qi]
        if ans is None:
            continue

        ss_idx = q["ss"]
        ss_raw[ss_idx] += q["sc"][ans]
        ss_max[ss_idx] += 2  # max par question = 2

    # Normalisation SS → niveau 1/2/3
    ss_levels = []
    for i in range(8):
        if ss_max[i] == 0:
            ss_levels.append(2)
            continue
        pct = ss_raw[i] / ss_max[i]
        if pct >= 0.65:
            ss_levels.append(3)
        elif pct >= 0.35:
            ss_levels.append(2)
        else:
            ss_levels.append(1)

    return {
        "ss": ss_levels,
        "ss_raw": ss_raw,
        "ss_max": ss_max,
    }
