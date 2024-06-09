class TradeDecision:
    def __init__(self, row):
        self.gain = row['gain']
        self.loss = row['loss']
        self.signal = row['signal']
        self.SL = row['SL']
        self.TP = row['TP']
        self.pair = row['pair']
        
        
    def __repr__(self):
        return f'Pair: {self.pair} - Signal: {self.signal} - Gain: {self.gain} - SL: {self.SL} - TP: {self.TP}'