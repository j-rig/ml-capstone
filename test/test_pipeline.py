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


def get_page_cf(o):
    o["scratch"]["page"] = open(
        os.path.join(os.path.dirname(__file__), "data", "bbs_listing_cf.html")
    ).read()
    return True, o


def get_page_nocf(o):
    o["scratch"]["page"] = open(
        os.path.join(os.path.dirname(__file__), "data", "bbs_listing_nocf.html")
    ).read()
    return True, o


def test_predict_pipeline():
    url = "https://www.bizbuysell.com/Business-Opportunity/Wholesale-Distributor-of-Auto-and-Marine-Upholstery-Supplies/2093773/"
    predict_funcs[1] = get_page_nocf
    r = pipeline(dict(url=url), predict_funcs)
    assert "error" not in r.keys()
    assert "pprice" in r.keys()
    assert "model" in r.keys()
    assert "text" == r["model"]


def test_predict_pipeline_cashflow():
    url = (
        "https://www.bizbuysell.com/Business-Opportunity/Gambino-s-Restaurant/1971050/"
    )
    predict_funcs[1] = get_page_cf
    r = pipeline(dict(url=url), predict_funcs)
    assert "error" not in r.keys()
    assert "pprice" in r.keys()
    assert "model" in r.keys()
    assert "text+feature" == r["model"]


def test_predict_pipeline_bad_url():
    url = "https://www.bizbuysell.com/bad_url"
    predict_funcs[1] = get_page_nocf
    r = pipeline(dict(url=url), predict_funcs)
    assert "error" in r.keys()
    assert r["error"]["code"] == 1


def get_listings(o):
    o["scratch"]["page"] = open(
        os.path.join(os.path.dirname(__file__), "data", "bbs_search.html")
    ).read()
    return True, o


def test_listing_pipeline():
    listing_funcs[1] = get_listings
    r = pipeline(dict(url=""), listing_funcs)
    assert "error" not in r.keys()
    assert "listings" in r.keys()
