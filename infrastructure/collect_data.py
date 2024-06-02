import pandas as pd
import datetime as dt
from dateutil import parser

from infrastructure.instrument_collection import InstrumentCollection
from api.oanda_api import OandaAPI


CANDLE_COUNT = 3000
INCREMENTS = {
    'M5': 5 * CANDLE_COUNT,
    'M15': 15 * CANDLE_COUNT,
    'H1': 60 * CANDLE_COUNT,
    'H4': 240 * CANDLE_COUNT
}


def save_file(df_final: pd.DataFrame, file_prefix, granularity, pair):
    filename = f'{file_prefix}{pair}_{granularity}.pkl'
    
    df_final.drop_duplicates(subset=['time'], inplace=True)
    df_final.sort_values(by='time', inplace=True)
    df_final.reset_index(drop=True, inplace=True)
    df_final.to_pickle(filename)
    
    print(f'*** {pair} - {granularity} - {df_final['time'].min()} - {df_final['time'].max()} --> {df_final.shape[0]} candles ***')


def fetch_candles(pair, granularity, date_from: dt.datetime, date_to: dt.datetime, api: OandaAPI):
    attempts = 0
    
    while attempts < 3:
        df_candles = api.get_candles_df(pair, granularity=granularity, date_from=date_from, date_to=date_to)
        
        if df_candles is not None:
            break
        
        attempts += 1
    
    if df_candles is not None and df_candles.empty is False:
        return df_candles
    
    return None


def collect_data(pair, granularity, date_from, date_to, file_prefix, api: OandaAPI):
    time_step = INCREMENTS[granularity]
    
    end_date = parser.parse(date_to)
    from_date = parser.parse(date_from)
    
    candle_dfs = []
    
    to_date = from_date
    
    while to_date < end_date:
        to_date = from_date + dt.timedelta(minutes=time_step)
        
        if to_date > end_date:
            to_date = end_date
            
        candles = fetch_candles(pair, granularity, from_date, to_date, api)
        
        if candles is not None:
            candle_dfs.append(candles)
            print(f'Pair: {pair} - Granularity: {granularity} - From date: {from_date} - To date: {to_date} --> {candles.shape[0]} candles loaded')
        else:
            print(f'Pair: {pair} - Granularity: {granularity} - From date: {from_date} - To date: {to_date} --> NO CANDLES!')
        
        from_date = to_date
    
    if len(candle_dfs) > 0:
        df_final = pd.concat(candle_dfs)
        save_file(df_final, file_prefix, granularity, pair)
    else:
        print(f'Pair: {pair} - Granularity: {granularity} --> NO DATA SAVED!')
    

def run_collection(instr_col: InstrumentCollection, api: OandaAPI):
    currencies = ['USD', 'CHF', 'GBP', 'EUR', 'JPY', 'AUD']
    
    for curr_1 in currencies:
        for curr_2 in currencies:
            pair = f'{curr_1}_{curr_2}'
            
            if pair in instr_col.instruments_dict.keys():
                for gran in ['M5', 'M15', 'H1', 'H4']:
                    print(f'{pair} - {gran}')
                    
                    collect_data(pair, gran, '2016-01-01T00:00:00Z', '2024-06-01T00:00:00Z', './data/', api)
