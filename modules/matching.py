import pandas as pd

def calculate_match_score(user_ss, user_mbti, metier_row):
    """
    Calcule le score de compatibilité (sur 100) pour un métier.
    - SS: 70%
    - MBTI: 30%
    """
    # 1. Soft skills score
    ss_score = 0
    metier_ss = [
        metier_row['SS_Communication'], metier_row['SS_Esprit_critique'],
        metier_row['SS_Ethique'], metier_row['SS_Intelligence_emotionnelle'],
        metier_row['SS_Intelligence_sociale'], metier_row['SS_Management_projet'],
        metier_row['SS_Management_equipe'], metier_row['SS_Organisation']
    ]
    
    for i in range(8):
        diff = abs(user_ss[i] - metier_ss[i])
        if diff == 0: ss_score += 3
        elif diff == 1: ss_score += 1.5
        # diff 2 -> +0
        
    ss_pct = ss_score / (8 * 3)
    
    # 2. MBTI bonus
    m_mbti = str(metier_row['MBTI_Type'])
    mbti_match = sum(1 for i in range(4) if i < len(user_mbti) and i < len(m_mbti) and user_mbti[i] == m_mbti[i])
    mbti_pct = mbti_match / 4
    
    # Final Score 0-100
    score = round((ss_pct * 0.7 + mbti_pct * 0.3) * 100)
    return score

def get_top_metiers(df, user_ss, user_mbti, top_n=30, secteur_filter=None, niveau_filter=None):
    """Retourne les meilleurs métiers pour l'utilisateur."""
    if df.empty: return []
    
    pool = df.copy()
    
    if secteur_filter and secteur_filter != "Tous":
        # Garder les métiers dont le secteur (qui peut contenir plusieurs valeurs séparées par ;) inclut le filtre
        pool = pool[pool['Secteur'].apply(lambda s: secteur_filter in [x.strip() for x in str(s).split(';') if x.strip()])]
        
    if niveau_filter and niveau_filter != "Tous":
        pool = pool[pool['Niveau'].str.strip() == niveau_filter]
        
    if pool.empty: return []
    
    # Score all
    pool['Score'] = pool.apply(lambda row: calculate_match_score(user_ss, user_mbti, row), axis=1)
    
    # Deduplicate by métier name (case insensitive)
    pool['Lower_Metier'] = pool['Métier'].str.lower().str.strip()
    pool = pool.drop_duplicates(subset=['Lower_Metier'])
    
    # Sort and top N
    results = pool.sort_values(by=['Score'], ascending=False).head(top_n)
    
    return results.to_dict('records')
