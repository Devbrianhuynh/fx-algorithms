import time

from algorithms.trade_risk_calculator import get_trade_units
from api.oanda_api import OandaAPI
from constants.defs import *
from infrastructure.instrument_collection import instrument_collection
from models.candle_timing import CandleTiming


def log_msg(msg, pair):
    print(msg, pair)

if __name__ == '__main__':
    api = OandaAPI()
    
    instrument_collection.load_instruments('./data')
    
    # print(api.get_prices(['USD_CHF']))
    
    print(get_trade_units(api, 'USD_CAD', BUY, 0.007, 15, log_msg))
    
    
    