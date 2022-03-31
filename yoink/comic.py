from yoink.config import required_archive_files, skippable_images, library_path, config
from yoink.scraper import Scrapable

import os
import shutil
import urllib
import re



class Comic(Scrapable):
    def __init__(self, url, path=None) -> None:
        super().__init__(url)
        self.archiver = ComicArchiver(self, library=path)

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
        year_regex = re.search("(\([12]\d{3}\))", self.title)

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


class ComicArchiver:
    def __init__(self, comic : Comic, library=None) -> None:
        self.comic = comic
        self.worktree = library if library else os.path.join(config.library_path, f'comics/{self.comic.title}')
        self.queue = []

    def add(self, link : str) -> None:
        self.queue.append(link)
    
    def download(self) -> None:

        if not os.path.exists(self.worktree):
            os.makedirs(self.worktree, mode=0o777)

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)

        for index,url in enumerate(self.comic.filelist):

            if not url.endswith('.jpg'):
                formatted_file = os.path.join(self.worktree, f'{self.comic.title} ' + ''.join([str(index).zfill(3), '.jpg']))
                print(formatted_file, end='\r')
                urllib.request.urlretrieve(url, filename=formatted_file)
            else:
                page_number = str(index).zfill(3)
                file_extension = url.split('/')[-1].split('.')[1]

                if len(file_extension) > 3:
                    file_extension = 'jpg'

                formatted_file = f'{self.comic.title} - {page_number}.{file_extension}'
                print(formatted_file, end='\r',)
                urllib.request.urlretrieve(url, filename=os.path.join(self.worktree, formatted_file))
        print()

    def generate_archive(self, archive_format='.cbr'):

        archive_from = os.path.basename(self.worktree)
        if os.path.exists(os.path.join(self.worktree, f'{self.comic.title}{archive_format}')):
            return

        output = shutil.make_archive(self.comic.title, 'zip', self.worktree, self.worktree)
        # os.rename casuses OSError: [Errno 18] Invalid cross-device link and files build test
        # os rename only works if src and dest are on the same file system
        shutil.move(output, os.path.join(self.worktree, f'{self.comic.title}{archive_format}'))


    def cleanup_worktree(self):
        for image in os.listdir(self.worktree):
            if not image.endswith(required_archive_files):
                os.remove(os.path.join(self.worktree, image))

if __name__ == '__main__':
    comic = Comic('http://www.readallcomics.com/static-season-one-4-2021/') # all links
    # comic = Comic('http://readallcomics.com/static-season-one-001-2021/') # no prev link
    # comic = Comic('http://readallcomics.com/static-season-one-6-2022/') # no next link
    # comic = Comic('http://readallcomics.com/superman-vs-lobo-4-2022/')
    # test_comic_b = 'http://readallcomics.com/captain-marvel-vs-rogue-2021-part-1/'
    # print(comic.next)
    # print(comic.prev)
    # print(comic.issue_number)