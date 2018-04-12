import numpy as np

from osm.data_streams.active_learner.measures.abstract_measure import AbstractMeasure


class MaxPosterior(AbstractMeasure):
    """
    Calculates the maximum posterior probability
    """
    def calculate(self, proba):
        """
        Calculate the maximum posterior probability
        :param proba: the probabilities of prediction
        :return: the max posterior probability
        """
        return np.amax(proba, axis=1)

    def check(self, proba_x, threshold):
        """
        Checks if the instance x with max posterior proba_x
        can be sampled
        :param proba_x: the max posterior probability of x
        :param threshold: the threshold to compare with
        :return: True if it satisfies the threshold condition
        """
        return proba_x < threshold

    def get_name(self):
        return "max_posterior"
