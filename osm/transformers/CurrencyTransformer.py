from sklearn.base import TransformerMixin
from textacy.preprocess import replace_currency_symbols


class CurrencyTransformer(TransformerMixin):

    def __init__(self, replace_currency_with=None) -> None:
        super().__init__()
        self.replace_currency_with = replace_currency_with

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return [replace_currency_symbols(doc, self.replace_currency_with) for doc in x]
