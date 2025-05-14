import streamlit as st
from datetime import datetime
from database.db import init_db
# Configuration de la page
st.set_page_config(
    page_title="TRADINGWEB - Accueil", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# État de connexion
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

from database.db import init_db

# L'appel unique ici
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

        .hero {
            display: flex;
            align-items: center;
            min-height: 80vh;
            padding: 4rem 2rem;
        }

        .hero-content {
            max-width: 1200px;
            margin: 0 auto;
            width: 100%;
        }

        .hero-title {
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, #ffffff, #d1d1d1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
            font-size: 1.25rem;
            color: rgba(255,255,255,0.8);
            margin-top: 1rem;
            line-height: 1.6;
        }

        .btn {
            background: linear-gradient(90deg, #f6a623, #ff9a3c);
            color: white;
            padding: 0.8rem 2rem;
            border-radius: 50px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(246, 166, 35, 0.3);
            margin-right: 1rem;
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(246, 166, 35, 0.4);
        }

        .btn-outline {
            background: transparent;
            border: 2px solid #f6a623;
            color: #f6a623;
        }

        .hero-image {
            border-radius: 20px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            transform: perspective(1000px) rotateY(-10deg);
            transition: transform 0.5s ease;
        }

        .hero-image:hover {
            transform: perspective(1000px) rotateY(0deg);
        }

        .footer {
            background: rgba(30,30,47,0.95);
            padding: 4rem 2rem 2rem;
            color: white;
            border-top: 1px solid rgba(255,255,255,0.1);
            margin-top: 4rem;
        }

        .footer-container {
            max-width: 1200px;
            margin: auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
        }

        .footer-title {
            color: #f6a623;
            font-weight: bold;
            margin-bottom: 1rem;
        }

        .footer a {
            color: rgba(255,255,255,0.7);
            text-decoration: none;
        }

        .footer a:hover {
            color: #f6a623;
        }

        .footer-bottom {
            text-align: center;
            margin-top: 2rem;
            color: rgba(255,255,255,0.5);
            font-size: 0.9rem;
        }

        @media (max-width: 992px) {
            .hero {
                flex-direction: column;
                text-align: center;
            }

            .hero-title {
                font-size: 2.5rem;
            }

            .hero-subtitle {
                margin-left: auto;
                margin-right: auto;
            }
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

# --- Hero Section ---
st.markdown("""
    <div class="hero">
        <div class="hero-content">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; align-items: center;">
                <div>
                    <h1 class="hero-title">Plateforme de trading innovante</h1>
                    <p class="hero-subtitle">
                        Que vous soyez débutant ou expert, notre objectif est de vous offrir un environnement 
                        puissant et intuitif pour développer, tester et exécuter vos stratégies de trading.
                    </p>
""", unsafe_allow_html=True)

if not st.session_state.logged_in:
    st.markdown("""
        <div style="margin-top: 2rem;">
            <button class="btn" onclick="window.location"><a href="/login" target="_self">Créer un compte</a></button>
            <button class="btn btn-outline" "><a href="/conn" target="_self">Se connecter</a></button>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
        <div style="margin-top: 2rem; background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
            <p style="color: #f6a623;">Bienvenue, {st.session_state.get('username', 'utilisateur')}!</p>
            <button class="btn" onclick="window.location.href='/back'">Accéder au tableau de bord</button>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
                </div>
                <div>
                    <img src="https://www.eslsca.fr/sites/eslsca.fr/files/images/ARTICLE_Trading-haute-frequence-tellement-plus-rapide-vraiment-plus-fort.jpg" 
                         class="hero-image" style="width: 100%; height: auto; object-fit: cover;">
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Footer ---
st.markdown(f"""
    <div class="footer">
        <div class="footer-container">
            <div>
                <h3 class="footer-title">TRADINGWEB</h3>
                <p>Plateforme de trading innovante pour débutants et experts.</p>
            </div>
            <div>
                <h3 class="footer-title">Liens rapides</h3>
                <p><a href="/home">Accueil</a></p>
                <p><a href="/back">Backtesting</a></p>
                <p><a href="/conn">Connexion</a></p>
                <p><a href="/stra">Stratégies</a></p>
            </div>
            <div>
                <h3 class="footer-title">Contact</h3>
                <p><a href="mailto:contact@tradingweb.com">contact@tradingweb.com</a></p>
                <p><a href="tel:+33123456789">+33 1 23 45 67 89</a></p>
                <p>Support 24h/24</p>
            </div>
        </div>
        <div class="footer-bottom">
            © {datetime.now().year} TRADINGWEB. Tous droits réservés.
        </div>
    </div>
""", unsafe_allow_html=True)
