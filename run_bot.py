from algorithms.bot import Bot
from infrastructure.instrument_collection import instrument_collection


if __name__ == '__main__':
    instrument_collection.load_instruments('./data')
    
    bot = Bot('./algorithms', 'settings', 'M1', 10)
    bot.run()