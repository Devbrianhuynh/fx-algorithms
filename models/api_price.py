class APIPrice:
    def __init__(self, api_obj, home_conversions):
        self.instrument = api_obj['instrument']
        self.ask = float(api_obj['asks'][0]['price'])
        self.bid = float(api_obj['bids'][0]['price'])
        
        quote_currency = self.instrument.split('_')[1]
        
        for hc in home_conversions:
            if hc['currency'] == quote_currency:
                self.sell_conv = float(hc['positionValue'])
                self.buy_conv = float(hc['positionValue'])
        
    
    def __repr__(self):
        return f'APIPrice(): Instrument: {self.instrument} - Ask: {self.ask} - Bid: {self.bid} - Sell conversion: {self.sell_conv:.6f} - Buy conversion: {self.buy_conv:.6f}'
        
        