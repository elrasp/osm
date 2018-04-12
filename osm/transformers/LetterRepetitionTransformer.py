from sklearn.base import TransformerMixin
import osm.transformers.preprocessor as utils


class LetterRepetitionTransformer(TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return [utils.run_replace_repeated_letters(doc) for doc in x]
