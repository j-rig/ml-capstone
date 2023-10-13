from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDRegressor
from sklearn.ensemble import GradientBoostingRegressor
import joblib
import glob

import logging

logger = logging.getLogger(__name__)


def train(df, model_path):
    logger.info("checking dataframe...")
    columns = [
        "pptitle",
        "ppdesc",
        "ppdetails",
        "ppfinancials",
        "price",
        "cash_flow",
        "gross_revenue",
    ]
    assert columns in df.columns
    logger.info("vectorizing text...")
    vect_text = TfidfVectorizer(
        stop_words="english", ngram_range=(1, 2), max_df=0.5, min_df=20
    )
    text = (
        df_in.pptitle
        + " "
        + df_in.ppdesc
        + " "
        + df_in.ppdetails
        + " "
        + df_in.ppfinancials
    )
    X_text = vect_text.fit_transform(text)

    logger.info("training text model...")
    regr = SGDRegressor()
    regr.fit(X_text, df.price)

    logger.info("predicting price from text model...")
    y_text = regr.predict(X_text)
    y_text_df = pd.DataFrame(y_text, columns=["text_price"], index=df.index)

    logger.info("training text + gross revenue model...")
    regrf1 = GradientBoostingRegressor()
    Xf1_train = pd.concat([df[["gross_revenue"]], y_text_df], axis=1)
    regrf1.fit(Xf1_train, df.price)

    logger.info("training text + cash flow + gross revenue model...")
    regrf2 = GradientBoostingRegressor()
    Xf2_train = pd.concat([df[["cash_flow", "gross_revenue"]], y_text_df], axis=1)
    regrf2.fit(Xf2_train, df.price)

    logger.info(f"saving model to {model_path}...")
    joblib.dump((vect_text, regr, regrf1, regrf2), model_path, True)

    logger.info("done.")


def partial_fit(self, data):
    if hasattr(self, "vocabulary_"):
        vocab = self.vocabulary_
    else:
        vocab = {}
    self.fit(data)
    vocab = list(set(vocab.keys()).union(set(self.vocabulary_)))
    self.vocabulary_ = {vocab[i]: i for i in range(len(vocab))}


CountVectorizer.partial_fit = partial_fit


# I have scaled my machine learning model to handle the complete
# dataset that I have collected, and it is also capable of
# handling all of the data that a real-world version of the
# application would need to handle by using batch training.


def batch_train(parquet_folder, model_path):
    logger.info("batch training...")
    paths = glob.glob(parquet_folder + "*.parquet")
    vect_text = CountVectorizer(
        stop_words="english", ngram_range=(1, 2), max_df=0.5, min_df=20
    )
    regr = SGDRegressor()
    for path in paths:
        df_in = pd.read_parquet(parquet)
        columns = [
            "pptitle",
            "ppdesc",
            "ppdetails",
            "ppfinancials",
            "price",
            "cash_flow",
            "gross_revenue",
        ]
        assert columns in df.columns
        logger.info(f"vectorizing text for {path}...")
        text = (
            df_in.pptitle
            + " "
            + df_in.ppdesc
            + " "
            + df_in.ppdetails
            + " "
            + df_in.ppfinancials
        )
        vect_text.partial_fit(text)

    for path in paths:
        df_in = pd.read_parquet(parquet)
        logger.info(f"training text model for {path}...")
        text = (
            df_in.pptitle
            + " "
            + df_in.ppdesc
            + " "
            + df_in.ppdetails
            + " "
            + df_in.ppfinancials
        )
        X_text = vect_text.fit_transform(text)

        regr.partial_fit(X_text, df.price)

    logger.info(f"saving model to {model_path}...")
    joblib.dump((vect_text, regr), model_path, True)

    logger.info("done.")
