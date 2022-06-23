from urllib.error import HTTPError
from yoink.config import required_archive_files, skippable_images, config
from yoink.scraper import Scrapable

import os
import shutil
import urllib
import re



class Comic(Scrapable):
    def __init__(self, url, path=None) -> None:
        super().__init__(url)

    def __is_supported_image(self, image):
        return image.endswith('.jpg' or '.jpeg')


    def __get_image_src(self, comic) -> str:
        if comic.attrs:
            try:
                return comic.attrs['src']
            except KeyError:
                return comic['data-src']

        for image in comic:
            return image.attrs['src']

    def __parse_soup(self) -> list:
        soup = {
            'default': self.soup.find_all('div', class_='separator'),
            'no-div': self.soup.find_all('img', attrs={'width': '1000px'}),
            'excaliber': self.soup.find_all('img'),
            'dbsuper': self.soup.findAll('meta', attrs={'property': 'twitter:image'}),
            'mangadex': self.soup.find_all('img', attrs={'draggable': 'false'})
        }

        for case in soup.keys():
            comics = soup.get(case)

            if len(comics) > 0:
                return comics

    @property
    def filelist(self) -> list:
        comics = self.__parse_soup()
        return [comic for comic in list(map(self.__get_image_src, comics)) if not comic.endswith(skippable_images)]


    @property
    def title(self) -> str:
        if 'readallcomics' in self.url:
            return self.soup.title.string.replace(' | Read All Comics Online For Free', '').replace('…', '').replace('#', '').replace(':', '').strip()
        elif 'mangadex' in self.url:
            return self.soup.find('meta', property='og:title').attrs['content'].replace(' - Mangadex', '').replace('Read ', '')
        else:
            return 'Uncategorized'

    @property
    def category(self) -> str:
        data = self.soup.find('a', attrs={'rel': 'category tag'} )
        return data.text

    @property
    def series_list(self) -> list:
        queue = []

        return queue

    @property
    def issue_number(self) -> int:
        # matches any year in parentheses (xxxx)
        year_regex = re.search("(\\([12]\\d{3}\\))", self.title)

        try:
            return int(self.title[:year_regex.start() - 1][-1])
        except TypeError:
            return 1
        except AttributeError:
            return 1

    @property
    def volume(self) -> int:
        return

    @property
    def next(self) -> str:
        ''' returns the url of the next comic in the series. returns None if current'''
        try:
            return self.soup.find('img', attrs={'title': 'Next Issue'}).parent.attrs['href'] or None
        except AttributeError:
            return None

    @property
    def prev(self) -> str:
        ''' returns the url of the previous comic in the series. returns None if first'''
        try:
            return self.soup.find('img', attrs={'title': 'Previous Issue'}).parent.attrs['href']
        except AttributeError:
            return None


    def can_remove(self, filename : str) -> bool:
        return not filename.endswith(config.skippable_images)



def download_comic_files(comic: Comic, worktree = None):
    if not worktree:
        worktree = os.path.join(config.library_path, f'comics/{comic.title}')

    if not os.path.exists(worktree):
        os.makedirs(worktree, mode=0o777)

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', "Mozilla/5.0")]
    urllib.request.install_opener(opener)

    try:
        for index,url in enumerate(comic.filelist):
            if not url.endswith('.jpg'):
                formatted_file = os.path.join(worktree, f'{comic.title} ' + ''.join([str(index).zfill(3), '.jpg']))
                print(formatted_file, end='\r')
                urllib.request.urlretrieve(url, filename=formatted_file)
            else:
                page_number = str(index).zfill(3)
                file_extension = url.split('/')[-1].split('.')[1]

                if len(file_extension) > 3:
                    file_extension = 'jpg'

                formatted_file = f'{comic.title} - {page_number}.{file_extension}'
                print(formatted_file, end='\r',)
                urllib.request.urlretrieve(url, filename=os.path.join(worktree, formatted_file))
    except HTTPError:
        # the page itself loads but the images (stored on another server) 4040
        raise ReferenceError(f'Issue {comic.title} #{comic.issue_number} could not be found. The page may be down or the images might have errored: {self.comic.url}')

def generate_archive(comic: Comic, worktree = None, archive_format = '.cbr'):
    if not worktree:
        worktree = os.path.join(config.library_path, f'comics/{comic.title}')

    archive_from = os.path.basename(worktree)
    if os.path.exists(os.path.join(worktree, f'{comic.title}{archive_format}')):
        return

    output = shutil.make_archive(comic.title, 'zip', worktree, worktree)
    # os.rename causes OSError: [Errno 18] Invalid cross-device link and files build test
    # os rename only works if src and dest are on the same file system
    shutil.move(output, os.path.join(worktree, f'{comic.title}{archive_format}'))

def clean_up(comic: Comic):
    worktree = os.path.join(config.library_path, f'comics/{comic.title}')

    for image in os.listdir(worktree):
            if not image.endswith(required_archive_files):
                os.remove(os.path.join(worktree, image))
                


if __name__ == '__main__':
    comic = Comic('http://www.readallcomics.com/static-season-one-4-2021/') # all links
    # comic = Comic('http://readallcomics.com/static-season-one-001-2021/') # no prev link
    # comic = Comic('http://readallcomics.com/static-season-one-6-2022/') # no next link
    # comic = Comic('http://readallcomics.com/superman-vs-lobo-4-2022/')
    # test_comic_b = 'http://readallcomics.com/captain-marvel-vs-rogue-2021-part-1/'
    # print(comic.next)
    # print(comic.prev)
    # print(comic.issue_number)