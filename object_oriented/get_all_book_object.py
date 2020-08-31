from urllib.request import urlopen, Request
from bs4 import BeautifulSoup



class Book:
    """object Book contains needed info from product book from 'books.toscrape.com'"""

    def __init__(self, title, url, price):
        self.title = title
        self.url = url
        self.price = price

    def __str__(self):
        return 'Title: '.format(self.title) + '\n' + ('Url: {}'.format(self.url)) + '\n' + (
            'Price: {}'.format(self.price)) + '\n' + ('-----------------------------')


def get_html(url):
    """get html soup object from input url"""
    headers = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    request = Request(url=url, headers=headers)
    response = urlopen(request)
    return BeautifulSoup(response.read(), 'html.parser')


def get_books(url):
    global all_books
    global page_number
    # if exception occurs meaning there is no more pages to iterrate, escape function
    try:
        soup = get_html(url)
    except:
        print('=====End of pages=====')
        return

    articles = soup.find_all(name='article', attrs={'class': 'product_pod'})
    for article in articles:
        title = article.find(name='h3').find(name='a').attrs['title']
        url = article.find(name='h3').find(name='a').attrs['href']
        price = article.find(name='p', attrs={'class': 'price_color'}).text
        book = Book(title, url, price)
        all_books.add(book)
        print(book)

    # recursion to continue loop through the next page
    page_number += 1
    get_books('http://books.toscrape.com/catalogue/page-{}.html'.format(str(page_number)))


if __name__ == '__main__':
    # execute script alone
    url = 'http://books.toscrape.com/catalogue/page-1.html'
    all_books = set()
    page_number = 1
    get_books(url)
