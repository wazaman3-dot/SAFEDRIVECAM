import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# Config page
st.set_page_config(
    page_title="DASHBOARD ROAD SAFETY MOVE-YAOUNDE", 
    layout="wide", 
    page_icon="🚦",
    initial_sidebar_state="expanded"
)

# Palette de couleurs harmonisée
COLORS = {
    'primary': '#0056D2',
    'secondary': '#4CAF50',
    'danger': '#FF3D00',
    'warning': '#FF9800',
    'info': '#2196F3',
    'dark': '#323F4B',
    'light': '#7B8794',
    'success': '#4CAF50',
    'taxi': '#FFC107',
    'moto': '#9C27B0',
    'utilitaire': '#607D8B',
    'cross_analysis': '#FFC107'
}

# Style CSS complet avec design des onglets et KPIs alignés horizontalement
st.markdown(f"""
<style>
/* ============================================= */
/* STYLE DES KPIs ALIGNÉS HORIZONTALEMENT        */
/* ============================================= */

.kpi-row-container {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin: 1.5rem 0 2rem 0;
    width: 100%;
}}

.kpi-item {{
    background: white;
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    transition: all 0.3s ease;
    border-top: 4px solid;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
}}

.kpi-item:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}}

.kpi-icon {{
    font-size: 1.5rem;
    margin-bottom: 0.3rem;
    display: block;
}}

.kpi-value {{
    font-weight: 700;
    font-size: 1.4rem;
    color: {COLORS['dark']};
    margin: 0.2rem 0;
    line-height: 1.2;
}}

.kpi-label {{
    font-weight: 600;
    font-size: 0.7rem;
    color: {COLORS['light']};
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 0;
}}

.kpi-percentage {{
    font-size: 0.75rem;
    font-weight: 600;
    margin-top: 0.2rem;
}}

/* ============================================= */
/* STYLE DES ONGLETS PRINCIPAUX - ANCIEN DESIGN  */
/* ============================================= */

.stTabs [data-baseweb="tab-list"] {{
    gap: 2px;
    margin-bottom: 1.5rem;
    background-color: #f0f2f6;
    padding: 4px;
    border-radius: 8px;
}}

.stTabs [data-baseweb="tab"] {{
    height: 45px;
    white-space: nowrap;
    border-radius: 6px;
    background-color: white;
    border: 1px solid #e0e0e0;
    font-weight: 600;
    font-size: 0.85rem;
    color: #555;
    transition: all 0.3s ease;
    padding: 0 16px;
    margin: 0 2px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.stTabs [data-baseweb="tab"]:hover {{
    background-color: #f8f9fa;
    border-color: #0056D2;
    color: #0056D2;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0, 86, 210, 0.1);
}}

.stTabs [aria-selected="true"] {{
    background-color: #0056D2 !important;
    color: white !important;
    border-color: #0056D2 !important;
    box-shadow: 0 2px 8px rgba(0, 86, 210, 0.2);
}}

/* Animation pour le tab actif */
.stTabs [aria-selected="true"]::after {{
    content: '';
    position: absolute;
    bottom: -2px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-bottom: 6px solid #0056D2;
}}

/* Style spécifique pour chaque tab avec couleurs d'icônes */
.stTabs [data-baseweb="tab"]:nth-child(1) {{ /* 📈 Synthèse */
    border-left: 3px solid #4CAF50;
}}

.stTabs [data-baseweb="tab"]:nth-child(2) {{ /* ⏰ Temporelle */
    border-left: 3px solid #FF9800;
}}

.stTabs [data-baseweb="tab"]:nth-child(3) {{ /* 📍 Spatiale */
    border-left: 3px solid #2196F3;
}}

.stTabs [data-baseweb="tab"]:nth-child(4) {{ /* 🎯 Causes */
    border-left: 3px solid #FF3D00;
}}

.stTabs [data-baseweb="tab"]:nth-child(5) {{ /* 👥 Usagers */
    border-left: 3px solid #9C27B0;
}}

.stTabs [data-baseweb="tab"]:nth-child(6) {{ /* 🚗 Véhicules */
    border-left: 3px solid #607D8B;
}}

.stTabs [data-baseweb="tab"]:nth-child(7) {{ /* 🔬 Analyses Croisées - NOUVEAU */
    border-left: 3px solid {COLORS['cross_analysis']};
}}

.stTabs [data-baseweb="tab"]:nth-child(8) {{ /* 📋 Données Brutes */
    border-left: 3px solid #795548;
}}

/* Animation hover spécifique par tab */
.stTabs [data-baseweb="tab"]:nth-child(1):hover {{
    border-color: #4CAF50;
    color: #4CAF50;
}}

.stTabs [data-baseweb="tab"]:nth-child(2):hover {{
    border-color: #FF9800;
    color: #FF9800;
}}

.stTabs [data-baseweb="tab"]:nth-child(3):hover {{
    border-color: #2196F3;
    color: #2196F3;
}}

.stTabs [data-baseweb="tab"]:nth-child(4):hover {{
    border-color: #FF3D00;
    color: #FF3D00;
}}

.stTabs [data-baseweb="tab"]:nth-child(5):hover {{
    border-color: #9C27B0;
    color: #9C27B0;
}}

.stTabs [data-baseweb="tab"]:nth-child(6):hover {{
    border-color: #607D8B;
    color: #607D8B;
}}

.stTabs [data-baseweb="tab"]:nth-child(7):hover {{ /* Analyses Croisées */
    border-color: {COLORS['cross_analysis']};
    color: {COLORS['cross_analysis']};
}}

.stTabs [data-baseweb="tab"]:nth-child(8):hover {{
    border-color: #795548;
    color: #795548;
}}

/* ============================================= */
/* STYLES GÉNÉRAUX                               */
/* ============================================= */

/* Style pour les tables */
.dataframe-container {{
    overflow-x: auto;
    margin: 1rem 0;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border: 1px solid #e0e0e0;
}}

/* Style pour les filtres */
.filter-group {{
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    border: 1px solid #dee2e6;
}}

/* Section export */
.export-section {{
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 8px;
    margin: 2rem 0;
    border: 1px solid #dee2e6;
}}

/* Cartes statistiques */
.stat-card {{
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
    border-left: 4px solid {COLORS['primary']};
}}

/* Badges */
.filter-badge {{
    background: #e3f2fd;
    color: {COLORS['primary']};
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 0.75rem;
    margin-right: 4px;
    display: inline-block;
    margin-bottom: 4px;
}}

/* Titres harmonisés */
h1, h2, h3 {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}}

h1 {{
    color: {COLORS['primary']};
    margin-bottom: 0.5rem;
}}

h2 {{
    color: {COLORS['dark']};
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid {COLORS['primary']};
}}

h3 {{
    color: {COLORS['dark']};
    margin-top: 1rem;
    margin-bottom: 0.8rem;
}}

/* Style pour les sections dans les tabs */
.tab-section {{
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border: 1px solid #e0e0e0;
}}

.tab-section h3 {{
    color: {COLORS['primary']};
    margin-top: 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #f0f2f6;
}}

/* Style pour les cartes dans l'onglet Analyses Croisées */
.analysis-card {{
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border: 1px solid #e0e0e0;
    border-left: 4px solid {COLORS['cross_analysis']};
}}

.analysis-card h4 {{
    color: {COLORS['cross_analysis']};
    margin-top: 0;
    margin-bottom: 1rem;
}}

/* Animation de transition entre tabs */
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.stTabs [role="tabpanel"] {{
    animation: fadeIn 0.3s ease-out;
}}

/* ============================================= */
/* RESPONSIVE DESIGN                             */
/* ============================================= */

/* Tablet: 3 columns */
@media (min-width: 768px) {{
    .kpi-row-container {{
        grid-template-columns: repeat(3, 1fr);
    }}
}}

/* Desktop: 4 columns */
@media (min-width: 1024px) {{
    .kpi-row-container {{
        grid-template-columns: repeat(4, 1fr);
    }}
}}

@media (max-width: 992px) {{
    .stTabs [data-baseweb="tab"] {{
        height: 40px;
        font-size: 0.8rem;
        padding: 0 12px;
    }}
    .kpi-item {{
        padding: 0.8rem;
    }}
}}

@media (max-width: 768px) {{
    .stTabs [data-baseweb="tab-list"] {{
        overflow-x: auto;
        flex-wrap: nowrap;
        padding-bottom: 5px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        min-width: 120px;
        font-size: 0.75rem;
        padding: 0 8px;
    }}
    
    .kpi-row-container {{
        gap: 0.5rem;
    }}
    
    .tab-section {{
        padding: 1rem;
    }}
}}

@media (max-width: 576px) {{
    .stTabs [data-baseweb="tab"] {{
        min-width: 100px;
        height: 35px;
        font-size: 0.7rem;
    }}
    
    .kpi-item {{
        padding: 0.6rem;
        height: 100px;
    }}
    
    .kpi-value {{
        font-size: 1.2rem;
    }}
    
    .tab-section {{
        padding: 0.8rem;
        margin-bottom: 1rem;
    }}
}}

/* Style spécial pour le nouvel onglet Analyses Croisées */
.cross-analysis-tab {{
    background: linear-gradient(135deg, #FFF8E1 0%, #FFECB3 100%);
    border: 1px solid #FFD54F;
}}

.cross-analysis-tab:hover {{
    background: linear-gradient(135deg, #FFECB3 0%, #FFE082 100%);
}}

/* Style pour les sous-sections dans les tabs */
.sub-section {{
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 6px;
    margin: 1rem 0;
    border-left: 3px solid {COLORS['primary']};
}}
</style>
""", unsafe_allow_html=True)

