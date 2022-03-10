import click

from yoink.common import qb_client, app_root, library_path, config_path



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

    click.echo('Downloading')

if __name__=='__main__':
    yoink()