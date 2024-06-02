import requests
import constants.defs as defs
import pandas as pd
from dateutil import parser
from datetime import datetime as dt


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
        
        try:
            response = None
            
            if verb == 'get':
                response = self.session.get(api_url, params=params, data=None, headers=None)
                
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
        