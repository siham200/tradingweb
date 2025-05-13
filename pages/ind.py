import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from forex_api import get_forex_data


# Configuration
st.set_page_config(
    page_title="Tableau Forex", 
    layout="wide",
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

# --- Contenu principal ---
st.markdown('<div class="section-title">📈 Tableau Forex en Temps Réel</div>', unsafe_allow_html=True)

# Carte de contrôle
with st.container():
    st.markdown('<div class="control-card">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_pair = st.selectbox("Paire de devises", ["EUR/USD", "USD/JPY", "GBP/USD", "USD/CHF", "AUD/USD", "USD/CAD"])
    with col2:
        selected_indicator = st.selectbox("Indicateur technique", ["Aucun", "SMA", "RSI", "MACD", "Bollinger Bands", "EMA", "Stochastic Oscillator"])
    with col3:
        selected_interval = st.selectbox("Fréquence", ["1min", "5min", "15min", "30min", "1h", "1day"])
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Indicateurs ---
def calculate_sma(df, period=14):
    df["SMA"] = df["close"].rolling(window=period).mean()
    return df

def calculate_rsi(df, period=14):
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))
    return df

def calculate_macd(df):
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    return df

def calculate_bollinger_bands(df, period=20, std_dev=2):
    df["SMA"] = df["close"].rolling(window=period).mean()
    df["Upper Band"] = df["SMA"] + (df["close"].rolling(window=period).std() * std_dev)
    df["Lower Band"] = df["SMA"] - (df["close"].rolling(window=period).std() * std_dev)
    return df

def calculate_ema(df, period=14):
    df["EMA"] = df["close"].ewm(span=period, adjust=False).mean()
    return df

def calculate_stochastic_oscillator(df, period=14):
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df["high"] = pd.to_numeric(df["high"], errors="coerce")
    df["low"] = pd.to_numeric(df["low"], errors="coerce")

    high_roll = df["high"].rolling(window=period).max()
    low_roll = df["low"].rolling(window=period).min()
    df["Stochastic"] = 100 * ((df["close"] - low_roll) / (high_roll - low_roll))
    return df

# Chargement des données
with st.spinner("Chargement des données..."):
    loading_text = st.markdown('<p class="loading-text" style="text-align:center;">Récupération des données en cours...</p>', unsafe_allow_html=True)
    data = get_forex_data(selected_pair, selected_interval)
    loading_text.empty()

# --- Affichage ---
if data is not None:
    st.markdown(f'<div class="section-title">Graphique des prix - {selected_pair} - Intervalle : {selected_interval}</div>', unsafe_allow_html=True)
    
    # Configuration du thème sombre pour Plotly
    plotly_template = {
        'layout': {
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'font': {'color': 'white'},
            'xaxis': {
                'gridcolor': 'rgba(255,255,255,0.1)',
                'linecolor': 'rgba(255,255,255,0.2)'
            },
            'yaxis': {
                'gridcolor': 'rgba(255,255,255,0.1)',
                'linecolor': 'rgba(255,255,255,0.2)'
            },
            'hoverlabel': {
                'bgcolor': 'rgba(30,30,47,0.9)',
                'font': {'color': 'white'}
            }
        }
    }

    price_fig = go.Figure()
    price_fig.add_trace(go.Scatter(
        x=data.index, 
        y=data["close"], 
        name="Prix",
        line=dict(color='#f6a623', width=2),
        hovertemplate='%{y:.4f}<extra></extra>'
    ))

    if selected_indicator == "SMA":
        data = calculate_sma(data)
        price_fig.add_trace(go.Scatter(
            x=data.index, 
            y=data["SMA"], 
            name="SMA",
            line=dict(color='#00c8ff', width=1.5)
        ))

    elif selected_indicator == "EMA":
        data = calculate_ema(data)
        price_fig.add_trace(go.Scatter(
            x=data.index, 
            y=data["EMA"], 
            name="EMA",
            line=dict(color='#00ffaa', width=1.5)
        ))

    price_fig.update_layout(
        template=plotly_template,
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    st.plotly_chart(price_fig, use_container_width=True)

    # Indicateur secondaire
    if selected_indicator == "RSI":
        data = calculate_rsi(data)
        rsi_fig = go.Figure()
        rsi_fig.add_trace(go.Scatter(
            x=data.index, 
            y=data["RSI"], 
            name="RSI",
            line=dict(color='#ff6b6b', width=2)
        ))
        rsi_fig.add_hline(y=70, line=dict(dash='dash', color='red', width=1))
        rsi_fig.add_hline(y=30, line=dict(dash='dash', color='green', width=1))
        rsi_fig.update_layout(
            title="RSI (Relative Strength Index)",
            template=plotly_template,
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(rsi_fig, use_container_width=True)

    elif selected_indicator == "MACD":
        data = calculate_macd(data)
        macd_fig = go.Figure()
        macd_fig.add_trace(go.Scatter(
            x=data.index, 
            y=data["MACD"], 
            name="MACD",
            line=dict(color='#4cc9f0', width=1.5)
        ))
        macd_fig.add_trace(go.Scatter(
            x=data.index, 
            y=data["Signal"], 
            name="Signal",
            line=dict(color='#f72585', width=1.5)
        ))
        macd_fig.update_layout(
            title="MACD (Moving Average Convergence Divergence)",
            template=plotly_template,
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(macd_fig, use_container_width=True)

    elif selected_indicator == "Bollinger Bands":
        data = calculate_bollinger_bands(data)
        bollinger_fig = go.Figure()
        bollinger_fig.add_trace(go.Scatter(
            x=data.index, 
            y=data["close"], 
            name="Prix",
            line=dict(color='#f6a623', width=2)
        ))
        bollinger_fig.add_trace(go.Scatter(
            x=data.index, 
            y=data["Upper Band"], 
            name="Bande supérieure",
            line=dict(color='#ef476f', width=1, dash='dot')
        ))
        bollinger_fig.add_trace(go.Scatter(
            x=data.index, 
            y=data["Lower Band"], 
            name="Bande inférieure",
            line=dict(color='#06d6a0', width=1, dash='dot')
        ))
        bollinger_fig.update_layout(
            title="Bandes de Bollinger",
            template=plotly_template,
            height=500,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(bollinger_fig, use_container_width=True)

    elif selected_indicator == "Stochastic Oscillator":
        data = calculate_stochastic_oscillator(data)
        stoch_fig = go.Figure()
        stoch_fig.add_trace(go.Scatter(
            x=data.index, 
            y=data["Stochastic"], 
            name="Stochastic Oscillator",
            line=dict(color='#7209b7', width=2)
        ))
        stoch_fig.add_hline(y=80, line=dict(dash='dash', color='red', width=1))
        stoch_fig.add_hline(y=20, line=dict(dash='dash', color='green', width=1))
        stoch_fig.update_layout(
            title="Stochastic Oscillator",
            template=plotly_template,
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(stoch_fig, use_container_width=True)

# --- Footer ---
st.markdown(f"""
    <div class="custom-footer">
        <div class="copyright">
            © {datetime.now().year} TRADINGWEB - Plateforme de trading professionnelle
        </div>
    </div>
""", unsafe_allow_html=True)