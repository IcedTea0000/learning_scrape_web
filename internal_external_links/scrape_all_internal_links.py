from urllib.request import urlopen, Request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random


def get_internal_links(web_page):
    """extract domain and get all internal links belong to this domain"""
    global internal_links
    headers = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    request = Request(url=web_page, headers=headers)
    response = urlopen(request)
    soup = BeautifulSoup(response.read(), 'html.parser')
    web_domain = '{}://{}'.format(urlparse(web_page).scheme, urlparse(web_page).netloc)
    href_regex = '^(?!www\.|(?:http|ftp)s?://|[A-Za-z]:\\|//|\.\.).*'
    a_list = soup.find_all(name= 'a', attrs={'href':re.compile(href_regex)})

    for tag in a_list:
        if tag.attrs['href'] is not None:
            link = web_domain +'/'+ tag.attrs['href']
            if link not in internal_links:
                internal_links.add(link)
                print(link)
                get_internal_links(link)

def get_all_internal_links(web_domain):
    """test"""


if __name__ == '__main__':
    internal_links = set()
    random.seed(datetime.datetime.now())

    webpage = 'http://books.toscrape.com/'
    get_internal_links(webpage)
    # print(internal_links)
    # url = 'https://en.wikipedia.org/wiki/Shinzo_Abe'
