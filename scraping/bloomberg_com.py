import cloudscraper
from bs4 import BeautifulSoup


def get_article(card):
    return {
        'headline': card.get_text(),
        'link': 'https://www.reuters.com' + card.get('href')
    }


def bloomberg_com():
    scraper = cloudscraper.create_scraper()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    
    response = scraper.get('https://www.reuters.com/business/finance/', headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    links = []
    
    cards = soup.select('[class^="media-story-card__body"]')
    
    for card in cards:
        card_article = card.find('a', {'data-testid': 'Heading'})
        
        if card_article is None:
            continue
        
        links.append(get_article(card_article))
        
    return links
    
    
    
    