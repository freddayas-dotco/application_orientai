# OrientAI — Contexte complet du projet

> Fichier de contexte pour agent IA (Antigravity / Claude / Copilot).
> Contient toute la logique métier, les structures de données et les règles du projet OrientAI.

---

## 1. Présentation du projet

**OrientAI** est un outil d'orientation scolaire et professionnelle basé sur les soft skills et le profil MBTI.
Il permet à un élève (collège, lycée) ou un adulte de répondre à 48 questions, d'obtenir son profil de soft skills + son type MBTI, puis de se voir recommander les métiers les plus compatibles parmi une base de 1 170 métiers.

**Public cible :** élèves de collège/lycée, étudiants, adultes en reconversion  
**Contexte d'usage :** conseiller d'orientation, établissement scolaire, usage individuel  
**Stack actuelle :** HTML + JavaScript pur (fichier unique auto-contenu)  
**Stack cible :** Streamlit (Python) pour version avancée avec sauvegarde des résultats

---

## 2. Fichiers du projet

| Fichier | Description |
|---------|-------------|
| `OrientAI_v2_48questions.html` | Application web complète (questionnaire + matching) |
| `Metiers_OrientAI_v5.1.xlsx` | Base de données Excel des 1 170 métiers |
| `Questionnaire_v5_Lycee_Adulte_48q.xlsx` | Questionnaire 48 questions version lycée/adulte |
| `Questionnaire_v5_College_48q.xlsx` | Questionnaire 48 questions version collège |
| `metiers_v51_final.csv` | Source de vérité CSV de la base métiers |

---

## 3. Structure de la base métiers (Excel v5.1)

**1 170 métiers · 33 colonnes · 2 feuilles** (Métiers + Référentiels)

### Colonnes principales

| Col | Nom | Type | Description |
|-----|-----|------|-------------|
| A | N° | int | Identifiant unique |
| B | Métier | str | Nom du métier |
| C | Secteur(s) d'activité | str | Un ou plusieurs secteurs séparés par ` ; ` |
| D | Domaine | str | Domaine d'activité |
| E | Niveau | str | Niveau hiérarchique |
| F | Diplômes requis | str | Formation nécessaire |
| G | Salaire | str | Fourchette salariale |
| H | Descriptif | str | Description du métier |
| I | ONISEP | str | URL fiche métier ONISEP |
| J–Q | 8 Soft Skills | int | Valeurs 1/2/3 (voir section 4) |
| R–U | MBTI | str | Lettres MBTI : E/I, S/N, T/F, J/P |
| V–AD | 9 Capacités | bool | V ou vide |
| AE | Code ROME | str | Code ROME 4.0 (France Travail) |
| AF | Éco | bool | Indicateur économique |
| AG | Num | bool | Indicateur numérique |

### Niveaux hiérarchiques
`Opérationnel` · `Manager` · `Responsable` · `Directeur` · `PDG / Dirigeant` · `Entrepreneur`

