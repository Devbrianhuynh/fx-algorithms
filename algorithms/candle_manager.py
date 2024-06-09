from api.oanda_api import OandaAPI
from models.candle_timing import CandleTiming


class CandleManager:
    def __init__(self, api: OandaAPI, trade_settings: dict, log_message, granularity):
        self.api = api
        self.trade_settings = trade_settings
        self.log_message = log_message
        self.granularity = granularity
        self.pairs_lst = list(self.trade_settings.keys())
        self.timings = {pair:CandleTiming(self.api.last_complete_candle(pair, self.granularity)) for pair in self.pairs_lst}
        
        for key, value in self.timings.items():
            self.log_message(f'candle_manager.py --> CandleManager() __init__(): \n Last candle: {value}', key)
            
    
    def update_timings(self):
        triggered = []
        
        for pair in self.pairs_lst:
            current = self.api.last_complete_candle(pair, self.granularity)
            
            if current is None:
                self.log_message('candle_manager.py --> update_timings(): Unable to fetch candle', pair)
                continue
            
            self.timings[pair].is_ready = False
            
            if current >= self.timings[pair].last_time:
                self.timings[pair].is_ready = True
                self.timings[pair].last_time = current
                
                self.log_message(f'candle_manager.py --> CandleManager() update_timings(): \n New candle: {self.timings[pair]}', pair)
                
                triggered.append(pair)
            
        return triggered
                
        