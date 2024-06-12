import json

from models.instrument import Instrument
from mongodb.mongodb import MongoDB


class InstrumentCollection:
    FILENAME = 'instruments.json'
    API_KEYS = ['name', 'type', 'displayName', 'pipLocation', 'displayPrecision', 'tradeUnitsPrecision', 'marginRate']
    
    def __init__(self):
        self.instruments_dict = {}
        
        
    def load_instruments(self, path):
        self.instruments_dict = {}
        
        file_name = f'{path}/{self.FILENAME}'
        
        with open(file_name, 'r') as file:
            data = json.loads(file.read())
            
            for key, value in data.items():
                self.instruments_dict[key] = Instrument.from_api_obj(value)
                
    
    def load_instruments_db(self):
        self.instruments_dict = {}
        
        data = MongoDB().query_single(MongoDB.INSTRUMENTS_COLL)
        
        for key, value in data.items():
            self.instruments_dict[key] = Instrument.from_api_obj(value)
                
    
    def print_instruments(self):
        [print(key, value) for key, value in self.instruments_dict.items()]
        print(len(self.instruments_dict.keys()), 'instruments')
        
    
    def create_file(self, data, path):
        assert data is not None, 'Instrument file creation failed'
        
        instruments_dict = {}
        
        for instr in data:
            instruments_dict[instr['name']] = {key: instr[key] for key in self.API_KEYS}
            
        file_name = f'{path}/{self.FILENAME}'
        
        with open(file_name, 'w') as file:
            file.write(json.dumps(instruments_dict, indent=2))
    
    
    def create_db(self, data)   :
        assert data is not None, 'Instrument file creation failed'

        instruments_dict = {}
        
        for instr in data:
            instruments_dict[instr['name']] = {key: instr[key] for key in self.API_KEYS}
        
        database = MongoDB()
        database.delete_many(MongoDB.INSTRUMENTS_COLL)
        database.add_one(MongoDB.INSTRUMENTS_COLL, instruments_dict)
        

instrument_collection = InstrumentCollection()        
