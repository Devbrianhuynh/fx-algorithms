import copy
import random
import threading
import time
from queue import Queue

from streaming_api.stream_base import StreamBase


class PriceProcessor(StreamBase):
    def __init__(self, shared_prices: dict, price_lock: threading.Lock, price_events, log_name, pair, work_queue: Queue):
        super().__init__(shared_prices, price_lock, price_events, log_name)
        
        self.pair = pair
        self.work_queue = work_queue
        

    def process_price(self):
        price = None
        
        try:
            self.price_lock.acquire() 
            price = copy.deepcopy(self.shared_prices[self.pair])
        except Exception as error:
            self.log_message(f'stream_processor.py --> process_price(): Crash: {error}', error=True)
        finally:
            self.price_lock.release()
            
        if price is None:
            self.log_message('stream_processor.py --> process_price(): No price', error=True)
        else:
            self.log_message(f'stream_processor.py --> process_price(): Found price: {price}')
            
            # Computations and algorithms
            # Trading decisions, candle logic, technical indicator(s):
            time.sleep(random.randint(2, 5))

            self.log_message(f'stream_processor.py --> process_price(): Done processing price: {price}')
            
            # Do something here:
            # If signaled a trade, place trade here
            if random.randint(0, 5) == 3:
                self.log_message(f'stream_processor.py --> process_price(): Adding work: {price}')
                self.work_queue.put(price)

    
    def run(self):
        while True:
            self.price_events[self.pair].wait()
            
            # Candle logic and technical indicator(s) code:
            self.process_price()
            
            self.price_events[self.pair].clear()

        
    