import warnings
import random
import requests
from bs4 import BeautifulSoup
import extruct
from urllib.parse import urlparse
import logging
import json
import os.path
import numpy as np
import re
import pandas as pd

import joblib
import extruct

import nltk
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

warnings.filterwarnings("ignore")

logger = logging.getLogger(__name__)

nltk.download("punkt")
nltk.download("stopwords")

# model_path = os.environ.get(
#     "WEBAPP_MODEL_PATH",
#     os.path.join(os.path.dirname(__file__), "data", "model.sdgr.joblib"),
# )


Q = [0.8, 1.2]

model_path = os.environ.get(
    "WEBAPP_MODEL_PATH",
    os.path.join(os.path.dirname(__file__), "data", "model.final.joblib"),
)
vect_text, model_text, model_feature = joblib.load(model_path)

ua = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/111.0.5563.101 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/111.0.5563.101 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPod; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/111.0.5563.101 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-N960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; LM-Q710(FGN)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62",
    "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36 EdgA/110.0.1587.66",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36 EdgA/110.0.1587.66",
    "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36 EdgA/110.0.1587.66",
    "Mozilla/5.0 (Linux; Android 10; ONEPLUS A6003) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36 EdgA/110.0.1587.66",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 EdgiOS/111.1661.62 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Windows Mobile 10; Android 10.0; Microsoft; Lumia 950XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36 Edge/40.15254.603",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edge/44.18363.8131",
]

base_url = "https://www.bizbuysell.com/Business-Opportunity"


def preprocess_text(text):
    text = text.lower()
    text_p = "".join([char if char not in string.punctuation else " " for char in text])
    words = word_tokenize(text_p)
    stop_words = stopwords.words("english")
    stop_words.append("bizbuysell")
    filtered_words = [word for word in words if word not in stop_words]
    porter = PorterStemmer()
    stemmed = [porter.stem(word) for word in filtered_words]
    return " ".join(stemmed)


def validate_url(o):
    logger.info("validating url")
    assert "url" in o.keys()
    o["scratch"] = dict()
    if not o["url"].lower().startswith(base_url.lower()):
        o["error"] = dict(
            code=1,
            message="invalid url",
            data=f"url must start with {base_url}",
        )
        return False, o
    try:
        urlparse(o["url"])
    except:
        o["error"] = dict(
            code=2, message="invalid url", data=f"unable to parse url {o['url']}"
        )
        return False, o

    return True, o


def get_page(o):
    logger.info("getting page")
    headers = {"User-Agent": random.choice(ua)}
    result = requests.get(o["url"], headers=headers, timeout=60, verify=False)
    if not result.status_code == 200:
        o["error"] = dict(
            code=result.status_code, message="failed to read page", data=result.reason
        )
        return False, o
    o["scratch"]["page"] = result.text
    return True, o


def get_metadata(o):
    logger.info("getting metadata")
    metadata = extruct.extract(
        o["scratch"]["page"], base_url="https://www.bizbuysell.com"
    )
    o["scratch"]["metadata"] = metadata
    return True, o


def get_soup(o):
    logger.info("getting soup")
    soup = BeautifulSoup(o["scratch"]["page"], "lxml")
    o["scratch"]["soup"] = soup
    return True, o


def extract_price(o):
    logger.info("getting price")
    if "json-ld" in o["scratch"]["metadata"].keys():
        for i in o["scratch"]["metadata"]["json-ld"]:
            if i["@type"] == "Product":
                o["price"] = i["offers"]["price"]
                return True, o
    o["error"] = dict(code=3, message="failed get business price", data="")
    return False, o


def extract_title(o):
    logger.info("getting title")
    o["title"] = ""
    o["title"] = o["scratch"]["soup"].find("title").text.strip()
    if o["title"] == "":
        o["error"] = dict(code=4, message="failed to get title", data="")
        return False, o
    return True, o


def extract_desc(o):
    o["desc"] = ""
    logger.info("getting description")
    pc = o["scratch"]["soup"].find("div", {"class": "pageContent"})
    bd = pc.find("div", {"class": "businessDescription"})
    o["desc"] = bd.text.strip()
    if o["desc"] == "":
        o["error"] = dict(code=5, message="failed to get description", data="")
        return False, o
    return True, o


def extract_id(o):
    logger.info("getting listing id")
    if "json-ld" in o["scratch"]["metadata"].keys():
        for i in o["scratch"]["metadata"]["json-ld"]:
            if i["@type"] == "Product":
                o["id"] = i["productid"]
                return True, o
    o["error"] = dict(code=6, message="failed get business listing id", data="")
    return False, o


def extract_image(o):
    logger.info("getting image")
    o["image"] = None
    if "json-ld" in o["scratch"]["metadata"].keys():
        for i in o["scratch"]["metadata"]["json-ld"]:
            if i["@type"] == "LocalBusiness":
                o["image"] = i["image"]
                return True, o
    return True, o


