import os
import requests
import urllib
from bs4 import BeautifulSoup
from urllib.parse import urlparse


root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
config_dir = os.path.abspath(os.environ.get('HOME'))

class Downloadable(object):
    stopped_state = ('pausedUP', 'stalledUP', 'uploading', 'seeding')

    def __init__(self, uri) -> None:
        self.uri = uri
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

    @property
    def markup(self):
        return requests.get(self.uri)

    @property
    def soup(self):
        return BeautifulSoup(self.markup.content, 'html.parser')

    def download(self):
        pass


class PirateBay(Downloadable):
    @property
    def magnet(self):
        self.soup.find('', attrs={'title': 'Get this torrent'}).attrs['href']

class ReadAllComics(Downloadable):

    def __init__(self, uri) -> None:
        super().__init__(uri)
        self.filelist = self.__get_comic_filelist()

    @classmethod
    def get_frontpage_links(cls):
        markup = requests.get('http://www.readallcomics.com')
        soup = BeautifulSoup(markup.content, 'html.parser')
        posts = soup.find_all('div', class_='type-post')
        links = []

        for post in posts:
            links.append({
                'title': post.find('h2').text,
                'image': post.find('img', height='250').attrs['src'],
                'uri': post.find('a', class_='font-link').attrs['href']
            })

        return links
    
    @property
    def title(self):
        return self.soup.title.string.replace(' | Read All Comics Online For Free', '').replace('…', '').replace('#', '').replace(':', '').strip()

    @property
    def category(self):
        data = self.soup.find('a', attrs={'rel': 'category tag'})
        return data.text

    def __can_remove(self, filename):
        ignore = ('.cbr', '.cbz', '000.jpg', '001.jpg')
        return not filename.endswith(ignore)

    def __get_image_src(self, comic):
        if comic.attrs:
            return comic.attrs['src']

        for image in comic:
            return image.attrs['src']

    def __parse_soup(self):
        soup = {
            'default': self.soup.find_all('div', class_='separator'),
            'no-div': self.soup.find_all('img', attrs={'width': '1000px'}),
            'excaliber': self.soup.find_all('img')
        }

        for case in soup.keys():
            comics = soup.get(case)

            if len(comics) > 0:
                return comics

    def __get_comic_filelist(self):
        comics = self.__parse_soup()
        return list(map(self.__get_image_src, comics))


    def download(self):
        skippable_files = ('logo-1.png', 'logo.png', 'report.png', 'request.png', 'prev.png', 'Next.png', 'Donate.png', '11.png')

        for url in self.filelist:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', self.headers['user-agent'])]
            urllib.request.install_opener(opener)

            if url.endswith(skippable_files):
                continue

            if not url.endswith('.jpg'):
                urllib.request.urlretrieve(url, filename=os.path.join(self.download_path + f'/{self.title}', f'{self.title}'.join([str(url.index(url)).zfill(3), '.jpg'])))
            else:
                page_number = url.split('/')[-1].split('.')[0].zfill(3)
                file_extension = url.split('/')[-1].split('.')[1]
                urllib.request.urlretrieve(url, filename=os.path.join(self.download_path + f'/{self.title}', f'{self.title}{page_number}.{file_extension}'))


def Provider(site='http://readallcomics.com'):
    providers = {
        'readallcomics': ReadAllComics
    }

    domain = urlparse(site)

    name=domain.netloc.split('.')[0]

    if name not in providers:
        raise ValueError('Downloads for this site are not yet supported')

    return providers[name](uri=site)