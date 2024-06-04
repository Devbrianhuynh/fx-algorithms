import pandas as pd
from candle_pattern_criteria import *


# Single candlestick patterns
def apply_hanging_man(row):
    return row['body_bottom_perc'] > HANGING_MAN_HEIGHT and row['body_perc'] < HANGING_MAN_BODY


def apply_shooting_star(row):
    return row['body_top_perc'] < SHOOTING_STAR_HEIGHT and row['body_perc'] < SHOOTING_STAR_BODY


def apply_spinning_top(row):
    return row['body_top_perc'] < SPINNING_TOP_MAX and row['body_bottom_perc'] > SPINNING_TOP_MIN and row['body_perc'] < SPINNING_TOP_BODY


def apply_marubozu(row):
    return row['body_perc'] > MARUBOZU_BODY


# Dual candlestick patterns
def apply_engulfing(row):
    if row['direction'] != row['direction_prev']:
        if row['body_size'] > row['body_size_prev'] * ENGULFING_FACTOR:
            return True
    return False


def apply_tweezer_top(row):
    if abs(row['body_size_change']) < TWEEZER_BODY:
        if row['direction'] == -1 and row['direction'] != row['direction_prev']:
            if abs(row['low_change']) < TWEEZER_HL and abs(row['high_change']) < TWEEZER_HL:
                if row['body_top_perc'] < TWEEZER_TOP_BODY:
                    return True
    return False


def apply_tweezer_bottom(row):
    if abs(row['body_size_change']) < TWEEZER_BODY:
        if row['direction'] == 1 and row['direction'] != row['direction_prev']:
            if abs(row['low_change']) < TWEEZER_HL and abs(row['high_change']) < TWEEZER_HL:
                if row['body_bottom_perc'] > TWEEZER_BOTTOM_BODY:
                    return True
    return False


# Triple candlestick pattern
def apply_morning_star(row, direction=1):
    if row['body_perc_prev_2'] > MORNING_STAR_PREV_2_BODY:
        if row['body_perc_prev'] < MORNING_STAR_PREV_BODY:
            if row['direction'] == direction and row['direction_prev_2'] != direction:
                if direction == 1:
                    if row['mid_c'] > row['mid_point_prev_2']:
                        return True
                else:
                    if row['mid_c'] < row['mid_point_prev_2']:
                        return True
    return False


def apply_candle_props(df: pd.DataFrame):
    df_analysis = df.copy()
    
    direction = df_analysis['mid_c'] - df_analysis['mid_o']
    body_size = abs(direction)
    full_range = df_analysis['mid_h'] - df_analysis['mid_l']
    body_perc = (body_size / full_range) * 100
    body_lower = df_analysis[['mid_c', 'mid_o']].min(axis=1)
    body_upper = df_analysis[['mid_c', 'mid_o']].max(axis=1)
    body_bottom_perc = ((body_lower - df_analysis['mid_l']) / full_range) * 100
    body_top_perc = 100 - (((df_analysis['mid_h'] - body_upper) / full_range) * 100)
    
    direction = [1 if x >= 0 else -1 for x in direction]
    
    mid_point = full_range / 2 + df_analysis['mid_l']
    
    low_change = df_analysis['mid_l'].pct_change() * 100
    high_change = df_analysis['mid_h'].pct_change() * 100
    body_size_change = body_size.pct_change() * 100
    
    df_analysis['body_lower'] = body_lower
    df_analysis['body_upper'] = body_upper
    df_analysis['body_bottom_perc'] = body_bottom_perc
    df_analysis['body_top_perc'] = body_top_perc
    df_analysis['body_perc'] = body_perc
    
    df_analysis['direction'] = direction
    
    df_analysis['body_size'] = body_size
    df_analysis['body_size_change'] = body_size_change
    
    df_analysis['low_change'] = low_change
    df_analysis['high_change'] = high_change
    
    df_analysis['mid_point'] = mid_point
    df_analysis['mid_point_prev_2'] = mid_point.shift(2)
    
    df_analysis['body_size_prev'] = df_analysis['body_size'].shift(1)

    df_analysis['direction_prev'] = df_analysis['direction'].shift(1)
    df_analysis['direction_prev_2'] = df_analysis['direction'].shift(2)

    df_analysis['body_perc_prev'] = df_analysis['body_perc'].shift(1)
    df_analysis['body_perc_prev_2'] = df_analysis['body_perc'].shift(2)
    
    return df_analysis


def set_candle_patterns(df_analysis: pd.DataFrame):
    # Single candlestick patterns
    df_analysis['hanging_man'] = df_analysis.apply(apply_hanging_man, axis=1)
    df_analysis['shooting_star'] = df_analysis.apply(apply_shooting_star, axis=1)
    df_analysis['spinning_top'] = df_analysis.apply(apply_spinning_top, axis=1)
    df_analysis['marubozu'] = df_analysis.apply(apply_marubozu, axis=1)

    # Dual candlestick patterns
    df_analysis['engulfing'] = df_analysis.apply(apply_engulfing, axis=1)
    df_analysis['tweezer_top'] = df_analysis.apply(apply_tweezer_top, axis=1)
    df_analysis['tweezer_bottom'] = df_analysis.apply(apply_tweezer_bottom, axis=1)

    # Triple candlestick patterns
    df_analysis['morning_star'] = df_analysis.apply(apply_morning_star, axis=1)
    df_analysis['evening_star'] = df_analysis.apply(apply_morning_star, axis=1, direction=-1)
    
    
def apply_patterns(df: pd.DataFrame):
    df_analysis = apply_candle_props(df)
    set_candle_patterns(df_analysis)
    
    return df_analysis
    