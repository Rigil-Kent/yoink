import requests
from bs4 import BeautifulSoup


from yoink.common import supported_sites



class Scrapable:
    def __init__(self, url) -> None:
        self.url = url

        for link in supported_sites:
            if link in self.url:
                return
            else:
                raise ValueError('Unsupported site')



    @property
    def markup(self) -> str: return requests.get(self.url).content

    @property
    def soup(self) -> BeautifulSoup: return BeautifulSoup(self.markup, 'html.parser')