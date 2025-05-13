# forex_api.py

import requests
import pandas as pd

API_KEY = "4708e1ed080e4c4aa11251e58bcfc67a"  # Remplace avec ta vraie clé Twelve Data

def get_forex_data(symbol="EUR/USD", interval="1h", outputsize=100):
    url = f"https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "values" in data:
            df = pd.DataFrame(data["values"])
            df["datetime"] = pd.to_datetime(df["datetime"])
            df = df.sort_values("datetime")
            return df
        else:
            raise ValueError(f"Erreur API : {data.get('message', 'inconnue')}")

    except Exception as e:
        print(f"Erreur de récupération des données : {e}")
        return pd.DataFrame()  # Retourne un dataframe vide en cas d'erreur