# =====================================================
# FONCTIONS DE TÉLÉCHARGEMENT
# =====================================================

def create_html_report(df_filtre, kpis_data, filters_text):
    """Crée un rapport HTML simple pour le téléchargement"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Rapport CESR - Sécurité Routière Yaoundé</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: {COLORS['primary']}; }}
            h2 {{ color: {COLORS['dark']}; border-bottom: 2px solid {COLORS['primary']}; padding-bottom: 10px; }}
            .kpi-container {{ display: flex; flex-wrap: wrap; gap: 20px; margin: 20px 0; }}
            .kpi-card {{ background: #f5f5f5; padding: 15px; border-radius: 8px; border-left: 4px solid; min-width: 200px; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: {COLORS['primary']}; color: white; }}
        </style>
    </head>
    <body>
        <h1>CESR - Rapport d'Analyse Sécurité Routière</h1>
        <p><strong>Date du rapport:</strong> {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}</p>
        <p><strong>Nombre d'accidents analysés:</strong> {len(df_filtre):,}</p>
        
        <h2>Filtres appliqués</h2>
        <p>{' | '.join(filters_text) if filters_text else 'Aucun filtre spécifique'}</p>
        
        <h2>Indicateurs Clés de Performance</h2>
        <div class="kpi-container">
    """
    
    for kpi in kpis_data[:8]:
        html_content += f"""
            <div class="kpi-card" style="border-left-color: {kpi['color']};">
                <strong>{kpi['label']}</strong><br>
                <span style="font-size: 1.5em; font-weight: bold;">{kpi['value']}</span>
            </div>
        """
    
    html_content += """
        </div>
        
        <h2>Statistiques principales</h2>
        <table>
            <tr>
                <th>Type d'accident</th>
                <th>Nombre</th>
                <th>Pourcentage</th>
            </tr>
    """
    
    # Statistiques de gravité
    grav_counts = df_filtre['Gravite'].value_counts()
    total = len(df_filtre)
    for gravite, count in grav_counts.items():
        percentage = (count / total * 100) if total > 0 else 0
        html_content += f"""
            <tr>
                <td>{gravite}</td>
                <td>{count:,}</td>
                <td>{percentage:.1f}%</td>
            </tr>
        """
    
    html_content += """
        </table>
        
        <h2>Top 10 des points noirs</h2>
        <table>
            <tr>
                <th>Rue/Carrefour</th>
                <th>Nombre d'accidents</th>
            </tr>
    """
    
    # Top 10 des rues
    top_rues = df_filtre['Rue'].value_counts().head(10)
    for rue, count in top_rues.items():
        html_content += f"""
            <tr>
                <td>{rue}</td>
                <td>{count:,}</td>
            </tr>
        """
    
    html_content += """
        </table>
        
        <hr>
        <p style="text-align: center; color: #666; font-size: 0.9em;">
            CESR - Cabinet d'Expertise Sécurité Routière<br>
            Yaoundé, Cameroun • Rapport généré automatiquement
        </p>
    </body>
    </html>
    """
    
    return html_content.encode('utf-8')

