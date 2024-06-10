import pandas as pd
import numpy as np

from constants.defs import *
from api.oanda_api import OandaAPI
from models.trade_settings import TradeSettings
from models.trade_decision import TradeDecision
from technicals.indicators import *


pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', None)


def process_candles(df: pd.DataFrame, pair, trade_settings: TradeSettings, log_message):
    df.reset_index(drop=True, inplace=True)
    
    df['pair'] = pair
    df['spread'] = df['ask_c'] - df['bid_c']
    
    df = bollinger_bands(df, trade_settings.n_ma, trade_settings.n_std)
    
    df['gain'] = abs(df['mid_c'] - df['BB_ma'])
    
    df['signal'] = np.where((df['spread'] <= trade_settings.maxspread) & (df['gain'] >= trade_settings.mingain), 
                            np.where((df['mid_c'] > df['BB_upper']) & (df['mid_o'] < df['BB_upper']), SELL,
                                     np.where((df['mid_c'] < df['BB_lower']) & (df['mid_o'] > df['BB_lower']), BUY, NONE)), 
                            NONE)
    
    df['TP'] = np.where(df['signal'] == BUY, df['mid_c'] + df['gain'], 
                        np.where(df['signal'] == SELL, df['mid_c'] - df['gain'], 0.0))
    
    df['SL'] = np.where(df['signal'] == BUY, df['mid_c'] - (df['gain'] / trade_settings.riskreward), 
                        np.where(df['signal'] == SELL, df['mid_c'] + (df['gain'] / trade_settings.riskreward), 0.0))
    
    df['loss'] = abs(df['mid_c'] - df['SL'])
    
    # Plug and play: bot.py can execute any strategy as long as following cols in log_cols are returned
    # Build whatever strategy as wished; the rest of the code will work as long as log_cols's cols are returned
    log_cols = ['pair', 'time', 'mid_c', 'mid_o', 'SL', 'TP', 'spread', 'gain', 'loss', 'signal']
    
    log_message(f'technicals_manager.py --> process_candles(): \n {df[log_cols].tail()}', pair)
    
    return df[log_cols].iloc[-1]
    

def fetch_candles(pair, rows, candle_time, granularity, api: OandaAPI, log_message):
    df = api.get_candles_df(pair, count=rows, granularity=granularity)
    
    if df is None or df.shape[0] == 0:
        log_message('technicals_manager.py --> fetch_candles(): Failed to get candles', pair)
        return None
    
    # Fetch the current candle (the [-1] one)
    # Any pair that comes before are past candles
    if df.iloc[-1]['time'] != candle_time:
        tries = 0
        
        while tries < 3:
            df = api.get_candles_df(pair, count=rows, granularity=granularity)
            
            if df.iloc[-1]['time'] == candle_time:
                break
        
        if df.iloc[-1]['time'] != candle_time:
            log_message(f'technicals_manager.py --> fetch_candles(): {df.iloc[-1]['time']} not correct', pair)
            return None
    
    return df


def get_trade_decision(candle_time, pair, granularity, api: OandaAPI, trade_settings: TradeSettings, log_message, add_rows):
    max_rows = trade_settings.n_ma + add_rows
    
    log_message(f'technicals_manager.py --> get_trade_decision(): \n max_rows: {max_rows} \n candle_time: {candle_time} \n granularity: {granularity}', pair)
    
    df = fetch_candles(pair, max_rows, candle_time, granularity, api, log_message)
    
    if df is not None:
      last_row = process_candles(df, pair, trade_settings, log_message)  
      print(last_row)
      return TradeDecision(last_row)
    
    else:
        print('none')
    
    return None
    