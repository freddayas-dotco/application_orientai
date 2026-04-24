import pandas as pd
import streamlit as st
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METIERS_FILE = os.path.join(BASE_DIR, "Metiers_OrientAI_v5.1.xlsx")

@st.cache_data
def load_metiers():
    """Charge et nettoie la base de données métiers Excel."""
    try:
        # Lire la première feuille
        df = pd.read_excel(METIERS_FILE, header=2) # Le header est sur la 3ème ligne (index 2)
        
        # Filtrer les lignes vides
        df = df[df.iloc[:, 1].notna() & (df.iloc[:, 1] != "")]
        
        # Renommer les colonnes pour un accès facile
        df = df.rename(columns={
            df.columns[1]: 'Métier',
            df.columns[2]: 'Secteur',
            df.columns[3]: 'Domaine',
            df.columns[4]: 'Niveau',
            df.columns[5]: 'Diplômes_requis',
            df.columns[6]: 'Salaire',
            df.columns[7]: 'Descriptif',
            df.columns[8]: 'ONISEP',
            df.columns[9]: 'SS_Communication',
            df.columns[10]: 'SS_Esprit_critique',
            df.columns[11]: 'SS_Ethique',
            df.columns[12]: 'SS_Intelligence_emotionnelle',
            df.columns[13]: 'SS_Intelligence_sociale',
            df.columns[14]: 'SS_Management_projet',
            df.columns[15]: 'SS_Management_equipe',
            df.columns[16]: 'SS_Organisation',
            df.columns[17]: 'MBTI_EI',
            df.columns[18]: 'MBTI_SN',
            df.columns[19]: 'MBTI_TF',
            df.columns[20]: 'MBTI_JP',
        })
        
        # Remplir les NA par des chaînes vides pour les colonnes texte
        text_cols = ['Métier', 'Secteur', 'Domaine', 'Niveau', 'Diplômes_requis', 
                     'Salaire', 'Descriptif', 'ONISEP']
        df[text_cols] = df[text_cols].fillna("")
        
        # S'assurer que les soft skills sont des entiers entre 1 et 3
        ss_cols = ['SS_Communication', 'SS_Esprit_critique', 'SS_Ethique', 'SS_Intelligence_emotionnelle',
                   'SS_Intelligence_sociale', 'SS_Management_projet', 'SS_Management_equipe', 'SS_Organisation']
        for col in ss_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(2).clip(1, 3).astype(int)
            
        # S'assurer que les dims MBTI sont des lettres simples et fusionner en 1 colonne MBTI
        def get_letter(val, default):
            if pd.isna(val) or str(val).strip() == "": return default
            return str(val).strip()[0].upper()
            
        df['MBTI_EI'] = df['MBTI_EI'].apply(lambda x: get_letter(x, 'E'))
        df['MBTI_SN'] = df['MBTI_SN'].apply(lambda x: get_letter(x, 'N'))
        df['MBTI_TF'] = df['MBTI_TF'].apply(lambda x: get_letter(x, 'T'))
        df['MBTI_JP'] = df['MBTI_JP'].apply(lambda x: get_letter(x, 'J'))
        
        df['MBTI_Type'] = df['MBTI_EI'] + df['MBTI_SN'] + df['MBTI_TF'] + df['MBTI_JP']
        
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des métiers : {str(e)}")
        return pd.DataFrame()

def get_secteurs(df):
    """Retourne la liste unique de tous les secteurs."""
    secteurs = set()
    for s_str in df['Secteur']:
        if s_str:
            for s in str(s_str).split(';'):
                if s.strip():
                    secteurs.add(s.strip())
    return sorted(list(secteurs))
