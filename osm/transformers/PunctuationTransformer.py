from sklearn.base import TransformerMixin
from textacy.preprocess import remove_punct


class PunctuationTransformer(TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return [remove_punct(doc) for doc in x]
