import sys
sys.path.append('../')

import pandas as pd
import datetime as dt
import numpy as np

from simulation.constants import *


# Direction on patterns and direction on ema/macd will conflict; make sure to change the generic name to a descriptive one
def apply_take_profit(row, profit_factor):
    if row['signal'] != NONE:
        if row['signal'] == BUY:
            if row['direction'] == BUY:
                return (row['ask_c'] - row['ask_o']) * profit_factor + row['ask_c']
            else:
                return (row['ask_o'] - row['ask_c']) * profit_factor + row['ask_o']
        else:
            if row['direction'] == SELL:
                return (row['bid_c'] - row['bid_o']) * profit_factor + row['bid_c']
            else:
                return (row['bid_o'] - row['bid_c']) * profit_factor + row['bid_o']
    else:
        return 0.0
    

def apply_stop_loss(row):
    if row['signal'] != NONE:
        if row['signal'] == BUY:
            if row['direction'] == BUY:
                return row['ask_o']
            else:
                return row['ask_c']
        else:
            if row['direction'] == SELL:
                return row['bid_o']
            else:
                return row['bid_c']
    else:
        return 0.0
    

def remove_spread(df):
    for price in ['ask', 'bid']:
        for point in ['o', 'h', 'l', 'c']:
            price_point = f'{price}_{point}'
            df[price_point] = df[f'mid_{point}']
            

def apply_signals(df: pd.DataFrame, profit_factor, signal):
    df['signal'] = signal(df)
    df['TP'] = df.apply(apply_take_profit, axis=1, profit_factor=profit_factor)
    df['SL'] = df.apply(apply_stop_loss, axis=1)
    
    
def create_signals(df: pd.DataFrame, time_delta=1):
    df_signals = df[df['signal'] != NONE].copy()
    df_signals['m5_start'] = [x + dt.timedelta(hours=time_delta) for x in df_signals['time']]
    df_signals.drop(['time', 'mid_o', 'mid_h', 'mid_l', 'bid_o', 'bid_h', 'bid_l', 'ask_o', 'ask_h', 'ask_l', 'direction'],
                    axis=1, inplace=True)
    
    df_signals.rename(columns={
        'bid_c': 'start_price_buy',
        'ask_c': 'start_price_sell',
        'm5_start': 'time'
    }, inplace=True)
    
    return df_signals


class Trade:
    def __init__(self, row, i, profit_factor, loss_factor):
        self.running = True
        self.start_index_m5 = row[INDEX_NAME][i]
        self.profit_factor = profit_factor
        self.loss_factor = loss_factor
        
        if row[INDEX_SIGNAL][i] == BUY:
            self.start_price = row[INDEX_START_PRICE_BUY][i]
            self.trigger_price = row[INDEX_START_PRICE_BUY][i]
        elif row[INDEX_SIGNAL][i] == SELL:
            self.start_price = row[INDEX_START_PRICE_SELL][i]
            self.trigger_price = row[INDEX_START_PRICE_SELL][i]
        
        self.signal = row[INDEX_SIGNAL][i]
        self.TP = row[INDEX_TP][i]
        self.SL = row[INDEX_SL][i]
        self.result = 0.0
        self.start_time = row[INDEX_TIME][i]
        self.end_time = row[INDEX_TIME][i]
        
    
    def close_trade(self, row, i, result, trigger_price):
        self.running = False
        self.result = result
        self.end_time = row[INDEX_TIME][i]
        self.trigger_price = trigger_price
        
        
    def update(self, row, i):
        if self.signal == BUY:
            if row[INDEX_BID_H][i] >= self.TP:
                self.close_trade(row, i, self.profit_factor, row[INDEX_BID_H][i])
            elif row[INDEX_BID_L][i] <= self.SL:
                self.close_trade(row, i, self.loss_factor, row[INDEX_BID_L][i])
                
        elif self.signal == SELL:
            if row[INDEX_ASK_L][i] <= self.TP:
                self.close_trade(row, i, self.profit_factor, row[INDEX_ASK_L][i])
            elif row[INDEX_ASK_H][i] >= self.SL:
                self.close_trade(row, i, self.loss_factor, row[INDEX_ASK_H][i])
                

# Time delta: Granularity; can change to any hour as needed and will match df['time'] with df_m5['time']
class GuruTester:
    def __init__(self, df_big: pd.DataFrame, apply_signal, df_m5: pd.DataFrame, use_spread=True, loss_factor=-1.0, profit_factor=1.5, time_delta=1):
        self.df_big = df_big.copy()
        self.apply_signal = apply_signal
        self.df_m5 = df_m5.copy()
        self.use_spread = use_spread
        self.loss_factor = loss_factor
        self.profit_factor = profit_factor
        self.time_delta = time_delta
        
        self.prepare_data()
        
    
    def prepare_data(self):
        # print('prepare_data(): Executed')
        
        if self.use_spread is False:
            remove_spread(self.df_big)
            remove_spread(self.df_m5)
            
        apply_signals(self.df_big, self.profit_factor, self.apply_signal)
        
        df_m5_slim = self.df_m5[['time', 'bid_h', 'bid_l', 'ask_h', 'ask_l']].copy()
        df_signals = create_signals(self.df_big, self.time_delta)
        
        self.merged = pd.merge(left=df_m5_slim, right=df_signals, on='time', how='left')
        self.merged.fillna(0, inplace=True)
        self.merged['signal'] = self.merged['signal'].astype(int)
        
    
    def run_test(self):
        list_value_refs = [
            self.merged['start_price_buy'].array,
            self.merged['start_price_sell'].array,
            self.merged['signal'].array,
            self.merged['TP'].array,
            self.merged['SL'].array,
            self.merged['time'].array,
            self.merged['bid_h'].array,
            self.merged['bid_l'].array,
            self.merged['ask_h'].array,
            self.merged['ask_l'].array,
            self.merged.index.array,
        ]
        
        open_trades_m5 = []
        closed_trades_m5 = []
        
        for i in range(self.merged.shape[0]):
            if list_value_refs[INDEX_SIGNAL][i] != NONE:
                open_trades_m5.append(Trade(row=list_value_refs, i=i, profit_factor=self.profit_factor, loss_factor=self.loss_factor))
                
            for ot in open_trades_m5:
                ot.update(list_value_refs, i)

                if ot.running == False:
                    closed_trades_m5.append(ot)
                
            open_trades_m5 = [ot for ot in open_trades_m5 if ot.running is True]
                    
        self.df_results = pd.DataFrame.from_dict([vars(ct) for ct in closed_trades_m5])
    