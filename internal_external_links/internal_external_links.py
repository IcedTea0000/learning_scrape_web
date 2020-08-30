from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random


def get_internal_links(soup, include_url):
    """tim tat ca internal link (link bat dau bang absolute path include_url hoac relative path bat dau voi '/') trong webpage"""
    internal_links = []
    try:
        # chiet xuat full domain trang web tu include_url
        url_parse = urlparse(include_url)
        include_url = '{}://{}'.format(url_parse.scheme, url_parse.netloc)


        # tim tat ca link bat dau bang '/' hoac include_url
        for link in soup.find_all('a', href=re.compile('^(/|.*' + include_url + ')')):
            if link.attrs['href'] is not None:
                if (link.attrs['href'].startswith('/')):
                    # tao absolute path tu relative path tim duoc
                    internal_links.append(include_url + link.attrs['href'])
                else:
                    internal_links.append(link.attrs['href'])
    except:
        print('something is wrong when get_internal_link')
    return internal_links


def get_external_links(soup, exclude_url):
    """tim tat ca absolute path trong webpage khong thuoc domain cua exclude_url"""
    external_links = []
    try:
        # chiet xuat domain trang web tu exclude_url
        url_parse = urlparse(exclude_url)
        exclude_url = url_parse.netloc

        for link in soup.find_all('a', href=re.compile('^(http|www)((?!' + exclude_url + ').)*$')):
            if link.attrs['href'] is not None:
                if link.attrs['href'] not in external_links:
                    external_links.append((link.attrs['href']))
    except:
        print('something is wrong when get_external_link')
    return external_links


def get_random_external_link(starting_page):
    html = urlopen(starting_page)
    soup = BeautifulSoup(html, 'html.parser')
    external_links = get_external_links(soup, starting_page)

    if len(external_links) == 0:
        print('No external links, looking around the site for one')
        domain = '{}://{}'.format(urlparse(starting_page).scheme, urlparse(starting_page).netloc)
        internal_links = get_internal_links(soup, domain)
        return get_random_external_link(internal_links[random.randint(0, len(internal_links) - 1)])
    else:
        return external_links[random.randint(0, len(external_links) - 1)]


def follow_external_only(starting_site):
    external_link = get_random_external_link(starting_site)
    print('Random external link is: {}'.format(external_link))
    follow_external_only(external_link)


if __name__ == '__main__':
    pages = set()
    random.seed(datetime.datetime.now())
    url = 'https://en.wikipedia.org/wiki/Shinzo_Abe'
    # html = urlopen(url)
    # soup = BeautifulSoup(html, 'html.parser')
    follow_external_only(url)
    # print(*get_external_links(soup, url), sep='\n')

    # # note: script se gap loi khi crawl toi nhung trang web khong tra ve html ma phai trigger js code