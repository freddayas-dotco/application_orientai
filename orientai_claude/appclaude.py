import os
"""
OrientAI — Application Streamlit complète
Questionnaire 48 questions + Résultats + Sauvegarde + Dashboard conseiller
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from questionnaire import QUESTIONS_ADULTE, QUESTIONS_ELEVE, SS_SECTION_NAMES
from scoring import compute_profile, compute_matching, SS_LABELS, SS_TEXT, SS_COLS
from sauvegarde import sauvegarder, charger_resultats, effacer_resultats, sauvegarder_enquete, charger_enquete
from rapport_v2 import generer_rapport_v2
from rapport_pdf import generer_pdf
from donnees_rapport import MENTION_SALAIRE

# ── Configuration page ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OrientAI",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS personnalisé ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: 700; color: #1a1a2e; margin-bottom: 0; }
    .subtitle { font-size: 1rem; color: #7a7a8c; margin-bottom: 2rem; }
    .gold { color: #c9a84c; }
    .rose { color: #d4667a; }
    .question-header { font-size: 0.75rem; font-weight: 600; letter-spacing: 2px;
        text-transform: uppercase; color: #c9a84c; margin-bottom: 0.3rem; }
    .question-text { font-size: 1.2rem; font-weight: 500; color: #1a1a2e; margin-bottom: 1.5rem; }
    .score-badge { display: inline-block; padding: 4px 12px; border-radius: 20px;
        font-size: 0.85rem; font-weight: 600; }
    .score-high { background: #e8f3ec; color: #2a6a44; }
    .score-med { background: #fdf3dc; color: #8a6a14; }
    .score-low { background: #f5f5f5; color: #666; }
    .mbti-badge { font-size: 2.5rem; font-weight: 700; color: #d4667a; }
    div[data-testid="stRadio"] > label { font-size: 1rem; }
    .stProgress > div > div { background-color: #c9a84c; }
</style>
""", unsafe_allow_html=True)

# ── Chargement données métiers ─────────────────────────────────────────────────
@st.cache_data
def load_metiers():
    try:
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), "data/metiers_v52_final.csv"), sep=";", encoding="utf-8-sig")
        return df
    except FileNotFoundError:
        return None


df_metiers = load_metiers()
if df_metiers is None:
    st.warning("⚠️ Fichier data/metiers_v52_final.csv introuvable. Placez-le dans le dossier data/.")
    df_metiers = pd.DataFrame()


@st.cache_data
def load_excel_metiers():
    df = pd.read_excel(
        "data/Metiers_OrientAI_v5.2.xlsx",
        sheet_name=0, header=0
    )
    df = df.dropna(subset=["Métier"])
    df = df[df["Métier"].astype(str).str.strip() != ""]
    return df


# ── Mot de passe conseiller (à modifier ici) ─────────────────────────────────
CONSEILLER_PASSWORD = "orientai2025"

# ── Initialisation session state global ──────────────────────────────────────
if "espace" not in st.session_state:
    st.session_state.espace = None          # None | "eleve" | "conseiller"
if "conseiller_auth" not in st.session_state:
    st.session_state.conseiller_auth = False
if "enquete_envoyee" not in st.session_state:
    st.session_state.enquete_envoyee = False

# ── Sidebar : uniquement visible si espace choisi ────────────────────────────
if st.session_state.espace == "eleve":
    with st.sidebar:
        st.markdown("## 🧭 OrientAI")
        st.markdown("*Espace élève*")
        st.markdown("---")
        page = st.radio(
            "Navigation",
            ["🏠 Accueil", "📋 Questionnaire", "🔎 Explorer les métiers"],
            label_visibility="collapsed",
        )
        st.markdown("---")
        if st.button("← Changer d'espace", use_container_width=True):
            st.session_state.espace = None
            st.session_state.etape = "accueil"
            st.rerun()
        st.markdown("*OrientAI v5.2 — 1 163 métiers*")

elif st.session_state.espace == "adulte":
    with st.sidebar:
        st.markdown("## 🧭 OrientAI")
        st.markdown("*Espace adulte / pro*")
        st.markdown("---")
        page = st.radio(
            "Navigation",
            ["🏠 Accueil", "📋 Questionnaire", "🔎 Explorer les métiers"],
            label_visibility="collapsed",
        )
        st.markdown("---")
        if st.button("← Changer d'espace", use_container_width=True):
            st.session_state.espace = None
            st.session_state.etape = "accueil"
            st.rerun()
        st.markdown("*OrientAI v5.2 — 1 163 métiers*")

elif st.session_state.espace == "conseiller":
    with st.sidebar:
        st.markdown("## 🧭 OrientAI")
        st.markdown("*Espace conseiller*")
        st.markdown("---")
        page = st.radio(
            "Navigation",
            ["📊 Dashboard"],
            label_visibility="collapsed",
        )
        st.markdown("---")
        if st.button("← Changer d'espace", use_container_width=True):
            st.session_state.espace = None
            st.session_state.conseiller_auth = False
            st.rerun()
        st.markdown("*OrientAI v5.2 — 1 163 métiers*")
else:
    page = None


