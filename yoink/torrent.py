from bs4 import BeautifulSoup
import requests

import os

from yoink.common import  library_path, config_path, app_root, headers
from yoink.scraper import Scrapable



stopped_state = ('pausedUP', 'stalledUP', 'uploading', 'seeding')






class TorrentDownloader:
    def __init__(self) -> None:
        self.limit = 1
        self.queue = []
        self.download_path = self.set_path(os.path.join(library_path, 'downloads'))

    @classmethod
    def create_torrent(cls, url):
        return Torrent(url)

    # @classmethod
    # def get_torrent(cls, name):
    #     return [torrent for torrent in new_downloader.torrents() if name == torrent['name']][0]

    @classmethod
    def quick_download(cls, url):
        if not isinstance(url, str):
            raise TypeError('URL string expected')

        if not url.startswith('magnet'):
            markup = requests.get(url, headers=headers).content
            soup = BeautifulSoup(markup, 'html.parser')
            magnet_link = soup.find('a', attrs={'title': 'Get this torrent'}.attrs['href'])

        


    def set_path(self, path):
        if path.strip() == '': raise ValueError('Path cannot be an empty string')

        if not os.path.exists(path):
            os.makedirs(path)

        return path

    def empty_queue(self):
        self.queue = []

    def add(self, torrent):
        if not isinstance(torrent, Torrent):
            raise TypeError('Not a valid torrent')

        self.queue.append(torrent)

    # TODO separate download method into new thread
    def download(self):
        while len(self.queue) > 0:
            for torrent in self.queue:
                if not isinstance(torrent, Torrent):
                    raise TypeError('Not a valid torrent')

                print(torrent.magnet_link)



downloader = TorrentDownloader()



class Torrent(Scrapable):
    def __init__(self, url) -> None:
        super().__init__(url)

    
    @property
    def name(self) -> str: return self.soup.find('div', attrs={'id': 'title'})

    @property
    def magnet_link(self) -> str: return self.soup.find('a', attrs={'title': 'Get this torrent'}).attrs['href'] 
