from email.policy import default
import os
from subprocess import check_output
import sys
import click
from click_default_group import DefaultGroup

from yoink.config import  YoinkConfig, app_root, config_from_file, library_path, config_path
from yoink.comic import Comic



queue = []
config = config_from_file('yoink.json')


def download_comic(url, series):
    try:
        comic = Comic(url)
    except ValueError:
        click.echo(f'{url} is not supported or is not a valid URL')
        return 1

    click.echo(f'Downloading {comic.title}')
    comic.archiver.download()

    click.echo('Building comic archive')
    comic.archiver.generate_archive()

    click.echo('Cleaning up')
    comic.archiver.cleanup_worktree()

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
# @click.option('-c', '--comic', is_flag=True, help='Download a Comic file')
# @click.option('-t', '--torrent', is_flag=True, help='Download a Torrent')
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