def extract_details(o):
    logger.info("getting details")
    o["details"] = ""
    pc = o["scratch"]["soup"].find("div", {"class": "pageContent"})
    dt = pc.find("dl", {"class": "listingProfile_details"})
    if dt is not None:
        o["details"] = dt.text.strip()
    return True, o


def extract_finanicals(o):
    logger.info("getting finanicals")
    o["finanicals"] = ""
    pc = o["scratch"]["soup"].find("div", {"class": "pageContent"})
    fin = pc.find("div", {"class": "financials"})
    if fin is not None:
        o["finanicals"] = fin.text.strip()
    return True, o


def process_title(o):
    logger.info("processing title")
    o["ptitle"] = preprocess_text(o["title"])
    return True, o


def process_desc(o):
    logger.info("processing description")
    o["pdesc"] = preprocess_text(o["desc"])
    return True, o


def process_details(o):
    logger.info("processing details")
    o["pdetails"] = preprocess_text(o["details"])
    return True, o


def process_finanicals(o):
    logger.info("processing finanicals")
    o["pfinanicals"] = preprocess_text(o["finanicals"])
    return True, o


def extract_cash_flow(o):
    logger.info("processing cash flow")
    o["cash_flow"] = None
    r = re.search("[cC]ash\s+[fF]low:\s+\$?(\d[\d,]*)", o["finanicals"])
    if r is not None:
        r = r.groups()[0]
        r = r.replace(",", "")
        o["cash_flow"] = int(r)
    return True, o


def extract_gross_revenue(o):
    logger.info("processing gross revenue")
    o["gross_revenue"] = None
    r = re.search("[gG]ross\s+[rR]evenue:\s+\$?(\d[\d,]*)", o["finanicals"])
    if r is not None:
        r = r.groups()[0]
        r = r.replace(",", "")
        o["gross_revenue"] = int(r)
    return True, o


def predict_price(o):
    logger.info("predicting price")
    docs = [
        o["ptitle"] + " " + o["pdesc"] + " " + o["pdetails"] + " " + o["pfinanicals"]
    ]
    Xtest = vect_text.transform(docs)
    # print(Xtest)
    importance = np.argsort(np.asarray(Xtest.sum(axis=0)).ravel())[::-1]
    feature_names = np.array(vect_text.get_feature_names_out())
    # print(Xtest[importance[:20]])
    ytest = model_text.predict(Xtest)
    o["pprice"] = ytest[0]
    o["ppricet"] = ytest[0]
    o["model"] = "text"

    o["pwords"] = [str(x) for x in feature_names[importance[:20]]]
    o["pwi"] = [float(x) for x in importance[:20]]

    if o["cash_flow"] != None and o["gross_revenue"] != None:
        Xf = pd.DataFrame(
            {
                "cash_flow": [
                    o["cash_flow"],
                ],
                "gross_revenue": [
                    o["gross_revenue"],
                ],
            }
        )
        yftest = model_feature.predict(Xf)
        o["pprice"] = yftest[0]
        o["ppricef"] = yftest[0]
        o["model"] = "feature"

        if o["pprice"] > o["ppricef"] * Q[0] and o["pprice"] < o["ppricef"] * Q[1]:
            w = 0.6
            o["pprice"] = w * o["ppricef"] + (1.0 - w) * o["ppricet"]
            o["model"] = "text+feature"

    if o["pprice"] < 0:
        o["error"] = dict(code=99, message="negative price prediction", data="")
        return False, o

    return True, o


predict_funcs = [
    validate_url,
    get_page,
    get_metadata,
    get_soup,
    extract_price,
    extract_title,
    process_title,
    extract_desc,
    process_desc,
    extract_id,
    extract_image,
    extract_details,
    process_details,
    extract_finanicals,
    process_finanicals,
    extract_cash_flow,
    extract_gross_revenue,
    predict_price,
]


def set_listings_url(o):
    logger.info("setting listings url")
    o["scratch"] = dict()
    o["url"] = "https://www.bizbuysell.com/businesses-for-sale"
    return True, o


def extract_listings(o):
    logger.info("extracting listings")
    o["listings"] = list()
    if "json-ld" in o["scratch"]["metadata"].keys():
        for i in o["scratch"]["metadata"]["json-ld"]:
            if i["@type"] == "SearchResultsPage":
                for j in i["about"]:
                    if j["@type"] == "ListItem":
                        url = "https://www.bizbuysell.com" + j["item"]["url"]
                        if url.startswith(base_url):
                            o["listings"].append(url)
    if len(o["listings"]):
        return True, o
    o["error"] = dict(code=7, message="failed get listings", data="")
    return False, o


listing_funcs = [
    set_listings_url,
    get_page,
    get_metadata,
    extract_listings,
]


def pipeline(o, l):
    for func in l:
        r, o = func(o)
        if not r:
            break
    return o
