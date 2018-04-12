import numpy as np
from scipy.stats import entropy

from osm.data_streams.active_learner.measures.abstract_measure import AbstractMeasure


class Entropy(AbstractMeasure):
    """
    Calculates the entropy
    """
    def calculate(self, proba):
        """
        Calculate the entropy
        :param proba: the probabilities of prediction
        :return: the entropy scores
        """
        return np.apply_along_axis(entropy, 1, proba, base=proba.shape[1])

    def check(self, entropy_x, threshold):
        """
        Checks if the instance x with entropy x can be sampled.
        For entropy higher values mean more uncertain
        :param entropy_x: the entropy of x
        :param threshold: the threshold to compare with
        :return: True if it satisfies the threshold condition
        """
        return self.get_max_value() - entropy_x < threshold

    def get_name(self):
        return "entropy"
