from api.oanda_api import OandaAPI
from infrastructure.instrument_collection import instrument_collection

if __name__ == '__main__':
    oanda_api = OandaAPI()
    
    instrument_collection.create_file(data=oanda_api.get_account_instruments(), path='./data')
    instrument_collection.load_instruments('./data')
    instrument_collection.print_instruments()
    
    # data = oanda_api.get_account_summary()
    # print(data)
    
    # instrument_collection.load_instruments('./data')
    # instrument_collection.print_instruments()
    