class TradeSettings:
    def __init__(self, obj, pair):
        self.n_ma = obj['n_ma']
        self.n_std = obj['n_std']
        self.maxspread = obj['maxspread']
        self.mingain = obj['mingain']
        self.riskreward = obj['riskreward']
        
        
    def __repr__(self):
        return str(vars(self))
    
    
    @classmethod
    def settings_to_str(cls, settings: dict):
        return_str = 'Trade settings:\n'
        
        for _, value in settings.items():
            return_str += f'{value}\n'
            
        return return_str
            