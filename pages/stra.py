import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from forex_api import get_forex_data
from strategies import moving_average_crossover_strategy





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
st.title("Stratégies de Trading")

# Sélection de la stratégie
strategie = st.selectbox("Sélectionner une stratégie", ["Croisement des Moyennes Mobiles"])

if strategie == "Croisement des Moyennes Mobiles":
    st.subheader("Croisement des Moyennes Mobiles")

    symbol = st.text_input("Saisir une paire de devises (par exemple, EUR/USD)", "EUR/USD")
    interval = st.selectbox("Intervalle de temps", ["1h", "30min", "15min" , "1day"])
    outputsize = st.slider("Nombre de points de données", 10, 200, 100)

    df = get_forex_data(symbol=symbol, interval=interval, outputsize=outputsize)

    if df.empty:
        st.warning("Aucune donnée chargée. Vérifie la paire ou l'intervalle.")
    else:
        df['close'] = df['close'].astype(float)
        df = moving_average_crossover_strategy(df)

        # Tracer les courbes
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['datetime'], y=df['close'], mode='lines', name='Prix'))
        fig.add_trace(go.Scatter(x=df['datetime'], y=df['short_ma'], mode='lines', name='Moyenne mobile courte'))
        fig.add_trace(go.Scatter(x=df['datetime'], y=df['long_ma'], mode='lines', name='Moyenne mobile longue'))

        # Signaux d'achat
        df_buy = df[df['position'] == 1]
        fig.add_trace(go.Scatter(
            x=df_buy['datetime'], y=df_buy['close'], mode='markers',
            marker=dict(symbol='triangle-up', color='green', size=10),
            name='Signal Achat'))

        # Signaux de vente
        df_sell = df[df['position'] == -1]
        fig.add_trace(go.Scatter(
            x=df_sell['datetime'], y=df_sell['close'], mode='markers',
            marker=dict(symbol='triangle-down', color='red', size=10),
            name='Signal Vente'))

        st.plotly_chart(fig)
