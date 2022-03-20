from email.policy import default
import os
import sys
import click
from click_default_group import DefaultGroup

from yoink.common import  app_root, library_path, config_path
from yoink.comic import Comic



queue = []

@click.group(cls=DefaultGroup, default='download', default_if_no_args=True)
def yoink():
    pass



@yoink.command()
def init():

    click.echo(f'Initializing for {sys.platform}')


@yoink.command()
# @click.option('-c', '--comic', is_flag=True, help='Download a Comic file')
# @click.option('-t', '--torrent', is_flag=True, help='Download a Torrent')
@click.option('-s', '--series', is_flag=True, help='Download the entire series')
@click.option('-p', '--path', help='Change the download path')
@click.argument('url')
def download(url, path, series):
    # Account for whitespace/blank urls
    if url.strip() == '':
        click.echo('url cannot be blank')
        return 1

    try:
        comic = Comic(url, path=path if path else None)
    except ValueError:
        click.echo(f'{url} is not supported or is not a valid URL')
        return 1

    if series:
        comic.generate_series_queue()

    click.echo(f'Downloading {comic.title}')
    comic.archiver.download()

    click.echo('Building comic archive')
    comic.archiver.generate_archive()

    click.echo('Cleaning up')
    comic.archiver.cleanup_worktree()

    click.echo('Success')
    


if __name__=='__main__':
    yoink()