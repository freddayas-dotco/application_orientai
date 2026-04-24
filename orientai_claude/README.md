# OrientAI — Application d'orientation scolaire

Application Streamlit d'orientation par soft skills et profil MBTI. Questionnaire 48 questions, matching sur 1 170+ métiers.

## Structure des fichiers

```
orientai_claude/
├── appclaude.py        ← application principale
├── questionnaire.py    ← les 48 questions
├── scoring.py          ← calcul SS + MBTI
├── matching.py         ← algorithme de matching métiers
├── sauvegarde.py       ← sauvegarde Google Sheets + CSV
├── rapport_pdf.py      ← génération de rapports PDF
├── rapport_v2.py       ← génération de rapports Word
├── donnees_rapport.py  ← données pour les rapports
├── requirements.txt    ← dépendances Python
└── data/
    ├── Metiers_OrientAI_v5.2.xlsx   ← base de données métiers
    └── resultats.csv                ← créé automatiquement (local)
```

## Installation locale

### 1. Créer et activer l'environnement virtuel
```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash
.venv\Scripts\activate.bat      # Windows CMD
source .venv/bin/activate       # Mac/Linux
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configurer les credentials Google (optionnel)
Placer le fichier `google_credentials.json` dans ce dossier pour activer la sauvegarde Google Sheets.

Pour le développement local avec `st.secrets`, créer `.streamlit/secrets.toml` à la racine du projet (voir `.streamlit/secrets.toml` pour le format).

### 4. Lancer l'application
```bash
streamlit run appclaude.py
```

L'application s'ouvre sur http://localhost:8501

---

## Déploiement sur Streamlit Cloud

### Étape 1 — Créer le dépôt GitHub

1. Aller sur https://github.com/new
2. Nom du dépôt : `orientai` (ou autre)
3. Visibilité : **Public** (requis pour Streamlit Cloud gratuit) ou Private (avec abonnement)
4. Ne pas initialiser avec README (vous avez déjà les fichiers)
5. Cliquer **Create repository**

### Étape 2 — Pousser le code sur GitHub

Dans le terminal, à la racine du projet (`Application orientation/`) :

```bash
git init
git add .
git commit -m "Initial commit — OrientAI"
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/orientai.git
git push -u origin main
```

> Vérifier que `.gitignore` exclut bien `google_credentials.json` et `secrets.toml` avant le push.

### Étape 3 — Déployer sur Streamlit Cloud

1. Aller sur https://share.streamlit.io
2. Se connecter avec GitHub
3. Cliquer **New app**
4. Remplir le formulaire :
   - **Repository** : `VOTRE_USERNAME/orientai`
   - **Branch** : `main`
   - **Main file path** : `orientai_claude/appclaude.py`
5. Cliquer **Advanced settings** pour configurer les secrets (voir ci-dessous)
6. Cliquer **Deploy**

### Étape 4 — Configurer les secrets Google Sheets

Dans Streamlit Cloud, aller dans **App menu (⋮) → Settings → Secrets** et coller :

```toml
GOOGLE_SHEET_ID = "1-clYEeefpu5Hx9Cl2Tp-4R1AVRsbACcLZtJVvFPrdZc"

[gcp_service_account]
type = "service_account"
project_id = "votre-project-id"
private_key_id = "votre-key-id"
private_key = "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----\n"
client_email = "votre-compte@votre-projet.iam.gserviceaccount.com"
client_id = "votre-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/votre-compte%40votre-projet.iam.gserviceaccount.com"
universe_domain = "googleapis.com"
```

> Copier les vraies valeurs depuis votre fichier `google_credentials.json`.

---

## Fonctionnalités

- **Questionnaire 48 questions** (version Collège / Lycée-Adulte)
- **Profil calculé** : 8 soft skills + type MBTI (16 types)
- **Matching** sur 1 170+ métiers (70% soft skills + 30% MBTI)
- **Filtres** par secteur d'activité et niveau hiérarchique
- **Rapports** PDF et Word téléchargeables
- **Sauvegarde** dans Google Sheets (cloud) + CSV local (backup)
- **Dashboard conseiller** : statistiques MBTI, soft skills, métiers populaires

## Notes sur la persistance des données

- Google Sheets : persistance totale, accessible depuis n'importe où
- CSV local : **ne persiste pas** entre les sessions sur Streamlit Cloud (système de fichiers éphémère)
- Recommandation : toujours configurer Google Sheets pour un usage en production
