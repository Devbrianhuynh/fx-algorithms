class BaseAPIPrice:
    def __init__(self, api_obj):
        self.instrument = api_obj['instrument']
        self.ask = float(api_obj['asks'][0]['price'])
        self.bid = float(api_obj['bids'][0]['price'])
        
       
        
        