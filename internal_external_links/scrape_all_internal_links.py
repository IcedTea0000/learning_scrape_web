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
    try:
        response = urlopen(request)
    except:
        print('error requesting. Skipping ' + web_page)
        return
    soup = BeautifulSoup(response.read(), 'html.parser')
    web_domain = '{}://{}'.format(urlparse(web_page).scheme, urlparse(web_page).netloc)
    href_regex = web_domain + """| # contain web domain or
                                 ^(\/) # starts with character '/'
                                 |^[^\.} # or not starts with '.'
                                 | # or
                                 ^[^\/(http)(www)] # not start with '/' and 'http' and 'www'
                                 """
    a_list = soup.find_all(name='a', attrs={'href': re.compile(href_regex, re.VERBOSE)})

    for tag in a_list:
        if tag.attrs['href'] is not None:
            link = convert_full_link(tag.attrs['href'], web_page)
            if link not in internal_links:
                internal_links.add(link)
                print(link)
                get_internal_links(link)


def convert_full_link(href, origin_path):
    web_domain = '{}://{}'.format(urlparse(origin_path).scheme, urlparse(origin_path).netloc)
    if href.startswith('http') or href.startswith('www'):
        return href
    elif href.startswith('/'):
        return web_domain + href
    else:
        return origin_path + '/' + href


def get_all_internal_links(web_domain):
    """test"""


if __name__ == '__main__':
    internal_links = set()
    random.seed(datetime.datetime.now())

    webpage = 'http://books.toscrape.com/catalogue/page-2.html'
    get_internal_links(webpage)
    # print(internal_links)
    # url = 'https://en.wikipedia.org/wiki/Shinzo_Abe'


# issue remaining:
# relative path dang 'catalogue/link/link' va '../../link' chua convert duoc thanh full url