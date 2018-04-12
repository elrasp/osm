from sklearn.base import TransformerMixin

from osm.transformers.preprocessor import run_regex


class RegexTransformer(TransformerMixin):

    def __init__(self, regex, replacement) -> None:
        super().__init__()
        self.regex = regex
        self.replacement = replacement

    def convert(self, doc):
        return run_regex(self.regex, self.replacement, doc)

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [self.convert(doc) for doc in X]


