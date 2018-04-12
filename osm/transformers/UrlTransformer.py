from sklearn.base import TransformerMixin
from textacy.preprocess import replace_urls


class UrlTransformer(TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return [replace_urls(doc) for doc in x]
