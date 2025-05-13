import pandas as pd

def moving_average_crossover_strategy(df, short_window=5, long_window=20):
    df = df.copy()
    df['short_ma'] = df['close'].rolling(window=short_window).mean()
    df['long_ma'] = df['close'].rolling(window=long_window).mean()
    
    # Signaux : 1 quand short_ma > long_ma, 0 sinon
    df['signal'] = 0
    df['signal'] = (df['short_ma'] > df['long_ma']).astype(int)
    
    # position = signal d'aujourd'hui - signal d'hier
    df['position'] = df['signal'].diff()
    
    return df
