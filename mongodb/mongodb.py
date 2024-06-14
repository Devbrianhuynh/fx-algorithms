from pymongo import MongoClient, errors

from constants.defs import MONGO_CONNECTION_STR


# Make class more declarative
class MongoDB:
    SAMPLE_COLL = 'forex_sample'
    CALENDAR_COLL = 'forex_calendar'
    INSTRUMENTS_COLL = 'forex_instruments'
    
    def __init__(self):
        self.client = MongoClient(MONGO_CONNECTION_STR)
        self.db = self.client.foreign_exchange_algorithms
        
    
    def test_connection(self):
        return self.db.list_collection_names()
    

    def delete_many(self, collection, **kwargs):
        try:
            _ = self.db[collection].delete_many(kwargs)
        except errors.InvalidOperation as error:
            print(f'delete_many() error: {error}')
        
        
    def add_one(self, collection, obj):
        try:
            _ = self.db[collection].insert_one(obj)
            
        except errors.InvalidOperation as error:
            print(f'add_one() error: {error}')
            
    
    def add_many(self, collection, obj):
        try:
            _ = self.db[collection].insert_many(obj)
            
        except errors.InvalidOperation as error:
            print(f'add_many() error: {error}')
            
    
    def query_distinct(self, collection, key):
        try:
            return self.db[collection].distinct(key)
        
        except errors.InvalidOperation as error:
            print(f'query_distinct() error: {error}')
            
        
    def query_single(self, collection, **kwargs):
        try:
            return self.db[collection].find_one(kwargs, {'_id': 0})
        
        except errors.InvalidOperation as error:
            print(f'query_single() error: {error}')
            
    
    def query_all(self, collection, **kwargs):
        try:
            data = []
            result = self.db[collection].find(kwargs, {'_id': 0})
            
            for item in result:
                data.append(item)
            
            return data
            
        except errors.InvalidOperation as error:
            print(f'query_all() error: {error}')
                