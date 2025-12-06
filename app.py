import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
import json
import time
import folium
from streamlit_folium import folium_static, st_folium
import hashlib
import base64
from io import BytesIO
from PIL import Image
import requests
import io
import math
from geopy.distance import geodesic
import random

# Configuration de la page
st.set_page_config(
    page_title="SafeDriveCam Cameroun - Sécurité Routière",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Régions du Cameroun
REGIONS_CAMEROUN = [
    "Adamaoua", "Centre", "Est", "Extrême-Nord", "Littoral",
    "Nord", "Ouest", "Sud", "Sud-Ouest", "Nord-Ouest"
]

# Villes principales par région
VILLES_CAMEROUN = {
    "Adamaoua": ["Ngaoundéré", "Tibati", "Banyo"],
    "Centre": ["Yaoundé", "Mbalmayo", "Obala", "Monatélé", "Nanga-Eboko"],
    "Est": ["Bertoua", "Batouri", "Abong-Mbang", "Yokadouma"],
    "Extrême-Nord": ["Maroua", "Kousséri", "Mokolo", "Yagoua"],
    "Littoral": ["Douala", "Nkongsamba", "Edéa", "Loum", "Manjo"],
    "Nord": ["Garoua", "Guider", "Poli", "Rey Bouba"],
    "Ouest": ["Bafoussam", "Bamenda", "Dschang", "Foumban", "Mbouda"],
    "Sud": ["Ebolowa", "Kribi", "Sangmélima", "Ambam"],
    "Sud-Ouest": ["Buea", "Limbe", "Kumba", "Mamfe", "Tiko"],
    "Nord-Ouest": ["Bamenda", "Ndop", "Wum", "Kumbo", "Nkambe"]
}

# Coordonnées des villes principales
COORDONNEES_VILLES = {
    "Yaoundé": {"lat": 3.8480, "lng": 11.5021},
    "Douala": {"lat": 4.0511, "lng": 9.7679},
    "Bafoussam": {"lat": 5.4775, "lng": 10.4176},
    "Bamenda": {"lat": 5.9631, "lng": 10.1591},
    "Garoua": {"lat": 9.3077, "lng": 13.3937},
    "Maroua": {"lat": 10.5912, "lng": 14.3159},
    "Ngaoundéré": {"lat": 7.3275, "lng": 13.5837},
    "Bertoua": {"lat": 4.5776, "lng": 13.6806},
    "Ebolowa": {"lat": 2.9167, "lng": 11.1500},
    "Buea": {"lat": 4.1534, "lng": 9.2423},
    "Kumba": {"lat": 4.6415, "lng": 9.4387},
    "Limbe": {"lat": 4.0167, "lng": 9.2167},
    "Dschang": {"lat": 5.4439, "lng": 10.0558},
    "Foumban": {"lat": 5.7167, "lng": 10.9167},
    "Kribi": {"lat": 2.9375, "lng": 9.9077},
    "Sangmélima": {"lat": 2.9333, "lng": 11.9833},
    "Edéa": {"lat": 3.8000, "lng": 10.1333},
    "Mbalmayo": {"lat": 3.5167, "lng": 11.5000},
    "Obala": {"lat": 4.1667, "lng": 11.5333},
    "Batouri": {"lat": 4.4333, "lng": 14.3667},
    "Kousséri": {"lat": 12.0833, "lng": 15.0333},
    "Mokolo": {"lat": 10.7411, "lng": 13.8022},
    "Yagoua": {"lat": 10.3411, "lng": 15.2372},
    "Guider": {"lat": 9.9333, "lng": 13.9500},
    "Poli": {"lat": 8.4833, "lng": 13.2500},
    "Abong-Mbang": {"lat": 3.9833, "lng": 13.1833},
    "Yokadouma": {"lat": 3.5167, "lng": 15.0500},
    "Nkongsamba": {"lat": 4.9667, "lng": 9.9333},
    "Loum": {"lat": 4.7167, "lng": 9.7333},
    "Manjo": {"lat": 4.8500, "lng": 9.8167},
    "Rey Bouba": {"lat": 8.6667, "lng": 14.1833},
    "Mbouda": {"lat": 5.6333, "lng": 10.2500},
    "Monatélé": {"lat": 4.3167, "lng": 11.1500},
    "Nanga-Eboko": {"lat": 4.6833, "lng": 12.3667},
    "Ambam": {"lat": 2.3833, "lng": 11.2833},
    "Mamfe": {"lat": 5.7667, "lng": 9.2833},
    "Tiko": {"lat": 4.0750, "lng": 9.3600},
    "Ndop": {"lat": 6.0667, "lng": 10.4833},
    "Wum": {"lat": 6.3833, "lng": 10.0667},
    "Kumbo": {"lat": 6.2000, "lng": 10.6667},
    "Nkambe": {"lat": 6.2333, "lng": 10.9833},
    "Banyo": {"lat": 6.7500, "lng": 11.8167},
    "Tibati": {"lat": 6.4667, "lng": 12.6333}
}

# Routes nationales principales
ROUTES_NATIONALES = {
    "RN1": "Yaoundé - Douala",
    "RN2": "Yaoundé - Mbalmayo - Ebolowa",
    "RN3": "Yaoundé - Bafoussam - Bamenda",
    "RN4": "Douala - Bafoussam",
    "RN5": "Douala - Kumba - Mamfe",
    "RN6": "Yaoundé - Bertoua - Garoua - Maroua",
    "RN7": "Bafoussam - Foumban",
    "RN8": "Buea - Kumba",
    "RN9": "Douala - Edéa - Kribi",
    "RN10": "Bafoussam - Mbouda",
    "RN11": "Bertoua - Batouri",
    "RN12": "Maroua - Kousséri"
}

# Initialisation de la session
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "connexion"
if 'position_actuelle' not in st.session_state:
    st.session_state.position_actuelle = {"lat": 3.8480, "lng": 11.5021, "ville": "Yaoundé"}
if 'destination' not in st.session_state:
    st.session_state.destination = None
if 'itineraire_choisi' not in st.session_state:
    st.session_state.itineraire_choisi = None

# Base de données
def init_db():
    conn = sqlite3.connect('safedrivecam_cm.db')
    cursor = conn.cursor()
    
    # Table des utilisateurs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT,
        email TEXT,
        role TEXT,
        nom_complet TEXT,
        telephone TEXT,
        region TEXT,
        ville TEXT,
        points INTEGER DEFAULT 0,
        niveau TEXT DEFAULT 'débutant',
        date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Table des accidents
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude REAL,
        longitude REAL,
        region TEXT,
        ville TEXT,
        route TEXT,
        type_accident TEXT,
        gravite TEXT,
        nb_vehicules INTEGER,
        nb_victimes INTEGER,
        description TEXT,
        photos TEXT,
        audio_note TEXT,
        declare_par INTEGER,
        statut TEXT DEFAULT 'signalé',
        date_signalement TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Table des obstacles
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS obstacles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude REAL,
        longitude REAL,
        region TEXT,
        ville TEXT,
        route TEXT,
        type_obstacle TEXT,
        description TEXT,
        photo_url TEXT,
        audio_note TEXT,
        declare_par INTEGER,
        confirmations INTEGER DEFAULT 0,
        score_confiance REAL DEFAULT 0.0,
        date_signalement TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Table des comportements
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comportements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude REAL,
        longitude REAL,
        region TEXT,
        ville TEXT,
        route TEXT,
        type_comportement TEXT,
        description TEXT,
        plaque_immatriculation TEXT,
        declare_par INTEGER,
        anonyme BOOLEAN DEFAULT 1,
        points_gagnes INTEGER DEFAULT 10,
        date_signalement TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Table des conditions météo
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS meteo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        region TEXT,
        ville TEXT,
        temperature REAL,
        conditions TEXT,
        visibilite TEXT,
        precipitation REAL,
        vent_vitesse REAL,
        date_mise_a_jour TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Table des hôpitaux
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hopitaux (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        region TEXT,
        ville TEXT,
        latitude REAL,
        longitude REAL,
        telephone TEXT,
        services TEXT,
        lits_disponibles INTEGER,
        date_mise_a_jour TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Données initiales
    cursor.execute("SELECT COUNT(*) FROM hopitaux")
    if cursor.fetchone()[0] == 0:
        hopitaux_initiaux = [
            ("Hôpital Central Yaoundé", "Centre", "Yaoundé", 3.8686, 11.5117, "+237 222 22 22 22", "Urgences, Chirurgie, Maternité", 120),
            ("Hôpital Laquintinie", "Littoral", "Douala", 4.0566, 9.6981, "+237 233 44 22 11", "Urgences, Cardiologie, Pédiatrie", 180),
            ("Hôpital Régional Bafoussam", "Ouest", "Bafoussam", 5.4778, 10.4189, "+237 233 46 12 34", "Urgences, Traumatologie", 80),
            ("Hôpital Régional Garoua", "Nord", "Garoua", 9.3000, 13.4000, "+237 222 27 20 20", "Urgences, Médecine générale", 60),
            ("Hôpital Régional Maroua", "Extrême-Nord", "Maroua", 10.5914, 14.3161, "+237 222 29 30 30", "Urgences, Maternité", 70),
        ]
        for hopital in hopitaux_initiaux:
            cursor.execute('''
                INSERT INTO hopitaux (nom, region, ville, latitude, longitude, telephone, services, lits_disponibles)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', hopital)
    
    conn.commit()
    conn.close()

# Initialisation
init_db()

# Fonctions utilitaires
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def calculer_distance(lat1, lng1, lat2, lng2):
    """Calcule la distance en km entre deux points GPS"""
    point1 = (lat1, lng1)
    point2 = (lat2, lng2)
    return geodesic(point1, point2).kilometers

def obtenir_meteo_ville(ville):
    """Obtenir les conditions météo pour une ville (simulation)"""
    conditions_possibles = ["Ensoleillé", "Partiellement nuageux", "Nuageux", "Pluie légère", 
                           "Pluie forte", "Orage", "Brouillard", "Venteux"]
    return {
        "temperature": random.uniform(20, 35),
        "conditions": random.choice(conditions_possibles),
        "visibilite": random.choice(["Bonne", "Moyenne", "Réduite"]),
        "precipitation": random.uniform(0, 100),
        "vent_vitesse": random.uniform(0, 30)
    }

def trouver_hopitaux_proches(lat, lng, rayon_km=20):
    """Trouve les hôpitaux dans un rayon donné"""
    conn = sqlite3.connect('safedrivecam_cm.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hopitaux")
    hopitaux = cursor.fetchall()
    conn.close()
    
    hopitaux_proches = []
    for hopital in hopitaux:
        distance = calculer_distance(lat, lng, hopital[4], hopital[5])
        if distance <= rayon_km:
            hopitaux_proches.append({
                "id": hopital[0],
                "nom": hopital[1],
                "distance": distance,
                "telephone": hopital[6],
                "lits": hopital[8]
            })
    
    return sorted(hopitaux_proches, key=lambda x: x["distance"])[:3]

# Page de connexion avec régions du Cameroun
def login_page():
    st.title("🔐 Connexion SafeDriveCam Cameroun")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.subheader("Identifiez-vous")
            
            login_type = st.radio(
                "Type de connexion",
                ["👤 Utilisateur", "👮 Autorités", "🏛️ Service Central"]
            )
            
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe", type="password")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("Se connecter", use_container_width=True):
                    if username and password:
                        conn = sqlite3.connect('safedrivecam_cm.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            "SELECT id, password_hash, role FROM users WHERE username = ?",
                            (username,)
                        )
                        user = cursor.fetchone()
                        conn.close()
                        
                        if user and verify_password(password, user[1]):
                            st.session_state.user_id = user[0]
                            st.session_state.user_role = user[2]
                            st.session_state.current_page = "dashboard"
                            st.success(f"Connecté en tant que {user[2]}")
                            st.rerun()
                        else:
                            st.error("Identifiants incorrects")
                    else:
                        st.warning("Veuillez remplir tous les champs")
            
            with col_btn2:
                if st.button("S'inscrire", use_container_width=True):
                    st.session_state.current_page = "inscription"
                    st.rerun()
            
            st.divider()
            
            # Connexion rapide démo
            st.caption("Accès démo rapide:")
            col_demo1, col_demo2, col_demo3 = st.columns(3)
            with col_demo1:
                if st.button("Utilisateur", use_container_width=True):
                    st.session_state.user_role = "utilisateur"
                    st.session_state.current_page = "dashboard"
                    st.rerun()
            with col_demo2:
                if st.button("Autorités", use_container_width=True):
                    st.session_state.user_role = "autorite"
                    st.session_state.current_page = "dashboard"
                    st.rerun()
            with col_demo3:
                if st.button("Admin", use_container_width=True):
                    st.session_state.user_role = "admin"
                    st.session_state.current_page = "dashboard"
                    st.rerun()

def register_page():
    st.title("📝 Inscription")
    
    with st.form("form_inscription"):
        role = st.selectbox(
            "Rôle",
            ["utilisateur", "autorite", "admin"],
            format_func=lambda x: {
                "utilisateur": "👤 Utilisateur",
                "autorite": "👮 Autorités",
                "admin": "🏛️ Service Central"
            }[x]
        )
        
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            username = st.text_input("Nom d'utilisateur*")
            email = st.text_input("Email*")
            nom_complet = st.text_input("Nom complet*")
        with col_info2:
            telephone = st.text_input("Téléphone")
            region = st.selectbox("Région*", REGIONS_CAMEROUN)
            ville = st.selectbox("Ville*", VILLES_CAMEROUN.get(region, ["Yaoundé"]))
        
        password = st.text_input("Mot de passe*", type="password")
        password_confirm = st.text_input("Confirmer le mot de passe*", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("S'inscrire", use_container_width=True)
        with col2:
            if st.form_submit_button("Annuler", use_container_width=True):
                st.session_state.current_page = "connexion"
                st.rerun()
        
        if submit:
            if password != password_confirm:
                st.error("Les mots de passe ne correspondent pas")
            elif username and email and password and nom_complet and region:
                conn = sqlite3.connect('safedrivecam_cm.db')
                cursor = conn.cursor()
                try:
                    cursor.execute('''
                        INSERT INTO users 
                        (username, password_hash, email, role, nom_complet, telephone, region, ville)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        username,
                        hash_password(password),
                        email,
                        role,
                        nom_complet,
                        telephone,
                        region,
                        ville
                    ))
                    conn.commit()
                    st.success("Inscription réussie! Vous pouvez vous connecter.")
                    time.sleep(2)
                    st.session_state.current_page = "connexion"
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("Ce nom d'utilisateur existe déjà")
                finally:
                    conn.close()

# INTERFACE UTILISATEUR AMÉLIORÉE
def user_interface():
    st.sidebar.title(f"👤 {st.session_state.get('username', 'Utilisateur')}")
    
    menu = st.sidebar.selectbox(
        "Navigation",
        ["🏠 Tableau de bord", "🚨 Signaler", "🗺️ Itinéraire intelligent", "📱 Notifications", "🏆 Récompenses", "⚙️ Profil"]
    )
    
    if menu == "🏠 Tableau de bord":
        st.title("🏠 Tableau de bord - SafeDriveCam Cameroun")
        
        # Sélection de la région
        region_utilisateur = st.selectbox("📍 Sélectionnez votre région", REGIONS_CAMEROUN)
        ville_utilisateur = st.selectbox("🏙️ Sélectionnez votre ville", VILLES_CAMEROUN.get(region_utilisateur, ["Yaoundé"]))
        
        # Mettre à jour la position
        if ville_utilisateur in COORDONNEES_VILLES:
            st.session_state.position_actuelle = {
                "lat": COORDONNEES_VILLES[ville_utilisateur]["lat"],
                "lng": COORDONNEES_VILLES[ville_utilisateur]["lng"],
                "ville": ville_utilisateur
            }
        
        # Métriques rapides
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Mes points", "1250", "+150")
        with col2:
            st.metric("Signalements", "24", "+3")
        with col3:
            st.metric("Badges", "8", "+1")
        with col4:
            st.metric("Niveau", "Expert", "↗️")
        
        # Carte des dangers proches
        st.subheader("🗺️ Dangers à proximité de " + ville_utilisateur)
        
        # Créer la carte centrée sur la ville
        m = folium.Map(
            location=[
                st.session_state.position_actuelle["lat"], 
                st.session_state.position_actuelle["lng"]
            ], 
            zoom_start=12
        )
        
        # Ajouter le marqueur de position actuelle
        folium.Marker(
            [st.session_state.position_actuelle["lat"], st.session_state.position_actuelle["lng"]],
            popup=f"Vous êtes ici: {ville_utilisateur}",
            icon=folium.Icon(color="blue", icon="user", prefix="fa")
        ).add_to(m)
        
        # Ajouter des dangers simulés dans un rayon de 10km
        for i in range(8):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0.5, 10)  # km
            lat_offset = distance * math.cos(angle) / 111.32
            lng_offset = distance * math.sin(angle) / (111.32 * math.cos(st.session_state.position_actuelle["lat"] * math.pi / 180))
            
            danger_lat = st.session_state.position_actuelle["lat"] + lat_offset
            danger_lng = st.session_state.position_actuelle["lng"] + lng_offset
            
            danger_type = random.choice(["accident", "obstacle", "travaux"])
            couleur = "red" if danger_type == "accident" else "orange" if danger_type == "obstacle" else "yellow"
            
            folium.CircleMarker(
                [danger_lat, danger_lng],
                radius=8,
                popup=f"{danger_type.title()} à {distance:.1f}km",
                color=couleur,
                fill=True,
                fill_opacity=0.6
            ).add_to(m)
        
        # Ajouter un cercle de 10km
        folium.Circle(
            [st.session_state.position_actuelle["lat"], st.session_state.position_actuelle["lng"]],
            radius=10000,  # 10km en mètres
            popup="Rayon de 10km pour les notifications",
            color="blue",
            fill=False
        ).add_to(m)
        
        # Afficher la carte
        folium_static(m, width=1000, height=400)
        
        # Météo locale
        st.subheader("🌤️ Météo actuelle à " + ville_utilisateur)
        
        meteo = obtenir_meteo_ville(ville_utilisateur)
        col_met1, col_met2, col_met3, col_met4 = st.columns(4)
        with col_met1:
            st.metric("Température", f"{meteo['temperature']:.1f}°C")
        with col_met2:
            st.metric("Conditions", meteo['conditions'])
        with col_met3:
            st.metric("Visibilité", meteo['visibilite'])
        with col_met4:
            st.metric("Vent", f"{meteo['vent_vitesse']:.1f} km/h")
    
    elif menu == "🚨 Signaler":
        st.title("🚨 Signaler un incident")
        
        tab1, tab2, tab3 = st.tabs(["Accident", "Obstacle", "Comportement"])
        
        with tab1:
            with st.form("form_accident"):
                st.subheader("Signaler un accident")
                
                # Localisation automatique ou manuelle
                col_loc_type, col_gps = st.columns([2, 1])
                with col_loc_type:
                    localisation_type = st.radio(
                        "Localisation",
                        ["Utiliser ma position GPS", "Saisir manuellement"]
                    )
                
                if localisation_type == "Saisir manuellement":
                    col_region, col_ville = st.columns(2)
                    with col_region:
                        region = st.selectbox("Région", REGIONS_CAMEROUN)
                    with col_ville:
                        ville = st.selectbox("Ville", VILLES_CAMEROUN.get(region, ["Yaoundé"]))
                    
                    if ville in COORDONNEES_VILLES:
                        latitude = COORDONNEES_VILLES[ville]["lat"]
                        longitude = COORDONNEES_VILLES[ville]["lng"]
                    else:
                        col_lat, col_lng = st.columns(2)
                        with col_lat:
                            latitude = st.number_input("Latitude", value=3.8480, format="%.6f")
                        with col_lng:
                            longitude = st.number_input("Longitude", value=11.5021, format="%.6f")
                else:
                    # Utiliser la position GPS de la session
                    latitude = st.session_state.position_actuelle["lat"]
                    longitude = st.session_state.position_actuelle["lng"]
                    st.info(f"Position GPS: {latitude:.6f}, {longitude:.6f}")
                
                col_details1, col_details2 = st.columns(2)
                with col_details1:
                    type_accident = st.selectbox(
                        "Type d'accident",
                        ["Collision frontale", "Collision arrière", "Sortie de route", 
                         "Accident avec piéton", "Multi-véhicules", "Autre"]
                    )
                    nb_vehicules = st.number_input("Nombre de véhicules", 1, 20, 1)
                with col_details2:
                    gravite = st.select_slider(
                        "Gravité",
                        ["Léger", "Moyen", "Grave", "Très grave", "Catastrophique"]
                    )
                    nb_victimes = st.number_input("Nombre de victimes", 0, 50, 0)
                
                route = st.selectbox("Route concernée", list(ROUTES_NATIONALES.keys()))
                description = st.text_area("Description détaillée", placeholder="Décrivez l'accident...")
                
                # Média
                st.subheader("📸 Preuves multimédias")
                col_media1, col_media2 = st.columns(2)
                with col_media1:
                    photos = st.file_uploader("Photos", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)
                with col_media2:
                    audio = st.file_uploader("Note audio", type=['mp3', 'wav', 'm4a'])
                
                # Notification des secours
                if nb_victimes > 0:
                    st.warning("⚠️ Victimes détectées - Notification automatique aux services d'urgence")
                    
                    # Trouver les hôpitaux proches
                    hopitaux_proches = trouver_hopitaux_proches(latitude, longitude, 20)
                    if hopitaux_proches:
                        st.info("🏥 Hôpitaux les plus proches:")
                        for hopital in hopitaux_proches:
                            st.write(f"- {hopital['nom']} ({hopital['distance']:.1f}km) - 📞 {hopital['telephone']}")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    submit = st.form_submit_button("🚨 Signaler aux secours", use_container_width=True)
                with col_btn2:
                    if st.form_submit_button("💾 Enregistrer", use_container_width=True):
                        st.info("Signalement enregistré localement")
                
                if submit:
                    # Simuler l'envoi aux services d'urgence
                    services = ["Police", "SAMU", "Pompiers"]
                    if nb_victimes > 0:
                        services.append("Services médicaux d'urgence")
                    
                    st.success(f"""
                    ✅ Accident signalé aux secours!
                    
                    **Services notifiés:** {', '.join(services)}
                    **Localisation:** {latitude:.6f}, {longitude:.6f}
                    **Route:** {route}
                    **Gravité:** {gravite}
                    **Victimes:** {nb_victimes}
                    
                    Les usagers dans un rayon de 10km seront notifiés.
                    """)
        
        with tab2:
            with st.form("form_obstacle"):
                st.subheader("Signaler un obstacle")
                
                type_obstacle = st.selectbox(
                    "Type d'obstacle",
                    ["Nid-de-poule", "Travaux routiers", "Arbre tombé", "Animal sur route",
                     "Déchet dangereux", "Éclairage défaillant", "Glissement de terrain", "Autre"]
                )
                
                description = st.text_area("Description de l'obstacle")
                
                # Localisation
                col_region, col_ville = st.columns(2)
                with col_region:
                    region = st.selectbox("Région de l'obstacle", REGIONS_CAMEROUN)
                with col_ville:
                    ville = st.selectbox("Ville", VILLES_CAMEROUN.get(region, ["Yaoundé"]))
                
                if ville in COORDONNEES_VILLES:
                    latitude = COORDONNEES_VILLES[ville]["lat"]
                    longitude = COORDONNEES_VILLES[ville]["lng"]
                else:
                    col_lat, col_lng = st.columns(2)
                    with col_lat:
                        latitude = st.number_input("Latitude obstacle", value=3.8480, format="%.6f")
                    with col_lng:
                        longitude = st.number_input("Longitude obstacle", value=11.5021, format="%.6f")
                
                route = st.selectbox("Route concernée", list(ROUTES_NATIONALES.keys()))
                
                # Photo
                photo = st.file_uploader("Prendre une photo de l'obstacle", type=['jpg', 'png'])
                
                if st.form_submit_button("⚠️ Signaler l'obstacle", use_container_width=True):
                    # Enregistrement dans la base de données
                    conn = sqlite3.connect('safedrivecam_cm.db')
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO obstacles 
                        (latitude, longitude, region, ville, route, type_obstacle, description, declare_par)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (latitude, longitude, region, ville, route, type_obstacle, description, st.session_state.user_id))
                    conn.commit()
                    conn.close()
                    
                    st.success(f"""
                    ✅ Obstacle '{type_obstacle}' signalé!
                    
                    **Localisation:** {ville}, {region}
                    **Route:** {route}
                    
                    Les utilisateurs à moins de 10km seront notifiés automatiquement.
                    """)
        
        with tab3:
            with st.form("form_comportement"):
                st.subheader("Signaler un comportement dangereux")
                
                type_comportement = st.selectbox(
                    "Type de comportement",
                    ["Excès de vitesse", "Conduite agressive", "Téléphone au volant", 
                     "État d'ébriété suspect", "Non-respect des feux", "Dépassement dangereux",
                     "Conduite sans permis", "Chargement dangereux", "Fatigue au volant"]
                )
                
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    plaque = st.text_input("Plaque d'immatriculation (optionnel)", 
                                          help="Ex: CE 1234 AB")
                with col_info2:
                    type_vehicule = st.selectbox(
                        "Type de véhicule",
                        ["Voiture", "Camion", "Moto", "Bus", "Taxi", "Autre"]
                    )
                
                # Localisation
                col_region, col_ville = st.columns(2)
                with col_region:
                    region = st.selectbox("Région du comportement", REGIONS_CAMEROUN)
                with col_ville:
                    ville = st.selectbox("Ville du comportement", VILLES_CAMEROUN.get(region, ["Yaoundé"]))
                
                description = st.text_area("Description détaillée du comportement")
                
                # Confidentialité et récompense
                anonyme = st.checkbox("Rester anonyme", value=True)
                points_gagnes = 15
                
                if st.form_submit_button("🚫 Signaler ce comportement", use_container_width=True):
                    # Enregistrement
                    conn = sqlite3.connect('safedrivecam_cm.db')
                    cursor = conn.cursor()
                    
                    # Ajouter le signalement
                    cursor.execute('''
                        INSERT INTO comportements 
                        (latitude, longitude, region, ville, type_comportement, description, 
                         plaque_immatriculation, declare_par, anonyme, points_gagnes)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        COORDONNEES_VILLES[ville]["lat"], COORDONNEES_VILLES[ville]["lng"],
                        region, ville, type_comportement, description,
                        plaque, st.session_state.user_id, anonyme, points_gagnes
                    ))
                    
                    # Mettre à jour les points utilisateur
                    cursor.execute('''
                        UPDATE users SET points = points + ? WHERE id = ?
                    ''', (points_gagnes, st.session_state.user_id))
                    
                    conn.commit()
                    conn.close()
                    
                    st.balloons()
                    st.success(f"""
                    ✅ Comportement signalé! 
                    
                    **Récompense:** +{points_gagnes} points
                    **Confidentialité:** {"Anonyme" if anonyme else "Identifié"}
                    **Région:** {region}
                    
                    Votre contribution améliore la sécurité routière au Cameroun!
                    """)
    
    elif menu == "🗺️ Itinéraire intelligent":
        st.title("🗺️ Itinéraire intelligent - Cameroun")
        
        # Section 1: Position actuelle
        st.subheader("📍 Ma position actuelle")
        
        col_gps1, col_gps2, col_gps3 = st.columns([2, 2, 1])
        with col_gps1:
            region_actuelle = st.selectbox(
                "Ma région",
                REGIONS_CAMEROUN,
                key="region_itineraire"
            )
        with col_gps2:
            ville_actuelle = st.selectbox(
                "Ma ville",
                VILLES_CAMEROUN.get(region_actuelle, ["Yaoundé"]),
                key="ville_itineraire"
            )
        with col_gps3:
            if st.button("📍 Utiliser GPS", use_container_width=True):
                if ville_actuelle in COORDONNEES_VILLES:
                    st.session_state.position_actuelle = {
                        "lat": COORDONNEES_VILLES[ville_actuelle]["lat"],
                        "lng": COORDONNEES_VILLES[ville_actuelle]["lng"],
                        "ville": ville_actuelle
                    }
                    st.success(f"Position mise à jour: {ville_actuelle}")
        
        # Afficher les coordonnées
        if ville_actuelle in COORDONNEES_VILLES:
            st.info(f"**Coordonnées GPS:** {COORDONNEES_VILLES[ville_actuelle]['lat']:.6f}, {COORDONNEES_VILLES[ville_actuelle]['lng']:.6f}")
        
        # Section 2: Choix de la destination sur la carte
        st.subheader("🎯 Choisir la destination sur la carte")
        
        # Créer une carte interactive du Cameroun
        m = folium.Map(location=[5.9631, 10.1591], zoom_start=7)
        
        # Ajouter les marqueurs pour les villes principales
        for ville, coords in COORDONNEES_VILLES.items():
            folium.Marker(
                [coords["lat"], coords["lng"]],
                popup=ville,
                icon=folium.Icon(color="green", icon="map-marker")
            ).add_to(m)
        
        # Ajouter le marqueur de position actuelle
        folium.Marker(
            [st.session_state.position_actuelle["lat"], st.session_state.position_actuelle["lng"]],
            popup=f"Départ: {st.session_state.position_actuelle['ville']}",
            icon=folium.Icon(color="blue", icon="user", prefix="fa")
        ).add_to(m)
        
        # Interface pour sélectionner la destination
        st.write("**Cliquez sur une ville de destination sur la carte:**")
        
        # Utiliser st_folium pour interagir avec la carte
        map_data = st_folium(m, width=1000, height=500, returned_objects=["last_clicked"])
        
        # Gérer la sélection de destination
        if map_data and map_data["last_clicked"]:
            lat_dest = map_data["last_clicked"]["lat"]
            lng_dest = map_data["last_clicked"]["lng"]
            
            # Trouver la ville la plus proche
            ville_destination = None
            distance_min = float('inf')
            
            for ville, coords in COORDONNEES_VILLES.items():
                distance = calculer_distance(lat_dest, lng_dest, coords["lat"], coords["lng"])
                if distance < distance_min and distance < 20:  # Dans un rayon de 20km
                    distance_min = distance
                    ville_destination = ville
            
            if ville_destination:
                st.session_state.destination = {
                    "lat": COORDONNEES_VILLES[ville_destination]["lat"],
                    "lng": COORDONNEES_VILLES[ville_destination]["lng"],
                    "ville": ville_destination
                }
                st.success(f"✅ Destination sélectionnée: {ville_destination}")
        
        # Section 3: Calcul d'itinéraire
        if st.session_state.destination:
            st.subheader("🚗 Calcul d'itinéraire")
            
            depart = st.session_state.position_actuelle
            arrivee = st.session_state.destination
            
            # Calculer la distance directe
            distance_directe = calculer_distance(
                depart["lat"], depart["lng"],
                arrivee["lat"], arrivee["lng"]
            )
            
            st.write(f"**Trajet:** {depart['ville']} → {arrivee['ville']}")
            st.write(f"**Distance à vol d'oiseau:** {distance_directe:.1f} km")
            
            # Options d'itinéraire
            with st.expander("⚙️ Options de sécurité"):
                col_opt1, col_opt2, col_opt3 = st.columns(3)
                with col_opt1:
                    éviter_accidents = st.checkbox("Éviter les zones à accidents", True)
                with col_opt2:
                    éviter_obstacles = st.checkbox("Éviter les obstacles signalés", True)
                with col_opt3:
                    éviter_controles = st.checkbox("Contourner les contrôles", False)
                
                alertes_meteo = st.checkbox("Prendre en compte la météo", True)
                priorite_securite = st.slider("Priorité sécurité vs temps", 1, 10, 7)
            
            if st.button("📍 Calculer les itinéraires", use_container_width=True):
                with st.spinner("Calcul des itinéraires en cours..."):
                    time.sleep(2)
                    
                    # Simuler 3 itinéraires différents
                    itineraires = []
                    
                    # Itinéraire 1: Le plus rapide
                    distance_rapide = distance_directe * random.uniform(1.1, 1.3)
                    duree_rapide = distance_rapide / random.uniform(60, 80) * 60  # minutes
                    itineraires.append({
                        "nom": "🚀 Le plus rapide",
                        "distance": distance_rapide,
                        "duree": duree_rapide,
                        "couleur": "green",
                        "description": "Priorité à la vitesse, routes principales",
                        "points_forts": ["Autoroutes", "Routes nationales", "Peu de péages"],
                        "points_faibles": ["Plus de circulation", "Prix péages élevé"],
                        "score_securite": random.randint(65, 75),
                        "alertes": random.randint(1, 3)
                    })
                    
                    # Itinéraire 2: Le plus sûr
                    distance_sur = distance_directe * random.uniform(1.3, 1.5)
                    duree_sur = distance_sur / random.uniform(50, 60) * 60
                    itineraires.append({
                        "nom": "🛡️ Le plus sûr",
                        "distance": distance_sur,
                        "duree": duree_sur,
                        "couleur": "blue",
                        "description": "Priorité à la sécurité, évite les zones à risques",
                        "points_forts": ["Moins d'accidents", "Routes sécurisées", "Éclairage bon"],
                        "points_faibles": ["Plus long", "Routes secondaires"],
                        "score_securite": random.randint(85, 95),
                        "alertes": random.randint(0, 1)
                    })
                    
                    # Itinéraire 3: Équilibré
                    distance_eq = distance_directe * random.uniform(1.2, 1.4)
                    duree_eq = distance_eq / random.uniform(55, 70) * 60
                    itineraires.append({
                        "nom": "⚖️ Équilibré",
                        "distance": distance_eq,
                        "duree": duree_eq,
                        "couleur": "orange",
                        "description": "Bon compromis temps/sécurité",
                        "points_forts": ["Bon rapport temps/sécurité", "Routes variées", "Péages modérés"],
                        "points_faibles": ["Quelques zones à risque"],
                        "score_securite": random.randint(75, 85),
                        "alertes": random.randint(1, 2)
                    })
                    
                    # Afficher les 3 itinéraires
                    st.subheader("🎯 3 itinéraires proposés")
                    
                    for idx, itineraire in enumerate(itineraires):
                        with st.container():
                            col_it1, col_it2, col_it3 = st.columns([4, 3, 2])
                            
                            with col_it1:
                                st.write(f"### {itineraire['nom']}")
                                st.write(itineraire['description'])
                                
                                col_pts1, col_pts2 = st.columns(2)
                                with col_pts1:
                                    st.write("**✅ Points forts:**")
                                    for point in itineraire['points_forts']:
                                        st.write(f"- {point}")
                                with col_pts2:
                                    st.write("**⚠️ Points faibles:**")
                                    for point in itineraire['points_faibles']:
                                        st.write(f"- {point}")
                            
                            with col_it2:
                                st.metric("Distance", f"{itineraire['distance']:.1f} km")
                                st.metric("Durée", f"{itineraire['duree']:.0f} min")
                                st.metric("Score sécurité", f"{itineraire['score_securite']}/100")
                            
                            with col_it3:
                                if st.button(f"Choisir", key=f"choix_{idx}", use_container_width=True):
                                    st.session_state.itineraire_choisi = itineraire
                                    st.success(f"Itinéraire sélectionné: {itineraire['nom']}")
                            
                            st.divider()
                    
                    # Carte des itinéraires
                    st.subheader("🗺️ Visualisation des itinéraires")
                    
                    m_it = folium.Map(
                        location=[
                            (depart["lat"] + arrivee["lat"]) / 2,
                            (depart["lng"] + arrivee["lng"]) / 2
                        ],
                        zoom_start=9
                    )
                    
                    # Ajouter départ et arrivée
                    folium.Marker(
                        [depart["lat"], depart["lng"]],
                        popup=f"Départ: {depart['ville']}",
                        icon=folium.Icon(color="blue", icon="play", prefix="fa")
                    ).add_to(m_it)
                    
                    folium.Marker(
                        [arrivee["lat"], arrivee["lng"]],
                        popup=f"Arrivée: {arrivee['ville']}",
                        icon=folium.Icon(color="red", icon="flag", prefix="fa")
                    ).add_to(m_it)
                    
                    # Simuler des trajets différents
                    couleurs = ["green", "blue", "orange"]
                    for idx, couleur in enumerate(couleurs):
                        # Générer des points intermédiaires aléatoires
                        points = []
                        points.append([depart["lat"], depart["lng"]])
                        
                        # Points intermédiaires
                        for i in range(1, 4):
                            lat_inter = depart["lat"] + (arrivee["lat"] - depart["lat"]) * i/4 + random.uniform(-0.2, 0.2)
                            lng_inter = depart["lng"] + (arrivee["lng"] - depart["lng"]) * i/4 + random.uniform(-0.2, 0.2)
                            points.append([lat_inter, lng_inter])
                        
                        points.append([arrivee["lat"], arrivee["lng"]])
                        
                        folium.PolyLine(
                            points,
                            color=couleur,
                            weight=3,
                            opacity=0.8,
                            popup=f"Itinéraire {idx+1}"
                        ).add_to(m_it)
                    
                    folium_static(m_it, width=1000, height=500)
                    
                    # Informations complémentaires
                    st.subheader("📋 Informations complémentaires")
                    
                    # Météo sur le trajet
                    meteo_depart = obtenir_meteo_ville(depart["ville"])
                    meteo_arrivee = obtenir_meteo_ville(arrivee["ville"])
                    
                    col_meteo1, col_meteo2 = st.columns(2)
                    with col_meteo1:
                        st.write(f"**Météo à {depart['ville']}:**")
                        st.write(f"- Température: {meteo_depart['temperature']:.1f}°C")
                        st.write(f"- Conditions: {meteo_depart['conditions']}")
                        st.write(f"- Visibilité: {meteo_depart['visibilite']}")
                    
                    with col_meteo2:
                        st.write(f"**Météo à {arrivee['ville']}:**")
                        st.write(f"- Température: {meteo_arrivee['temperature']:.1f}°C")
                        st.write(f"- Conditions: {meteo_arrivee['conditions']}")
                        st.write(f"- Visibilité: {meteo_arrivee['visibilite']}")
                    
                    # Hôpitaux sur le trajet
                    st.write("**🏥 Hôpitaux sur le trajet:**")
                    hopitaux_trajet = trouver_hopitaux_proches(
                        (depart["lat"] + arrivee["lat"]) / 2,
                        (depart["lng"] + arrivee["lng"]) / 2,
                        50
                    )
                    
                    if hopitaux_trajet:
                        for hopital in hopitaux_trajet:
                            st.write(f"- {hopital['nom']} ({hopital['distance']:.1f}km du milieu du trajet) - 📞 {hopital['telephone']}")
                    else:
                        st.info("Aucun hôpital majeur sur le trajet direct")
        
        # Section 4: Navigation en temps réel
        if st.session_state.itineraire_choisi:
            st.subheader("🧭 Navigation en temps réel")
            
            itineraire = st.session_state.itineraire_choisi
            
            col_nav1, col_nav2, col_nav3 = st.columns(3)
            with col_nav1:
                st.metric("Distance restante", f"{itineraire['distance']:.1f} km")
            with col_nav2:
                st.metric("Temps restant", f"{itineraire['duree']:.0f} min")
            with col_nav3:
                st.metric("Prochaine sortie", "15 km")
            
            # Alertes en temps réel
            st.write("**🚨 Alertes sur votre trajet:**")
            
            alertes = [
                {"type": "radar", "location": "RN3, km 45", "distance": "32 km", "severite": "moyenne"},
                {"type": "accident", "location": "Sortie Bafoussam", "distance": "78 km", "severite": "haute"},
                {"type": "travaux", "location": "RN4, près de Douala", "distance": "120 km", "severite": "basse"},
                {"type": "météo", "location": "Région de l'Ouest", "distance": "55 km", "severite": "moyenne", "message": "Pluie prévue"}
            ]
            
            for alerte in alertes:
                icon = "📡" if alerte["type"] == "radar" else "🚗" if alerte["type"] == "accident" else "🚧" if alerte["type"] == "travaux" else "🌧️"
                couleur = "🟡" if alerte["severite"] == "moyenne" else "🔴" if alerte["severite"] == "haute" else "🟢"
                
                st.warning(f"{icon} {couleur} **{alerte['type'].title()}** à {alerte['distance']} - {alerte['location']}")
            
            # Boutons de contrôle
            col_control1, col_control2, col_control3 = st.columns(3)
            with col_control1:
                if st.button("▶️ Démarrer la navigation", use_container_width=True):
                    st.success("Navigation démarrée! Suivez les instructions.")
            with col_control2:
                if st.button("⏸️ Pause", use_container_width=True):
                    st.info("Navigation en pause")
            with col_control3:
                if st.button("⏹️ Arrêter", use_container_width=True):
                    st.session_state.itineraire_choisi = None
                    st.success("Navigation arrêtée")
    
    elif menu == "📱 Notifications":
        st.title("📱 Notifications")
        
        # Filtrer les notifications par région
        region_notif = st.selectbox("Filtrer par région", ["Toutes"] + REGIONS_CAMEROUN)
        
        # Liste des notifications
        notifications = [
            {"type": "alerte", "titre": "Accident sur RN3", "message": "Accident signalé à 2km de votre position près de Bafoussam", 
             "time": "15 min", "lue": False, "region": "Ouest"},
            {"type": "recompense", "titre": "Nouveau badge Camerounais!", "message": "Vous avez obtenu le badge 'Sentinelle du Cameroun'", 
             "time": "1h", "lue": False, "region": "Toutes"},
            {"type": "systeme", "titre": "Mise à jour régionale", "message": "Nouvelles données pour la région du Littoral", 
             "time": "2h", "lue": True, "region": "Littoral"},
            {"type": "message", "titre": "Validation de signalement", "message": "Votre signalement d'obstacle à Yaoundé a été confirmé", 
             "time": "1j", "lue": True, "region": "Centre"},
        ]
        
        # Filtrer par région
        if region_notif != "Toutes":
            notifications = [n for n in notifications if n["region"] == region_notif or n["region"] == "Toutes"]
        
        for notif in notifications:
            with st.container():
                col_icon, col_content = st.columns([1, 10])
                with col_icon:
                    icon = "🚨" if notif["type"] == "alerte" else "🏆" if notif["type"] == "recompense" else "💬" if notif["type"] == "message" else "⚙️"
                    st.write(icon)
                with col_content:
                    st.write(f"**{notif['titre']}**")
                    st.caption(f"{notif['message']}")
                    st.caption(f"⏰ {notif['time']} • 🌍 {notif['region']}")
                st.divider()
        
        # Bouton pour marquer tout comme lu
        if st.button("📭 Tout marquer comme lu", use_container_width=True):
            st.success("Toutes les notifications sont marquées comme lues!")
    
    elif menu == "🏆 Récompenses":
        st.title("🏆 Système de récompenses")
        
        # Points et niveau
        col_points, col_badges, col_rank = st.columns(3)
        with col_points:
            st.metric("Points totaux", "1,250")
            st.progress(75, "Prochain niveau: 1500 points")
        with col_badges:
            st.metric("Badges obtenus", "8/15")
        with col_rank:
            st.metric("Classement national", "45ème")
        
        # Badges spécifiques au Cameroun
        st.subheader("🎖️ Vos badges camerounais")
        
        badges = [
            {"nom": "Sentinelle", "description": "10 signalements validés", "obtenu": True, "icone": "👁️", "region": "Toutes"},
            {"nom": "Héros Yaoundé", "description": "5 interventions à Yaoundé", "obtenu": True, "icone": "🦸", "region": "Centre"},
            {"nom": "Explorateur Littoral", "description": "1000km parcourus au Littoral", "obtenu": True, "icone": "🧭", "region": "Littoral"},
            {"nom": "Vigilant Ouest", "description": "5 alertes météo dans l'Ouest", "obtenu": True, "icone": "🌩️", "region": "Ouest"},
            {"nom": "Citoyen modèle", "description": "50 contributions nationales", "obtenu": False, "icone": "👥", "region": "Toutes"},
            {"nom": "Expert RN3", "description": "Connaissance parfaite de la RN3", "obtenu": False, "icone": "🛣️", "region": "Ouest/Centre"},
        ]
        
        # Filtrer par région
        region_badge = st.selectbox("Voir les badges par région", ["Toutes"] + REGIONS_CAMEROUN)
        
        badges_filtres = badges
        if region_badge != "Toutes":
            badges_filtres = [b for b in badges if b["region"] == region_badge or b["region"] == "Toutes" or region_badge in b["region"]]
        
        cols = st.columns(min(6, len(badges_filtres)))
        for idx, badge in enumerate(badges_filtres[:6]):
            with cols[idx % 6]:
                st.markdown(f"<h3 style='text-align: center;'>{badge['icone']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; font-weight: bold;'>{badge['nom']}</p>", unsafe_allow_html=True)
                st.caption(badge['region'])
                if badge['obtenu']:
                    st.success("✓ Obtenu")
                else:
                    st.info("🔒 À débloquer")
        
        # Récompenses disponibles au Cameroun
        st.subheader("🎁 Échanger vos points - Offres locales")
        
        recompenses = [
            {"nom": "Billet de train Yaoundé-Douala", "points": 1000, "description": "Trajet Yaoundé-Douala"},
            {"nom": "Stationnement gratuit Yaoundé", "points": 500, "description": "1 mois stationnement"},
            {"nom": "Carburant offert", "points": 800, "description": "20L dans station partenaire"},
            {"nom": "Don à la sécurité routière", "points": 200, "description": "Association camerounaise"},
        ]
        
        for recomp in recompenses:
            col_rec1, col_rec2, col_rec3 = st.columns([3, 2, 1])
            with col_rec1:
                st.write(f"**{recomp['nom']}**")
                st.caption(recomp['description'])
            with col_rec2:
                st.write(f"🏷️ {recomp['points']} points")
            with col_rec3:
                if st.button("Échanger", key=f"ech_{recomp['nom']}"):
                    st.success(f"{recomp['nom']} échangé! Code envoyé par SMS.")
    
    elif menu == "⚙️ Profil":
        st.title("⚙️ Mon profil")
        
        with st.form("form_profil"):
            col_info, col_stats = st.columns(2)
            
            with col_info:
                st.subheader("Informations personnelles")
                nom = st.text_input("Nom complet", "Jean Dupont")
                email = st.text_input("Email", "jean.dupont@email.com")
                telephone = st.text_input("Téléphone", "+237 6 12 34 56 78")
                region = st.selectbox("Région", REGIONS_CAMEROUN)
                ville = st.selectbox("Ville", VILLES_CAMEROUN.get(region, ["Yaoundé"]))
                
                # Préférences
                st.subheader("Préférences")
                notifications_push = st.checkbox("Notifications push", True)
                partage_position = st.checkbox("Partage position pour alertes", True)
                rayon_notif = st.slider("Rayon de notification (km)", 1, 50, 10)
                langue = st.selectbox("Langue", ["Français", "Anglais", "Duala", "Bassa"])
            
            with col_stats:
                st.subheader("Statistiques régionales")
                
                # Graphique d'activité par région
                activite_data = pd.DataFrame({
                    'Région': REGIONS_CAMEROUN[:5],
                    'Signalements': np.random.randint(0, 20, 5),
                    'Kilomètres': np.random.randint(0, 500, 5)
                })
                
                fig = px.bar(activite_data, x='Région', y=['Signalements', 'Kilomètres'],
                             title="Votre activité par région", barmode='group')
                st.plotly_chart(fig, use_container_width=True)
                
                # Contributions par type
                contributions = pd.DataFrame({
                    'Type': ['Accidents', 'Obstacles', 'Comportements', 'Validations'],
                    'Région Centre': [12, 8, 15, 24],
                    'Autres régions': [5, 3, 8, 12]
                })
                
                st.dataframe(contributions, use_container_width=True)
            
            if st.form_submit_button("💾 Enregistrer les modifications"):
                st.success("Profil mis à jour avec succès!")

# Fonctions pour les autres interfaces (Autorités et Service Central) restent similaires
# mais adaptées aux régions du Cameroun

# Gestion de la navigation principale
def main():
    # Barre latérale supérieure
    st.sidebar.title("🚗 SafeDriveCam Cameroun")
    st.sidebar.markdown("---")
    
    # Affichage selon le rôle
    if st.session_state.user_role == "utilisateur":
        user_interface()
    elif st.session_state.user_role == "autorite":
        # Interface autorités adaptée
        st.title("👮 Interface Autorités - Cameroun")
        st.write("### Sélectionnez votre région d'intervention")
        region_autorite = st.selectbox("Région", REGIONS_CAMEROUN)
        st.info(f"Interface autorités pour la région {region_autorite}")
        
        # Ajouter les fonctionnalités spécifiques aux autorités ici
        col_auth1, col_auth2, col_auth3 = st.columns(3)
        with col_auth1:
            if st.button("📊 Tableau de bord régional"):
                st.info("Tableau de bord régional (à implémenter)")
        with col_auth2:
            if st.button("🚨 Gestion des urgences"):
                st.info("Gestion des urgences (à implémenter)")
        with col_auth3:
            if st.button("📈 Statistiques"):
                st.info("Statistiques régionales (à implémenter)")
                
    elif st.session_state.user_role == "admin":
        # Interface service central adaptée
        st.title("🏛️ Service Central - Cameroun")
        st.write("### Vue nationale des 10 régions")
        
        # Carte nationale du Cameroun
        m_national = folium.Map(location=[5.9631, 10.1591], zoom_start=6)
        
        # Ajouter des marqueurs pour chaque région
        for region in REGIONS_CAMEROUN:
            # Coordonnées approximatives des régions
            coords_regions = {
                "Adamaoua": [6.5, 13.5],
                "Centre": [3.8480, 11.5021],
                "Est": [4.0, 14.0],
                "Extrême-Nord": [11.0, 14.5],
                "Littoral": [4.0511, 9.7679],
                "Nord": [9.3077, 13.3937],
                "Ouest": [5.4775, 10.4176],
                "Sud": [2.9167, 11.1500],
                "Sud-Ouest": [4.1534, 9.2423],
                "Nord-Ouest": [6.2333, 10.9833]
            }
            
            if region in coords_regions:
                folium.Marker(
                    coords_regions[region],
                    popup=region,
                    icon=folium.Icon(color="blue", icon="flag")
                ).add_to(m_national)
        
        folium_static(m_national, width=1000, height=500)
        
        # Statistiques nationales
        st.subheader("📊 Statistiques nationales")
        
        stats_nationales = pd.DataFrame({
            'Région': REGIONS_CAMEROUN,
            'Accidents (24h)': np.random.randint(0, 15, 10),
            'Signalements': np.random.randint(50, 500, 10),
            'Utilisateurs': np.random.randint(100, 2000, 10),
            'Temps réponse moyen (min)': np.random.uniform(5, 15, 10).round(1)
        })
        
        st.dataframe(stats_nationales, use_container_width=True)
        
    else:
        # Page de connexion
        if st.session_state.current_page == "connexion":
            login_page()
        elif st.session_state.current_page == "inscription":
            register_page()

# Lancement de l'application
if __name__ == "__main__":
    main()