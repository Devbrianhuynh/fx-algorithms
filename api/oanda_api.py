import requests
import constants.defs as defs
import pandas as pd
import json
from dateutil import parser
from datetime import datetime as dt

from infrastructure.instrument_collection import instrument_collection as ic
from models.open_trade import OpenTrade
from models.api_price import APIPrice


# Make everything declarative
class OandaAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {defs.API_KEY}',
            'Content-Type': 'application/json'
        })
        
    
    def make_request(self, url, verb='get', code=200, params=None, data=None, headers=None):
        api_url = f'{defs.OANDA_URL}/{url}'
        
        if data is not None:
            data = json.dumps(data)
        
        try:
            response = None
            
            if verb == 'get':
                response = self.session.get(api_url, params=params, data=data, headers=headers)
            if verb == 'post':
                response = self.session.post(api_url, params=params, data=data, headers=headers)
            if verb =='put':
                response = self.session.put(api_url, params=params, data=data, headers=headers)
                
            if response is None:
                return False, {'error': 'verb not found'}
            
            if response.status_code == code:
                return True, response.json()
            else:
                return False, response.json()
            
        except Exception as error:
            return False, {'Exception': error}
        
    
    def get_account_endpoint(self, endpoint, data_key):
        url = f'accounts/{defs.ACCOUNT_ID}/{endpoint}'
        ok, data = self.make_request(url=url)
        
        assert ok is True and data_key in data, 'Error get_account_endpoint()'

        return data[data_key]
    
    
    def get_account_summary(self):
        return self.get_account_endpoint(endpoint='summary', data_key='account')
    
    
    def get_account_instruments(self):
        return self.get_account_endpoint(endpoint='instruments', data_key='instruments')
        
    
    def fetch_candles(self, pair, count=10, granularity='H1', price='MBA', date_from=None, date_to=None):
        url = f'instruments/{pair}/candles'

        params = {
            'granularity': granularity,
            'price': price
        }
        
        if date_from is not None and date_to is not None:
            date_format = '%Y-%m-%dT%H:%M:%SZ'
            
            params['from'] = dt.strftime(date_from, date_format)
            params['to'] = dt.strftime(date_to, date_format)
        else:
            params['count'] = count

        ok, data = self.make_request(url, params=params)
        
        assert ok is True and 'candles' in data, f'Error fetch_candles() - Params: {params} - Data: {data}'
        
        return data['candles']
    
    
    def get_candles_df(self, pair, **kwargs):
        data = self.fetch_candles(pair, **kwargs)
        
        if data is None:
            return None
        if len(data) == 0:
            return pd.DataFrame()

        final_data = []

        prices = ['mid', 'bid', 'ask']
        ohlc = ['o', 'h', 'l', 'c']

        for candle in data:
            new_dict = {}

            if candle['complete'] is True:
                new_dict['time'] = parser.parse(candle['time'])
                new_dict['volume'] = candle['volume']

                for price in prices:
                    if price in candle:
                        for o in ohlc:
                            new_dict[f'{price}_{o}'] = float(candle[price][o])

                final_data.append(new_dict)
            else:
                continue
            
        final_data_df = pd.DataFrame.from_dict(data=final_data)
        return final_data_df
    
    
    def last_complete_candle(self, pair, granularity):
        df = self.get_candles_df(pair, granularity=granularity, count=20)
        
        if df.shape[0] == 0:
            return None
        
        return df.iloc[-1]['time']
    
    
    def place_trade(self, pair, units: float, direction: int, stop_loss: float=None, take_profit: float=None):
        url = f'accounts/{defs.ACCOUNT_ID}/orders'
        
        instrument = ic.instruments_dict[pair]
        units = round(units, instrument.trade_units_precision)
        
        if direction == defs.SELL:
            units = units * defs.SELL
        
        data = {
            'order': {
                'units': str(units),
                'instrument': pair,
                'type': 'MARKET'
            }
        }
        
        if stop_loss is not None:
            stop_loss_dict = {
                'price': str(round(stop_loss, instrument.display_precision))
            }
            
            data['order']['stopLossOnFill'] = stop_loss_dict
            
        if take_profit is not None:
            take_profit_dict = {
                'price': str(round(take_profit, instrument.display_precision))
            }
            
            data['order']['takeProfitOnFill'] = take_profit_dict 
         
        ok, response = self.make_request(url=url, verb='post', data=data, code=201)
        
        if ok is True and 'orderFillTransaction' in response:
            return response['orderFillTransaction']['id']
        
        return None
    
    
    def close_trade(self, trade_id):
        url = f'accounts/{defs.ACCOUNT_ID}/trades/{trade_id}/close'
        ok, _ = self.make_request(url=url, verb='put', code=200)
        
        if ok is True:
            print(f'Closed {trade_id} successfully')
        else:
            print(f'Failed to close {trade_id}')
        
        return ok
    

    def get_open_trade(self, trade_id):
        url = f'accounts/{defs.ACCOUNT_ID}/trades/{trade_id}'
        
        ok, response = self.make_request(url=url, code=200)
        
        if ok is True and 'trade' in response:
            return OpenTrade(response['trade']) 
         
    
    def get_open_trades(self):
        url = f'accounts/{defs.ACCOUNT_ID}/openTrades'
        
        ok, response = self.make_request(url=url, code=200)
        
        if ok is True and 'trades' in response:
            return [OpenTrade(trade) for trade in response['trades']]
        
        
    def get_prices(self, instruments_lst):
        url = f'accounts/{defs.ACCOUNT_ID}/pricing'
        
        params = {
            'instruments': ','.join(instruments_lst),
            'includeHomeConversions': True
        }
        
        ok, response = self.make_request(url=url, params=params, code=200)
        
        if ok is True and 'prices' in response and 'homeConversions' in response:
            return [APIPrice(res, response['homeConversions']) for res in response['prices']]
        
        return None
        