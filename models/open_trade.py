from dateutil import parser

class OpenTrade:
    def __init__(self, api_obj):
        self.id = api_obj['id']
        self.instrument = api_obj['instrument']
        self.price = float(api_obj['price'])
        self.current_units = float(api_obj['currentUnits'])
        self.unrealized_pl = float(api_obj['unrealizedPL'])
        self.margin_used = float(api_obj['marginUsed'])

        
    def __repr__(self):
        return str(vars(self))
