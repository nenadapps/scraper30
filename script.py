from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
import requests
from time import sleep
 
def get_html(url):
    
    html_content = ''
    try:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        pass
    
    return html_content

def get_value(html, index):
    
    info_value = None
       
    try:
        info_value = html.select('td')[index].get_text().strip();
    except:
        pass
    
    return info_value 

def get_details(html):
    
    stamp = {}
    
    stamp['country'] = get_value(html, 0)
    stamp['scott_num'] = get_value(html, 1)
    stamp['sg'] = get_value(html, 2)
    stamp['status'] = get_value(html, 3)
    stamp['condition'] = get_value(html, 4)
    stamp['raw_text'] = get_value(html, 5)
    
    price = get_value(html, 6)
    if price:
       price = price.replace('$', '').strip()
    stamp['price'] = price
    
    images = []
    try:
        for img_item in html.select('img'):
            img = img_item.get('src').replace('thumbnails/', '')
            if img not in images:
                images.append(img)
    except:
        pass
    
    stamp['images'] = images
       
    stamp['currency'] = 'USD'
    
    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date
    
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
           
    return stamp

def get_page_items(url):

    items = []

    try:
        html = get_html(url)
    except:
        return items

    try:
        for item in html.find_all('td', {'width': '75%'})[0].select('tr'):
            td0 = item.select('td')[0].get_text().strip()
            if ((item not in items) and (td0 != 'Country')):
                items.append(item)
    except:
        pass
    
    shuffle(list(set(items)))
    
    return items

def get_page_urls(url):

    items = []

    items.append(url)

    try:
        html = get_html(url)
    except:
        return items

    try:
        for item in html.select('p a'):
            item_link = item.get('href')
            if ((item_link not in items) and ('page=results.html' in item_link)):
                items.append(item_link)
    except:
        pass
    
    shuffle(list(set(items)))
    
    return items

url = 'https://kaystamps.com/~worldofw/cgi-bin/shopkc.pl/page=results.html/SID=133426759'
page_urls = get_page_urls(url)
for page_url in page_urls:
    page_items = get_page_items(page_url)
    for page_item in page_items:
        stamp = get_details(page_item)
