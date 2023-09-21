import click
import sys
import json
import logging

from bizwiz.pipeline import pipeline

logging.basicConfig(level=logging.DEBUG)


@click.group()
def main(ctx=None):
    """bizwiz command line interface"""


@main.command("predict")
@click.argument("url")
def predict(url):
    """predict business price from bizbuysell url"""
    result = pipeline(dict(url=url))
    del result["scratch"]
    sys.stdout.write(json.dumps(result))
    sys.stdout.write("\n")
    sys.stdout.flush()


if __name__ == "__main__":
    """TBR"""
    sys.exit(main())
