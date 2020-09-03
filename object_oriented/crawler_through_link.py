import re
import requests
from bs4 import BeautifulSoup


class Website:
    def __init__(self, name, url, target_pattern, absolute_url, title_tag, body_tag):
        self.name = name
        self.url = url
        self.target_pattern = target_pattern
        self.absolute_url = absolute_url
        self.title_tag = title_tag
        self.body_tag = body_tag


class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print('Url: {}'.format(self.url))
        print('Title: {}'.format(self.title))
        print('Body: \n{}'.format(self.body))


class Crawler:
    def __init__(self, site):
        self.site = site
        self.visited = []

    def get_page(self, url):
        try:
            request = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(request.text, 'html.parser')

    def safe_get(self, page_object, selector):
        selected_elements = page_object.select(selector)
        if selected_elements is not None and len(selected_elements) > 0:
            return '\n'.join([element.get_text() for element in selected_elements])
        return ''

    def parse(self, url):
        # get content attributes from soup object of an url
        soup = self.get_page(url)
        if soup is not None:
            title = self.safe_get(soup, self.site.title_tag)
            body = self.safe_get(soup, self.site.body_tag)
            if title != '' and body != '':
                content = Content(url, title, body)
                content.print()

    def crawl(self):
        """get pages from website home page"""
        soup = self.get_page(self.site.url)
        target_pages = soup.find_all('a', href=re.compile(self.site.target_pattern))
        for target_page in target_pages:
            target_page = target_page.attrs['href']
            if target_page not in self.visited:
                self.visited.append(target_page)
                if not self.site.absolute_url:
                    target_page = '{}{}'.format(self.site.url, target_page)
                self.parse(target_page)


if __name__ == '__main__':
    reuters = Website('Reuters', 'http://www.reuters.com', '^(/article)', False, 'h1',
                      'div.StandardArticleBody_body_1gnLA')
    crawler = Crawler(reuters)
    crawler.crawl()
