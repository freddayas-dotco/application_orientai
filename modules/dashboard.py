import pandas as pd
import streamlit as st
import os
import plotly.express as px

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTATS_FILE = os.path.join(DATA_DIR, "resultats.csv")

def assurer_dossier_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def sauvegarder_resultat(nom, prenom, classe, profil_type, mbti, ss_scores, top_metiers):
    assurer_dossier_data()
    
    # Format des 3 premiers métiers
    top3 = ""
    if top_metiers and len(top_metiers) > 0:
        noms = [m['Métier'] for m in top_metiers[:3]]
        top3 = " | ".join(noms)
        
    nouvelle_ligne = pd.DataFrame([{
        "Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
        "Nom": nom,
        "Prénom": prenom,
        "Classe/Statut": classe,
        "Profil_Base": profil_type,
        "MBTI": mbti,
        "SS_Communication": ss_scores[0],
        "SS_Esprit_critique": ss_scores[1],
        "SS_Ethique": ss_scores[2],
        "SS_Intel_emo": ss_scores[3],
        "SS_Intel_soc": ss_scores[4],
        "SS_Mgmt_projet": ss_scores[5],
        "SS_Mgmt_equipe": ss_scores[6],
        "SS_Organisation": ss_scores[7],
        "Top3_Metiers": top3
    }])
    
    try:
        if os.path.exists(RESULTATS_FILE):
            df = pd.read_csv(RESULTATS_FILE)
            df = pd.concat([df, nouvelle_ligne], ignore_index=True)
        else:
            df = nouvelle_ligne
            
        df.to_csv(RESULTATS_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"Erreur de sauvegarde : {e}")
        return False

def afficher_dashboard():
    st.title("📊 Dashboard Conseiller")
    
    if not os.path.exists(RESULTATS_FILE):
        st.info("Aucun résultat enregistré pour le moment.")
        return
        
    try:
        df = pd.read_csv(RESULTATS_FILE)
        
        # Stats globales
        col1, col2, col3 = st.columns(3)
        col1.metric("Total passations", len(df))
        col2.metric("Profils Lycée/Adulte", len(df[df['Profil_Base'] != 'college']))
        col3.metric("Profils Collège", len(df[df['Profil_Base'] == 'college']))
        
        st.divider()
        
        col_charts1, col_charts2 = st.columns(2)
        
        with col_charts1:
            st.subheader("Répartition des profils MBTI")
            mbti_counts = df['MBTI'].value_counts().reset_index()
            mbti_counts.columns = ['MBTI', 'Count']
            fig_mbti = px.pie(mbti_counts, values='Count', names='MBTI', hole=0.4)
            st.plotly_chart(fig_mbti, use_container_width=True)
            
        with col_charts2:
            st.subheader("Classes / Statuts")
            classe_counts = df['Classe/Statut'].value_counts().reset_index()
            classe_counts.columns = ['Classe', 'Count']
            fig_classe = px.bar(classe_counts, x='Classe', y='Count')
            st.plotly_chart(fig_classe, use_container_width=True)
            
        st.divider()
        
        st.subheader("Détail des résultats récents")
        st.dataframe(
            df.sort_values(by="Date", ascending=False).head(50),
            use_container_width=True,
            hide_index=True
        )
        
        # Bouton d'export CSV
        with open(RESULTATS_FILE, "rb") as file:
            st.download_button(
                label="📥 Télécharger tous les résultats (CSV)",
                data=file,
                file_name="orientai_resultats.csv",
                mime="text/csv",
            )
            
    except Exception as e:
        st.error(f"Erreur de lecture du dashboard : {e}")
