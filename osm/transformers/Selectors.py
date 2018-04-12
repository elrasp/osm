from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_selection import SelectKBest, f_classif


class TextSelector(BaseEstimator, TransformerMixin):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    Use on text columns in the data
    """

    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if self.key == 'index':
            return X.index.get_level_values('review_id')
        return X[self.key]


class NumberSelector(BaseEstimator, TransformerMixin):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    Use on numeric columns in the data
    """

    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[[self.key]]


class StatsSelector(BaseEstimator, TransformerMixin):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    Use on numeric columns in the data
    """

    def __init__(self, stats_dataset, key, dtype):
        self.dtype = dtype
        self.keys = key
        self.stats_dataset = stats_dataset

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [[self.dtype(self.stats_dataset.loc[review_id, key]) for key in self.keys] for review_id in X]


class CategorySelector(BaseEstimator, TransformerMixin):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    Use on numeric columns in the data
    """

    def __init__(self, category_dataset):
        self.category_dataset = category_dataset

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # return [[value for value in self.category_dataset.loc[business_id].as_sparse_array().get_values()] for business_id in X]
        return self.category_dataset.loc[X].to_coo()


class SelectDynamicKBest(SelectKBest):

    def __init__(self, score_func=f_classif, k_max=10):
        super().__init__(score_func, k_max)
        self.k_max = k_max

    def _check_params(self, X, y):
        self.k = min(X.shape[1], self.k_max)
        return super()._check_params(X, y)
