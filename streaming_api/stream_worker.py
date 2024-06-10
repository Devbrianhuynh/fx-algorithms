import threading
import time
from queue import Queue

from infrastructure.log_wrapper import LogWrapper
from models.live_api_price import LiveAPIPrice


class WorkProcessor(threading.Thread):
    def __init__(self, work_queue: Queue):
        super().__init__()
        self.work_queue = work_queue
        self.log = LogWrapper('WorkProcessor')
        
    
    def run(self):
        while True:
            work: LiveAPIPrice = self.work_queue.get()
            self.log.logger.debug(f'stream_worker.py --> run(): New work: {work}')

            # Computations
            # Trading decisions, technical indicator(s), placing trades, etc.
            time.sleep(5)
            