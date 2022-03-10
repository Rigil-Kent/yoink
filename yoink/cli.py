from pydoc import cli
import click

from yoink.common import qb_client, app_root, library_path, config_path
from yoink.comic import Comic, ComicArchiver
from yoink.torrent import Torrent, TorrentDownloader



@click.group()
def yoink():
    pass


@yoink.command()
@click.argument('url')
def download(url):
    # Account for whitespace/blank urls
    if url.strip() == '':
        click.echo('url cannot be blank')
        return 1

    comic = Comic(url)
    archiver = ComicArchiver(comic)
    click.echo(f'Downloading {comic.title}')
    archiver.download()
    click.echo('Building comic archive')
    archiver.generate_archive()
    click.echo('Cleaning up')
    archiver.cleanup_worktree()
    click.echo('Success')

if __name__=='__main__':
    yoink()