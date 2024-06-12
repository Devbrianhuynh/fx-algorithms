import requests
import time
import random
import datetime as dt
import pandas as pd
from bs4 import BeautifulSoup
from dateutil import parser

from mongodb.mongodb import MongoDB


pd.set_option('display.max_rows', None)


def get_date(child: BeautifulSoup):
    tr = child.select_one('tr')
    ths = tr.select('th')
    
    for th in ths:
        if th.has_attr('colspan'):
            date_text = th.get_text().strip()
            return parser.parse(date_text)
    
    return None


def get_data_point(key, element: BeautifulSoup):
    for elem in ['span', 'a']:
        data = element.select_one(f'{elem}#{key}')
        
        if data is not None:
            return data.get_text()
    
    return ''


def get_data_for_key(tr: BeautifulSoup, key):
    if tr.has_attr(key):
        return tr.attrs[key]
    
    return ''


def get_data_dict(date, table_rows):
    data = []
    
    for tr in table_rows:
        data.append({
            'date': date,
            'country': get_data_for_key(tr, 'data-country'),
            'category': get_data_for_key(tr, 'data-category'),
            'event': get_data_for_key(tr, 'data-event'),
            'symbol': get_data_for_key(tr, 'data-symbol'),
            'actual': get_data_point('actual', tr),
            'previous': get_data_point('previous', tr),
            'forecast': get_data_point('forecast', tr)
        })
        
    return data


def get_fx_calendar(from_date):
    session = requests.Session()
    
    from_date_str = dt.datetime.strftime(from_date, '%Y-%m-%d 00:00:00')
    
    to_date = from_date + dt.timedelta(days=6)
    to_date_str = dt.datetime.strftime(to_date, '%Y-%m-%d 00:00:00')
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'Cookie': f'calendar-importance=3; cal-custom-range={from_date_str}|{to_date_str}; cal-timezone-offset=0; TEServer=TEIIS;'
    }
    
    response = session.get('https://tradingeconomics.com/calendar', headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.select_one('table#calendar')
    
    last_header_date = None
    
    trs = {}
    final_data = []
    
    for c in table.children:
        if c.name == 'thead':
            if 'class' in c.attrs and 'hidden-head' in c.attrs['class']:
                continue
            
            last_header_date = get_date(c)    
            trs[last_header_date] = []
            
        elif c.name == 'tr':
            trs[last_header_date].append(c)
           
            
    for date, table_rows in trs.items():
        final_data += get_data_dict(date, table_rows)
    
    return final_data
    

def fx_calendar():
    final_data = []
    
    start = parser.parse('2023-07-03T00:00:00Z')
    end = parser.parse('2024-06-12T00:00:00Z')        
    
    database = MongoDB()

    while start < end:
        data = get_fx_calendar(start)
        
        print(start, len(data))
        
        database.add_many(MongoDB.CALENDAR_COLL, data)
        
        start = start + dt.timedelta(days=7)
        time.sleep(random.randint(1, 5))
    