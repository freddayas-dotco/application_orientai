"""
OrientAI — Module de scoring
Calcule le profil soft skills et MBTI à partir des réponses au questionnaire.
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

MBTI_DESCS = {
    "INTJ": "Architecte — Stratège indépendant, visionnaire et organisé",
    "INTP": "Logicien — Penseur créatif, analytique et curieux",
    "ENTJ": "Commandant — Leader énergique, stratégique et déterminé",
    "ENTP": "Innovateur — Débatteur créatif, ingénieux et stimulant",
    "INFJ": "Avocat — Altruiste idéaliste, empathique et profond",
    "INFP": "Médiateur — Poète idéaliste, créatif et authentique",
    "ENFJ": "Protagoniste — Leader charismatique, bienveillant et inspirant",
    "ENFP": "Explorateur — Créatif enthousiaste, sociable et imaginatif",
    "ISTJ": "Logisticien — Praticien fiable, méthodique et responsable",
    "ISFJ": "Défenseur — Protecteur dédié, loyal et attentionné",
    "ESTJ": "Directeur — Organisateur efficace, pragmatique et structuré",
    "ESFJ": "Consul — Soignant populaire, sociable et attentionné",
    "ISTP": "Virtuose — Artisan expérimental, pragmatique et observateur",
    "ISFP": "Aventurier — Artiste flexible, sensible et curieux",
    "ESTP": "Entrepreneur — Pragmatique énergique, perceptif et direct",
    "ESFP": "Amuseur — Artiste spontané, enthousiaste et joueur",
}


def compute_profile(answers: list[int], questions: list[dict]) -> dict:
    """
    Calcule le profil SS + MBTI à partir des réponses.

    Args:
        answers: liste de 48 entiers (0=A, 1=B, 2=C, 3=D), None si sans réponse
        questions: liste des 48 questions (voir questionnaire.py)

    Returns:
        dict avec 'ss' (liste 8 valeurs 1-3), 'mbti' (str ex: 'INTJ'),
        'ss_raw' (scores bruts), 'mbti_votes' (dict comptage)
    """
    ss_raw = [0] * 8
    ss_max = [0] * 8
    mbti_votes = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}

    for qi, q in enumerate(questions):
        ans = answers[qi]
        if ans is None:
            continue

        # Score soft skill
        ss_idx = q["ss"]
        score = q["sc"][ans]
        ss_raw[ss_idx] += score
        ss_max[ss_idx] += 2  # max par question = 2

        # Vote MBTI
        mp = q["mp"][ans]
        if mp > 0:
            mbti_votes[q["ml"]] += mp

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

    # Calcul MBTI
    e_i = "E" if mbti_votes["E"] >= mbti_votes["I"] else "I"
    s_n = "S" if mbti_votes["S"] >= mbti_votes["N"] else "N"
    t_f = "T" if mbti_votes["T"] >= mbti_votes["F"] else "F"
    j_p = "J" if mbti_votes["J"] >= mbti_votes["P"] else "P"
    mbti = e_i + s_n + t_f + j_p

    # MBTI conservé en mémoire mais non utilisé pour corriger les SS
    # (cohérence désactivée — MBTI jugé peu fiable avec 48 questions)
    return {
        "ss": ss_levels,
        "mbti": mbti,
        "mbti_desc": MBTI_DESCS.get(mbti, ""),
        "ss_raw": ss_raw,
        "ss_max": ss_max,
        "mbti_votes": mbti_votes,
    }


def compute_matching(profile: dict, df_metiers) -> list[dict]:
    """
    Calcule le score de compatibilité entre le profil et chaque métier.

    Args:
        profile: résultat de compute_profile()
        df_metiers: DataFrame pandas des métiers

    Returns:
        Liste de dicts triée par score décroissant (Top 30, dédupliquée)
    """
    user_ss = profile["ss"]
    mbti_cols = ["E/I", "S/N", "T/F", "J/P"]  # gardé pour info dans les résultats

    results = []
    for _, row in df_metiers.iterrows():
        # Score SS (100%) — MBTI retiré du matching, utilisé uniquement en affichage
        ss_score = 0
        for i, col in enumerate(SS_COLS):
            job_val = SS_FROM_TEXT.get(str(row.get(col, "Nécessaire")), 2)
            diff = abs(user_ss[i] - job_val)
            if diff == 0:
                ss_score += 3
            elif diff == 1:
                ss_score += 1.5
        score = round((ss_score / (8 * 3)) * 100)

        results.append({
            "metier": str(row.get("Métier", "")),
            "secteur": str(row.get("Secteur(s) activité", "")),
            "domaine": str(row.get("Domaine", "")),
            "niveau": str(row.get("Niveau", "")),
            "salaire": str(row.get("Salaire", "")),
            "descriptif": str(row.get("Descriptif", "")),
            "diplomes": str(row.get("Diplômes", "")),
            "mbti_type": str(row.get("E/I", "")),
            "score": score,
        })

    # Tri + déduplication + Top 30
    seen = set()
    top = []
    for r in sorted(results, key=lambda x: -x["score"]):
        key = r["metier"].lower().strip()
        if key not in seen:
            seen.add(key)
            top.append(r)
        if len(top) >= 30:
            break

    return top
