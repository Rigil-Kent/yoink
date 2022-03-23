import requests
from bs4 import BeautifulSoup

import os
from enum import Enum, auto

from yoink.common import supported_sites, library_path



class Scrapable:
    def __init__(self, url : str) -> None:
        self.url = url
        comic_path = os.path.join(library_path, 'comics')
        
        if not os.path.exists(comic_path):
            os.makedirs(comic_path)

        self.__check_site_support()


    @property
    def markup(self) -> str:
        try:
            # raise_for_status alters the default response behavior allowing http errors to raise exception
            req = requests.get(self.url)
            req.raise_for_status()
            return req.content
        except requests.exceptions.HTTPError as e:
            # returns {status_code} Client Error: Not found for url: {self.url} in the event of any http errors and exits
            raise SystemExit(e)


    @property
    def soup(self) -> BeautifulSoup: return BeautifulSoup(self.markup, 'html.parser')


    def __check_site_support(self) -> None:
        num_of_sites = len(supported_sites)

        while num_of_sites > 0:
            for link in supported_sites:
                if link in self.url:
                    return

            num_of_sites = num_of_sites - 1

        raise ValueError('Unsupported site')