from api.oanda_api import OandaAPI
from infrastructure.instrument_collection import instrument_collection
from simulation.ma_cross import run_ma_sim


if __name__ == '__main__':
    run_ma_sim(currencies=['USD', 'GBP', 'SGD', 'NOK', 'EUR', 'AUD'])
    
    # oanda_api = OandaAPI()
    
    # instrument_collection.create_file(data=oanda_api.get_account_instruments(), path='./data')
    # instrument_collection.load_instruments('./data')
    # instrument_collection.print_instruments()
    