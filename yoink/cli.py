from email.policy import default
import os
import sys
import click
from click_default_group import DefaultGroup

from yoink.common import  app_root, library_path, config_path
from yoink.comic import Comic



queue = []

@click.group(cls=DefaultGroup, default='init', default_if_no_args=True)
@click.option('-c', '--comic', help='Download a Comic file')
@click.option('-t', '--torrent', help='Download a Torrent')
def yoink(comic, torrent):
    if comic:
        click.echo('Downloading a comic')
    
    if torrent:
        click.echo('Downloading a torrent')



@yoink.command()
def init():

    click.echo(f'Initializing for {sys.platform}')


@yoink.command()
@click.argument('url')
def download(url):
    # Account for whitespace/blank urls
    if url.strip() == '':
        click.echo('url cannot be blank')
        return 1

    # comic = Comic(url)
    # click.echo(f'Downloading {comic.title}')
    # comic.archiver.download()
    # click.echo('Building comic archive')
    # comic.archiver.generate_archive()
    # click.echo('Cleaning up')
    # comic.archiver.cleanup_worktree()
    # click.echo('Success')


if __name__=='__main__':
    yoink()