def create_text_report(df_filtre, kpis_data, filters_text):
    """Crée un rapport texte simple pour le téléchargement"""
    text_content = f"""
    =============================================
    CESR - RAPPORT D'ANALYSE SÉCURITÉ ROUTIÈRE
    =============================================
    
    Date du rapport: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}
    Nombre d'accidents analysés: {len(df_filtre):,}
    
    FILTRES APPLIQUÉS:
    {' | '.join(filters_text) if filters_text else 'Aucun filtre spécifique'}
    
    INDICATEURS CLÉS DE PERFORMANCE:
    """
    
    for kpi in kpis_data[:8]:
        text_content += f"\n{kpi['label']}: {kpi['value']}"
    
    text_content += "\n\nSTATISTIQUES PRINCIPALES:\n"
    text_content += "-" * 40
    
    # Statistiques de gravité
    grav_counts = df_filtre['Gravite'].value_counts()
    total = len(df_filtre)
    for gravite, count in grav_counts.items():
        percentage = (count / total * 100) if total > 0 else 0
        text_content += f"\n{gravite}: {count:,} ({percentage:.1f}%)"
    
    text_content += "\n\nTOP 10 DES POINTS NOIRS:\n"
    text_content += "-" * 40
    
    # Top 10 des rues
    top_rues = df_filtre['Rue'].value_counts().head(10)
    for i, (rue, count) in enumerate(top_rues.items(), 1):
        text_content += f"\n{i:2d}. {rue}: {count:,}"
    
    text_content += f"""

=============================================
CESR - Cabinet d'Expertise Sécurité Routière
Yaoundé, Cameroun • Rapport généré automatiquement
=============================================
"""
    
    return text_content.encode('utf-8')

# =====================================================
# FONCTION JOURS FRANÇAIS ← AJOUTEZ ICI
# =====================================================
def get_french_day_names():
    return {0: 'Lundi', 1: 'Mardi', 2: 'Mercredi', 3: 'Jeudi', 
            4: 'Vendredi', 5: 'Samedi', 6: 'Dimanche'}
            
            
# CHARGEMENT BASE DE DONNÉES EXTERNE
df = pd.read_csv('donnees_securite_routiere_cesr.csv', parse_dates=['Date'])
df['Date'] = pd.to_datetime(df['Date'])  # Assure format datetime



# =====================================================
# SIDEBAR - FILTRES AVANCÉS
# =====================================================
st.sidebar.header("🔍 Filtres")

# Groupe 1: Période
st.sidebar.markdown('<div class="filter-group">', unsafe_allow_html=True)
st.sidebar.subheader("⏰ Période")
annee_min, annee_max = st.sidebar.slider(
    "Années", 
    2020, 2024, (2020, 2024),
    help="Sélectionnez la plage d'années"
)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Groupe 2: Gravité
st.sidebar.markdown('<div class="filter-group">', unsafe_allow_html=True)
st.sidebar.subheader("⚠️ Gravité")
gravite_filtre = st.sidebar.multiselect(
    "Type d'accident", 
    df['Gravite'].unique(), 
    default=df['Gravite'].unique(),
    help="Sélectionnez les types d'accidents"
)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Groupe 3: Localisation
st.sidebar.markdown('<div class="filter-group">', unsafe_allow_html=True)
st.sidebar.subheader("📍 Localisation")
rue_filtre = st.sidebar.multiselect(
    "Rue/ Carrefour", 
    sorted(df['Rue'].unique()),
    default=[],
    help="Filtrer par rue spécifique"
)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Groupe 4: Horaires
st.sidebar.markdown('<div class="filter-group">', unsafe_allow_html=True)
st.sidebar.subheader("🕐 Plage horaire")
heure_range = st.sidebar.slider(
    "Heures",
    0, 23,
    (14, 22),
    help="Plage horaire d'analyse"
)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Groupe 5: Options avancées
with st.sidebar.expander("⚙️ Options avancées"):
    sexe_filtre = st.multiselect(
        "Sexe conducteur", 
        df['Sexe_Conducteur'].unique(),
        default=df['Sexe_Conducteur'].unique()
    )
    age_range = st.slider(
        "Âge conducteur", 
        int(df['Age_Conducteur'].min()), 
        int(df['Age_Conducteur'].max()),
        (int(df['Age_Conducteur'].min()), int(df['Age_Conducteur'].max()))
    )
    vehicule_filtre = st.multiselect(
        "Type de véhicule",
        df['Type_Vehicule'].unique(),
        default=df['Type_Vehicule'].unique()
    )
    cause_filtre = st.multiselect(
        "Cause",
        df['Cause'].unique(),
        default=df['Cause'].unique()
    )

# =====================================================
# APPLICATION DES FILTRES
# =====================================================
df_filtre = df.copy()

# Filtres temporels
df_filtre = df_filtre[(df_filtre['Annee'] >= annee_min) & (df_filtre['Annee'] <= annee_max)]

# Filtres gravité
df_filtre = df_filtre[df_filtre['Gravite'].isin(gravite_filtre)]

# Filtres localisation
if rue_filtre:
    df_filtre = df_filtre[df_filtre['Rue'].isin(rue_filtre)]

# Filtres horaires
df_filtre = df_filtre[(df_filtre['Heure'] >= heure_range[0]) & (df_filtre['Heure'] <= heure_range[1])]

# Filtres avancés optionnels
df_filtre = df_filtre[df_filtre['Sexe_Conducteur'].isin(sexe_filtre)]
df_filtre = df_filtre[(df_filtre['Age_Conducteur'] >= age_range[0]) & (df_filtre['Age_Conducteur'] <= age_range[1])]
df_filtre = df_filtre[df_filtre['Type_Vehicule'].isin(vehicule_filtre)]
df_filtre = df_filtre[df_filtre['Cause'].isin(cause_filtre)]

# =====================================================
# EN-TÊTE PRINCIPAL
# =====================================================
col_title1, col_title2 = st.columns([3, 1])
with col_title1:
    st.markdown("# 🚦 ROAD SAFETY DASHBOARD 🚦")
    st.markdown(" Centre-ville Yaoundé, Cameroun • Analyse stratégique 2020-2024 • ")
    
