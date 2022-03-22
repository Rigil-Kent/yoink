from pathlib import Path
# TODO replace os path with pathlib
import os
from enum import Enum, auto



# TODO replace expan user
home_folder = Path.home()
app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
config_path = os.path.abspath(os.path.join(os.path.expanduser('~'), '.config/yoink'))
library_path = os.path.abspath(os.path.join(os.path.expanduser('~'), 'yoink/library'))
required_comic_files = ('.cbr', '.cbz', '000.jpg', '001.jpg')
skippable_images = ('logo-1.png', 'logo.png', 'report.png', 'request.png', 'prev.png', 'Next.png', 'Donate.png', '11.png', 'navbar.svg')
supported_sites = ['readallcomics.com', 'tpb.party', 'dragonballsupermanga.net', 'mangadex.tv']
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
