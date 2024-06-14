import requests
import cloudscraper
from bs4 import BeautifulSoup

import pandas as pd


def get_pairs(soup: BeautifulSoup):
    rows = soup.select_one('#pairSublinksLevel2')
    li = rows.select('li')

    pairs = []

    for i in range(len(li)):
        pair = li[i].get_text().replace('/', '-').replace('\n', '').lower()
        pair += '-'
        pairs.append(pair)
        
    return pairs


def get_data(session: cloudscraper, headers, pairs):
    investing_com_dict = []

    for p in pairs:
        print(p)

        if p == 'eur-usd-':
            response = session.get(f'https://www.investing.com/technical/technical-analysis', headers=headers)
        else:
            response = session.get(f'https://www.investing.com/technical/{p}technical-analysis', headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')

        # Last price
        last_value = soup.select_one('.lastValue')
        last_value = float(last_value.get_text())
        
        # Summary
        summary = soup.select_one('span.uppercaseText').get_text()

        # Consensus metrics
        sum_table_line = soup.select('.summaryTableLine')

        ma_buy = int(sum_table_line[0].select('#maBuy')[0].get_text())
        ma_sell = int(sum_table_line[0].select('#maSell')[0].get_text())

        ti_buy = int(sum_table_line[1].select('#maBuy')[0].get_text())
        ti_sell = int(sum_table_line[1].select('#maSell')[0].get_text())

        # Pivot Points
        pivot_points = soup.select_one('#curr_table')
        tbody = pivot_points.select('tr')[1]
        td = tbody.select('td')

        s1 = float(td[3].get_text())
        s2 = float(td[2].get_text())
        s3 = float(td[1].get_text())

        pivot = float(td[4].get_text())

        r1 = float(td[5].get_text())
        r2 = float(td[6].get_text())
        r3 = float(td[7].get_text())


        investing_com_dict.append({
            'pair': '_'.join(p.split('-')[:2]).upper(),
            'last_price': last_value,
            'summary': summary,
            'ti_buy': ti_buy,
            'ti_sell': ti_sell,
            'ma_buy': ma_buy,
            'ma_sell': ma_sell,
            's1': s1,
            's2': s2,
            's3': s3,
            'pivot': pivot,
            'r1': r1,
            'r2': r2,
            'r3': r3
        })
    
    return investing_com_dict


def investing_com(type):
    session = cloudscraper.create_scraper()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'Referer': 'https:/www.google.com/',
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Pragma': 'no-cache'
    }

    response = session.get('https://www.investing.com/technical/technical-analysis', headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    pairs = get_pairs(soup)
    investing_com_dict = get_data(session, headers, pairs)
    
    if type == 'dataframe':
        return pd.DataFrame.from_dict(investing_com_dict)
    elif type == 'dict':
        return investing_com_dict


def get_pair(pair, type='dataframe'):
    investing_com_data = investing_com(type)
    
    if type == 'dataframe':
        return investing_com_data[investing_com_data['pair'] == pair]
    
    elif type == 'dict':
        for data in investing_com_data:
            if data['pair'] == pair:
                return data