with col_title2:
    st.markdown("")
    st.markdown(f"<div style='text-align: right; color: #666; font-size: 0.9rem;'>"
                f"Données mises à jour: {pd.Timestamp.now().strftime('%d/%m/%Y')}<br>"
                f"Accidents analysés: {len(df_filtre):,}</div>", 
                unsafe_allow_html=True)

# Affichage des filtres actifs
if st.sidebar.checkbox("Afficher les filtres actifs", value=True):
    with st.expander("📋 Filtres actuellement appliqués", expanded=False):
        filters_text = []
        if annee_min != 2020 or annee_max != 2024:
            filters_text.append(f"Années: {annee_min}-{annee_max}")
        if set(gravite_filtre) != set(df['Gravite'].unique()):
            filters_text.append(f"Gravité: {', '.join(gravite_filtre)}")
        if rue_filtre:
            filters_text.append(f"Rues: {', '.join(rue_filtre[:3])}{'...' if len(rue_filtre) > 3 else ''}")
        if heure_range != (14, 22):
            filters_text.append(f"Heures: {heure_range[0]}-{heure_range[1]}h")
        if set(sexe_filtre) != set(df['Sexe_Conducteur'].unique()):
            filters_text.append(f"Sexe: {', '.join(sexe_filtre)}")
        if age_range != (int(df['Age_Conducteur'].min()), int(df['Age_Conducteur'].max())):
            filters_text.append(f"Âge: {age_range[0]}-{age_range[1]} ans")
        if set(vehicule_filtre) != set(df['Type_Vehicule'].unique()):
            filters_text.append(f"Véhicules: {', '.join(vehicule_filtre[:2])}{'...' if len(vehicule_filtre) > 2 else ''}")
        if set(cause_filtre) != set(df['Cause'].unique()):
            filters_text.append(f"Causes: {', '.join(cause_filtre[:2])}{'...' if len(cause_filtre) > 2 else ''}")
        
        if filters_text:
            for text in filters_text:
                st.markdown(f'<span class="filter-badge">{text}</span>', unsafe_allow_html=True)
        else:
            st.markdown("*Toutes les données affichées (aucun filtre spécifique)*")

# =====================================================
# KPIs ALIGNÉS HORIZONTALEMENT DE GAUCHE À DROITE
# =====================================================
st.markdown("### 📊 Indicateurs Clés de Performance")

# Calcul des valeurs des KPIs
total_accidents = len(df_filtre)
materiels = (df_filtre['Gravite'] == 'Dommages matériels').sum()
corporels = (df_filtre['Gravite'] == 'Blessures corporelles').sum()
mortels = (df_filtre['Gravite'] == 'Mortels').sum()
pic_horaire = ((df_filtre['Heure'] >= heure_range[0]) & (df_filtre['Heure'] <= heure_range[1])).sum()
hommes = (df_filtre['Sexe_Conducteur'] == 'Homme').sum()
femmes = (df_filtre['Sexe_Conducteur'] == 'Femme').sum()
taux_mortalite = f"{(mortels / total_accidents * 100):.1f}%" if total_accidents > 0 else "0%"

# Distribution des véhicules
vehicule_counts = df_filtre['Type_Vehicule'].value_counts()
vehicule_tourisme = vehicule_counts.get('Véhicule tourisme', 0)
taxi = vehicule_counts.get('Taxi', 0)
utilitaire = vehicule_counts.get('Véhicule utilitaire', 0)
moto = vehicule_counts.get('Moto', 0)
bus = vehicule_counts.get('Bus', 0)

# KPIs alignés horizontalement dans une seule ligne

kpis_horizontal = [
    {'icon': '🚗', 'label': 'Total Accidents', 'color': COLORS['primary'], 'value': f"{total_accidents:,}"},
    {'icon': '🔧', 'label': 'Dommages Matériels', 'color': COLORS['success'], 'value': f"{materiels:,}"},
    {'icon': '🏥', 'label': 'Blessures Corporelles', 'color': COLORS['warning'], 'value': f"{corporels:,}"},
    {'icon': '💀', 'label': 'Accidents Mortels', 'color': COLORS['danger'], 'value': f"{mortels:,}"},
    {'icon': '⏰', 'label': f'{heure_range[0]}-{heure_range[1]}h', 'color': COLORS['info'], 'value': f"{pic_horaire:,}"},
    {'icon': '🚖', 'label': 'Taxis', 'color': COLORS['taxi'], 'value': f"{taxi:,}"},
    {'icon': '🏍️', 'label': 'Motos', 'color': COLORS['moto'], 'value': f"{moto:,}"},
    {'icon': '📊', 'label': 'Taux Mortalité', 'color': COLORS['dark'], 'value': taux_mortalite},
]
# Build HTML content as a list and join for better performance
html_parts = ['<div class="kpi-row-container">']

for kpi in kpis_horizontal:
    if kpi['label'] != 'Taux Mortalité':
        try:
            value_num = int(kpi['value'].replace(',', ''))
            pct = (value_num / total_accidents * 100) if total_accidents > 0 else 0
            pct_html = f'<div class="kpi-percentage" style="color: {kpi["color"]};">{pct:.1f}%</div>'
        except:
            pct_html = ''
    else:
        pct_html = ''
    
    html_parts.append(
        f'<div class="kpi-item" style="border-top-color: {kpi["color"]};">'
        f'<span class="kpi-icon">{kpi["icon"]}</span>'
        f'<div class="kpi-value">{kpi["value"]}</div>'
        f'<div class="kpi-label">{kpi["label"]}</div>'
        f'{pct_html}'
        f'</div>'
    )

html_parts.append('</div>')
final_html_content = ''.join(html_parts)

# Render HTML - try st.html() first (Streamlit 1.28+), fallback to st.markdown()
if hasattr(st, 'html'):
    st.html(final_html_content)
else:
    st.markdown(final_html_content, unsafe_allow_html=True)

# =====================================================
# ONGLETS PRINCIPAUX
# =====================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📈 Synthèse", "⏰ Temporelle", "📍 Spatiale", 
    "🎯 Causes", "👥 Usagers", "🚗 Véhicules", 
    "🔬 Analyses Croisées", "📋 Données Brutes"
])

