import requests
import constants.defs as defs


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
            
        