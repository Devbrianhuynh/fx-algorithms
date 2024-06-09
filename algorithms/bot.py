import json
import time

from algorithms.candle_manager import CandleManager
from algorithms.technicals_manager import get_trade_decision
from algorithms.trade_manager import place_trade
from constants.defs import *
from infrastructure.log_wrapper import LogWrapper
from models.trade_settings import TradeSettings
from api.oanda_api import OandaAPI


class Bot:
    ERROR_LOG = 'error'
    MAIN_LOG = 'main'
    
    def __init__(self, settings_path, settings_name, granularity, sleep):
        self.load_settings(settings_path, settings_name)
        self.setup_logs()
        self.log_to_main('__init__(): Bot started')
        self.log_to_error('__init__(): Bot started')
        
        self.granularity = granularity
        self.api = OandaAPI()
        self.candle_manager = CandleManager(self.api, self.trade_settings, self.log_message, self.granularity)
        self.sleep = sleep
        
        
    def load_settings(self, path, name):
        with open(f'{path}/{name}.json', 'r') as file:
            data = json.loads(file.read())
            
            self.trade_settings = {key:TradeSettings(value, key) for key, value in data['pairs'].items()}
            self.trade_risk = data['trade_risk']
        
    
    def setup_logs(self):
        self.logs = {}
        
        for key in self.trade_settings.keys():
            self.logs[key] = LogWrapper(key)
            self.log_message(f'{self.trade_settings[key]}', key)
        
        self.logs[Bot.ERROR_LOG] = LogWrapper(Bot.ERROR_LOG)
        self.logs[Bot.MAIN_LOG] = LogWrapper(Bot.MAIN_LOG)
        
        self.log_to_main(f'setup_logs(): Bot started with {TradeSettings.settings_to_str(self.trade_settings)}')
        
    
    def log_message(self, msg, key):
        self.logs[key].logger.debug(msg)
    
    
    def log_to_main(self, msg):
        self.log_message(msg, Bot.MAIN_LOG)
        
    
    def log_to_error(self, msg):
        self.log_message(msg, Bot.ERROR_LOG)
        
    
    def process_candles(self, triggered):
        if len(triggered) > 0:
            self.log_to_main(f'process_candles(): Triggered: {triggered}')
            
            for pair in triggered:
                last_time = self.candle_manager.timings[pair].last_time
                trade_decision = get_trade_decision(last_time, pair, self.granularity, self.api, self.trade_settings[pair], self.log_message, 20)
                
                if trade_decision is not None and trade_decision.signal != NONE:
                    self.log_message(f'process_candles(): Place trade: {trade_decision}', pair)
                    self.log_message(f'process_candles(): Place trade: {trade_decision}')
                    
                    place_trade(trade_decision, self.api, self.log_message, self.log_to_error, self.trade_risk)
                
        
    def run(self):
        while True:
            time.sleep(self.sleep)
            
            try:
                triggered = self.candle_manager.update_timings()
                self.process_candles(triggered)
            except Exception as error:
                self.log_to_error(f'run(): crash: {error}')
                break
        