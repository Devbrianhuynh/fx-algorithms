from dateutil import parser

from models.base_api_price import BaseAPIPrice


class LiveAPIPrice(BaseAPIPrice):
    def __init__(self, api_obj):
        super().__init__(api_obj)
        self.time = parser.parse(api_obj['time'])
        
        
    def __repr__(self):
        return f'LiveAPIPrice(): Instrument: {self.instrument} - Ask: {self.ask} - Bid: {self.bid} - Time: {self.time}'

    
    def get_dict(self):
        return {
            'instrument': self.instrument,
            'time': self.time,
            'ask': self.ask,
            'bid': self.bid
        }
    
    
    