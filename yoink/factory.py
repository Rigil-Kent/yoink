from typing import Callable, Any

from yoink.scraper import Scrapable


downloader_creation_funcs: dict[str, Callable[..., Scrapable]] = {}


def register(url: str, creation_function: Callable[..., Scrapable]):
    downloader_creation_funcs[url] = creation_function

def unregister(url: str):
    downloader_creation_funcs.pop(url, None)

def create(arguments: dict[str, Any]) -> Scrapable:
    arguments_copy = arguments.copy()

    url = arguments_copy.pop('url')

    try:
        creation_func = downloader_creation_funcs[url]
        return creation_func(**arguments_copy)
    except KeyError:
        raise ValueError(f'Unsupported website: {url}')