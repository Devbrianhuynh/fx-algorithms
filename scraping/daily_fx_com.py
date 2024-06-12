import requests
import cloudscraper
from bs4 import BeautifulSoup

import pandas as pd

def dailyfx_com():
    response = requests.get('https://www.dailyfx.com/sentiment')
    
    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.select('.dfx-technicalSentimentCard')
    
    pair_data = []
    
    for r in rows:
        card = r.select_one('.dfx-technicalSentimentCard__pairAndSignal')
        
        change_values = r.select('.dfx-technicalSentimentCard__changeValue')
        
        pair_data.append({
            'pair': card.select_one('a').get_text().replace('/', '_').replace('\n', ''),
            'sentiment': card.select_one('span').get_text().replace('\n', ''),
            'longs_day': change_values[0].get_text(),
            'shorts_day': change_values[1].get_text(), 
            'longs_week': change_values[3].get_text(), # Index 2 is open interest (OI) and is not needed for this algorithm
            'shorts_week': change_values[4].get_text(),
        })
        
    return pd.DataFrame.from_dict(pair_data)



        
        
    
    

