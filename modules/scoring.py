def compute_ss_scores(questions, answers):
    """
    Calcule les scores Soft Skills (niveau 1, 2, ou 3) sur les 8 dimensions.
    answers: list d'index de réponse (0=A, 1=B, 2=C, 3=D) pour chaque question.
    """
    ss_raw = [0] * 8
    ss_max = [0] * 8
    
    for i, q in enumerate(questions):
        if i >= len(answers) or answers[i] is None: continue
        
        ans = answers[i]
        idx = q["ss_idx"]
        ss_max[idx] += 2
        
        pts = 0
        if q["scoring"] == "normal":
            if ans == 0: pts = 2       # A
            elif ans == 1: pts = 1     # B
        else: # scoring inversé
            if ans == 2: pts = 2       # C
            elif ans == 3: pts = 1     # D
            
        ss_raw[idx] += pts
        
    ss_levels = []
    for i in range(8):
        max_pts = ss_max[i] if ss_max[i] > 0 else 1
        pct = ss_raw[i] / max_pts
        if pct >= 0.65: ss_levels.append(3)
        elif pct >= 0.35: ss_levels.append(2)
        else: ss_levels.append(1)
        
    return ss_levels

def compute_mbti(questions, answers):
    """Calcule le profil MBTI (4 lettres) en fonction des choix."""
    counts = {'E':0, 'I':0, 'S':0, 'N':0, 'T':0, 'F':0, 'J':0, 'P':0}
    
    for i, q in enumerate(questions):
        if i >= len(answers) or answers[i] is None or not q["mbti_dim"]: continue
        
        ans = answers[i]
        dim = q["mbti_dim"] # ex: 'EI', 'SN'
        if len(dim) != 2: continue
        
        l1, l2 = dim[0], dim[1]
        letter = None
        
        if q["scoring"] == "normal":
            if ans in (0, 1): letter = l1
            else: letter = l2
        else:
            if ans in (2, 3): letter = l1
            else: letter = l2
            
        if letter in counts:
            counts[letter] += 1
            
    mbti = ""
    mbti += 'E' if counts['E'] >= counts['I'] else 'I'
    mbti += 'S' if counts['S'] >= counts['N'] else 'N'
    mbti += 'T' if counts['T'] >= counts['F'] else 'F'
    mbti += 'J' if counts['J'] >= counts['P'] else 'P'
    
    return mbti
