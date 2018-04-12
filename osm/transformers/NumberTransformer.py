from sklearn.base import TransformerMixin
from textacy.preprocess import replace_numbers


class NumberTransformer(TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return [replace_numbers(doc) for doc in x]
