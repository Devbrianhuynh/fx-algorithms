import os
from api.oanda_api import OandaAPI
from infrastructure.instrument_collection import instrument_collection
from simulation.ma_cross import run_ma_sim
from simulation.ema_macd_mp import run_ema_macd
from simulation.performance_metrics import *
from dateutil import parser
from infrastructure.collect_data import run_collection



if __name__ == '__main__':
    df = get_df('./data', 'EUR_USD', 'M5')
    print(get_iloc_performance(df))
    print(get_arr_performance(df))
    print(get_items_performance(df))
    
    # print(os.cpu_count())
    
    # instrument_collection.load_instruments('./data')
    # run_ema_macd(instrument_collection, ['USD', 'CHF', 'GBP', 'EUR', 'JPY', 'AUD'])
    
    # instrument_collection.load_instruments('./data')
    # run_ema_macd(instrument_collection)
    
    # run_ma_sim()
    
    # oanda_api = OandaAPI()
    
    # instrument_collection.load_instruments('./data')
    # run_collection(instrument_collection, oanda_api)

    # date_from = parser.parse('2022-11-28T00:00:00Z')
    # date_to = parser.parse('2022-11-29T00:00:00Z')
    
    # df_candles = oanda_api.get_candles_df('USD_CHF', granularity='M15', date_from=date_from, date_to=date_to)
    
    # print('Head')
    # print(df_candles.head())
    # print('Tail')
    # print(df_candles.tail())
    
    