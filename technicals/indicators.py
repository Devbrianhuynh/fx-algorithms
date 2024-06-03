import pandas as pd

def bollinger_bands(df: pd.DataFrame, n=20, n_std=2):
    typical_price = (df['mid_c'] + df['mid_h'] + df['mid_l']) / 3
    std = typical_price.rolling(window=n).std()
    
    df['BB_ma'] = typical_price.rolling(window=n).mean()
    df['BB_upper'] = df['BB_ma'] + std * n_std
    df['BB_lower'] = df['BB_ma'] - std * n_std
    
    return df


def atr(df: pd.DataFrame, n=14):
    prev_c = df['mid_c'].shift(1)
    
    true_range_1 = df['mid_h'] - df['mid_l']
    true_range_2 = abs(df['mid_h'] - prev_c)
    true_range_3 = abs(prev_c - df['mid_l'])
    
    true_range = pd.DataFrame({'true_range_1': true_range_1, 'true_range_2': true_range_2, 'true_range_3': true_range_3}).max(axis=1)
    
    df[f'ATR_{n}'] = true_range.rolling(window=n).mean()
    return df


def keltner_channels(df: pd.DataFrame, n_ema=20, n_atr=10):
    df['ema'] = df['mid_c'].ewm(span=n_ema, min_periods=n_ema).mean()
    
    df = atr(df, n_atr)
    
    df['KC_upper'] = df[f'ATR_{n_atr}'] * 2 + df['ema']
    df['KC_lower'] = df['ema'] - df[f'ATR_{n_atr}'] * 2
    
    df.drop(f'ATR_{n_atr}', axis=1, inplace=True)
    return df


def rsi(df: pd.DataFrame, n=14):
    alpha = 1.0 / n
    gains = df['mid_c'].diff()
    
    wins = pd.Series([x if x >= 0 else 0.0 for x in gains], name='wins')
    losses = pd.Series([x * -1 if x < 0 else 0.0 for x in gains], name='losses')
    
    wins_rma = wins.ewm(min_periods=n, alpha=alpha).mean()
    losses_rma = losses.ewm(min_periods=n, alpha=alpha).mean()
    
    rs = wins_rma / losses_rma
    
    df[f'RSI_{n}'] = 100 - (100 / (1 + rs))
    return df


def macd(df: pd.DataFrame, n_slow=26, n_fast=12, n_signal=9):
    ema_long = df['mid_c'].ewm(span=n_slow, min_periods=n_slow).mean()
    ema_short = df['mid_c'].ewm(span=n_fast, min_periods=n_fast).mean()
    
    df['MACD'] = ema_short - ema_long
    df['signal'] = df['MACD'].ewm(span=n_signal, min_periods=n_signal).mean()
    df['histogram'] = df['MACD'] - df['signal']
    
    return df
