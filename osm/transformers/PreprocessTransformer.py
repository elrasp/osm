from sklearn.base import TransformerMixin, BaseEstimator
import osm.transformers.preprocessor as utils


class PreprocessTransformer(BaseEstimator, TransformerMixin):

    def __init__(self,
                 replace_urls=False,
                 replace_emoticons=False,
                 replace_exclamations=False,
                 replace_punctuations=False,
                 replace_numbers=False,
                 replace_negations=False,
                 replace_colloquials=False,
                 replace_repeated_letters=False,
                 replace_contractions=False,
                 replace_whitespace=True,
                 replace_currency=False,
                 replace_currency_with=None,
                 colloq_dict=None
                 ) -> None:
        if replace_colloquials is True and colloq_dict is None:
            raise ValueError("The colloquial dictionary is missing")

        super().__init__()
        self.replace_urls = replace_urls
        self.replace_emoticons = replace_emoticons
        self.replace_exclamations = replace_exclamations
        self.replace_punctuations = replace_punctuations
        self.replace_numbers = replace_numbers
        self.replace_negations = replace_negations
        self.replace_colloquials = replace_colloquials
        self.replace_repeated_letters = replace_repeated_letters
        self.replace_contractions = replace_contractions
        self.replace_whitespace = replace_whitespace
        self.replace_currency = replace_currency
        self.replace_currency_with = replace_currency_with
        self.colloq_dict = colloq_dict

        self.colloq_pattern = None
        # build regex for colloquials
        if replace_colloquials is True:
            self.colloq_pattern = utils.build_colloquial_regex_pattern(self.colloq_dict)

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return [utils.run_preprocessor(doc,
                                       replace_urls=self.replace_urls,
                                       replace_emoticons=self.replace_emoticons,
                                       replace_exclamations=self.replace_exclamations,
                                       replace_punctuations=self.replace_punctuations,
                                       replace_numbers=self.replace_numbers,
                                       replace_negations=self.replace_numbers,
                                       replace_colloquials=self.replace_colloquials,
                                       replace_repeated_letters=self.replace_repeated_letters,
                                       replace_contractions=self.replace_contractions,
                                       replace_whitespace=self.replace_whitespace,
                                       replace_currency=self.replace_currency,
                                       replace_currency_with=self.replace_currency_with,
                                       colloq_dict=self.colloq_dict,
                                       colloq_pattern=self.colloq_pattern
                                       ) for doc in x]
