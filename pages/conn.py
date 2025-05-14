import streamlit as st
from datetime import datetime
from database.db import authenticate_user, init_db

# Initialisation de la base
init_db()

# Configuration de la page
st.set_page_config(page_title="Connexion - TRADINGWEB", layout="centered")

# CSS moderne
st.markdown(f"""
    <style>
        /* Reset Streamlit */
        [data-testid="collapsedControl"] {{ display: none; }}
        [data-testid="stSidebar"] {{ display: none !important; }}
        header {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        
        /* Police moderne */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {{
            font-family: 'Inter', sans-serif;
        }}
        
        /* Navbar glassmorphism */
        .navbar {{
            background: rgba(30, 30, 47, 0.9);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            color: white;
            padding: 1rem 2rem;
            font-size: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .navbar a {{
            color: rgba(255, 255, 255, 0.8);
            margin-left: 2rem;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            position: relative;
        }}
        
        .navbar a:hover {{
            color: #f6a623;
        }}
        
        .navbar a::after {{
            content: '';
            position: absolute;
            width: 0;
            height: 2px;
            bottom: -5px;
            left: 0;
            background-color: #f6a623;
            transition: width 0.3s ease;
        }}
        
        .navbar a:hover::after {{
            width: 100%;
        }}
        
        /* Conteneur principal */
        .stApp {{
            margin-top: 80px;
            background: linear-gradient(135deg, #0f0f1a 0%, #1e1e2f 100%);
            min-height: calc(100vh - 80px);
            color: white;
        }}
        
        /* Carte de contrôle moderne */
        .control-card {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        /* Titres modernes */
        .section-title {{
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 1rem;
            background: linear-gradient(90deg, #f6a623 0%, #ffd166 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        /* Sélecteurs modernes */
        .stSelectbox>div>div {{
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            border-radius: 8px !important;
        }}
        
        .stSelectbox label {{
            color: rgba(255, 255, 255, 0.8) !important;
            font-weight: 500 !important;
        }}
        
        /* Graphiques modernes */
        .js-plotly-plot .plotly {{
            background: transparent !important;
        }}
        
        /* Footer moderne */
        .custom-footer {{
            background: rgba(30, 30, 47, 0.9);
            color: white;
            padding: 2rem 1rem;
            margin-top: 3rem;
            text-align: center;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .copyright {{
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.9rem;
        }}
        
        /* Animation de chargement */
        @keyframes pulse {{
            0% {{ opacity: 0.5; }}
            50% {{ opacity: 1; }}
            100% {{ opacity: 0.5; }}
        }}
        
        .loading-text {{
            animation: pulse 1.5s infinite;
        }}
    </style>
""", unsafe_allow_html=True)

# --- Navbar ---
st.markdown("""
    <div class='navbar'>
        <div><strong style="font-size: 1.2rem;">TRADINGWEB</strong></div>
        <div>
            <a href="/home" target="_self">Accueil</a>
            <a href="/ind" target="_self">Indicateurs</a>
            <a href="/back" target="_self">Backtesting</a>
            <a href="/stra" target="_self">Stratégies</a>
            <a href="/conn" target="_self">Connexion</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# Contenu principal
st.markdown('<div class="login-container">', unsafe_allow_html=True)
st.markdown('<div class="login-title">Connexion à TRADINGWEB</div>', unsafe_allow_html=True)

with st.form("login_form"):
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    submitted = st.form_submit_button("Se connecter")

    if submitted:
        if username and password:
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Connexion réussie")
                st.rerun()
            else:
                st.error("❌ Nom d'utilisateur ou mot de passe incorrect")
        else:
            st.warning("⚠️ Remplissez tous les champs")

st.markdown("""
    <div style="text-align: center; margin-top: 1rem;">
        <span style="color: rgba(255,255,255,0.6);">Nouveau ?</span>
        <a href="/login" style="color: #f6a623; text-decoration: none; font-weight: 500;">Créer un compte</a>
    </div>
""", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; margin-top: 0.8rem;">
        <a href="/forget_passw" style="color: #f6a623; text-decoration: none; font-size: 0.9rem;">
            🔐 Mot de passe oublié ?
        </a>
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
