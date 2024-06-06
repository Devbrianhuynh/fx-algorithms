import sys
sys.path.append('../')

import pandas as pd
from dateutil import parser
import numpy as np

from technicals.indicators import macd
from simulation.guru_tester import GuruTester
from infrastructure.instrument_collection import InstrumentCollection
from simulation.constants import BUY, SELL, NONE


def apply_signal(df):
    df['signal'] = np.where((df['direction'] == BUY) & (df['mid_l'] > df['EMA']), BUY,
                            np.where((df['direction'] == SELL) & (df['mid_h'] < df['EMA']), SELL, NONE))
    return df['signal']


def apply_cross(df):
    df['direction'] = np.where((df['macd_delta'] > 0) & (df['macd_delta_prev'] < 0), BUY,
                               np.where((df['macd_delta'] < 0) & (df['macd_delta_prev'] > 0), SELL, NONE))
    return df['direction']


def prepare_data(df: pd.DataFrame, slow, fast, signal, ema):
    df_an = df.copy()
    df_an = macd(df_an, n_slow=slow, n_fast=fast, n_signal=signal)
    
    df_an['macd_delta'] = df_an.MACD - df_an.signal
    df_an['macd_delta_prev'] = df_an.macd_delta.shift(1)
    df_an['direction'] = apply_cross(df_an)
    df_an['EMA'] = df_an.mid_c.ewm(span=ema, min_periods=ema).mean()
    
    df_an.dropna(inplace=True)
    df_an.reset_index(drop=True, inplace=True)
    
    return df_an


def load_data(pair, time_delta=1):
    # Change start year to 2016 and end year to 2024 to get the full package
    start = parser.parse("2020-10-01T00:00:00Z")
    end = parser.parse("2021-01-01T00:00:00Z")

    df = pd.read_pickle(f"./data/{pair}_H{time_delta}.pkl")
    df_m5 = pd.read_pickle(f"./data/{pair}_M5.pkl")

    df = df[(df.time >= start) & (df.time < end)]
    df_m5 = df_m5[(df_m5.time >= start) & (df_m5.time <end)]

    df.reset_index(drop=True, inplace=True)
    df_m5.reset_index(drop=True, inplace=True)

    return df, df_m5


def simulate_params(pair, df, df_m5,  slow, fast, signal, ema, time_delta):
    prepped_df = prepare_data(df, slow, fast, signal, ema)
    
    gt = GuruTester(
        prepped_df,
        apply_signal,
        df_m5,
        use_spread=True,
        time_delta=time_delta
    )
    
    gt.run_test()

    gt.df_results['slow'] = slow
    gt.df_results['fast'] = fast
    gt.df_results['signal'] = signal
    gt.df_results['ema'] = ema
    gt.df_results['pair'] = pair

    return gt.df_results


def run_pair(pair):
    time_delta = 4

    df, df_m5 = load_data(pair, time_delta=time_delta)

    results = []
    trades = []

    print("\n--> Running", pair)

    for slow in [26, 52]:
        for fast in [12, 18]:
            
            if slow <= fast:
                continue
            
            for signal in [9, 12]:
                
                for ema in [50, 100]:
                    sim_res_df = simulate_params(pair, df, df_m5, slow, fast, signal, ema, time_delta)
                    r = sim_res_df.result.sum()
                    trades.append(sim_res_df)
                    
                    print(f"--> {pair} {slow} {fast} {ema} {signal} {r}")
                    
                    results.append({
                        'pair': pair,
                        'slow': slow,
                        'fast': fast,
                        'ema': ema,
                        'result': r,
                        'signal': signal
                    })
                    
    pd.concat(trades).to_pickle(f"./exploration/macd_ema/trades/macd_ema_trades_{pair}.pkl")
    return pd.DataFrame.from_dict(results)


def run_ema_macd(ic: InstrumentCollection):
    results = []
    our_curr = ['USD', 'GBP', 'JPY', 'CHF', 'EUR', 'AUD']
    
    for p1 in our_curr:
        for p2 in our_curr:
            pair = f"{p1}_{p2}"
            
            if pair in ic.instruments_dict.keys():
                results = run_pair(pair)
                results.to_pickle(f"./exploration/macd_ema/macd_ema_res_{pair}.pkl")

