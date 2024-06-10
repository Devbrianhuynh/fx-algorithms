import os
from dateutil import parser

from api.oanda_api import OandaAPI
from infrastructure.instrument_collection import instrument_collection
from simulation.ma_cross import run_ma_sim
from simulation.ema_macd_mp import run_ema_macd
from simulation.performance_metrics import *
from streaming_api.streamer import run_streamer
from infrastructure.collect_data import run_collection


if __name__ == '__main__':
    api = OandaAPI()
    instrument_collection.load_instruments('./data')
    run_streamer('algorithms', 'settings')
    
    