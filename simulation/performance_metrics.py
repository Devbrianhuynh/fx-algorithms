import pandas as pd
from timeit import default_timer as timer


def get_df(path, pair, granularity):
    df = pd.read_pickle(f'{path}/{pair}_{granularity}.pkl')
    print(f'# of rows: {df.shape[0]}')
    
    return df


def get_iterrows_performance(df: pd.DataFrame):
    start = timer()
    
    for _, row in df.iterrows():
        # Calculations are for testing purposes only
        val_1 = row['mid_c'] * 12
        val_2 = row['mid_h'] - 14
    
    return f'df.iterrows() --> {(timer() - start):.4f}s'


def get_iloc_performance(df: pd.DataFrame):
    start = timer()
    
    for i in range(df.shape[0]):
        val_1 = df['mid_c'].iloc[i] * 12
        val_2 = df['mid_h'].iloc[i] - 14
    
    return f'.iloc[i] --> {(timer() - start):.4f}s'


def get_arr_performance(df: pd.DataFrame):
    start = timer()
    
    arr_1 = df['mid_c'].array
    arr_2 = df['mid_h'].array
    
    for i in range(df.shape[0]):
        val_1 = arr_1[i] * 12
        val_2 = arr_2[i] * 14
        
    return f'arr_#[i] --> {(timer() - start):.4f}s'


def get_items_performance(df: pd.DataFrame):
    start = timer()
    items = [df['mid_c'].array, df['mid_h'].array]
    
    for i in range(df.shape[0]):
        val_1 = items[0][i] * 12
        val_2 = items[1][i] - 14
    
    return f'items[i] --> {(timer() - start):.4f}s'
