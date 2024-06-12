from scraping.daily_fx_com import *
from scraping.investing_com import *
from scraping.bloomberg_com import *
from scraping.trading_economics_com import *


def execute_web_scraping(site_num):
    if site_num == 1:
        print('dailyfx.com')
        print(dailyfx_com())
    elif site_num == 2:
        print('investing.com')
        print(investing_com())
    elif site_num == 3:
        print('bloomberg.com')
        [print(x) for x in bloomberg_com()]
    elif site_num == 4:
        print('tradingeconomics.com')
        print(fx_calendar())


if __name__ == '__main__':
    execute_web_scraping(2)
    
