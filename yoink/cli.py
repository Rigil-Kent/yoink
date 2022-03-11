import click
import libtorrent as lib

from yoink.common import  app_root, library_path, config_path
from yoink.comic import Comic
from yoink.torrent import Torrent, downloader


session = lib.session()
session.listen_on(6881, 6891)
queue = []

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

    # comic = Comic(url)
    # click.echo(f'Downloading {comic.title}')
    # comic.archiver.download()
    # click.echo('Building comic archive')
    # comic.archiver.generate_archive()
    # click.echo('Cleaning up')
    # comic.archiver.cleanup_worktree()
    # click.echo('Success')

    torrent = Torrent(url)
    print(torrent.magnet_link)

    # queue.append(lib.add_magnet_uri(session, torrent.magnet_link, {'save_path': library_path}))

    # while queue:
    #     next_shift = 0

    #     for index, download in enumerate(queue):
    #         if not download.is_seed():
    #             status = download.status()


    # downloader.add(torrent)
    # downloader.download()

if __name__=='__main__':
    yoink()