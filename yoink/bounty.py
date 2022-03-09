import os
from qbittorrent import Client
from yoink.provider import PirateBay, Provider, ReadAllComics



class Downloader:
    def __init__(self) -> None:
        self.qb = Client('http://127.0.0.1:8080')
        self.qb.login('admin', 'adminadmin')
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
        self.limit = 1
        self.queue = []
        self.config_path = self.set_path(os.path.abspath(os.path.join(os.environ.get('HOME'), '.config/yoink')))
        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.download_path = self.set_path(os.path.join(os.environ.get('HOME'), 'yoink/downloads'))


    def __download_torrent(self, magnetlink):
        pass


    def set_path(self, path):
        if path.strip() == '': raise ValueError('Path cannot be an empty string')

        if not os.path.exists(path):
            os.makedirs(path)

        return path

    def empty_queue(self):
        self.queue = []

    def add(self, item):
        self.queue.append(item)

    def download(self, file):
        if isinstance(file, ReadAllComics):
            pass
        elif isinstance(file, PirateBay):
            pass
        else:
            raise TypeError('Downloads from this site are not yet supported')


class Bounty:
    def __init__(self, url):
        self.provider = Provider(site=url)
        self.downloader = Downloader()

    def plunder(self, *args, **kwargs):
        if isinstance(self.provider, ReadAllComics):
            pass
        else:
            raise TypeError(f'{self.provider} is not a valid provider')
            





if __name__ == '__main__':
    item = Bounty('http://readallcomics.com/static-season-one-4-2021/')
    # downloader = Downloader()
    # print(downloader.download_path)
    item.provider.download()