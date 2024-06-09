class Instrument:
    def __init__(self, name, ins_type, dispay_name, pip_location, trade_units_precision, margin_rate, display_precision):
        self.name = name
        self.ins_type = ins_type
        self.display_name = dispay_name
        self.pip_location = pow(10, pip_location)
        self.trade_units_precision = trade_units_precision
        self.margin_rate = float(margin_rate)
        self.display_precision = display_precision
        
    
    def __repr__(self):
        return str(vars(self))
    
    
    @classmethod
    def from_api_obj(cls, obj):
        return Instrument(
            obj['name'],
            obj['type'],
            obj['displayName'],
            obj['pipLocation'],
            obj['tradeUnitsPrecision'],
            obj['marginRate'],
            obj['displayPrecision']
        )