# ══════════════════════════════════════════════════════════════════════════════
# PAGE D'ACCUEIL — CHOIX DE L'ESPACE (3 cartes)
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.espace is None:

    st.markdown("""
    <style>
    .orientai-card {
        background: #faf8f3;
        border: 2px solid #e8e2d5;
        border-radius: 18px;
        padding: 36px 20px 28px 20px;
        text-align: center;
        margin-bottom: 14px;
        min-height: 175px;
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease, background 0.18s ease;
    }
    .orientai-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 32px rgba(26, 26, 46, 0.13);
        border-color: #c9a84c;
        background: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:

        # ── Titre principal ────────────────────────────────────────────────────
        st.markdown("""
        <div style="text-align:center; padding: 2.8rem 0 1.8rem 0;">
            <div style="font-size:4rem; font-weight:900; color:#1a1a2e;
                        letter-spacing:-2px; line-height:1.05;">
                🧭 Orient<span style="color:#d4667a">AI</span>
            </div>
            <div style="font-size:1.05rem; color:#7a7a8c; font-style:italic;
                        margin-top:1rem; line-height:1.7; font-weight:400;">
                Découvre les métiers qui te correspondent vraiment<br>
                grâce à tes soft skills et ton profil MBTI
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Bande de statistiques ──────────────────────────────────────────────
        st.markdown("""
        <div style="display:flex; background:#f5f2eb; border-radius:16px;
                    padding:1.8rem 0; margin: 0 0 2.5rem 0;">
            <div style="flex:1; text-align:center; border-right:1px solid #ddd6c8;">
                <div style="font-size:2.5rem; font-weight:800; color:#1a1a2e; line-height:1.1;">48</div>
                <div style="font-size:0.7rem; color:#9a9aac; text-transform:uppercase;
                            letter-spacing:1.5px; margin-top:7px; font-weight:600;">Questions</div>
            </div>
            <div style="flex:1; text-align:center; border-right:1px solid #ddd6c8;">
                <div style="font-size:2.5rem; font-weight:800; color:#c9a84c; line-height:1.1;">1 163</div>
                <div style="font-size:0.7rem; color:#9a9aac; text-transform:uppercase;
                            letter-spacing:1.5px; margin-top:7px; font-weight:600;">Métiers</div>
            </div>
            <div style="flex:1; text-align:center; border-right:1px solid #ddd6c8;">
                <div style="font-size:2.5rem; font-weight:800; color:#6b9e7e; line-height:1.1;">61</div>
                <div style="font-size:0.7rem; color:#9a9aac; text-transform:uppercase;
                            letter-spacing:1.5px; margin-top:7px; font-weight:600;">Secteurs</div>
            </div>
            <div style="flex:1; text-align:center;">
                <div style="font-size:2.5rem; font-weight:800; color:#d4667a; line-height:1.1;">8</div>
                <div style="font-size:0.7rem; color:#9a9aac; text-transform:uppercase;
                            letter-spacing:1.5px; margin-top:7px; font-weight:600;">Soft skills</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Section "Tu es :" ──────────────────────────────────────────────────
        st.markdown("""
        <div style="display:flex; align-items:center; gap:1.2rem; margin: 0 0 1.8rem 0;">
            <div style="flex:1; height:1px;
                        background:linear-gradient(to right, transparent, #d9d3c7);"></div>
            <div style="font-size:0.9rem; font-weight:700; color:#1a1a2e;
                        letter-spacing:2.5px; text-transform:uppercase; white-space:nowrap;">
                Tu es :
            </div>
            <div style="flex:1; height:1px;
                        background:linear-gradient(to left, transparent, #d9d3c7);"></div>
        </div>
        """, unsafe_allow_html=True)

        col_eleve, col_adulte, col_conseiller = st.columns(3)

        with col_eleve:
            st.markdown("""
            <div class="orientai-card">
                <div style="font-size:3.2rem; margin-bottom:12px;">🎓</div>
                <div style="font-size:1.05rem; font-weight:700; color:#1a1a2e; margin-bottom:7px;">Élève</div>
                <div style="font-size:0.8rem; color:#9a9aac;">Collège · Lycée</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Accéder →", key="btn_eleve", type="primary", use_container_width=True):
                st.session_state.espace = "eleve"
                st.session_state.mode = "lycee"
                st.session_state.etape = "accueil"
                st.rerun()

        with col_adulte:
            st.markdown("""
            <div class="orientai-card">
                <div style="font-size:3.2rem; margin-bottom:12px;">💼</div>
                <div style="font-size:1.05rem; font-weight:700; color:#1a1a2e; margin-bottom:7px;">Adulte / Pro</div>
                <div style="font-size:0.8rem; color:#9a9aac;">Étudiant·e · Professionnel·le</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Accéder →", key="btn_adulte", type="primary", use_container_width=True):
                st.session_state.espace = "adulte"
                st.session_state.mode = "adulte"
                st.session_state.etape = "accueil"
                st.rerun()

        with col_conseiller:
            st.markdown("""
            <div class="orientai-card">
                <div style="font-size:3.2rem; margin-bottom:12px;">👩‍🏫</div>
                <div style="font-size:1.05rem; font-weight:700; color:#1a1a2e; margin-bottom:7px;">Conseiller·e</div>
                <div style="font-size:0.8rem; color:#9a9aac;">Enseignant·e · CPE · COP</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Accéder →", key="btn_conseiller", type="secondary", use_container_width=True):
                st.session_state.espace = "conseiller"
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# ESPACE ÉLÈVE ou ADULTE — PAGE ACCUEIL
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.espace in ("eleve", "adulte") and page == "🏠 Accueil":
    col1, col2, col3 = st.columns([1, 2, 1])
    is_adulte = st.session_state.espace == "adulte"
    with col2:
        icon = "💼" if is_adulte else "🎓"
        titre = "Bienvenue" + (" dans l'espace adulte" if is_adulte else "")
        st.markdown(f"## {icon} {titre}")
        st.markdown("### Comment ça marche ?")
        st.markdown("""
1. **Réponds aux 48 questions** sur tes comportements et préférences
2. **Obtiens ton profil** : 8 soft skills + type MBTI
3. **Découvre tes métiers** classés par compatibilité
4. **Sauvegarde tes résultats** si ton conseiller te le demande
        """)
        st.info("👈 Clique sur **📋 Questionnaire** dans le menu pour commencer.")


# ══════════════════════════════════════════════════════════════════════════════
# ESPACE CONSEILLER — MOT DE PASSE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.espace == "conseiller" and not st.session_state.conseiller_auth:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 🔒 Espace conseiller")
        st.markdown("Cet espace est réservé aux conseillers d'orientation et enseignants.")
        st.markdown("")

        pwd = st.text_input("Mot de passe", type="password", placeholder="Entrez le mot de passe")

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Annuler", use_container_width=True):
                st.session_state.espace = None
                st.rerun()
        with col_btn2:
            if st.button("Connexion →", type="primary", use_container_width=True):
                if pwd == CONSEILLER_PASSWORD:
                    st.session_state.conseiller_auth = True
                    st.rerun()
                else:
                    st.error("Mot de passe incorrect.")

        st.markdown("---")
        st.caption(f"Mot de passe par défaut : `{CONSEILLER_PASSWORD}` — à modifier dans le code ligne 'CONSEILLER_PASSWORD'")


# ══════════════════════════════════════════════════════════════════════════════
# ESPACE QUESTIONNAIRE ÉLÈVE ou ADULTE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.espace in ("eleve", "adulte") and page == "📋 Questionnaire":

    # Sélection de la version des questions selon l'espace
    QUESTIONS = QUESTIONS_ELEVE if st.session_state.espace == "eleve" else QUESTIONS_ADULTE

    # Initialisation session state
    if "etape" not in st.session_state:
        st.session_state.etape = "accueil"
    if "answers" not in st.session_state:
        st.session_state.answers = [None] * len(QUESTIONS)
    if "q_idx" not in st.session_state:
        st.session_state.q_idx = 0
    if "profile" not in st.session_state:
        st.session_state.profile = None
    if "top_metiers" not in st.session_state:
        st.session_state.top_metiers = []

    # ── Étape ACCUEIL ─────────────────────────────────────────────────────────
    if st.session_state.etape == "accueil":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            is_adulte = st.session_state.espace == "adulte"
            st.markdown(f"## {'💼' if is_adulte else '🎓'} Avant de commencer")
            st.markdown(f"*Version : {'Adulte / Professionnel·le' if is_adulte else 'Élève / Lycéen·ne'}*")
            st.markdown("---")
            st.markdown("**Tes informations** *(optionnel — pour sauvegarder tes résultats)*")
            prenom = st.text_input("Prénom", placeholder="Ex: Marie")
            nom = st.text_input("Nom", placeholder="Ex: Dupont")
            classe = st.text_input(
                "Classe / Formation" if not is_adulte else "Poste / Formation actuelle",
                placeholder="Ex: Terminale S" if not is_adulte else "Ex: Chargé de projet, Master RH…"
            )

            st.markdown("---")
            if st.button("Commencer le questionnaire →", type="primary", use_container_width=True):
                st.session_state.prenom = prenom
                st.session_state.nom = nom
                st.session_state.classe = classe
                st.session_state.answers = [None] * len(QUESTIONS)
                st.session_state.q_idx = 0
                st.session_state.etape = "quiz"
                st.rerun()

    # ── Étape QUIZ ────────────────────────────────────────────────────────────
    elif st.session_state.etape == "quiz":
        idx = st.session_state.q_idx
        total = len(QUESTIONS)
        q = QUESTIONS[idx]
        current_answer = st.session_state.answers[idx]

        # CSS boutons réponse
        st.markdown("""
        <style>
        div[data-testid="column"] button {
            width: 100%;
            text-align: left !important;
            padding: 14px 20px !important;
            border-radius: 10px !important;
            font-size: 0.92rem !important;
            border: 1.5px solid #e8e2d5 !important;
            background: #faf8f3 !important;
            color: #1a1a2e !important;
            transition: all 0.15s !important;
            white-space: normal !important;
            height: auto !important;
            min-height: 56px !important;
            line-height: 1.4 !important;
        }
        div[data-testid="column"] button:hover {
            border-color: #c9a84c !important;
            background: #fffef8 !important;
        }
        .btn-selected button {
            border-color: #d4667a !important;
            background: #fde8ec !important;
            color: #1a1a2e !important;
            font-weight: 600 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        # Barre de progression
        pct = idx / total
        st.progress(pct)
        st.markdown(f"**Question {idx + 1} / {total}**")

        st.markdown("---")

        # Question
        st.markdown(f'<p class="question-text">{q["q"]}</p>', unsafe_allow_html=True)
        st.markdown("")

        # Boutons A / B / C / D
        lettres = ["A", "B", "C", "D"]
        for i, opt in enumerate(q["opts"]):
            is_selected = current_answer == i
            selected_class = "btn-selected" if is_selected else ""
            prefix = "✓ " if is_selected else ""

            col_btn = st.columns([1])[0]
            with col_btn:
                container = st.container()
                if is_selected:
                    container.markdown(f'<div class="btn-selected">', unsafe_allow_html=True)

                label = f"{prefix}{lettres[i]} — {opt}"
                if st.button(
                    label,
                    key=f"opt_{idx}_{i}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary",
                ):
                    st.session_state.answers[idx] = i
                    # Auto-avancement après 0.3s si ce n'est pas la dernière question
                    if idx < total - 1:
                        st.session_state.q_idx += 1
                    else:
                        with st.spinner("Analyse de ton profil en cours…"):
                            profile = compute_profile(st.session_state.answers, QUESTIONS)
                            top = compute_matching(profile, df_metiers)
                            st.session_state.profile = profile
                            st.session_state.top_metiers = top
                        st.session_state.etape = "profil"
                    st.rerun()

        st.markdown("---")

        # Navigation bas de page
        col_prev, col_center, col_next = st.columns([1, 2, 1])

        with col_prev:
            if idx > 0:
                if st.button("← Précédent", use_container_width=True, key="btn_prev"):
                    st.session_state.q_idx -= 1
                    st.rerun()

        with col_next:
            if current_answer is not None:
                label = "Voir mon profil ✦" if idx == total - 1 else "Suivant →"
                if st.button(label, type="primary", use_container_width=True, key="btn_next"):
                    if idx < total - 1:
                        st.session_state.q_idx += 1
                        st.rerun()
                    else:
                        with st.spinner("Analyse de ton profil en cours…"):
                            profile = compute_profile(st.session_state.answers, QUESTIONS)
                            top = compute_matching(profile, df_metiers)
                            st.session_state.profile = profile
                            st.session_state.top_metiers = top
                        st.session_state.etape = "profil"
                        st.rerun()
            else:
                st.button("Suivant →", disabled=True, use_container_width=True, key="btn_next_dis")

    # ── Étape PROFIL ──────────────────────────────────────────────────────────
    elif st.session_state.etape == "profil":
        profile = st.session_state.profile

        st.markdown("## 🎯 Ton profil de soft skills")

        SS_LABELS_ELEVE = {1: "À développer", 2: "Intermédiaire", 3: "Très développée"}
        SS_COLORS = {1: "#e8a87c", 2: "#c9a84c", 3: "#6b9e7e"}
        ss_vals = profile["ss"]

        # ── Graphique barres ──────────────────────────────────────────────────
        ss_data = []
        for i, label in enumerate(SS_LABELS):
            niveau = ss_vals[i]
            ss_data.append({
                "Soft skill": label,
                "Niveau": niveau * 33.3,
                "Texte": SS_LABELS_ELEVE[niveau],
                "Couleur": SS_COLORS[niveau],
            })

        df_ss = pd.DataFrame(ss_data)
        fig = go.Figure()
        for _, row in df_ss.iterrows():
            fig.add_trace(go.Bar(
                x=[row["Niveau"]], y=[row["Soft skill"]], orientation="h",
                text=row["Texte"], textposition="inside", insidetextanchor="middle",
                textfont=dict(size=12, color="white"),
                marker_color=row["Couleur"], showlegend=False,
                hovertemplate=f"<b>{row['Soft skill']}</b><br>{row['Texte']}<extra></extra>",
            ))
        fig.update_layout(
            height=380, margin=dict(l=0, r=80, t=10, b=0),
            xaxis=dict(range=[0, 105], visible=False),
            yaxis=dict(title="", autorange="reversed"),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", barmode="overlay",
        )
        st.plotly_chart(fig, use_container_width=True)

        col_leg1, col_leg2, col_leg3 = st.columns(3)
        col_leg1.markdown("🟠 **À développer**")
        col_leg2.markdown("🟡 **Intermédiaire**")
        col_leg3.markdown("🟢 **Très développée**")

        # ── Filtres ───────────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### Affiner les résultats *(optionnel)*")

        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            all_secteurs = sorted(set(
                s.strip() for secteurs in df_metiers["Secteur(s) activité"].dropna()
                for s in str(secteurs).split(";") if s.strip()
            ))
            sel_secteurs = st.multiselect("🏢 Secteur d'activité", all_secteurs, placeholder="Tous les secteurs")
        with col_f2:
            all_niveaux = sorted(df_metiers["Niveau"].dropna().unique().tolist())
            sel_niveaux = st.multiselect("📊 Niveau hiérarchique", all_niveaux, placeholder="Tous les niveaux")
        with col_f3:
            all_domaines_r = sorted(df_metiers["Domaine"].dropna().unique().tolist())
            sel_domaines_r = st.multiselect("📁 Domaine", all_domaines_r, placeholder="Tous les domaines")

        ACTIVITES_R = [
            ("Aider",      "🤝 Aider"),
            ("Communiquer","🗣️ Communiquer"),
            ("Concevoir",  "💡 Concevoir"),
            ("Conseiller", "🎯 Conseiller"),
            ("Diriger",    "📋 Piloter / Diriger"),
            ("Manipuler",  "🔧 Travailler de ses mains"),
            ("Preparer",   "📝 Préparer / Organiser"),
            ("Analyser",   "🔬 Analyser"),
            ("Saisir",     "⌨️ Traiter des données"),
        ]
        st.markdown("🎯 **Activités associées au métier**")
        cols_act_r = st.columns(9)
        sel_activites_r = []
        for i, (col, label) in enumerate(ACTIVITES_R):
            with cols_act_r[i]:
                if st.checkbox(label, key=f"ract_{col}"):
                    sel_activites_r.append(col)

        top = st.session_state.top_metiers
        if sel_secteurs:
            top = [r for r in top if any(s in r["secteur"].split(" ; ") for s in sel_secteurs)]
        if sel_niveaux:
            top = [r for r in top if r["niveau"] in sel_niveaux]
        if sel_domaines_r:
            top = [r for r in top if r["domaine"] in sel_domaines_r]
        if sel_activites_r:
            mask = df_metiers["Métier"].apply(lambda x: True)
            for act in sel_activites_r:
                if act in df_metiers.columns:
                    mask = mask & (df_metiers[act].astype(str).str.strip() == "V")
            metiers_valides = set(df_metiers[mask]["Métier"].str.lower().str.strip().tolist())
            top = [r for r in top if r["metier"].lower().strip() in metiers_valides]

        # ── ONGLETS ───────────────────────────────────────────────────────────
        st.markdown("---")
        tab_metiers, tab_analyse, tab_rapport, tab_scoring = st.tabs([
            "💼 Métiers recommandés",
            "🔍 Analyse détaillée de mes soft skills",
            "📄 Télécharger mon rapport",
            "ℹ️ Comment fonctionne le scoring ?",
        ])

        # ══ ONGLET 1 : MÉTIERS ════════════════════════════════════════════════
        with tab_metiers:
            st.markdown(f"### {len(top)} métiers compatibles avec ton profil")
            st.markdown("*Classés par compatibilité — basé sur tes 8 soft skills*")
            st.markdown("")

            if not top:
                st.warning("Aucun métier ne correspond aux filtres. Essaie d'élargir ta recherche.")
            else:
                # ── Pagination ────────────────────────────────────────────────
                PAGE_SIZE = 10
                if "metiers_page" not in st.session_state:
                    st.session_state.metiers_page = 0
                n_pages = max(1, (len(top) + PAGE_SIZE - 1) // PAGE_SIZE)
                page_num = min(st.session_state.metiers_page, n_pages - 1)
                start = page_num * PAGE_SIZE
                top_page = top[start: start + PAGE_SIZE]

                for r in top_page:
                    score = r["score"]
                    bg = "#e8f3ec" if score >= 80 else "#fdf3dc" if score >= 55 else "#f5f5f5"
                    fg = "#2a6a44" if score >= 80 else "#8a6a14" if score >= 55 else "#666"

                    with st.container():
                        col_score, col_info = st.columns([1, 7])
                        with col_score:
                            st.markdown(
                                f'<div style="text-align:center;padding:10px;background:{bg};border-radius:50%;'
                                f'width:58px;height:58px;display:flex;align-items:center;justify-content:center;'
                                f'font-weight:700;font-size:0.9rem;color:{fg}">{score}%</div>',
                                unsafe_allow_html=True,
                            )
                        with col_info:
                            st.markdown(f"**{r['metier']}**")
                            meta = []
                            if r["secteur"]: meta.append(f"🏢 {r['secteur'].split(' ; ')[0]}")
                            if r["niveau"]: meta.append(f"📊 {r['niveau']}")
                            if r["salaire"] and r["salaire"] not in ("nan", ""): meta.append(f"💶 {r['salaire']}")
                            st.markdown(" · ".join(meta) if meta else "")
                            if r["descriptif"] and r["descriptif"] not in ("nan", ""):
                                st.markdown(f"<small>{r['descriptif'][:200]}…</small>", unsafe_allow_html=True)
                        st.markdown("---")

                # ── Contrôles de pagination ───────────────────────────────────
                if n_pages > 1:
                    col_prev_p, col_page_info, col_next_p = st.columns([1, 2, 1])
                    with col_prev_p:
                        if page_num > 0:
                            if st.button("← Précédent", key="metiers_prev"):
                                st.session_state.metiers_page -= 1
                                st.rerun()
                    with col_page_info:
                        st.markdown(
                            f"<div style='text-align:center;color:#7a7a8c;font-size:0.9rem'>"
                            f"Page {page_num + 1} / {n_pages}</div>",
                            unsafe_allow_html=True,
                        )
                    with col_next_p:
                        if page_num < n_pages - 1:
                            if st.button("Suivant →", key="metiers_next"):
                                st.session_state.metiers_page += 1
                                st.rerun()

        # ══ ONGLET 2 : ANALYSE DÉTAILLÉE ══════════════════════════════════════
        with tab_analyse:
            from donnees_rapport import MAPPING_QUESTIONS, SS_RAPPORT_NOMS, SS_NIVEAUX

            st.markdown("### Analyse détaillée de tes soft skills")
            st.markdown("*Coche les cases pour confirmer ou infirmer chaque description — tes réponses seront intégrées dans le PDF.*")
            st.markdown("")

            # Initialiser les confirmations dans le session state
            if "confirmations" not in st.session_state:
                st.session_state.confirmations = {}

            lettres = ["A", "B", "C", "D"]

            # Construire le mapping
            ss_questions = {i: [] for i in range(8)}
            for q_idx, mapping in enumerate(MAPPING_QUESTIONS):
                sous_comp, ss_nom_map, textes = mapping
                ss_idx = next(
                    (i for i, n in SS_RAPPORT_NOMS.items()
                     if n.lower() in ss_nom_map.lower() or ss_nom_map.lower() in n.lower()), None
                )
                if ss_idx is not None:
                    ss_questions[ss_idx].append((q_idx, sous_comp, textes))

            for ss_idx, ss_nom in SS_RAPPORT_NOMS.items():
                niveau = ss_vals[ss_idx]
                couleur = SS_COLORS[niveau]
                niveau_txt = SS_LABELS_ELEVE[niveau]

                # En-tête avec badge
                col_titre, col_badge = st.columns([4, 1])
                with col_titre:
                    st.markdown(
                        f'<h4 style="color:{couleur};margin-bottom:4px">{ss_nom}</h4>',
                        unsafe_allow_html=True
                    )
                with col_badge:
                    st.markdown(
                        f'<div style="background:{couleur};color:white;padding:4px 10px;'
                        f'border-radius:12px;font-size:0.8rem;font-weight:600;text-align:center;'
                        f'margin-top:8px">{niveau_txt}</div>',
                        unsafe_allow_html=True
                    )

                qs = ss_questions.get(ss_idx, [])
                for row_idx, (q_idx, sous_comp, textes) in enumerate(qs):
                    ans_idx = st.session_state.answers[q_idx] if q_idx < len(st.session_state.answers) and st.session_state.answers[q_idx] is not None else 0
                    lettre = lettres[ans_idx]
                    texte = textes.get(lettre, "")

                    bg_row = "#faf8f3" if row_idx % 2 == 0 else "white"
                    c1, c2, c3, c4 = st.columns([3, 5, 1, 1])

                    with c1:
                        st.markdown(
                            f'<div style="background:{bg_row};padding:8px 10px;border-radius:6px;'
                            f'font-size:0.85rem;font-weight:600;min-height:48px;'
                            f'display:flex;align-items:center">{sous_comp}</div>',
                            unsafe_allow_html=True
                        )
                    with c2:
                        st.markdown(
                            f'<div style="background:{bg_row};padding:8px 10px;border-radius:6px;'
                            f'font-size:0.85rem;min-height:48px;display:flex;align-items:center">{texte}</div>',
                            unsafe_allow_html=True
                        )
                    key_oui = f"conf_oui_{ss_idx}_{q_idx}"
                    key_non = f"conf_non_{ss_idx}_{q_idx}"
                    with c3:
                        current = st.session_state.confirmations.get((ss_idx, q_idx), None)
                        if st.checkbox("✓ Oui", value=(current is True), key=key_oui):
                            st.session_state.confirmations[(ss_idx, q_idx)] = True
                            # Désactiver l'autre checkbox pour garantir l'exclusivité
                            if st.session_state.get(key_non):
                                st.session_state[key_non] = False
                        elif current is True:
                            st.session_state.confirmations[(ss_idx, q_idx)] = None
                    with c4:
                        current = st.session_state.confirmations.get((ss_idx, q_idx), None)
                        if st.checkbox("✗ Non", value=(current is False), key=key_non):
                            st.session_state.confirmations[(ss_idx, q_idx)] = False
                            # Désactiver l'autre checkbox pour garantir l'exclusivité
                            if st.session_state.get(key_oui):
                                st.session_state[key_oui] = False
                        elif current is False:
                            st.session_state.confirmations[(ss_idx, q_idx)] = None

                st.markdown("---")

        # ══ ONGLET 3 : TÉLÉCHARGEMENT ═════════════════════════════════════════
        with tab_rapport:
            st.markdown("### 📄 Ton rapport personnalisé")
            st.markdown(
                "Le rapport contient une **page de couverture**, un **diagramme radar**, "
                "le **top 15 des métiers**, et l'**analyse détaillée** avec tes confirmations cochées."
            )
            st.markdown("")

            prenom_dl = st.session_state.get("prenom", "") or "Anonyme"
            nom_dl = st.session_state.get("nom", "") or ""

            if not st.session_state.get("prenom"):
                col_p, col_n = st.columns(2)
                with col_p:
                    prenom_dl = st.text_input("Prénom", key="rapport_prenom", placeholder="Ex: Marie")
                with col_n:
                    nom_dl = st.text_input("Nom", key="rapport_nom", placeholder="Ex: Dupont")

            # ── Champ classe/formation pleine largeur — avant les colonnes ──────
            prenom_s = st.session_state.get("prenom") or prenom_dl
            nom_s    = st.session_state.get("nom") or nom_dl
            classe_s = st.session_state.get("classe", "")
            if not classe_s:
                classe_s = st.text_input(
                    "📚 Classe ou profession (optionnel)",
                    key="save_classe_tab",
                    placeholder="Ex : Terminale STMG, Étudiant BTS…",
                )
            st.markdown("")

            # CSS : hauteur fixe pour les blocs de titre des 3 colonnes
            st.markdown("""
            <style>
            .col-header {
                min-height: 52px;
                display: flex;
                flex-direction: column;
                justify-content: flex-start;
                margin-bottom: 10px;
            }
            .col-header .col-title {
                font-weight: 700;
                font-size: 0.95rem;
                margin-bottom: 2px;
            }
            .col-header .col-sub {
                font-size: 0.78rem;
                color: #7a7a8c;
            }
            </style>
            """, unsafe_allow_html=True)

            col_save, col_pdf, col_word = st.columns(3)

            with col_save:
                st.markdown("""<div class="col-header">
                    <div class="col-title">💾 Sauvegarder</div>
                    <div class="col-sub">Enregistre tes résultats</div>
                </div>""", unsafe_allow_html=True)
                if st.button("💾 Sauvegarder", type="secondary", use_container_width=True):
                    if prenom_s and nom_s:
                        google_ok, csv_ok = sauvegarder(
                            prenom=prenom_s, nom=nom_s, classe=classe_s,
                            mode=st.session_state.get("mode", "lycee"),
                            profile=profile, top_metiers=st.session_state.top_metiers,
                        )
                        if google_ok:
                            st.success(f"✅ {prenom_s} {nom_s} sauvegardé dans Google Sheets !")
                        elif csv_ok:
                            st.warning("⚠️ Sauvegardé en local uniquement (Google Sheets non disponible).")
                        else:
                            st.error("❌ Erreur lors de la sauvegarde.")
                    else:
                        st.warning("Renseigne ton prénom et ton nom.")

            with col_pdf:
                st.markdown("""<div class="col-header">
                    <div class="col-title">📥 Rapport PDF <em style="font-weight:400">(recommandé)</em></div>
                    <div class="col-sub">S'ouvre partout, mobile inclus</div>
                </div>""", unsafe_allow_html=True)
                try:
                    pdf_bytes = generer_pdf(
                        prenom=prenom_dl, nom=nom_dl,
                        answers=st.session_state.answers,
                        profile=profile,
                        confirmations=st.session_state.get("confirmations", {}),
                        top_metiers=st.session_state.top_metiers,
                        classe=classe_s or st.session_state.get("classe", ""),
                    )
                    st.download_button(
                        label="📥 Télécharger PDF",
                        data=pdf_bytes,
                        file_name=f"OrientAI_{prenom_dl}_{nom_dl}.pdf".replace(" ", "_"),
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"Erreur PDF : {e}")

            with col_word:
                st.markdown("""<div class="col-header">
                    <div class="col-title">📝 Rapport Word <em style="font-weight:400">(conseiller)</em></div>
                    <div class="col-sub">Annoter, personnaliser</div>
                </div>""", unsafe_allow_html=True)
                try:
                    rapport_bytes = generer_rapport_v2(
                        prenom=prenom_dl, nom=nom_dl,
                        answers=st.session_state.answers,
                        profile=profile,
                        top_metiers=st.session_state.top_metiers,
                    )
                    st.download_button(
                        label="📝 Télécharger Word",
                        data=rapport_bytes,
                        file_name=f"OrientAI_{prenom_dl}_{nom_dl}.docx".replace(" ", "_"),
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        type="secondary",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"Erreur Word : {e}")


        # ══ ONGLET 4 : SCORING ════════════════════════════════════════════════
        with tab_scoring:
            st.markdown("### ℹ️ Comment sont sélectionnés tes métiers ?")
            st.markdown("")

            st.markdown("#### 🎯 Le principe du matching")
            st.markdown("""
Chaque métier de la base OrientAI est associé à **8 soft skills** avec un niveau requis.
Après ton questionnaire, ton profil personnel est défini sur ces **mêmes 8 soft skills**.
L'algorithme compare ton profil à celui de chaque métier et calcule un **score de compatibilité** entre 0 et 100%.
            """)

            st.markdown("#### 💡 Les 8 soft skills évaluées")
            ss_data = {
                "Soft skill": ["🗣️ Communication","🔍 Esprit critique","⚖️ Éthique",
                    "❤️ Intelligence émotionnelle","🤝 Intelligence sociale",
                    "📋 Management de projet","👥 Management d'équipe","🗂️ Organisation"],
                "Ce que ça mesure": [
                    "Capacité à s'exprimer clairement, convaincre, négocier",
                    "Esprit analytique, curiosité, remise en question",
                    "Sens des responsabilités, intégrité, valeurs",
                    "Connaissance de soi, gestion des émotions, empathie",
                    "Travail en équipe, adaptabilité aux autres, sociabilité",
                    "Planification, prise de décision, gestion des risques",
                    "Leadership, résolution de conflits, coaching",
                    "Rigueur, respect des délais, gestion du temps",
                ],
            }
            st.dataframe(pd.DataFrame(ss_data), use_container_width=True, hide_index=True)

            st.markdown("#### 📊 Les 3 niveaux de soft skills")
            col_n1, col_n2, col_n3 = st.columns(3)
            with col_n1:
                st.markdown("""<div style="background:#f5e6d3;border-radius:12px;padding:16px;text-align:center">
<div style="font-size:2rem">🟠</div><div style="font-weight:700;color:#c0682a;margin:8px 0">À développer</div>
<div style="font-size:0.85rem;color:#555">Pas encore un point fort. Certains métiers ne la requièrent pas.</div>
</div>""", unsafe_allow_html=True)
            with col_n2:
                st.markdown("""<div style="background:#fdf3dc;border-radius:12px;padding:16px;text-align:center">
<div style="font-size:2rem">🟡</div><div style="font-weight:700;color:#8a6a14;margin:8px 0">Intermédiaire</div>
<div style="font-size:0.85rem;color:#555">Présente et fonctionnelle dans la plupart des situations.</div>
</div>""", unsafe_allow_html=True)
            with col_n3:
                st.markdown("""<div style="background:#e8f3ec;border-radius:12px;padding:16px;text-align:center">
<div style="font-size:2rem">🟢</div><div style="font-weight:700;color:#2a6a44;margin:8px 0">Très développée</div>
<div style="font-size:0.85rem;color:#555">Vrai point fort, utilisé naturellement même sous pression.</div>
</div>""", unsafe_allow_html=True)

            st.markdown("")
            st.markdown("#### 🧮 Comment le score est calculé")
            score_data = {
                "Situation": [
                    "✅ Ton niveau = niveau requis",
                    "🔶 Écart d'un niveau",
                    "❌ Écart de deux niveaux",
                ],
                "Points": ["3 pts", "1,5 pts", "0 pt"],
            }
            st.dataframe(pd.DataFrame(score_data), use_container_width=True, hide_index=True)
            st.markdown("**Score (%) = (Total des points / 24) × 100**")

            st.markdown("")
            st.markdown("#### 📖 Comment lire son score")
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.markdown("""<div style="background:#e8f3ec;border-radius:12px;padding:14px;text-align:center">
<div style="font-size:1.5rem;font-weight:700;color:#2a6a44">80% et +</div>
<div style="color:#2a6a44">🟢 Très compatible</div>
<div style="font-size:0.8rem;color:#555">Profil très proche des exigences</div></div>""", unsafe_allow_html=True)
            with col_s2:
                st.markdown("""<div style="background:#fdf3dc;border-radius:12px;padding:14px;text-align:center">
<div style="font-size:1.5rem;font-weight:700;color:#8a6a14">55–79%</div>
<div style="color:#8a6a14">🟡 Compatible</div>
<div style="font-size:0.8rem;color:#555">Quelques soft skills à renforcer</div></div>""", unsafe_allow_html=True)
            with col_s3:
                st.markdown("""<div style="background:#f5f5f5;border-radius:12px;padding:14px;text-align:center">
<div style="font-size:1.5rem;font-weight:700;color:#666">Moins de 55%</div>
<div style="color:#666">⚪ À explorer</div>
<div style="font-size:0.8rem;color:#555">Ce métier demande un profil différent</div></div>""", unsafe_allow_html=True)

            st.markdown("")
            st.markdown("#### ⚠️ Ce que le score ne mesure pas")
            st.info("""Le score est un **indicateur d'orientation**, pas une garantie. Il ne prend pas en compte :
- Ton intérêt personnel pour le métier
- Tes compétences techniques (hard skills)
- Le marché de l'emploi et les contraintes géographiques
- L'évolution possible de tes soft skills avec l'expérience

💡 **Utilise ce score comme point de départ pour discuter avec un conseiller d'orientation.**
            """)

        # ── Enquête de satisfaction ────────────────────────────────────────────
        st.markdown("")
        with st.expander("📝 Donne ton avis sur tes résultats (optionnel)"):
            if st.session_state.get("enquete_envoyee"):
                st.success("✅ Merci pour ton avis ! Tes réponses ont bien été enregistrées.")
            else:
                st.markdown("*Quelques questions rapides pour améliorer l'outil — complètement facultatif.*")
                st.markdown("")

                enq_pertinence = st.radio(
                    "Est-ce que les métiers proposés correspondent à ce que tu imagines pour ton avenir ?",
                    ["😕 Pas du tout", "😐 Un peu", "🙂 Plutôt oui", "😀 Tout à fait"],
                    index=None,
                    key="enq_pertinence",
                    horizontal=True,
                )
                enq_surprise = st.radio(
                    "Est-ce qu'un métier proposé t'a surpris positivement ?",
                    ["Oui", "Non"],
                    index=None,
                    key="enq_surprise",
                    horizontal=True,
                )
                enq_profil = st.radio(
                    "Est-ce que la description de tes soft skills te ressemble ?",
                    ["😕 Pas du tout", "😐 Un peu", "🙂 Plutôt oui", "😀 Tout à fait"],
                    index=None,
                    key="enq_profil",
                    horizontal=True,
                )
                enq_utilite = st.radio(
                    "Est-ce que ce test t'a aidé à mieux te connaître ?",
                    ["Oui", "Non", "Je ne sais pas"],
                    index=None,
                    key="enq_utilite",
                    horizontal=True,
                )

                st.markdown("")
                enq_suggestions = st.text_area(
                    "As-tu des suggestions afin d'améliorer le service ?",
                    placeholder="Écris ici tes idées, remarques ou suggestions… (optionnel)",
                    key="enq_suggestions",
                    height=100,
                )

                if st.button("Envoyer mon avis", type="primary"):
                    sauvegarder_enquete(
                        prenom=st.session_state.get("prenom", ""),
                        nom=st.session_state.get("nom", ""),
                        classe=st.session_state.get("classe", ""),
                        mode=st.session_state.get("mode", "lycee"),
                        pertinence=enq_pertinence or "",
                        surprise=enq_surprise or "",
                        profil=enq_profil or "",
                        utilite=enq_utilite or "",
                        suggestions=enq_suggestions or "",
                    )
                    st.session_state.enquete_envoyee = True
                    st.rerun()

        # ── Recommencer ───────────────────────────────────────────────────────
        st.markdown("")
        if st.button("↺ Recommencer le questionnaire", use_container_width=True):
            st.session_state.etape = "accueil"
            st.session_state.answers = [None] * len(QUESTIONS)
            st.session_state.q_idx = 0
            st.session_state.profile = None
            st.session_state.top_metiers = []
            st.session_state.enquete_envoyee = False
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# ESPACE CONSEILLER — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.espace == "conseiller" and st.session_state.conseiller_auth and page == "📊 Dashboard":
    st.markdown("## 📊 Dashboard conseiller")

    tab_resultats, tab_enquete = st.tabs(["📊 Résultats", "📝 Enquête de satisfaction"])

    # ══ ONGLET 1 : RÉSULTATS ══════════════════════════════════════════════════
    with tab_resultats:
        df_res = charger_resultats()

        if df_res.empty:
            st.info("Aucun résultat sauvegardé pour l'instant. Les résultats apparaîtront ici après que des accompagnés aient complété le questionnaire.")
        else:
            # ── Filtre global (espace + recherche identité) ───────────────────
            fcol1, fcol2, fcol3 = st.columns([1, 1, 2])
            with fcol1:
                filtre_espace = st.selectbox(
                    "Espace",
                    ["Tous", "Élève", "Adulte / Pro"],
                    key="dash_filtre_espace",
                )
            with fcol3:
                recherche_id = st.text_input(
                    "🔍 Rechercher par prénom / nom",
                    placeholder="Ex : Marie Dupont",
                    key="dash_recherche_id",
                )

            df_global = df_res.copy()
            if filtre_espace == "Élève":
                df_global = df_global[df_global["mode"].astype(str).str.lower().isin(["lycee", "eleve", "élève"])]
            elif filtre_espace == "Adulte / Pro":
                df_global = df_global[df_global["mode"].astype(str).str.lower().isin(["adulte", "pro"])]
            if recherche_id.strip():
                mots = recherche_id.strip().lower().split()
                for mot in mots:
                    mask = (
                        df_global["prenom"].astype(str).str.lower().str.contains(mot, na=False)
                        | df_global["nom"].astype(str).str.lower().str.contains(mot, na=False)
                    )
                    df_global = df_global[mask]

            st.markdown("---")

            # Métriques globales
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Accompagnés", len(df_global))
            col2.metric("MBTI le plus fréquent", df_global["mbti"].mode()[0] if not df_global.empty and not df_global["mbti"].isna().all() else "—")
            col3.metric("Classes", df_global["classe"].nunique() if not df_global.empty else 0)
            col4.metric("Dernier passage", df_global["date"].max() if not df_global.empty and not df_global["date"].isna().all() else "—")

            st.markdown("---")

            # Soft skills moyennes — pleine largeur
            st.markdown("### Soft skills moyennes des accompagnés")
            ss_cols_map = {
                "Communication": "ss_communication",
                "Esprit critique": "ss_esprit_critique",
                "Éthique": "ss_ethique",
                "Intel. émotionnelle": "ss_intel_emotionnelle",
                "Intel. sociale": "ss_intel_sociale",
                "Mgmt de projet": "ss_mgmt_projet",
                "Mgmt d'équipe": "ss_mgmt_equipe",
                "Organisation": "ss_organisation",
            }
            ss_means = []
            for label, col in ss_cols_map.items():
                if col in df_global.columns:
                    mean_val = pd.to_numeric(df_global[col], errors="coerce").mean()
                    ss_means.append({"Soft skill": label, "Moyenne": round(mean_val, 2) if not pd.isna(mean_val) else 0})

            if ss_means and not df_global.empty:
                df_ss_mean = pd.DataFrame(ss_means)
                fig_ss = px.bar(
                    df_ss_mean, x="Moyenne", y="Soft skill", orientation="h",
                    color="Moyenne",
                    color_continuous_scale=["#e8e2d5", "#6b9e7e", "#c9a84c"],
                    range_color=[1, 3],
                    height=320,
                )
                fig_ss.update_layout(
                    showlegend=False, coloraxis_showscale=False,
                    margin=dict(l=0, r=60, t=10, b=0),
                    xaxis=dict(range=[1, 3], title=""),
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig_ss, use_container_width=True)
            else:
                st.info("Aucune donnée pour ce filtre.")

            st.markdown("---")

            # Métiers populaires
            st.markdown("### Top métiers recommandés")
            metiers_list = []
            for col in ["top1_metier", "top2_metier", "top3_metier"]:
                if col in df_global.columns:
                    metiers_list.extend(df_global[col].dropna().tolist())
            if metiers_list:
                metiers_counts = pd.Series(metiers_list).value_counts().head(10).reset_index()
                metiers_counts.columns = ["Métier", "Occurrences"]
                fig_met = px.bar(
                    metiers_counts, x="Occurrences", y="Métier", orientation="h",
                    color="Occurrences",
                    color_continuous_scale=["#f0e2b0", "#d4667a"],
                    height=350,
                )
                fig_met.update_layout(
                    showlegend=False, coloraxis_showscale=False,
                    margin=dict(l=0, r=0, t=10, b=0),
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig_met, use_container_width=True)

            st.markdown("---")

            # ── Liste cliquable des accompagnés ───────────────────────────────
            st.markdown("### Détail par accompagné")

            filtre_classe = st.selectbox(
                "Filtrer par classe",
                ["Toutes"] + sorted(df_global["classe"].dropna().unique().tolist()),
            )
            df_affiche = df_global if filtre_classe == "Toutes" else df_global[df_global["classe"] == filtre_classe]
            df_affiche = df_affiche.reset_index(drop=True)

            if "conseiller_eleve_idx" not in st.session_state:
                st.session_state.conseiller_eleve_idx = None

            # En-tête de la liste
            hcols = st.columns([3, 2, 1, 3, 1])
            for h, t in zip(hcols, ["**Élève**", "**Classe**", "**MBTI**", "**Top métier**", ""]):
                h.markdown(t)
            st.markdown("<hr style='margin:4px 0 8px'>", unsafe_allow_html=True)

            for i, row in df_affiche.iterrows():
                nom_complet = f"{row.get('prenom', '')} {row.get('nom', '')}".strip() or "Anonyme"
                c1, c2, c3, c4, c5 = st.columns([3, 2, 1, 3, 1])
                date_str = str(row.get("date", ""))[:10]
                c1.markdown(f"**{nom_complet}**  \n<small style='color:#7a7a8c'>{date_str}</small>",
                            unsafe_allow_html=True)
                c2.markdown(str(row.get("classe", "—")))
                mbti_val = str(row.get("mbti", "—"))
                c3.markdown(f"`{mbti_val}`")
                top1 = str(row.get("top1_metier", "—"))
                top1_score = row.get("top1_score", "")
                c4.markdown(f"{top1}  \n<small style='color:#7a7a8c'>{top1_score}%</small>" if top1_score else top1,
                            unsafe_allow_html=True)
                with c5:
                    is_selected = st.session_state.conseiller_eleve_idx == i
                    btn_label = "✓ Ouvert" if is_selected else "Voir →"
                    btn_type = "primary" if is_selected else "secondary"
                    if st.button(btn_label, key=f"voir_{i}", type=btn_type, use_container_width=True):
                        st.session_state.conseiller_eleve_idx = None if is_selected else i
                        st.rerun()

            # ── Fiche individuelle ─────────────────────────────────────────────
            if st.session_state.conseiller_eleve_idx is not None:
                idx = st.session_state.conseiller_eleve_idx
                if idx < len(df_affiche):
                    eleve = df_affiche.iloc[idx]
                    nom_complet = f"{eleve.get('prenom', '')} {eleve.get('nom', '')}".strip() or "Anonyme"

                    st.markdown("---")
                    st.markdown(f"## 👤 Fiche de {nom_complet}")

                    col_info, col_mbti = st.columns([3, 1])
                    with col_info:
                        meta = []
                        if eleve.get("classe"): meta.append(f"🏫 **Classe :** {eleve['classe']}")
                        if eleve.get("mode"):   meta.append(f"📋 **Mode :** {eleve['mode']}")
                        if eleve.get("date"):   meta.append(f"📅 **Date :** {str(eleve['date'])[:16]}")
                        st.markdown("  \n".join(meta))
                    with col_mbti:
                        mbti_v = str(eleve.get("mbti", ""))
                        mbti_d = str(eleve.get("mbti_desc", ""))
                        st.markdown(
                            f'<div style="text-align:center;background:#fde8ec;border-radius:12px;'
                            f'padding:16px 8px">'
                            f'<div style="font-size:2rem;font-weight:700;color:#d4667a">{mbti_v}</div>'
                            f'<div style="font-size:0.75rem;color:#555;margin-top:4px">{mbti_d}</div>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

                    st.markdown("")

                    # ── Graphique soft skills ──────────────────────────────────
                    ss_fiche_map = [
                        ("Communication",       "ss_communication"),
                        ("Esprit critique",     "ss_esprit_critique"),
                        ("Éthique",             "ss_ethique"),
                        ("Intel. émotionnelle", "ss_intel_emotionnelle"),
                        ("Intel. sociale",      "ss_intel_sociale"),
                        ("Mgmt de projet",      "ss_mgmt_projet"),
                        ("Mgmt d'équipe",       "ss_mgmt_equipe"),
                        ("Organisation",        "ss_organisation"),
                    ]
                    SS_LABELS_F = {1: "À développer", 2: "Intermédiaire", 3: "Très développée"}
                    SS_COLORS_F = {1: "#e8a87c", 2: "#c9a84c", 3: "#6b9e7e"}

                    fiche_bars = go.Figure()
                    for label, col_key in ss_fiche_map:
                        niveau = int(pd.to_numeric(eleve.get(col_key, 2), errors="coerce") or 2)
                        niveau = max(1, min(3, niveau))
                        fiche_bars.add_trace(go.Bar(
                            x=[niveau * 33.3], y=[label], orientation="h",
                            text=SS_LABELS_F[niveau], textposition="inside", insidetextanchor="middle",
                            textfont=dict(size=11, color="white"),
                            marker_color=SS_COLORS_F[niveau], showlegend=False,
                            hovertemplate=f"<b>{label}</b><br>{SS_LABELS_F[niveau]}<extra></extra>",
                        ))
                    fiche_bars.update_layout(
                        height=320, margin=dict(l=0, r=60, t=10, b=0),
                        xaxis=dict(range=[0, 105], visible=False),
                        yaxis=dict(title="", autorange="reversed"),
                        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                        barmode="overlay",
                    )
                    st.plotly_chart(fiche_bars, use_container_width=True)

                    # ── Top 3 métiers ──────────────────────────────────────────
                    st.markdown("#### 💼 Top 3 métiers recommandés")
                    for rank in range(1, 4):
                        m_nom   = str(eleve.get(f"top{rank}_metier", "")).strip()
                        m_score = eleve.get(f"top{rank}_score", "")
                        m_sect  = str(eleve.get(f"top{rank}_secteur", "")).strip()
                        if not m_nom or m_nom in ("nan", ""):
                            continue
                        try:
                            score_int = int(float(m_score))
                        except (ValueError, TypeError):
                            score_int = 0
                        bg = "#e8f3ec" if score_int >= 80 else "#fdf3dc" if score_int >= 55 else "#f5f5f5"
                        fg = "#2a6a44" if score_int >= 80 else "#8a6a14" if score_int >= 55 else "#666"
                        c_sc, c_inf = st.columns([1, 8])
                        with c_sc:
                            st.markdown(
                                f'<div style="text-align:center;padding:10px;background:{bg};border-radius:50%;'
                                f'width:54px;height:54px;display:flex;align-items:center;justify-content:center;'
                                f'font-weight:700;font-size:0.85rem;color:{fg}">{score_int}%</div>',
                                unsafe_allow_html=True,
                            )
                        with c_inf:
                            st.markdown(f"**{m_nom}**")
                            if m_sect and m_sect not in ("nan", ""):
                                st.markdown(f"<small>🏢 {m_sect.split(';')[0].strip()}</small>",
                                            unsafe_allow_html=True)
                        st.markdown("")

                    st.markdown("---")

            # Export CSV — respecte les filtres actifs
            csv_data = df_global.to_csv(index=False, encoding="utf-8").encode("utf-8")
            csv_label = f"⬇️ Télécharger les résultats filtrés ({len(df_global)} accompagnés)"
            st.download_button(
                csv_label,
                data=csv_data,
                file_name="orientai_resultats.csv",
                mime="text/csv",
            )

            st.markdown("---")
            with st.expander("⚠️ Zone dangereuse"):
                st.warning("Cette action supprime définitivement tous les résultats sauvegardés.")
                if st.button("🗑️ Effacer tous les résultats", type="secondary"):
                    effacer_resultats()
                    st.success("Résultats effacés.")
                    st.rerun()

    # ══ ONGLET 2 : ENQUÊTE DE SATISFACTION ════════════════════════════════════
    with tab_enquete:
        st.markdown("### 📊 Statistiques de l'enquête de satisfaction")
        df_enq = charger_enquete()

        if df_enq.empty:
            st.info("Aucune réponse à l'enquête pour l'instant. Les réponses apparaîtront ici après que des élèves aient soumis leur avis.")
        else:
            n_total = len(df_enq)
            st.markdown(f"**{n_total} réponse(s) reçue(s)**")
            st.markdown("---")

            # Q1 — Pertinence des métiers
            st.markdown("#### Q1 — Les métiers proposés correspondent à ce que tu imagines pour ton avenir ?")
            if "enquete_pertinence" in df_enq.columns:
                ordre_q1 = ["😕 Pas du tout", "😐 Un peu", "🙂 Plutôt oui", "😀 Tout à fait"]
                counts_q1 = df_enq["enquete_pertinence"].value_counts().reindex(ordre_q1, fill_value=0).reset_index()
                counts_q1.columns = ["Réponse", "Nombre"]
                counts_q1["Pourcentage"] = (counts_q1["Nombre"] / n_total * 100).round(1)
                fig_q1 = px.bar(
                    counts_q1, x="Réponse", y="Pourcentage",
                    text=counts_q1["Pourcentage"].astype(str) + "%",
                    color="Réponse",
                    color_discrete_map={
                        "😕 Pas du tout": "#e8a87c", "😐 Un peu": "#c9a84c",
                        "🙂 Plutôt oui": "#6b9e7e", "😀 Tout à fait": "#2a6a44",
                    },
                    height=280,
                    category_orders={"Réponse": ordre_q1},
                )
                fig_q1.update_layout(
                    showlegend=False, yaxis_title="% des réponses",
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=20, b=20),
                )
                fig_q1.update_traces(textposition="outside")
                st.plotly_chart(fig_q1, use_container_width=True)

            st.markdown("---")

            # Q2 — Surprise positive
            st.markdown("#### Q2 — Un métier proposé t'a surpris positivement ?")
            if "enquete_surprise" in df_enq.columns:
                counts_q2 = df_enq["enquete_surprise"].value_counts().reindex(["Oui", "Non"], fill_value=0).reset_index()
                counts_q2.columns = ["Réponse", "Nombre"]
                counts_q2["Pourcentage"] = (counts_q2["Nombre"] / n_total * 100).round(1)
                col_q2a, col_q2b = st.columns([2, 1])
                with col_q2a:
                    fig_q2 = px.bar(
                        counts_q2, x="Réponse", y="Pourcentage",
                        text=counts_q2["Pourcentage"].astype(str) + "%",
                        color="Réponse",
                        color_discrete_map={"Oui": "#6b9e7e", "Non": "#e8a87c"},
                        height=250,
                    )
                    fig_q2.update_layout(
                        showlegend=False, yaxis_title="% des réponses",
                        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                        margin=dict(t=20, b=20),
                    )
                    fig_q2.update_traces(textposition="outside")
                    st.plotly_chart(fig_q2, use_container_width=True)
                with col_q2b:
                    for _, r in counts_q2.iterrows():
                        st.metric(r["Réponse"], f"{r['Pourcentage']}%", f"{int(r['Nombre'])} élève(s)")

            st.markdown("---")

            # Q3 — Description du profil
            st.markdown("#### Q3 — La description de tes soft skills te ressemble ?")
            if "enquete_profil" in df_enq.columns:
                ordre_q3 = ["😕 Pas du tout", "😐 Un peu", "🙂 Plutôt oui", "😀 Tout à fait"]
                counts_q3 = df_enq["enquete_profil"].value_counts().reindex(ordre_q3, fill_value=0).reset_index()
                counts_q3.columns = ["Réponse", "Nombre"]
                counts_q3["Pourcentage"] = (counts_q3["Nombre"] / n_total * 100).round(1)
                fig_q3 = px.bar(
                    counts_q3, x="Réponse", y="Pourcentage",
                    text=counts_q3["Pourcentage"].astype(str) + "%",
                    color="Réponse",
                    color_discrete_map={
                        "😕 Pas du tout": "#e8a87c", "😐 Un peu": "#c9a84c",
                        "🙂 Plutôt oui": "#6b9e7e", "😀 Tout à fait": "#2a6a44",
                    },
                    height=280,
                    category_orders={"Réponse": ordre_q3},
                )
                fig_q3.update_layout(
                    showlegend=False, yaxis_title="% des réponses",
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=20, b=20),
                )
                fig_q3.update_traces(textposition="outside")
                st.plotly_chart(fig_q3, use_container_width=True)

            st.markdown("---")

            # Q4 — Utilité du test
            st.markdown("#### Q4 — Ce test t'a aidé à mieux te connaître ?")
            if "enquete_utilite" in df_enq.columns:
                counts_q4 = df_enq["enquete_utilite"].value_counts().reindex(
                    ["Oui", "Non", "Je ne sais pas"], fill_value=0
                ).reset_index()
                counts_q4.columns = ["Réponse", "Nombre"]
                counts_q4["Pourcentage"] = (counts_q4["Nombre"] / n_total * 100).round(1)
                col_q4a, col_q4b = st.columns([2, 1])
                with col_q4a:
                    fig_q4 = px.bar(
                        counts_q4, x="Réponse", y="Pourcentage",
                        text=counts_q4["Pourcentage"].astype(str) + "%",
                        color="Réponse",
                        color_discrete_map={
                            "Oui": "#6b9e7e", "Non": "#e8a87c", "Je ne sais pas": "#c9a84c",
                        },
                        height=250,
                    )
                    fig_q4.update_layout(
                        showlegend=False, yaxis_title="% des réponses",
                        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                        margin=dict(t=20, b=20),
                    )
                    fig_q4.update_traces(textposition="outside")
                    st.plotly_chart(fig_q4, use_container_width=True)
                with col_q4b:
                    for _, r in counts_q4.iterrows():
                        st.metric(r["Réponse"], f"{r['Pourcentage']}%", f"{int(r['Nombre'])} élève(s)")

            # Suggestions libres
            if "enquete_suggestions" in df_enq.columns:
                suggestions_non_vides = df_enq["enquete_suggestions"].dropna()
                suggestions_non_vides = suggestions_non_vides[suggestions_non_vides.astype(str).str.strip() != ""]
                if not suggestions_non_vides.empty:
                    st.markdown("---")
                    st.markdown(f"#### Q5 — Suggestions d'amélioration ({len(suggestions_non_vides)} réponse(s))")
                    for i, (idx_row, row_enq) in enumerate(df_enq[df_enq["enquete_suggestions"].astype(str).str.strip() != ""].iterrows(), 1):
                        auteur = f"{row_enq.get('prenom', '')} {row_enq.get('nom', '')}".strip() or "Anonyme"
                        date_s = str(row_enq.get("date", ""))[:10]
                        st.markdown(
                            f'<div style="background:#faf8f3;border-left:3px solid #c9a84c;'
                            f'padding:10px 14px;border-radius:0 8px 8px 0;margin-bottom:8px">'
                            f'<div style="font-size:0.8rem;color:#7a7a8c;margin-bottom:4px">'
                            f'{auteur} · {date_s}</div>'
                            f'<div style="font-size:0.92rem;color:#1a1a2e">{row_enq["enquete_suggestions"]}</div>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

            st.markdown("---")
            csv_enq = df_enq.to_csv(index=False, encoding="utf-8").encode("utf-8")
            st.download_button(
                "⬇️ Télécharger les réponses enquête",
                data=csv_enq,
                file_name="orientai_enquete.csv",
                mime="text/csv",
            )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE EXPLORATEUR DE MÉTIERS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.espace in ("eleve", "adulte") and page == "🔎 Explorer les métiers":

    st.markdown("## 🔎 Explorer les métiers")
    st.markdown("*Recherche et filtre librement parmi les 1 163 métiers de la base OrientAI*")
    st.markdown("")

    try:
        df_xl = load_excel_metiers()
    except FileNotFoundError:
        st.error("⚠️ Fichier data/Metiers_OrientAI_v5.2.xlsx introuvable. Place-le dans le dossier data/.")
        st.stop()

    # ── Filtres ───────────────────────────────────────────────────────────────
    with st.expander("🎛️ Filtres", expanded=True):
        col_f1, col_f2, col_f3 = st.columns(3)

        with col_f1:
            # Recherche texte libre
            recherche = st.text_input("🔍 Recherche par mot-clé", placeholder="Ex: infirmier, data, chef...")

        with col_f2:
            # Filtre secteur
            all_secteurs_xl = sorted(set(
                s.strip()
                for val in df_xl["Secteur(s) activité"].dropna()
                for s in str(val).split(";")
                if s.strip()
            ))
            sel_secteur = st.selectbox("🏢 Secteur", ["Tous"] + all_secteurs_xl)

        with col_f3:
            # Filtre niveau
            all_niveaux_xl = ["Tous"] + sorted(df_xl["Niveau"].dropna().unique().tolist())
            sel_niveau = st.selectbox("📊 Niveau hiérarchique", all_niveaux_xl)

        col_f4, col_f5, col_f6 = st.columns(3)

        with col_f4:
            # Filtre soft skill prioritaire — noms exacts des colonnes Excel (source : SS_COLS)
            ss_choices = ["Peu importe"] + SS_COLS
            sel_ss = st.selectbox("💡 Soft skill prioritaire", ss_choices)

        with col_f5:
            # Filtre niveau soft skill
            if sel_ss != "Peu importe":
                sel_ss_niveau = st.selectbox(
                    "Niveau requis",
                    ["Peu importe", "Peu nécessaire", "Nécessaire", "Absolument nécessaire"]
                )
            else:
                sel_ss_niveau = "Peu importe"
                st.selectbox("Niveau requis", ["Peu importe"], disabled=True)

        with col_f6:
            # Filtre domaine
            all_domaines = ["Tous"] + sorted(df_xl["Domaine"].dropna().unique().tolist())
            sel_domaine = st.selectbox("📁 Domaine", all_domaines)

        ACTIVITES = [
            ("Aider",      "🤝 Aider"),
            ("Communiquer","🗣️ Communiquer"),
            ("Concevoir",  "💡 Concevoir"),
            ("Conseiller", "🎯 Conseiller"),
            ("Diriger",    "📋 Piloter / Diriger"),
            ("Manipuler",  "🔧 Travailler de ses mains"),
            ("Preparer",   "📝 Préparer / Organiser"),
            ("Analyser",   "🔬 Analyser"),
            ("Saisir",     "⌨️ Traiter des données"),
        ]
        st.markdown("🎯 **Activités associées au métier**")
        cols_act = st.columns(9)
        sel_activites = []
        for i, (col, label) in enumerate(ACTIVITES):
            with cols_act[i]:
                if st.checkbox(label, key=f"act_{col}"):
                    sel_activites.append(col)

    # ── Application des filtres ───────────────────────────────────────────────
    df_filtre = df_xl.copy()

    if recherche:
        mask = (
            df_filtre["Métier"].astype(str).str.contains(recherche, case=False, na=False) |
            df_filtre["Descriptif"].astype(str).str.contains(recherche, case=False, na=False) |
            df_filtre["Domaine"].astype(str).str.contains(recherche, case=False, na=False)
        )
        df_filtre = df_filtre[mask]

    if sel_secteur != "Tous":
        df_filtre = df_filtre[
            df_filtre["Secteur(s) activité"].astype(str).str.contains(sel_secteur, case=False, na=False)
        ]

    if sel_niveau != "Tous":
        df_filtre = df_filtre[df_filtre["Niveau"].astype(str) == sel_niveau]

    if sel_domaine != "Tous":
        df_filtre = df_filtre[df_filtre["Domaine"].astype(str) == sel_domaine]

    if sel_ss != "Peu importe" and sel_ss_niveau != "Peu importe":
        df_filtre = df_filtre[df_filtre[sel_ss].astype(str) == sel_ss_niveau]

    if sel_activites:
        for activite in sel_activites:
            if activite in df_filtre.columns:
                df_filtre = df_filtre[df_filtre[activite].astype(str).str.strip() == "V"]

    # ── Résultats ─────────────────────────────────────────────────────────────
    st.markdown(f"### {len(df_filtre)} métier(s) trouvé(s)")
    st.markdown("")

    if df_filtre.empty:
        st.warning("Aucun métier ne correspond à ces critères. Essaie d'élargir ta recherche.")
    else:
        # Tri
        col_tri, col_asc = st.columns([3, 1])
        with col_tri:
            tri = st.selectbox("Trier par", ["Métier (A→Z)", "Salaire", "Niveau"])
        with col_asc:
            asc = st.checkbox("Croissant", value=True)

        if tri == "Métier (A→Z)":
            df_filtre = df_filtre.sort_values("Métier", ascending=asc)
        elif tri == "Salaire":
            df_filtre = df_filtre.sort_values("Salaire", ascending=asc, na_position='last')
        elif tri == "Niveau":
            ordre_niveau = {
                "Opérationnel": 1, "Manager - Responsable - Chef d'équipe": 2,
                "Directeur": 3, "Entrepreneur - Profession libérale": 4, "Utilisateur": 5
            }
            df_filtre["_ordre"] = df_filtre["Niveau"].map(ordre_niveau).fillna(99)
            df_filtre = df_filtre.sort_values("_ordre", ascending=asc)

        # Affichage carte par carte
        for _, row in df_filtre.head(50).iterrows():
            with st.container():
                col_titre, col_niveau = st.columns([5, 1])
                with col_titre:
                    st.markdown(f"**{row['Métier']}**")
                with col_niveau:
                    niv = str(row.get('Niveau', ''))
                    couleur_niv = "#6b9e7e" if "Directeur" in niv or "Entrepreneur" in niv else "#c9a84c" if "Manager" in niv else "#7a7a8c"
                    st.markdown(
                        f'<div style="background:{couleur_niv};color:white;padding:2px 8px;'
                        f'border-radius:10px;font-size:0.75rem;text-align:center">{niv[:15]}</div>',
                        unsafe_allow_html=True
                    )

                meta = []
                secteur = str(row.get("Secteur(s) activité", ""))
                if secteur and secteur != "nan":
                    meta.append(f"🏢 {secteur.split(';')[0].strip()}")
                domaine = str(row.get("Domaine", ""))
                if domaine and domaine != "nan":
                    meta.append(f"📁 {domaine}")
                salaire = str(row.get("Salaire", ""))
                if salaire and salaire != "nan":
                    meta.append(f"💶 {salaire}")
                diplomes = str(row.get("Diplômes", ""))
                if diplomes and diplomes != "nan":
                    meta.append(f"🎓 {diplomes[:50]}")

                st.markdown(" · ".join(meta) if meta else "")

                descriptif = str(row.get("Descriptif", ""))
                if descriptif and descriptif != "nan":
                    st.markdown(f"<small>{descriptif[:250]}{'…' if len(descriptif) > 250 else ''}</small>",
                                unsafe_allow_html=True)

                # Soft skills du métier — noms exacts des colonnes Excel (source : SS_COLS)
                ss_display = []
                for ss in SS_COLS:
                    val = str(row.get(ss, ""))
                    if val and val != "nan":
                        emoji = "🟢" if val == "Absolument nécessaire" else "🟡" if val == "Nécessaire" else "⚪"
                        ss_display.append(f"{emoji} {ss}")

                if ss_display:
                    with st.expander("Voir les soft skills requises"):
                        cols = st.columns(4)
                        for i, s in enumerate(ss_display):
                            cols[i % 4].markdown(f"<small>{s}</small>", unsafe_allow_html=True)

                st.markdown("---")

        if len(df_filtre) > 50:
            st.info(f"Affichage limité aux 50 premiers résultats sur {len(df_filtre)}. Affine tes filtres pour voir des résultats plus précis.")
