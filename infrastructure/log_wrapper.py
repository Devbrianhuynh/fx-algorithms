import logging
import os


LOG_FORMAT = '%(asctime)s %(message)s'
SET_LEVEL = logging.DEBUG

class LogWrapper:
    def __init__(self, name, mode='w', path='./logs'):
        self.name = name
        self.mode = mode
        self.path = path
        
        self.create_directory()
        
        self.filename = f'{self.path}/{name}.log'
        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        file_handler = logging.FileHandler(self.filename, mode=self.mode)
        
        formatter = logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        
        self.logger.info(f'LogWrapper __init__(): {self.filename}')
    
    
    def create_directory(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

