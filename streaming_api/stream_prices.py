import threading
import json
import requests
import pandas as pd
from timeit import default_timer as timer

from constants.defs import SECURE_HEADER, STREAM_URL, ACCOUNT_ID
from infrastructure.log_wrapper import LogWrapper
from models.live_api_price import LiveAPIPrice
from streaming_api.stream_base import StreamBase


class PriceStreamer(StreamBase):
    LOG_FREQ = 60
    
    def __init__(self, shared_prices: dict, price_lock: threading.Lock, price_events):
        super().__init__(shared_prices, price_lock, price_events, 'PriceStreamer')
    
        self.pairs_lst = list(shared_prices.keys())
        
    
    def fire_new_price_event(self, instrument):
        if self.price_events[instrument].is_set() is False:
            self.price_events[instrument].set() 
        
    
    def update_live_price(self, live_api_price: LiveAPIPrice):
        try:
            self.price_lock.acquire()
            self.shared_prices[live_api_price.instrument] = live_api_price
            self.fire_new_price_event(live_api_price.instrument)
        except Exception as error:
            self.log_message(f'stream_prices.py --> update_live_price: Exception: {error}', error=True)
        finally:
            self.price_lock.release()
            
    
    def log_data(self):
        df = pd.DataFrame.from_dict([value.get_dict() for _, value in self.shared_prices.items()])
        self.log_message(f'\n{df}\n')
            

    def run(self):
        start = timer() - PriceStreamer.LOG_FREQ + 10
        
        params = {
            'instruments': ','.join(self.pairs_lst)
        }

        url = f'{STREAM_URL}/accounts/{ACCOUNT_ID}/pricing/stream'

        res = requests.get(url=url, params=params, headers=SECURE_HEADER, stream=True)

        # NOTICE: Find a way to fetch the open, high, low, and close candle prices from the streaming API
        # Build the technical indicators and trade placing from there
        for price in res.iter_lines():
            if price:
                decoded_price = json.loads(price.decode('utf-8'))
              
                if 'type' in decoded_price and decoded_price['type'] == 'PRICE':
                    self.update_live_price(LiveAPIPrice(decoded_price))
                    print(decoded_price)
                    if (timer() - start) > (PriceStreamer.LOG_FREQ):
                        print(LiveAPIPrice(decoded_price).get_dict())
                        
                        self.log_data()
                        start = timer()
                    
                    
                
