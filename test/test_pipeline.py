import warnings

warnings.filterwarnings("ignore")

import joblib
import os.path

from bizwiz.pipeline import pipeline, predict_funcs, listing_funcs


def pl_ok(o):
    return True, o


def pl_nok(o):
    o["error"] = dict(code=-1, message="not ok", data="test error")
    return False, o


def test_joblib_version():
    assert joblib.__version__ == "1.1.0"


def test_predict_pipeline():
    url = "https://www.bizbuysell.com/Business-Opportunity/Wholesale-Distributor-of-Auto-and-Marine-Upholstery-Supplies/2093773/"

    def get_page_nodf(o):
        o["scratch"]["page"] = open(
            os.path.join(os.path.dirname(__file__), "bbs_listing_nocf.html")
        ).read()
        return True, o

    predict_funcs[1] = get_page_nodf
    r = pipeline(dict(url=url), predict_funcs)


# def test_listing_pipeline():
#     # predict_funcs[1] = pl_ok
#     r = pipeline(dict(url=""), listing_funcs)
