from bs4 import BeautifulSoup
import requests

class Content:
    """common base class for all articles/pages"""
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        """print object output"""
        print('Title: {}'.format(self.title))
        print('Url: {}'.format(self.url))
        print('Body: \n{}'.format(self.body))

class Website:
    """information about website structure"""
    def __init__(self, name, url, title_tag, body_tag):
        self.name = name
        self.url = url
        self.title_tag = title_tag
        self.body_tag = body_tag

class Crawler:
    def get_page(self, url):
        try:
            request = requests.get(url)
        except requests.exceptions.RequestException:
            print('Error requesting')
            return None
        return BeautifulSoup(request.text, 'html.parser')

    def safe_get(self, page_object, selector):
        """utility function used to get a content string from
        a Beautiful Soup object and a selector.
        Return empty string if no object found on selector"""
        selected_element = page_object.select(selector)
        if selected_element is not None and len(selected_element) > 0:
            return '\n'.join([element.get_text() for element in selected_element])
        return ''

    def parse(self, site, url):
        """"""