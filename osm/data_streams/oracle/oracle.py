from abc import ABC, abstractmethod
import pandas as pd
from sklearn.base import BaseEstimator

from osm.data_streams.abstract_base_class import AbstractBaseClass


class Oracle(BaseEstimator, AbstractBaseClass):

    def __init__(self, cost_of_labelling=1) -> None:
        """
        An Oracle that provides true labels
        """
        super().__init__()
        self.data = pd.DataFrame()
        self.cost_of_labelling = cost_of_labelling
        self.queried = 0
        self.answered = 0

    def __getstate__(self):
        state = super().__getstate__()
        del state["data"]
        del state["cost_of_labelling"]
        del state["queried"]
        del state["answered"]
        return state

    def fit(self, X, y):
        """
        Fit the Oracle
        :param X: {array-like, dense matrix}, shape = [n_samples], the index of the instance
        :param y: {array-like, dense matrix}, shape = [n_samples], the label of the instance
        :return:
        """
        self.data = y

    def predict(self, X):
        """
        Get labels
        :param X: {array-like, dense matrix}, shape = [n_samples], the index of the instances for which labels need to be obtained
        :return: {array-like, dense matrix}, shape = [n_samples], labels of the provided instances. np.nan if oracle
        is not available
        """
        self.answered = len(X)
        return self.data[X]

    def get_cost(self):
        """
        Gets the total cost of labelling
        :return: the cost of labelling
        """
        return self.cost_of_labelling * self.queried

    def get_total_answered(self):
        """

        :return: The number of queries answered
        """
        return self.answered

    def get_total_queried(self):
        """

        :return: The total number of queries made to the oracle
        """
        return self.queried
