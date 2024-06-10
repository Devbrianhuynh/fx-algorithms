import json
import threading
import time
from queue import Queue

from streaming_api.stream_prices import PriceStreamer
from streaming_api.stream_processor import PriceProcessor
from streaming_api.stream_worker import WorkProcessor


def load_settings(path, name):
    with open(f'./{path}/{name}.json', 'r') as file:
        return json.loads(file.read())
    
    
def run_streamer(path, name):
    settings = load_settings(path, name)
    
    shared_prices = {}
    shared_prices_events = {}
    shrared_prices_lock = threading.Lock()
    work_queue = Queue()
    
    for pair in settings['pairs'].keys():
        shared_prices_events[pair] = threading.Event()
        shared_prices[pair] = {}
        
    threads = []
    
    price_stream_thread = PriceStreamer(shared_prices, shrared_prices_lock, shared_prices_events)
    price_stream_thread.daemon = True
    threads.append(price_stream_thread)
    price_stream_thread.start()
    
    worker_thread = WorkProcessor(work_queue)
    worker_thread.daemon = True
    threads.append(worker_thread)
    worker_thread.start()
    
    for pair in settings['pairs'].keys():
        processing_thread = PriceProcessor(shared_prices, shrared_prices_lock, shared_prices_events, f'PriceProcessor_{pair}', pair, work_queue)
        processing_thread.daemon = True
        threads.append(processing_thread)
        processing_thread.start()
    
    # Windows
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    
    # # macOS/Linux
    # try:
    #     for t in threads:
    #         t.join()
    # except KeyboardInterrupt:
    #     print('KeyboardInterrupt')
        
    print('all done.')
    
    