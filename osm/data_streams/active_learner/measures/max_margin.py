import numpy as np

from osm.data_streams.active_learner.measures.abstract_measure import AbstractMeasure


class MaxMargin(AbstractMeasure):
    """
    Calculates the max margin measure
    """
    def calculate(self, proba):
        """
        Calculate the max margin measure
        :param proba: the probabilities of prediction
        :return: the max margin scores
        """
        margin = np.partition(-proba, 1, axis=1)
        return -np.abs(margin[:, 0] - margin[:, 1])

    def check(self, max_margin, threshold):
        """
        Checks if the instance x with max_margin can be sampled
        :param max_margin: the max_margin of x
        :param threshold: the threshold to compare with
        :return: True if it satisfies the threshold condition
        """
        return max_margin < threshold

    def get_name(self):
        return "max_margin"
