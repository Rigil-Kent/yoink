import pathlib


import pathlib
# TODO replace os path with pathlib
import os



app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
config_path = os.path.abspath(os.path.join(os.environ.get('HOME'), '.config/yoink'))
library_path = os.path.abspath(os.path.join(os.environ.get('HOME'), 'yoink/library'))
required_comic_files = ('.cbr', '.cbz', '000.jpg', '001.jpg')
skippable_images = ('logo-1.png', 'logo.png', 'report.png', 'request.png', 'prev.png', 'Next.png', 'Donate.png', '11.png')
torrent_concurrent_download_limit = 1
supported_sites = ['readallcomics.com', 'tpb.party']
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
