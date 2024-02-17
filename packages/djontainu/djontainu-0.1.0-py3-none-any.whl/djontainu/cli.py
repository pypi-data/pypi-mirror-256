import click


@click.group()
def main():
    pass


@main.command()
def test_cli():
    click.echo('testing click echo')
    print('testing print')


@main.command()
@click.argument('filename')
@click.option('--verbose', is_flag=True, help='Increase output verbosity.')
def process(filename, verbose):
    """Process the given FILENAME."""
    click.echo(f'Processing file: {filename}')
    if verbose:
        click.echo('Verbosity turned on')


if __name__ == '__main__':
    main()
