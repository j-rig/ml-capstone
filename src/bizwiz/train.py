from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDRegressor
from sklearn.ensemble import GradientBoostingRegressor
import joblib

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

    # TODO FIXME

    logger.info("training feature model...")
    regrf = GradientBoostingRegressor()
    Xf_train = df[["cash_flow", "gross_revenue"]]
    regrf.fit(Xf_train, df.price)

    logger.info(f"saving model to {model_path}...")
    joblib.dump((vect_text, regr, regrf), model_path, True)

    logger.info("done.")