# TAB 1: SYNTHÈSE
with tab1:
    st.subheader("📈 Vue d'ensemble et tendances")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Évolution annuelle
        evo_annuelle = df_filtre.groupby('Annee').size().reset_index(name='Accidents')
        fig_evo = px.line(evo_annuelle, x='Annee', y='Accidents',
                         title="Évolution annuelle des accidents",
                         markers=True,
                         color_discrete_sequence=[COLORS['primary']])
        fig_evo.update_layout(yaxis_title="Nombre d'accidents")
        st.plotly_chart(fig_evo, use_container_width=True)
        
        # Répartition par gravité
        grav_counts = df_filtre['Gravite'].value_counts()
        fig_grav = px.pie(values=grav_counts.values, names=grav_counts.index,
                         title="Répartition par gravité",
                         hole=0.4,
                         color=grav_counts.index,
                         color_discrete_map={
                             'Dommages matériels': COLORS['success'],
                             'Blessures corporelles': COLORS['warning'],
                             'Mortels': COLORS['danger']
                         })
        fig_grav.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_grav, use_container_width=True)
    
    with col2:
        # Top 10 des points noirs
        top_rues = df_filtre['Rue'].value_counts().head(10)
        fig_rues = px.bar(x=top_rues.values, y=top_rues.index, orientation='h',
                         title="Top 10 des points noirs",
                         color=top_rues.values,
                         color_continuous_scale='Reds',
                         labels={'x': 'Nombre d\'accidents', 'y': ''})
        st.plotly_chart(fig_rues, use_container_width=True)
        
        # Distribution des véhicules
        veh_counts = df_filtre['Type_Vehicule'].value_counts()
        fig_veh = px.bar(x=veh_counts.index, y=veh_counts.values,
                        title="Véhicules impliqués",
                        color=veh_counts.values,
                        color_continuous_scale='Viridis',
                        labels={'x': 'Type de véhicule', 'y': 'Nombre'})
        st.plotly_chart(fig_veh, use_container_width=True)

# TAB 2: ANALYSE TEMPORELLE
with tab2:
    st.subheader("⏰ Analyse temporelle des accidents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Par jour de la semaine
        jours_ordre = list(get_french_day_names().values())
        jour_counts = df_filtre['Jour_Semaine'].value_counts().reindex(jours_ordre)
        fig_jour = px.bar(x=jour_counts.index, y=jour_counts.values,
                         title="Accidents par jour de la semaine",
                         color=jour_counts.values,
                         color_continuous_scale='Blues')
        fig_jour.update_layout(xaxis_title="Jour", yaxis_title="Accidents")
        st.plotly_chart(fig_jour, use_container_width=True)
        
        # Distribution horaire détaillée
        fig_heure_det = px.histogram(df_filtre, x='Heure', nbins=24,
                                    title="Distribution horaire détaillée",
                                    color_discrete_sequence=[COLORS['primary']])
        fig_heure_det.update_layout(
            xaxis_title="Heure de la journée",
            yaxis_title="Nombre d'accidents"
        )
        st.plotly_chart(fig_heure_det, use_container_width=True)
    
    with col2:
        # Heatmap Heure x Jour
        heatmap_data = df_filtre.groupby(['Heure', 'Jour_Semaine']).size().unstack(fill_value=0)
        heatmap_data = heatmap_data.reindex(columns=jours_ordre)
        fig_heat = px.imshow(heatmap_data,
                            title="Heatmap: Heure × Jour de la semaine",
                            labels=dict(x="Jour", y="Heure", color="Accidents"),
                            color_continuous_scale='RdBu',
                            aspect="auto")
        st.plotly_chart(fig_heat, use_container_width=True)
        
        # Distribution par mois
        mois_order = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
                     'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
        mois_counts = df_filtre['Mois_Nom'].value_counts().reindex(mois_order)
        fig_mois = px.line(mois_counts, markers=True,
                          title="Évolution mensuelle",
                          labels={'index': 'Mois', 'value': 'Accidents'},
                          color_discrete_sequence=[COLORS['primary']])
        st.plotly_chart(fig_mois, use_container_width=True)

# TAB 3: ANALYSE SPATIALE
with tab3:
    st.subheader("📍 Analyse spatiale et cartographie")
    
    # Carte des points chauds
    st.markdown("### 🗺️ Carte des points chauds d'accidents")
    
    # Préparer les données pour la carte
    spatial_data = df_filtre.groupby(['Rue', 'Latitude', 'Longitude']).agg({
        'ID_Accident': 'count',
        'Gravite': lambda x: (x == 'Mortels').sum()
    }).reset_index()
    
    spatial_data.columns = ['Rue', 'Latitude', 'Longitude', 'Accidents', 'Accidents_Mortels']
    
    # Créer la carte avec Plotly
    fig_map = px.scatter_mapbox(
        spatial_data,
        lat="Latitude",
        lon="Longitude",
        size="Accidents",
        color="Accidents",
        hover_name="Rue",
        hover_data=["Accidents", "Accidents_Mortels"],
        size_max=30,
        zoom=14,
        height=500,
        color_continuous_scale=px.colors.sequential.Reds,
        title="Carte thermique des accidents à Yaoundé"
    )
    
    # Utiliser le style OpenStreetMap
    fig_map.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":40,"l":0,"b":0},
        mapbox=dict(
            center=dict(lat=3.8650, lon=11.5180),
            zoom=14
        )
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Analyses spatiales détaillées
    col1, col2 = st.columns(2)
    
    with col1:
        # Analyse par type de voie
        df_filtre['Type_Voie'] = df_filtre['Rue'].apply(lambda x: 
            'Carrefour' if 'Carrefour' in x else
            'Avenue' if 'Avenue' in x else
            'Boulevard' if 'Boulevard' in x else
            'Rue'
        )
        
        type_counts = df_filtre['Type_Voie'].value_counts()
        fig_type = px.pie(values=type_counts.values, names=type_counts.index,
                         title="Répartition par type de voie",
                         hole=0.3)
        st.plotly_chart(fig_type, use_container_width=True)
    
    with col2:
        # Densité par secteur géographique
        df_filtre['Secteur'] = pd.cut(df_filtre['Longitude'], bins=5, labels=['Ouest', 'Centre-Ouest', 'Centre', 'Centre-Est', 'Est'])
        secteur_counts = df_filtre['Secteur'].value_counts().sort_index()
        
        fig_secteur = px.bar(x=secteur_counts.index, y=secteur_counts.values,
                            title="Accidents par secteur géographique",
                            color=secteur_counts.values,
                            color_continuous_scale='Blues')
        st.plotly_chart(fig_secteur, use_container_width=True)
    
    # Tableau des points noirs avec coordonnées
    st.markdown("### 📍 Points noirs avec coordonnées géographiques")
    
    points_noirs = df_filtre.groupby('Rue').agg({
        'ID_Accident': 'count',
        'Gravite': lambda x: (x == 'Mortels').sum(),
        'Latitude': 'first',
        'Longitude': 'first'
    }).reset_index()
    
    points_noirs.columns = ['Rue', 'Total_Accidents', 'Accidents_Mortels', 'Latitude', 'Longitude']
    points_noirs = points_noirs.sort_values('Total_Accidents', ascending=False)
    points_noirs['Taux_Mortalite'] = (points_noirs['Accidents_Mortels'] / points_noirs['Total_Accidents'] * 100).round(1)
    
    st.dataframe(
        points_noirs.head(15),
        column_config={
            "Rue": "Localisation",
            "Total_Accidents": st.column_config.NumberColumn("Total accidents", format="%d"),
            "Accidents_Mortels": st.column_config.NumberColumn("Accidents mortels", format="%d"),
            "Taux_Mortalite": st.column_config.NumberColumn("Taux mortalité (%)", format="%.1f"),
            "Latitude": st.column_config.NumberColumn("Latitude", format="%.6f"),
            "Longitude": st.column_config.NumberColumn("Longitude", format="%.6f")
        },
        use_container_width=True
    )

# TAB 4: ANALYSE DES CAUSES
with tab4:
    st.subheader("🎯 Analyse des causes principales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Causes principales
        cause_counts = df_filtre['Cause'].value_counts().reset_index()
        cause_counts.columns = ['Cause', 'Nombre']
        fig_cause = px.bar(cause_counts, x='Cause', y='Nombre',
                          title="Distribution des causes",
                          color='Nombre',
                          color_continuous_scale='Reds')
        fig_cause.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig_cause, use_container_width=True)
        
        # Causes par heure
        fig_cause_heure = px.box(df_filtre, x='Cause', y='Heure',
                                title="Distribution horaire des causes",
                                points=False)
        fig_cause_heure.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig_cause_heure, use_container_width=True)
    
    with col2:
        # Causes par gravité
        cause_grav = pd.crosstab(df_filtre['Cause'], df_filtre['Gravite'])
        fig_cause_grav = px.bar(cause_grav, barmode='group',
                               title="Causes par type de gravité",
                               labels={'value': 'Nombre', 'variable': 'Gravité'},
                               color_discrete_sequence=[COLORS['success'], COLORS['warning'], COLORS['danger']])
        fig_cause_grav.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig_cause_grav, use_container_width=True)
        
        # Causes par conditions météo
        if 'Conditions_Meteo' in df_filtre.columns:
            cross_meteo = pd.crosstab(df_filtre['Cause'], df_filtre['Conditions_Meteo'])
            fig_meteo = px.imshow(cross_meteo,
                                 title="Causes × Conditions météo",
                                 color_continuous_scale='YlOrRd')
            st.plotly_chart(fig_meteo, use_container_width=True)

