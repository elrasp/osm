from sklearn.base import TransformerMixin
from textacy.preprocess import normalize_whitespace


class WhitespaceTransformer(TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return [normalize_whitespace(doc) for doc in x]
