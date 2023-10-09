import click
import sys
import json
import logging

from bizwiz.pipeline import pipeline, predict_funcs, listing_funcs
from bizwiz.train import train

logging.basicConfig(level=logging.INFO)


@click.group()
def main(ctx=None):
    """bizwiz command line interface"""


@main.command("predict")
@click.argument("url")
def predict(url):
    """predict business price from bizbuysell url"""
    result = pipeline(dict(url=url), predict_funcs)
    del result["scratch"]
    sys.stdout.write(json.dumps(result))
    sys.stdout.write("\n")
    sys.stdout.flush()


@main.command("listings")
def listings():
    """get some bizbuysell listing urls"""
    result = pipeline(dict(), listing_funcs)
    del result["scratch"]
    sys.stdout.write(json.dumps(result))
    sys.stdout.write("\n")
    sys.stdout.flush()


@main.command("train")
@click.argument("parquet", type=click.Path(exists=True))
@click.argument("joblib", type=click.Path(exists=False))
def train_cmd(parquet, joblib):
    """train a model from parquet file and save to a joblib file"""
    df_in = pd.read_parquet(parquet)
    train(df_in, joblib)


if __name__ == "__main__":
    """TBR"""
    sys.exit(main())