# TAB 5: ANALYSE DES USAGERS
with tab5:
    st.subheader("👥 Analyse des usagers de la route")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pyramide des âges
        bins = [18, 25, 35, 45, 55, 65, 80]
        labels = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
        df_filtre['Age_Groupe'] = pd.cut(df_filtre['Age_Conducteur'], bins=bins, labels=labels)
        
        age_sexe = df_filtre.groupby(['Age_Groupe', 'Sexe_Conducteur']).size().reset_index(name='Nombre')
        fig_age = px.bar(age_sexe, x='Nombre', y='Age_Groupe', color='Sexe_Conducteur',
                        title="Pyramide des âges des conducteurs",
                        color_discrete_map={'Homme': COLORS['primary'], 'Femme': COLORS['info']},
                        orientation='h',
                        barmode='group')
        st.plotly_chart(fig_age, use_container_width=True)
        
        # Profession
        prof_counts = df_filtre['Profession_Conducteur'].value_counts()
        fig_prof = px.pie(values=prof_counts.values, names=prof_counts.index,
                         title="Répartition par profession")
        st.plotly_chart(fig_prof, use_container_width=True)
    
    with col2:
        # Âge vs Gravité
        fig_age_grav = px.box(df_filtre, x='Gravite', y='Age_Conducteur',
                             title="Âge des conducteurs par gravité",
                             points=False,
                             color='Gravite',
                             color_discrete_map={
                                 'Dommages matériels': COLORS['success'],
                                 'Blessures corporelles': COLORS['warning'],
                                 'Mortels': COLORS['danger']
                             })
        st.plotly_chart(fig_age_grav, use_container_width=True)
        
        # Sexe vs Heure
        fig_sexe_heure = px.box(df_filtre, x='Sexe_Conducteur', y='Heure',
                               title="Heures d'accident par sexe",
                               points=False,
                               color='Sexe_Conducteur',
                               color_discrete_map={'Homme': COLORS['primary'], 'Femme': COLORS['info']})
        st.plotly_chart(fig_sexe_heure, use_container_width=True)

