import os
from dateutil import parser

from api.oanda_api import OandaAPI
from mongodb.mongodb import MongoDB
from infrastructure.instrument_collection import instrument_collection
from simulation.ma_cross import run_ma_sim
from simulation.ema_macd_mp import run_ema_macd
from simulation.performance_metrics import *
from streaming_api.streamer import run_streamer
from infrastructure.collect_data import run_collection


def mongodb_tests(option):
    db = MongoDB()
    
    if option == 1:
        db.add_one(MongoDB.SAMPLE_COLL, {'name': 'MoonCake', 'city': 'Palo Alto', 'industry': 'software', 'speciality': 'computer vision', 'vc': 'Andreessen Horowitz'})
        
    elif option == 2:
        data = [
            {'name': 'Cakey', 'city': 'San Francisco', 'industry': 'software', 'speciality': 'ML algorithms', 'vc': 'Y Combinator'},
            {'name': 'Deepling', 'city': 'Menlo Park', 'industry': 'software', 'speciality': 'GPU inference', 'vc': 'Greylock Partners'},
            {'name': 'Coincake', 'city': 'Austin', 'industry': 'software', 'speciality': 'search engine', 'vc': 'Kleiner Perkins'},
            {'name': 'Fredo', 'city': 'Mountain View', 'industry': 'hardware', 'speciality': 'CPU manufacturing', 'vc': 'Index Ventures'},
            {'name': 'Moondata', 'city': 'Los Gatos', 'industry': 'software', 'speciality': 'Cloud infrastructure', 'vc': 'Khosla Ventures'}
        ]
        
        db.add_many(MongoDB.SAMPLE_COLL, data)
    
    elif option == 3:
        data = {'name': 'Sparkline', 'location': 'Paris', 'industry': 'software', 'speciality': 'IDE applications', 'vc': 'Accel'}
        
        db.add_one(MongoDB.SAMPLE_COLL, data)
    
    elif option == 4:
        print(db.query_all(MongoDB.SAMPLE_COLL, city='San Francisco'))
    
    elif option == 5:
        print(db.query_single(MongoDB.SAMPLE_COLL, city='San Francisco'))
        
    elif option == 6:
        print(db.query_distinct(MongoDB.SAMPLE_COLL, 'vc'))
    

if __name__ == '__main__':
    # db = MongoDB()
    
    # print(db.test_connection())
    # mongodb_tests(6)
    
    api = OandaAPI()
    
    instrument_collection.load_instruments_db()
    print(instrument_collection.instruments_dict)
    
    