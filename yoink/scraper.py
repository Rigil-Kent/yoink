import requests
from bs4 import BeautifulSoup


from yoink.common import supported_sites



class Scrapable:
    def __init__(self, url) -> None:
        self.url = url

        
        self.__check_site_support()
        # for link in supported_sites:
        #     if link in self.url:
        #         return
        #     else:
        #         raise ValueError('Unsupported site')
        # if not any(url in link for link in supported_sites):
        #     raise ValueError('Unsupported site')


    @property
    def markup(self) -> str: return requests.get(self.url).content

    @property
    def soup(self) -> BeautifulSoup: return BeautifulSoup(self.markup, 'html.parser')


    def __check_site_support(self):
        num_of_sites = len(supported_sites)

        while num_of_sites > 0:
            for link in supported_sites:
                if link in self.url:
                    return

            num_of_sites = num_of_sites - 1

        raise ValueError('Unsupported site')