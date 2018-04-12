from sklearn.base import TransformerMixin
from textacy.preprocess import unpack_contractions


class ContractionTransformer(TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return [unpack_contractions(doc) for doc in x]
