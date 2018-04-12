from sklearn.base import TransformerMixin
import osm.transformers.preprocessor as utils


class ColloquialTransformer(TransformerMixin):

    def __init__(self, colloq_dict=None) -> None:
        super().__init__()
        self.colloq_dict = colloq_dict
        self.colloq_pattern = utils.build_colloquial_regex_pattern(colloq_dict)

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return [utils.run_replace_colloquials(doc, self.colloq_dict, self.colloq_pattern) for doc in x]
