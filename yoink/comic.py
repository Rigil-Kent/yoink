from click import format_filename
from soupsieve import select
from yoink.common import required_comic_files, skippable_images, library_path
from yoink.scraper import Scrapable

import os
import shutil
import urllib



class Comic(Scrapable):
    def __init__(self, url) -> None:
        super().__init__(url)
        self.archiver = ComicArchiver(self)


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

    @property
    def filelist(self):
        comics = self.__parse_soup()
        return [comic for comic in list(map(self.__get_image_src, comics)) if not comic.endswith(skippable_images)]


    @property
    def title(self): return self.soup.title.string.replace(' | Read All Comics Online For Free', '').replace('…', '').replace('#', '').replace(':', '').strip()

    @property
    def category(self):
        data = self.soup.find('a', attrs={'rel': 'category tag'} )
        return data.text

    def can_remove(self, filename):
        return not filename.endswith(required_comic_files)


class ComicArchiver:
    def __init__(self, comic : Comic) -> None:
        self.comic = comic
        self.worktree = os.path.join(library_path, f'comics/{self.comic.title}')
    
    def download(self):

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
                page_number = url.split('/')[-1].split('.')[0].zfill(3)
                file_extension = url.split('/')[-1].split('.')[1]
                urllib.request.urlretrieve(url, filename=os.path.join(self.worktree, f'{self.comic.title}{page_number}.{file_extension}'))
        print()

    def generate_archive(self, archive_format='.cbr'):
        if os.path.exists(os.path.join(self.worktree, f'{self.comic.title}{archive_format}')):
            return

        output = shutil.make_archive(self.comic.title, 'zip', self.worktree)
        os.rename(output, os.path.join(self.worktree, f'{self.comic.title}{archive_format}'))


    def cleanup_worktree(self):
        for image in os.listdir(self.worktree):
            if not image.endswith(required_comic_files):
                os.remove(os.path.join(self.worktree, image))

if __name__ == '__main__':
    comic = Comic('http://www.readallcomics.com/static-season-one-4-2021/')
    # # print(comic.filelist)
    # # print(len(comic.filelist))
    # archiver = ComicArchiver(comic)
    # archiver.download()
    # archiver.generate_archive()
    # archiver.cleanup_worktree()
    print(comic.category)