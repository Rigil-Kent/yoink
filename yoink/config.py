from dataclasses import dataclass
import json
from pathlib import Path
# TODO replace os path with pathlib
import os
from enum import Enum, auto



@dataclass
class YoinkConfig:
    home_path: str
    config_path: str
    app_root: str
    library_path: str
    skippable_images: set
    supported_sites: set
    headers: dict
    plugins: list


defaults = {
    'home_path': str(Path.home()),
    'config_path': os.path.abspath(os.path.join(Path.home(), '.config/yoink')),
    'app_root': os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
    'library_path': os.path.abspath(os.path.join(Path.home(), 'yoink/library')),
    'skippable_images': ('.cbr', '.cbz', '000.jpg', '001.jpg'),
    'supported_sites': [
            {
                "name": 'readallcomics.com',
            },
            {
                "name": 'tpb.party',
            },
            {
                "name": 'dragonballsupermanga.net',
            },
            { 
                "name": 'mangadex.tv'
            }
         ],
    'headers': {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'},
    'plugins': []
}



def config_from_file(filepath: str) -> YoinkConfig:
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:

                data = json.load(file)
                return YoinkConfig(**data)
        else:
            # TODO prompt user for prefered file locations and save yoink.json
            return config_from_defaults()


def config_from_defaults() -> YoinkConfig:
    return YoinkConfig(**defaults)


home_folder = Path.home()


app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


config_path = os.path.abspath(os.path.join(home_folder, '.config/yoink'))


library_path = os.path.abspath(os.path.join(home_folder, 'yoink/library'))


required_archive_files = ('.cbr', '.cbz', '000.jpg', '001.jpg')

skippable_images = ('logo-1.png', 'logo.png', 'report.png', 'request.png', 'prev.png', 'Next.png', 'Donate.png', '11.png', 'navbar.svg')

_sites = ['readallcomics.com', 'tpb.party', 'dragonballsupermanga.net', 'mangadex.tv']

supported_sites = _sites


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}


config = config_from_file('yoink.json')