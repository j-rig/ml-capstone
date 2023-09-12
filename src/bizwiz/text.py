import nltk
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.download("punkt")
nltk.download("stopwords")


def preprocess_text(text):
    text = text.lower()
    text_p = "".join([char for char in text if char not in string.punctuation])
    words = word_tokenize(text_p)
    stop_words = stopwords.words("english")
    stop_words.append("bizbuysell")
    filtered_words = [word for word in words if word not in stop_words]
    porter = PorterStemmer()
    stemmed = [porter.stem(word) for word in filtered_words]
    return " ".join(stemmed)
