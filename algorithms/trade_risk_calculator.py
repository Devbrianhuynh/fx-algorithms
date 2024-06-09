from api.oanda_api import OandaAPI
from constants.defs import *
from infrastructure.instrument_collection import instrument_collection as ic


def get_trade_units(api: OandaAPI, pair, signal, loss, trade_risk, log_message):
    prices = api.get_prices([pair])
    
    if prices is None or len(prices) == 0:
        log_message('trade_risk_calculator.py --> get_trade_units(): Prices is None', pair)
        return False
    
    price = None
    
    for p in prices:
        if p.instrument == pair:
            price = p
            break
    
    if price is None:
        log_message('trade_risk_calculator.py --> get_trade_units(): Prices is assuredly None', pair)
        return False
    
    log_message(f'trade_risk_calculator.py --> get_trade_units(): Success: Price: {price}', pair)
    
    conv_rate = price.buy_conv
    
    if signal == SELL:
        conv_rate = price.sell_conv

    pip_location = ic.instruments_dict[pair].pip_location
    num_pips = loss / pip_location
    per_pip_loss = trade_risk / num_pips
    units = per_pip_loss / (conv_rate * pip_location)
    
    log_message(f'trade_risk_calculator.py --> get_trade_units(): pip_location: {pip_location} - num_pips: {num_pips} - per_pip_loss: {per_pip_loss} - units: {units:.1f}', pair)

    return units
    
    
        
