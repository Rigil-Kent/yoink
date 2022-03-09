import click



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