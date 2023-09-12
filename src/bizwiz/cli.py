import click


@click.group()
def main(ctx=None):
    """bizwiz command line interface"""


if __name__ == "__main__":
    """TBR"""
    sys.exit(main())
