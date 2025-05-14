import streamlit as st
from database.db import authenticate_user, init_db, add_user

# Configuration de la page
st.set_page_config(
    page_title="Créer un compte",
    page_icon="👤",
    layout="centered",
    initial_sidebar_state="collapsed"
)

init_db()

# CSS complet
st.markdown("""
    <style>
        [data-testid="collapsedControl"], [data-testid="stSidebar"],
        header, footer {
            display: none !important;
        }

        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        * {
            font-family: 'Inter', sans-serif;
            box-sizing: border-box;
        }

        .navbar {
            background: rgba(30, 30, 47, 0.9);
            backdrop-filter: blur(10px);
            color: white;
            padding: 1.5rem 3rem;
            font-size: 1.1rem;
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
        }

        .navbar-logo {
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, #f6a623, #ffd166);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .nav-links {
            display: flex;
            gap: 2rem;
        }

        .nav-links a {
            color: rgba(255,255,255,0.8);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            position: relative;
        }

        .nav-links a:hover {
            color: #f6a623;
        }

        .nav-links a::after {
            content: '';
            position: absolute;
            width: 0;
            height: 2px;
            bottom: -5px;
            left: 0;
            background-color: #f6a623;
            transition: width 0.3s ease;
        }

        .nav-links a:hover::after {
            width: 100%;
        }

        .stApp {
            margin-top: 100px;
            background: linear-gradient(135deg, #0f0f1a, #1e1e2f);
            color: white;
            min-height: 100vh;
        }

        /* Styles pour le formulaire */
        .form-container {
            background: white;
            padding: 2.5rem;
            border-radius: 15px;
            max-width: 450px;
            margin: 2rem auto;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        }

        .form-title {
            text-align: center;
            color: #f6a623;
            font-size: 2rem;
            margin-bottom: 1.8rem;
            font-weight: 600;
        }

        /* Styles pour les labels */
        .stTextInput > label, .stTextInput > div > label {
            color:#f6a623 # !important;
            font-weight: 500 !important;
            font-size: 0.95rem !important;
        }

        /* Styles pour les champs de saisie */
        .stTextInput input, .stTextInput input:focus {
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            padding: 0.75rem !important;
            background: #f8fafc !important;
        }
        /* Style amélioré pour la redirection */
        .redirect-message {
            text-align: center;
            color: #4a5568;
            margin-top: 1rem;
            font-size: 0.9rem;
        }
        /* Style pour le bouton */
        .stButton > button {
            width: 100%;
            padding: 0.75rem;
            border-radius: 8px;
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: white !important;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
            margin-top: 1rem;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(79, 70, 229, 0.3);
            background: linear-gradient(135deg, #5e56e8, #8b4ef7);
        }

        /* Lien de connexion */
        .login-link {
            text-align: center;
            margin-top: 1.5rem;
            color: #4a5568;
        }

        .login-link a {
            color: #4f46e5 !important;
            text-decoration: none;
            font-weight: 500;
        }

        .login-link a:hover {
            text-decoration: underline;
        }

        /* Messages */
        .stAlert {
            border-radius: 8px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Navbar ---
st.markdown("""
    <div class='navbar'>
        <div class="navbar-logo">TRADINGWEB</div>
        <div class="nav-links">
            <a href="/home" target="_self">Accueil</a>
            <a href="/ind" target="_self">Indicateurs</a>
            <a href="/back" target="_self">Backtesting</a>
            <a href="/stra" target="_self">Stratégies</a>
            <a href="/conn" target="_self">Connexion</a>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="form-container">', unsafe_allow_html=True)
st.markdown('<div class="form-title">Créer un compte</div>', unsafe_allow_html=True)

# Variable pour contrôler la redirection
redirect = False

with st.form("register_form"):
    username = st.text_input("Nom d'utilisateur", placeholder="Entrez votre nom d'utilisateur")
    email = st.text_input("Email", placeholder="Entrez votre email")
    password = st.text_input("Mot de passe", type="password", placeholder="Créez un mot de passe")
    confirm = st.text_input("Confirmer le mot de passe", type="password", placeholder="Confirmez votre mot de passe")
    
    submit = st.form_submit_button("Créer un compte")

    if submit:
        if not username or not email or not password or not confirm:
            st.error("Veuillez remplir tous les champs.", icon="⚠️")
        elif password != confirm:
            st.error("Les mots de passe ne correspondent pas.", icon="🔒")
        else:
            success = add_user(username, email, password)
            if success:
                st.success("✅ Compte créé avec succès!")
                redirect = True
            else:
                st.error("❌ Nom d'utilisateur ou email déjà utilisé.")

# Redirection automatique si le compte est créé avec succès
if redirect:
    st.markdown("""
        <div class="redirect-message">
            Redirection vers la page de connexion...
        </div>
        <script>
            setTimeout(function() {
                window.location.href = "/conn";
            }, 2000);
        </script>
    """, unsafe_allow_html=True)

# Lien vers la page de connexion
st.markdown("""
    <div class="login-link">
        Déjà un compte? <a href="/conn" target="_self">Se connecter</a>
    </div>
""", unsafe_allow_html=True)