# TAB 6: ANALYSE DES VÉHICULES
with tab6:
    st.subheader("🚗 Analyse des véhicules impliqués")
    
    # Statistiques résumées
    st.markdown(f"""
    <div class="stat-card">
        <h4 style="margin-top: 0;">Distribution des véhicules impliqués</h4>
        <p><strong>Véhicule tourisme:</strong> {vehicule_tourisme:,} ({vehicule_tourisme/total_accidents*100:.1f}%)</p>
        <p><strong>Taxi:</strong> {taxi:,} ({taxi/total_accidents*100:.1f}%)</p>
        <p><strong>Véhicule utilitaire:</strong> {utilitaire:,} ({utilitaire/total_accidents*100:.1f}%)</p>
        <p><strong>Moto:</strong> {moto:,} ({moto/total_accidents*100:.1f}%)</p>
        <p><strong>Bus:</strong> {bus:,} ({bus/total_accidents*100:.1f}%)</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Types de véhicules avec distribution
        veh_counts = df_filtre['Type_Vehicule'].value_counts()
        veh_percentages = (veh_counts / len(df_filtre) * 100).round(1)
        
        fig_veh_det = go.Figure(data=[
            go.Bar(
                x=veh_counts.index,
                y=veh_counts.values,
                text=[f"{p}%" for p in veh_percentages.values],
                textposition='auto',
                marker_color=[COLORS['primary'], COLORS['taxi'], COLORS['utilitaire'], COLORS['moto'], COLORS['dark']]
            )
        ])
        
        fig_veh_det.update_layout(
            title="Distribution des véhicules impliqués",
            xaxis_title="Type de véhicule",
            yaxis_title="Nombre d'accidents",
            showlegend=False
        )
        st.plotly_chart(fig_veh_det, use_container_width=True)
        
        # Véhicules par heure
        fig_veh_heure = px.box(df_filtre, x='Type_Vehicule', y='Heure',
                              title="Heures d'accident par type de véhicule",
                              points=False)
        st.plotly_chart(fig_veh_heure, use_container_width=True)
    
    with col2:
        # Véhicules par gravité
        cross_veh_grav = pd.crosstab(df_filtre['Type_Vehicule'], df_filtre['Gravite'])
        fig_cross_veh = px.bar(cross_veh_grav, barmode='group',
                              title="Véhicules × Gravité",
                              labels={'value': 'Nombre', 'variable': 'Gravité'},
                              color_discrete_sequence=[COLORS['success'], COLORS['warning'], COLORS['danger']])
        st.plotly_chart(fig_cross_veh, use_container_width=True)
        
        # Véhicules vs Causes
        cross_veh_cause = pd.crosstab(df_filtre['Type_Vehicule'], df_filtre['Cause'])
        fig_veh_cause = px.imshow(cross_veh_cause,
                                 title="Véhicules × Causes",
                                 color_continuous_scale='YlGnBu')
        st.plotly_chart(fig_veh_cause, use_container_width=True)

# TAB 7: ANALYSES CROISÉES
with tab7:
    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
    st.subheader("🔬 Analyses croisées avancées")
    st.markdown("Sélectionnez des variables pour créer des analyses croisées personnalisées.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sélection des variables pour analyses croisées
    col_sel1, col_sel2, col_sel3 = st.columns(3)
    
    with col_sel1:
        var_x = st.selectbox(
            "Variable X (axe horizontal)",
            ['Heure', 'Age_Conducteur', 'Annee', 'Mois', 'Type_Vehicule', 'Cause', 'Sexe_Conducteur'],
            index=0,
            key='var_x'
        )
    
    with col_sel2:
        var_y = st.selectbox(
            "Variable Y (axe vertical)",
            ['Age_Conducteur', 'Heure', 'Annee', 'Mois', 'Type_Vehicule', 'Cause'],
            index=1,
            key='var_y'
        )
    
    with col_sel3:
        var_color = st.selectbox(
            "Variable couleur",
            ['Gravite', 'Sexe_Conducteur', 'Type_Vehicule', 'Cause', 'Conditions_Meteo', 'Jour_Semaine'],
            index=0,
            key='var_color'
        )
    
    # Graphique d'analyse croisée 1: Scatter plot
    if var_x != var_y:
        fig_scatter = px.scatter(
            df_filtre,
            x=var_x,
            y=var_y,
            color=var_color,
            title=f"Nuage de points: {var_x} vs {var_y}",
            opacity=0.7,
            hover_data=['Rue', 'Gravite'],
            color_discrete_map={
                'Dommages matériels': COLORS['success'],
                'Blessures corporelles': COLORS['warning'],
                'Mortels': COLORS['danger'],
                'Homme': COLORS['primary'],
                'Femme': COLORS['info']
            }
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Analyses croisées additionnelles
    col_cross1, col_cross2 = st.columns(2)
    
    with col_cross1:
        st.markdown('<div class="sub-section">', unsafe_allow_html=True)
        st.markdown("**Analyse 1: Heatmap croisée**")
        cross_var1 = st.selectbox(
            "Variable 1",
            ['Rue', 'Type_Vehicule', 'Cause', 'Profession_Conducteur', 'Sexe_Conducteur', 'Jour_Semaine'],
            index=0,
            key='cross1'
        )
        cross_var2 = st.selectbox(
            "Variable 2",
            ['Gravite', 'Heure', 'Age_Conducteur', 'Type_Vehicule', 'Cause', 'Conditions_Meteo'],
            index=0,
            key='cross2'
        )
        
        if cross_var1 != cross_var2:
            cross_data = pd.crosstab(df_filtre[cross_var1], df_filtre[cross_var2])
            fig_cross = px.imshow(
                cross_data,
                title=f"Heatmap: {cross_var1} × {cross_var2}",
                color_continuous_scale='Viridis',
                aspect="auto"
            )
            st.plotly_chart(fig_cross, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_cross2:
        st.markdown('<div class="sub-section">', unsafe_allow_html=True)
        st.markdown("**Analyse 2: Distribution conditionnelle**")
        condition_var = st.selectbox(
            "Variable condition",
            ['Gravite', 'Sexe_Conducteur', 'Type_Vehicule', 'Cause'],
            index=0,
            key='condition'
        )
        dist_var = st.selectbox(
            "Variable à analyser",
            ['Heure', 'Age_Conducteur', 'Annee', 'Mois'],
            index=0,
            key='dist'
        )
        
        fig_dist = px.box(
            df_filtre,
            x=condition_var,
            y=dist_var,
            title=f"Distribution de {dist_var} par {condition_var}",
            points=False,
            color=condition_var,
            color_discrete_map={
                'Dommages matériels': COLORS['success'],
                'Blessures corporelles': COLORS['warning'],
                'Mortels': COLORS['danger'],
                'Homme': COLORS['primary'],
                'Femme': COLORS['info']
            }
        )
        st.plotly_chart(fig_dist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Matrice de corrélation pour variables numériques
    st.markdown('<div class="tab-section">', unsafe_allow_html=True)
    st.markdown("**Matrice de corrélation**")
    
    # Sélection des variables numériques
    numeric_cols = df_filtre.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) > 1:
        corr_matrix = df_filtre[numeric_cols].corr()
        fig_corr = px.imshow(
            corr_matrix,
            title="Matrice de corrélation des variables numériques",
            color_continuous_scale='RdBu',
            aspect="auto",
            zmin=-1,
            zmax=1
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("Pas suffisamment de variables numériques pour la matrice de corrélation.")
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 8: DONNÉES BRUTES
with tab8:
    st.subheader("📋 Données brutes")
    
    # Options d'affichage
    col_view1, col_view2, col_view3 = st.columns(3)
    with col_view1:
        items_per_page = st.selectbox("Lignes par page", [10, 25, 50, 100], index=0, key='items_page')
    with col_view2:
        sort_column = st.selectbox("Trier par", df_filtre.columns.tolist(), index=0, key='sort_col')
    with col_view3:
        sort_order = st.radio("Ordre", ["Croissant", "Décroissant"], horizontal=True, key='sort_order')
    
    # Tri des données
    df_sorted = df_filtre.sort_values(by=sort_column, ascending=(sort_order == "Croissant"))
    
    # Pagination
    total_pages = max(1, len(df_sorted) // items_per_page + (1 if len(df_sorted) % items_per_page > 0 else 0))
    page_number = st.number_input("Page", min_value=1, max_value=total_pages, value=1, key='page_num')
    
    start_idx = (page_number - 1) * items_per_page
    end_idx = start_idx + items_per_page
    df_page = df_sorted.iloc[start_idx:end_idx]
    
    # Affichage du tableau
    st.markdown(f"**Page {page_number} sur {total_pages} • {len(df_filtre)} lignes au total**")
    st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
    st.dataframe(df_page, use_container_width=True, height=400)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Statistiques descriptives
    with st.expander("📊 Statistiques descriptives", expanded=False):
        st.dataframe(df_filtre.describe(), use_container_width=True)
    
    # Résumé des données
    with st.expander("📝 Résumé des données", expanded=False):
        st.markdown(f"""
        - **Total des accidents**: {len(df_filtre):,}
        - **Période couverte**: {df_filtre['Annee'].min()} - {df_filtre['Annee'].max()}
        - **Variables disponibles**: {len(df_filtre.columns)}
        - **Plage horaire**: {df_filtre['Heure'].min()}h - {df_filtre['Heure'].max()}h
        - **Âge moyen des conducteurs**: {df_filtre['Age_Conducteur'].mean():.1f} ans
        """)

# =====================================================
# SECTION D'EXPORT
# =====================================================
st.markdown("---")
st.markdown('<div class="export-section">', unsafe_allow_html=True)
st.markdown("### 📤 Export des Analyses")

# Préparer les données pour l'export
filters_text = []
if annee_min != 2020 or annee_max != 2024:
    filters_text.append(f"Années: {annee_min}-{annee_max}")
if set(gravite_filtre) != set(df['Gravite'].unique()):
    filters_text.append(f"Gravité: {', '.join(gravite_filtre)}")
if rue_filtre:
    filters_text.append(f"Rues: {', '.join(rue_filtre[:3])}{'...' if len(rue_filtre) > 3 else ''}")
if heure_range != (14, 22):
    filters_text.append(f"Heures: {heure_range[0]}-{heure_range[1]}h")

kpis_for_export = kpis_horizontal + [
    {'label': 'Hommes', 'value': f"{hommes:,}", 'color': COLORS['primary']},
    {'label': 'Femmes', 'value': f"{femmes:,}", 'color': COLORS['info']}
]

st.markdown("Téléchargez les analyses dans différents formats:")

# Boutons d'export
col_dl1, col_dl2, col_dl3, col_dl4 = st.columns(4)

with col_dl1:
    # CSV
    csv = df_filtre.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Données CSV",
        data=csv,
        file_name=f"accidents_cesr_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        help="Télécharger les données filtrées au format CSV",
        use_container_width=True
    )

with col_dl2:
    # Excel
    @st.cache_data
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Accidents')
            
            # Ajouter un sheet avec les statistiques
            stats_df = pd.DataFrame({
                'Indicateur': ['Total accidents', 'Dommages matériels', 'Blessures corporelles', 
                              'Accidents mortels', 'Taux mortalité', 'Hommes', 'Femmes',
                              'Véhicule tourisme', 'Taxi', 'Véhicule utilitaire', 'Moto', 'Bus'],
                'Valeur': [total_accidents, materiels, corporels, mortels, taux_mortalite,
                          hommes, femmes, vehicule_tourisme, taxi, utilitaire, moto, bus]
            })
            stats_df.to_excel(writer, index=False, sheet_name='Statistiques')
            
            # Ajouter un sheet avec les filtres
            if filters_text:
                filters_df = pd.DataFrame({'Filtres appliqués': filters_text})
                filters_df.to_excel(writer, index=False, sheet_name='Filtres')
        
        return output.getvalue()
    
    excel_data = to_excel(df_filtre)
    
    st.download_button(
        label="📊 Rapport Excel",
        data=excel_data,
        file_name=f"rapport_cesr_{pd.Timestamp.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        help="Télécharger le rapport complet au format Excel",
        use_container_width=True
    )

with col_dl3:
    # HTML Report
    html_data = create_html_report(df_filtre, kpis_for_export, filters_text)
    st.download_button(
        label="🌐 Rapport HTML",
        data=html_data,
        file_name=f"rapport_cesr_{pd.Timestamp.now().strftime('%Y%m%d')}.html",
        mime="text/html",
        help="Télécharger le rapport au format HTML (ouvrable dans tout navigateur)",
        use_container_width=True
    )

with col_dl4:
    # TXT Report
    txt_data = create_text_report(df_filtre, kpis_for_export, filters_text)
    st.download_button(
        label="📄 Rapport Texte",
        data=txt_data,
        file_name=f"rapport_cesr_{pd.Timestamp.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
        help="Télécharger le rapport au format texte simple",
        use_container_width=True
    )

st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align:center; color:{COLORS['light']}; font-family: 'Segoe UI'; padding:1rem 0;">
    <strong>CESR - Cabinet d'Expertise Sécurité Routière</strong><br>
    Yaoundé, Cameroun • Dashboard analytique 2025<br>
    <small style="font-size: 0.8rem;">
        Système d'analyse prédictive et cartographique • 
        <a href="mailto:cabinetesr01@gmail.com" style="color: {COLORS['primary']}; text-decoration: none;">cabinetesr01@gmail.com</a> •
        Données mises à jour quotidiennement
    </small>
</div>
""", unsafe_allow_html=True)