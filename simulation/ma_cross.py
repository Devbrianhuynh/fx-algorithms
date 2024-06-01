import pandas as pd
import os.path
from infrastructure.instrument_collection import instrument_collection as ic


class MovingAverageResult:
    def __init__(self, df_trades, pair, ma_long, ma_short, granularity):
        self.df_trades = df_trades
        self.pair = pair
        self.ma_long = ma_long
        self.ma_short = ma_short
        self.granularity = granularity
        
        self.result = self.result_obj()
        
    
    def __repr__(self):
        return str(self.result) 
        
    
    def result_obj(self):
        return {
            'pair': self.pair,
            'num_trades': self.df_trades.shape[0],
            'total_gain': int(self.df_trades['gain'].sum(numeric_only=True)),
            'mean_gain': int(self.df_trades['gain'].mean(numeric_only=True)),
            'min_gain': int(self.df_trades['gain'].min(numeric_only=True)),
            'max_gain': int(self.df_trades['gain'].max(numeric_only=True)),
            'ma_long': self.ma_long,
            'ma_short': self.ma_short,
            'cross': f'{self.ma_short}_{self.ma_long}',
            'granularity': self.granularity
        }


BUY = 1
SELL = -1
NONE = 0

get_ma_col = lambda x: f'MA_{x}'
add_cross = lambda x: f'{x.ma_short}_{x.ma_long}'


def is_trade(row):
    if row['delta'] >= 0 and row['delta_prev'] < 0:
        return BUY
    elif row['delta'] < 0 and row['delta_prev'] >= 0:
        return SELL
    
    return NONE


def load_prices_data(pair, granularity, ma_list):
    df = pd.read_pickle(f'./data/{pair}_{granularity}.pkl')
    
    for ma in ma_list:
        df[get_ma_col(ma)] = df['mid_c'].rolling(window=ma).mean()
    
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    return df


def get_trades(df_analysis, instrument, granularity):
    df_trades = df_analysis[df_analysis['trade'] != NONE].copy()
    
    df_trades['diff'] = df_trades['mid_c'].diff().shift(-1)
    df_trades.fillna(value=0, inplace=True)
    df_trades['gain'] = df_trades['diff'] / instrument.pip_location
    df_trades['gain'] = df_trades['gain'] * df_trades['trade']
    df_trades['gain_cum'] = df_trades['gain'].cumsum()
    df_trades['granularity'] = granularity
    df_trades['pair'] = instrument.name
    
    return df_trades


def assess_pair(price_data, long, short, instrument, granularity):
    df_analysis = price_data.copy()
    df_analysis['delta'] = df_analysis[short] - df_analysis[long]
    df_analysis['delta_prev'] = df_analysis['delta'].shift(1)
    df_analysis['trade'] = df_analysis.apply(is_trade, axis=1)
    
    df_trades = get_trades(df_analysis, instrument, granularity)
    df_trades['ma_long'] = long
    df_trades['ma_short'] = short
    df_trades['cross'] = df_trades.apply(add_cross, axis=1)
    
    return MovingAverageResult(df_trades=df_trades, pair=instrument.name, ma_long=long, ma_short=short, granularity=granularity)


def append_df_to_file(df, filename):
    if os.path.isfile(filename):
        existing_file = pd.read_pickle(filename)
        df = pd.concat([existing_file, df]) 
    
    df.reset_index(drop=True, inplace=True)
    df.to_pickle(filename)
    
    print(filename, df.shape)
    print(df.head())


def get_fullname(filepath, filename):
    return f'{filepath}/{filename}.pkl'


def process_macro(results, filename):
    results = [res.result for res in results]
    df = pd.DataFrame.from_dict(results)
    append_df_to_file(df, filename)


def process_trades(results, filename):
    df = pd.concat([res.df_trades for res in results])
    append_df_to_file(df, filename)


def process_results(ma_results, filepath):
    process_macro(ma_results, get_fullname(filepath, 'ma_res'))
    process_trades(ma_results, get_fullname(filepath, 'ma_trades'))
    

def analyze_pair(instrument, granularity, ma_long, ma_short, filepath):
    ma_list = set(ma_long + ma_short)
    pair = instrument.name
    
    price_data = load_prices_data(pair, granularity, ma_list)
    
    ma_results = []
    
    for long in ma_long:
        for short in ma_short:
            
            if long <= short:
                continue
            
            ma_result = assess_pair(price_data, get_ma_col(long), get_ma_col(short), instrument, granularity)
            ma_results.append(ma_result)
    
    process_results(ma_results, filepath)
            

def run_ma_sim(currencies=['USD', 'GBP', 'CHF'], granularity=['H1', 'H4'], ma_long=[20, 21, 50, 200], ma_short=[10, 20, 50], filepath='./data'):
    ic.load_instruments('./data')
    
    for gran in granularity:
        for curr_1 in currencies:
            for curr_2 in currencies:
                pair = f'{curr_1}_{curr_2}'
                
                if pair in ic.instruments_dict.keys():
                    analyze_pair(ic.instruments_dict[pair], gran, ma_long, ma_short, filepath)                    
                    