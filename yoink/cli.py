from email.policy import default
import os
from subprocess import check_output
import sys
import click
from click_default_group import DefaultGroup

from yoink.config import  YoinkConfig, app_root, config_from_file, library_path, config_path
from yoink.comic import Comic, download_comic_files, generate_archive, clean_up



queue = []
config = config_from_file('yoink.json')


def download_comic(url, series):
    try:
        comic = Comic(url)
    except ValueError:
        click.echo(f'{url} is not supported or is not a valid URL')
        return 1

    click.echo(f'Downloading {comic.title}')
    download_comic_files(comic)

    click.echo('Building comic archive')
    generate_archive(comic)

    click.echo('Cleaning up')
    clean_up(comic)

    click.echo('Success')

    if series and comic.next:
        download_comic(comic.next, series)


@click.group(cls=DefaultGroup, default='download', default_if_no_args=True)
def yoink():
    pass



@yoink.command()
def init():

    click.echo(f'Initializing for {sys.platform}')
    click.echo(config)


@yoink.command()
@click.option('-s', '--series', is_flag=True, help='Download the entire series')
@click.argument('url')
def download(url, series):
    # Account for whitespace/blank urls
    if url.strip() == '':
        click.echo('url cannot be blank')
        return 1

    download_comic(url, series)
    


if __name__=='__main__':
    yoink()