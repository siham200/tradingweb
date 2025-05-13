import streamlit as st
from datetime import datetime

# Configuration de la page
st.set_page_config(
    layout="wide",
    page_title="TRADINGWEB - Connexion",
    initial_sidebar_state="collapsed"
)

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
        }}
        
        /* Carte de connexion moderne */
        .login-card {{
            max-width: 500px;
            margin: 2rem auto;
            padding: 2.5rem;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .login-title {{
            color: white;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            text-align: center;
            background: linear-gradient(90deg, #f6a623 0%, #ffd166 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        /* Inputs modernes */
        .stTextInput>div>div>input, 
        .stTextInput>div>div>input:focus {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: white;
            padding: 12px;
            border-radius: 8px;
        }}
        
        .stTextInput>label {{
            color: rgba(255, 255, 255, 0.7) !important;
            font-weight: 500;
        }}
        
        /* Bouton moderne */
        .stButton>button {{
            width: 100%;
            background: linear-gradient(90deg, #f6a623 0%, #ff9a3c 100%);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
            margin-top: 1rem;
        }}
        
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(246, 166, 35, 0.3);
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
        
        .footer-links {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-bottom: 1rem;
        }}
        
        .footer-links a {{
            color: rgba(255, 255, 255, 0.7);
            text-decoration: none;
            transition: all 0.3s ease;
        }}
        
        .footer-links a:hover {{
            color: #f6a623;
        }}
        
        .copyright {{
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.9rem;
        }}
        
        /* Animation subtile */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .login-card {{
            animation: fadeIn 0.6s ease-out;
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

# --- Contenu de connexion ---
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div class="login-card">
        <div class="login-title">Connexion</div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter")
        
        if submitted:
            if username and password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Connecté avec succès!")
                st.rerun()
            else:
                st.error("Veuillez remplir tous les champs")
    
    st.markdown("""
        <div style="text-align: center; margin-top: 1.5rem; color: rgba(255,255,255,0.6);">
            Nouveau sur TRADINGWEB ? <a href="/register" style="color: #f6a623; text-decoration: none;">Créer un compte</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown(f"""
    <div class="custom-footer">
        <div class="footer-links">
            <a href="/about">À propos</a>
            <a href="/contact">Contact</a>
            <a href="/privacy">Confidentialité</a>
            <a href="/terms">Conditions</a>
        </div>
        <div class="copyright">
            © {datetime.now().year} TRADINGWEB. Tous droits réservés.
        </div>
    </div>
""", unsafe_allow_html=True)