import requests
from bs4 import BeautifulSoup


class Content:
    """common base class for all artitcles/pages"""

    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.title = title
        self.body = body
        self.url = url

    def print(self):
        """flexible printing function controls output"""
        print('New article found for topic: {}'.format(self.topic))
        print('Title: {}'.format(self.title))
        print('Body: {}'.format(self.body))
        print('Url: {}'.format(self.url))


class Website:
    """contain info about website structure"""

    def __init__(self, name, url, search_url, result_listing, result_url, absolute_url, title_tag, body_tag):
        self.name = name
        self.url = url
        self.search_url = search_url
        self.result_listing = result_listing
        self.result_url = result_url
        self.absolute_url = absolute_url
        self.title_tag = title_tag
        self.body_tag = body_tag


class Crawler:
    def get_page(self, url):
        # get all html of request url as BeautifulSoup object
        try:
            request = requests.get(url)
        except requests.exceptions.RequestException:
            print('Request exception')
            return None
        return BeautifulSoup(request.text, 'html.parser')

    def safe_get(self, page_object, selector):
        # get all Tag matches selector in page BeautifulSoup object
        child_object = page_object.select(selector)
        if child_object is not None and len(child_object) > 0:
            return child_object[0].get_text()
        return ''

    def search(self, topic, site):
        """searches a given website for a topic and records all pages found"""
        soup = self.get_page(site.search_url + topic)
        search_results = soup.select(site.result_listing)
        for result in search_results:
            url = result.select(site.result_url)[0].attrs['href']
            # check to see whether its a relative or an absolute URL
            if (site.absolute_url):
                soup = self.get_page(url)
            else:
                soup = self.get_page(site.url + url)

            if soup is None:
                print('url wrong. Skipping.')
                return

            title = self.safe_get(soup, site.title_tag)
            body = self.safe_get(soup, site.body_tag)

            if title != '' and body != '':
                content = Content(topic.strip(), title.strip(), body.strip(), url)
                content.print()


if __name__ == '__main__':
    crawler = Crawler()
    site_data = [['O\'Reilly Media', 'http://oreilly.com',
                  'https://ssearch.oreilly.com/?q=', 'article.product-result',
                  'p.title a', True, 'h1', 'section#product-description'],
                 ['Reuters', 'http://reuters.com',
                  'http://www.reuters.com/search/news?blob=',
                  'div.search-result-content', 'h3.search-result-title a',
                  False, 'h1', 'div.StandardArticleBody_body_1gnLA'],
                 ['Brookings', 'http://www.brookings.edu',
                  'https://www.brookings.edu/search/?s=',
                  'div.list-content article', 'h4.title a', True, 'h1', 'div.post-body']]

    # create list of object Websites
    sites = []
    for row in site_data:
        sites.append(Website(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    topics = ['python', 'data science']
    for topic in topics:
        print('Processing getting info about: ' + topic)
        for site in sites:
            crawler.search(topic, site)