### Règle multi-secteurs
- Séparateur : ` ; ` (espace-point-virgule-espace)
- Premier secteur = le plus pertinent/naturel
- Filtrage : `metier.secteurs.split(' ; ').includes(secteurChoisi)`
- Cellules multi-secteurs colorées en vert clair (#E0F4F4) dans Excel

---

## 4. Les 8 Soft Skills

| Index | Soft Skill | Col Excel |
|-------|-----------|-----------|
| 0 | Communication | J |
| 1 | Esprit critique | K |
| 2 | Éthique | L |
| 3 | Intelligence émotionnelle | M |
| 4 | Intelligence sociale | N |
| 5 | Management de projet | O |
| 6 | Management et gestion d'équipe | P |
| 7 | Organisation | Q |

### Valeurs
- `1` = Peu nécessaire
- `2` = Nécessaire  
- `3` = Absolument nécessaire

### Règles de cohérence (auditées)
1. **Management d'équipe "AbsNec" (3)** → réservé aux niveaux Manager/Responsable/Directeur. Exceptions : chef cuisinier, chef sommelier, formateur, moniteur, maître d'…
2. **Communication "AbsNec" implique Intel. sociale ≥ "Nécessaire"** → jamais "Peu nécessaire"
3. **Esprit critique ≥ "Nécessaire" (2)** pour les métiers analytiques : Médical, Chimie, Informatique, Droit, Banque, Gestion de projet, et tous les Analyste*/Designer*/Concepteur*/Chef de projet*
4. **Éthique quasi-universelle** : 99% des métiers ont au moins "Nécessaire"

### Distribution actuelle
| Soft Skill | AbsNec (3) | Nec (2) | PeuNec (1) |
|---|---|---|---|
| Communication | 503 (43%) | 549 (47%) | 118 (10%) |
| Esprit critique | 463 (40%) | 649 (55%) | 58 (5%) |
| Éthique | 430 (37%) | 727 (62%) | 13 (1%) |
| Intel. émotionnelle | 310 (26%) | 480 (41%) | 380 (32%) |
| Intel. sociale | 343 (29%) | 498 (43%) | 329 (28%) |
| Mgmt de projet | 179 (15%) | 553 (47%) | 438 (37%) |
| Mgmt d'équipe | 129 (11%) | 212 (18%) | 829 (71%) |
| Organisation | 559 (48%) | 558 (48%) | 53 (5%) |

---

## 5. Les 9 Capacités (colonnes V–AD)

| Colonne | Capacité | Verbes associés |
|---------|---------|-----------------|
| V | Cap_Aider | Aider, secourir, soigner, protéger, défendre, soutenir, réparer, restaurer, entretenir |
| W | Cap_Communiquer | Communiquer, formuler, transmettre, échanger, informer, négocier |
| X | Cap_Concevoir | Concevoir, créer, inventer, produire, construire, assembler |
| Y | Cap_Conseiller | Conseiller, accompagner, former, guider, éduquer, orienter |
| Z | Cap_Diriger | Diriger, gérer, piloter, coordonner, planifier, superviser, élaborer |
| AA | Cap_Manipuler | Manipuler, réaliser, pratiquer, jouer |
| AB | Cap_Preparer | Préparer, installer, fournir, distribuer, conduire, transporter, livrer, ranger |
| AC | Cap_Analyser | Rechercher, analyser, étudier, contrôler, surveiller, tester, prouver, valider |
| AD | Cap_Saisir | Saisir, classer, ranger, organiser, ordonner, documenter, rédiger |

---

## 6. Les 61 Secteurs d'activité

```
Administration, Aéronautique et transport aérien, Agriculture, Agroalimentaire,
Animalier, Armée - sécurité - défense, Art, Artisanat, Assurance, Automobile,
Banque - finance, Bâtiment - construction, Chimie - biologie - science,
Cinéma - audiovisuel, Commerce, Commerce international, Communication,
Comptabilité - gestion - contrôle de gestion, Culture, Droit - justice,
Economie, Édition et métier du livre - littérature, Électronique, Énergie,
Enseignement, Environnement, Esthétique, Événementiel, Fonction publique,
Funéraire - mortuaire, Gestion de projet, Grande distribution,
Hôtellerie - restauration - gastronomie, Humanitaire, Immobilier, Industrie,
Informatique - numérique - digital, Internet - web, Jeux vidéo, Journalisme,
Luxe, Médias - multimédia - publicité, Médical - santé - Pharmaceutique,
Métallurgie - sidérurgie, Mode - textile, Musique,
Nautique - metiers de la mer, Plasturgie, Politique,
Psychologie - psychothérapie, Publicité, Puériculture,
Ressources humaines, Social, Spatial, Spectacle - divertissement,
Sport, Télécommunication, Transport - logistique - approvisionnement,
Vin, Voyages - tourisme
```

## 7. Les 42 Domaines d'activité

```
Accueil - service - suivi client, Achat - approvisionnement, Administratif,
Approvisionnement, Artisanat, Audit - contrôle de gestion, Commercial,
Communication, Comptabilité, Conduite du changement, Conception artistique,
Conception esthétique, Conception gastronomique, Conception graphique,
Conception mécanique, Conception technique technologique ou informatique,
Conseil - consulting, Distribution, Entretien - nettoyage, Étude et expertise,
Finance, Formation - coaching, Gestion de projet, Installation et/ou maintenance,
Juridique, Logistique, Marketing, Médical, Production, Qualité - conformité,
Recherche et développement, Recrutement - mobilité, Relation sociale,
Renseignement, Scientifique, Sécurité, Services à la personne,
Services aux entreprises, Sportif, Stratégie, Technique, Transport
```

---

## 8. Le questionnaire 48 questions

### Structure
- **48 questions** réparties en 8 groupes (6 questions par soft skill, sauf Communication = 7 et Intel. Sociale = 5)
- **4 options de réponse** par question (A, B, C, D)
- **2 versions** : Lycée/Adulte (vouvoiement, contexte pro) · Collège (tutoiement, contexte scolaire)
- **Double scoring** : chaque question score à la fois une soft skill ET une dimension MBTI

### Scoring Soft Skills
- Scoring normal (A=2, B=1, C=0, D=0) : ~75% des questions
- Scoring inversé (C=2, D=1, A=0, B=0) : ~25% des questions (questions à sens négatif)
- Score brut → normalisé en niveau 1/2/3 : ≥65% = 3, ≥35% = 2, <35% = 1

### Scoring MBTI
Chaque question vote pour une lettre MBTI selon la réponse :

| Dimension | Lettres | Signification |
|-----------|---------|---------------|
| E/I | Extraverti / Introverti | Énergie |
| S/N | Sensitif / iNtuitif | Recueil d'information |
| T/F | Thinking / Feeling | Prise de décision |
| J/P | Jugement / Perception | Mode d'action |

La lettre dominante dans chaque paire détermine le profil final (ex: INTJ, ENFP…)

### Répartition des questions par soft skill
| Soft Skill | Nb questions | Dimensions MBTI couvertes |
|---|---|---|
| Communication | 7 | E/I, J/P, T/F |
| Esprit critique | 6 | S/N, J/P |
| Éthique | 6 | T/F |
| Intel. émotionnelle | 6 | T/F, E/I, J/P |
| Intel. sociale | 6 | E/I |
| Mgmt de projet | 6 | J/P, T/F |
| Mgmt d'équipe | 6 | T/F, E/I, J/P |
| Organisation | 6 | J/P, S/N |

---

## 9. Algorithme de matching

```python
def compute_score(user_profile, metier):
    """
    user_profile = {
        'ss': [1-3, 1-3, 1-3, 1-3, 1-3, 1-3, 1-3, 1-3],  # 8 soft skills
        'mbti': 'INTJ'  # 4 lettres
    }
    """
    # SS score (70% du poids total)
    ss_score = 0
    for i in range(8):
        diff = abs(user_profile['ss'][i] - metier['ss'][i])
        if diff == 0:   ss_score += 3
        elif diff == 1: ss_score += 1.5
        else:           ss_score += 0
    ss_pct = ss_score / (8 * 3)  # normalisation 0-1

    # MBTI bonus (30% du poids total)
    mbti_match = sum(
        1 for i, (u, m) in enumerate(zip(user_profile['mbti'], metier['mbti']))
        if u == m
    )
    mbti_pct = mbti_match / 4  # 0 à 1

    # Score final
    score = round((ss_pct * 0.7 + mbti_pct * 0.3) * 100)
    return score
```

**Post-traitement :**
- Filtrage optionnel par secteur et/ou niveau hiérarchique
- Déduplication par nom de métier (casse insensible)
- Tri décroissant par score
- Affichage du Top 30

---

## 10. Architecture de l'application HTML actuelle

### Écrans (séquentiels)
1. **Accueil** → choix Lycéen / Adulte
2. **Quiz** → 48 questions avec barre de progression et auto-avancement
3. **Profil** → affichage MBTI + 8 barres soft skills + filtres secteur/niveau
4. **Chargement** → spinner 1,2s
5. **Résultats** → Top 30 métiers avec score, secteur, lien fiche ONISEP

### Variables d'état JavaScript
```javascript
let mode = null;          // 'lycee' ou 'adulte'
let currentQ = 0;         // index question courante (0-48)
let answers = [];         // tableau des réponses (0-3 = indice option)
let computedSS = [];      // [1-3] × 8 après calcul
let computedMBTI = '';    // ex: 'INTJ'
let selectedSecteurs = []; // filtres secteur actifs
let selectedNiveaux = [];  // filtres niveau actifs
```

### Données embarquées
Les 1 170 métiers sont embarqués directement dans le JS sous forme d'objet `DATA` :
```javascript
const DATA = {
  records: [{
    m: "Nom du métier",
    s: "Secteur",        // peut contenir ' ; ' pour multi-secteurs
    n: "Niveau",
    l: "https://...",    // lien ONISEP
    sal: "",             // salaire (souvent vide)
    ss: [2,2,3,1,2,1,1,3],  // 8 valeurs soft skills
    mbti: { "E/I": "E", "S/N": "N", "T/F": "T", "J/P": "J" }
  }],
  ss_labels: [...],
  secteurs: [...]
}
```

---

## 11. Évolutions prévues (version Streamlit)

### Fonctionnalités prioritaires
1. **Sauvegarde des résultats** → CSV ou SQLite par élève (nom, classe, date, profil MBTI, scores SS, top 10 métiers)
2. **Dashboard conseiller** → vue agrégée d'une classe, histogrammes des profils MBTI, métiers populaires
3. **Mise à jour base** → rechargement du CSV sans toucher au code
4. **Export PDF** → fiche résultat personnalisée par élève

### Structure Streamlit recommandée
```
orientai/
├── app.py                 # point d'entrée Streamlit
├── data/
│   ├── metiers_v51.csv    # base des métiers
│   └── resultats.csv      # résultats sauvegardés
├── modules/
│   ├── questionnaire.py   # logique des 48 questions
│   ├── scoring.py         # calcul SS + MBTI
│   ├── matching.py        # algorithme de matching
│   └── dashboard.py       # vue conseiller
└── requirements.txt       # streamlit, pandas, openpyxl
```

### Dépendances Python
```
streamlit>=1.30
pandas>=2.0
openpyxl>=3.1
```

---

## 12. Points d'attention / pièges connus

1. **Apostrophes françaises** dans les textes JS → toujours utiliser des guillemets doubles `"..."` ou des backticks `` `...` `` pour les chaînes contenant `l'`, `d'`, `j'`, etc.

2. **Multi-secteurs** → le champ `s` peut contenir plusieurs secteurs séparés par ` ; `. Toujours splitter avant de comparer : `r.s.split(' ; ').includes(filtre)`

3. **Valeurs SS** → échelle 1/2/3 (pas 0/1/2). Les formules de normalisation supposent min=1, max=3.

4. **MBTI dans la base** → stocké comme objet `{ "E/I": "E", "S/N": "N", ... }` et non comme string `"ENTJ"`. Adapter les comparaisons en conséquence.

5. **~145 métiers sans code ROME** → métiers très spécifiques non couverts par ROME 4.0. Champ `AE` vide pour ces entrées.

6. **Encodage** → tous les fichiers sont en UTF-8. Les accents français (é, è, ê, à, ù, ô, î, etc.) sont fréquents dans les noms de métiers et secteurs.

---

## 13. Sources de données

| Source | Usage | Accès |
|--------|-------|-------|
| ROME 4.0 (France Travail) | Codes métiers, appellations | Open data — 1 584 fiches, 13 120 appellations |
| ONISEP | Fiches métiers, liens | URLs directes web_fetch |
| Base maison | 1 170 métiers enrichis | `metiers_v51_final.csv` |

---

*Dernière mise à jour : mars 2026 — Version 5.1*
