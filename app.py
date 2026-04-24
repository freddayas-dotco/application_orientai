import streamlit as st
import time

from modules.data_loader import load_metiers, get_secteurs
from modules.questionnaire import load_questionnaire, SS_CATEGORIES
from modules.scoring import compute_ss_scores, compute_mbti
import modules.matching as matching
import modules.dashboard as dashboard

# --- CONFIGURATION PAGE ---
st.set_page_config(
    page_title="OrientAI - Orientation Scolaire & Pro",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for App styling
st.markdown("""
<style>
    .big-font {font-size:20px !important;}
    .hero-title {
        font-size: 3rem; font-weight: 800; background: -webkit-linear-gradient(45deg, #7c5cfc, #22d3ee);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 2rem;
    }
    .mbti-badge {
        display: inline-block; padding: 20px 40px; border-radius: 15px;
        background: linear-gradient(135deg, #7c5cfc 0%, #5b4fcf 100%);
        color: white; font-size: 3rem; font-weight: 900; letter-spacing: 2px;
        box-shadow: 0 10px 30px rgba(124, 92, 252, 0.3); text-align: center;
    }
    .stProgress .st-bo {background-color: #7c5cfc;}
    .stButton>button {width: 100%; border-radius: 8px;}
    .option-btn {text-align: left; justify-content: flex-start;}
    .metier-card {
        border: 1px solid #ddd; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;
        background: #f9f9fc; border-left: 4px solid #7c5cfc;
    }
    .metier-card-dark {
        border: 1px solid #333; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;
        background: #1e1e2d; border-left: 4px solid #7c5cfc;
    }
</style>
""", unsafe_allow_html=True)

# --- INIT SESSION STATE ---
if 'step' not in st.session_state:
    st.session_state.step = 'accueil' # accueil, quiz, profil, resultats, dashboard
if 'profil_type' not in st.session_state:
    st.session_state.profil_type = None # 'college' ou 'lycee'
if 'answers' not in st.session_state:
    st.session_state.answers = [] # list of ints (0 to 3)
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'computed_ss' not in st.session_state:
    st.session_state.computed_ss = []
if 'computed_mbti' not in st.session_state:
    st.session_state.computed_mbti = ""
if 'user_info' not in st.session_state:
    st.session_state.user_info = {"nom": "", "prenom": "", "classe": ""}
if 'top_metiers' not in st.session_state:
    st.session_state.top_metiers = []

# Navigation Sidebar
with st.sidebar:
    st.title("🧭 OrientAI")
    st.divider()
    if st.button("🏠 Accueil"):
        st.session_state.step = 'accueil'
        st.rerun()
    if st.session_state.step in ['profil', 'resultats']:
        if st.button("📊 Mon Profil"):
            st.session_state.step = 'profil'
            st.rerun()
        if st.button("🎯 Mes Métiers"):
            st.session_state.step = 'resultats'
            st.rerun()
    st.divider()
    if st.button("⚙️ Espace Conseiller"):
        st.session_state.step = 'dashboard'
        st.rerun()

# --- ÉCRANS ---

def view_accueil():
    st.markdown("<div class='hero-title'>OrientAI</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.2rem; color:#666; margin-bottom:3rem;'>Trouvez votre voie grâce à vos Soft Skills et votre profil MBTI</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🎒 **Pour les collégien·ne·s**\n\nQuestions adaptées au contexte scolaire et au jeune âge.")
        if st.button("Passer le test Collège", key="btn_col"):
            st.session_state.profil_type = 'college'
            st.session_state.answers = []
            st.session_state.current_q = 0
            st.session_state.step = 'infos'
            st.rerun()
            
    with col2:
        st.success("🎓 **Pour les lycéen·ne·s**\n\nQuestions ancrées dans les études et la vie quotidienne.")
        if st.button("Passer le test Lycée", key="btn_lyc"):
            st.session_state.profil_type = 'lycee'
            st.session_state.answers = []
            st.session_state.current_q = 0
            st.session_state.step = 'infos'
            st.rerun()
            
    with col3:
        st.warning("💼 **Pour les adultes**\n\nQuestions professionnelles (utilise la version Lycée avec vouvoiement).")
        if st.button("Passer le test Adulte", key="btn_adu"):
            st.session_state.profil_type = 'lycee'
            st.session_state.answers = []
            st.session_state.current_q = 0
            st.session_state.step = 'infos'
            st.rerun()
            
    st.divider()
    
    # Load metadata for display
    df_metiers = load_metiers()
    if not df_metiers.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Métiers analysés", len(df_metiers))
        c2.metric("Questions", "48 / 49")
        c3.metric("Secteurs", len(get_secteurs(df_metiers)))
        c4.metric("Algorithme", "SS + MBTI")

def view_infos():
    st.title("📝 Vos informations (Optionnel)")
    st.write("Ces informations permettront à votre conseiller d'orientation de retrouver vos résultats. Si vous utilisez cet outil de manière autonome, vous pouvez passer cette étape.")
    
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("Nom", value=st.session_state.user_info["nom"])
    with col2:
        prenom = st.text_input("Prénom", value=st.session_state.user_info["prenom"])
        
    classe = st.text_input("Classe / Situation (ex: 3ème A, Terminale, Reconversion)", value=st.session_state.user_info["classe"])
    
    if st.button("Continuer vers le questionnaire ➡️"):
        st.session_state.user_info = {"nom": nom, "prenom": prenom, "classe": classe}
        st.session_state.step = 'quiz'
        st.rerun()

def view_quiz():
    questions = load_questionnaire(st.session_state.profil_type)
    if not questions:
        st.error("Impossible de charger les questions.")
        if st.button("Retour à l'accueil"):
            st.session_state.step = 'accueil'
            st.rerun()
        return

    total_q = len(questions)
    
    # Rendre le tableau de réponses de taille dynamique au nombre_questions réel (49)
    if len(st.session_state.answers) < total_q:
        st.session_state.answers.extend([None] * (total_q - len(st.session_state.answers)))
        
    idx = st.session_state.current_q
    
    if idx >= total_q:
        # Fin du test, calcul !
        with st.spinner("Calcul de votre profil en cours (Soft skills + MBTI)..."):
            time.sleep(1) # Petit effet UX
            st.session_state.computed_ss = compute_ss_scores(questions, st.session_state.answers)
            st.session_state.computed_mbti = compute_mbti(questions, st.session_state.answers)
            st.session_state.step = 'profil'
            st.rerun()
        return

    q = questions[idx]
    
    # Header Quiz
    progress = idx / total_q
    st.progress(progress, text=f"Question {idx+1} sur {total_q}")
    
    st.markdown(f"**Compétence visée :** <span style='color:#7c5cfc;'>{q['cat_name']}</span>", unsafe_allow_html=True)
    if q['sous_cat']:
        st.caption(f"Sous-catégorie : {q['sous_cat']}")
        
    st.markdown(f"### {q['q']}")
    st.write("")
    
    # Options
    labels = ["A", "B", "C", "D"]
    for i, opt in enumerate(q['options']):
        if opt and str(opt).strip():
            if st.button(f"**{labels[i]}** — {opt}", key=f"q_{idx}_opt_{i}", use_container_width=True):
                st.session_state.answers[idx] = i
                st.session_state.current_q += 1
                st.rerun()
                
    st.divider()
    col1, col2, col3 = st.columns([1,2,1])
    with col1:
        if idx > 0:
            if st.button("⬅️ Précédent"):
                st.session_state.current_q -= 1
                st.rerun()
    with col3:
        # On permet de passer au suivant si on a déjà répondu dans le passé
        if st.session_state.answers[idx] is not None:
            if st.button("Suivant ➡️"):
                st.session_state.current_q += 1
                st.rerun()

def view_profil():
    st.title("✨ Mon Profil OrientAI")
    
    # MBTI
    st.markdown("<p style='text-align:center; font-size:1.2rem;'>Votre type MBTI :</p>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; margin-bottom:2rem;'><span class='mbti-badge'>{st.session_state.computed_mbti}</span></div>", unsafe_allow_html=True)
    
    MBTI_DESCR = {
        "INTJ": "Architecte — Visionnaire logique, stratège indépendant.",
        "INTP": "Logicien — Penseur analytique, curieux et inventif.",
        "ENTJ": "Commandant — Leader charismatique, décideur.",
        "ENTP": "Innovateur — Débateur créatif.",
        "INFJ": "Avocat — Idéaliste inspirant.",
        "INFP": "Médiateur — Rêveur créatif.",
        "ENFJ": "Protagoniste — Leader chaleureux.",
        "ENFP": "Animateur — Enthousiaste créatif.",
        "ISTJ": "Logisticien — Fiable, méthodique.",
        "ISFJ": "Défenseur — Dévoué, attentionné.",
        "ESTJ": "Dirigeant — Organisateur efficace.",
        "ESFJ": "Consul — Social, attentif aux autres.",
        "ISTP": "Virtuose — Pragmatique curieux.",
        "ISFP": "Aventurier — Artiste sensible.",
        "ESTP": "Entrepreneur — Dynamique, aime l'action.",
        "ESFP": "Animateur scène — Spontané, enthousiaste."
    }
    desc = MBTI_DESCR.get(st.session_state.computed_mbti, "Profil personnalisé.")
    st.info(f"**{desc}**")
    
    st.divider()
    
    # Soft skills
    st.subheader("Vos Soft Skills")
    ss_names = list(SS_CATEGORIES.keys())
    scores = st.session_state.computed_ss
    scores_padded = [scores[i] if i < len(scores) else 2 for i in range(8)]
    
    import plotly.express as px
    import pandas as pd
    
    labels_map = {1: "Peu développé", 2: "Développé", 3: "Très développé"}
    
    df_ss = pd.DataFrame({
        "Compétence": ss_names,
        "Niveau (1-3)": scores_padded,
        "Niveau": [labels_map[s] for s in scores_padded],
    })
    
    fig = px.bar(
        df_ss,
        x="Niveau (1-3)",
        y="Compétence",
        orientation='h',
        text="Niveau",
        color="Niveau",
        color_discrete_map={"Peu développé": "#f87171", "Développé": "#fbbf24", "Très développé": "#4ade80"}
    )
    
    fig.update_layout(
        xaxis=dict(range=[0, 3.2], showticklabels=False, title=""),
        yaxis=dict(title="", autorange="reversed"),
        showlegend=False,
        height=450,
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    # Positionner le texte à l'intérieur
    fig.update_traces(textposition='inside', insidetextanchor='end', textfont=dict(size=13, color='rgba(255,255,255,0.9)'))
    
    st.plotly_chart(fig, use_container_width=True)
            
    st.divider()
    
    if st.button("🚀 Voir les métiers compatibles avec mon profil", type="primary"):
        st.session_state.step = 'resultats'
        st.rerun()

def view_resultats():
    st.title("🎯 Les métiers faits pour vous")
    st.write("Score calculé sur la correspondance de vos Soft Skills (70%) et de votre MBTI (30%).")
    
    df_metiers = load_metiers()
    secteurs = get_secteurs(df_metiers)
    
    # Filtres
    col1, col2 = st.columns(2)
    with col1:
        f_secteur = st.selectbox("Secteur d'activité", ["Tous"] + secteurs)
    with col2:
        f_niveau = st.selectbox("Niveau hiérarchique", ["Tous", "Opérationnel", "Manager", "Responsable", "Directeur", "PDG / Dirigeant", "Entrepreneur"])
        
    # Calcul
    with st.spinner("Analyse de toute la base métiers..."):
        top_metiers = matching.get_top_metiers(
            df_metiers, 
            st.session_state.computed_ss, 
            st.session_state.computed_mbti, 
            top_n=30,
            secteur_filter=f_secteur,
            niveau_filter=f_niveau
        )
        
    # Sauvegarde silencieuse de la 1ere passe (pas des filtres secondaires)
    if 'saved' not in st.session_state and top_metiers and st.session_state.user_info.get("nom"):
        dashboard.sauvegarder_resultat(
            st.session_state.user_info["nom"],
            st.session_state.user_info["prenom"],
            st.session_state.user_info["classe"],
            st.session_state.profil_type,
            st.session_state.computed_mbti,
            st.session_state.computed_ss,
            top_metiers
        )
        st.session_state.saved = True
        
    st.session_state.top_metiers = top_metiers
    
    if not top_metiers:
        st.warning("Aucun métier ne correspond exactement à ces filtres. Essayez de les élargir.")
        return
        
    # Affichage
    for i, m in enumerate(top_metiers):
        theme_class = "metier-card-dark" if st.get_option("theme.base") == "dark" else "metier-card"
        
        score_color = "#4ade80" if m['Score'] >= 80 else "#fbbf24" if m['Score'] >= 60 else "#f87171"
        
        html = f"""
        <div class="metier-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <h3 style="margin-top:0;">#{i+1} — {m['Métier']}</h3>
                <h2 style="color:{score_color}; margin:0;">{m['Score']}%</h2>
            </div>
            <p><strong>Secteur:</strong> {m['Secteur']} | <strong>Niveau:</strong> {m['Niveau']}</p>
            <p style="font-size:0.9rem;">{m['Descriptif']}</p>
        """
        if m['ONISEP'] and "http" in str(m['ONISEP']):
            html += f'<a href="{m["ONISEP"]}" target="_blank" style="text-decoration:none; color:#22d3ee; font-weight:bold;">🔗 Fiche ONISEP ↗</a>'
            
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
        
    if st.button("↺ Recommencer le test"):
        st.session_state.clear()
        st.rerun()

# --- ROUTER ---
if st.session_state.step == 'accueil':
    view_accueil()
elif st.session_state.step == 'infos':
    view_infos()
elif st.session_state.step == 'quiz':
    view_quiz()
elif st.session_state.step == 'profil':
    view_profil()
elif st.session_state.step == 'resultats':
    view_resultats()
elif st.session_state.step == 'dashboard':
    dashboard.afficher_dashboard()
