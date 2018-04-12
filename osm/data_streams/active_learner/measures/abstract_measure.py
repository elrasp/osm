from abc import ABC, abstractmethod

from osm.data_streams.abstract_base_class import AbstractBaseClass


class AbstractMeasure(AbstractBaseClass):

    @abstractmethod
    def calculate(self, proba):
        """
        Calculates the confidence of the sample using the specified measure
        :param proba: probabilities of prediction
        :return:
        """
        pass

    @abstractmethod
    def check(self, proba_x, threshold):
        """
        Checks if an instance x with probability proba_x can be sampled for
        the given threshold
        :param proba_x: the probability of x
        :param threshold: the threshold to compare with
        :return: True if it satisfies the threshold condition
        """
        pass

    @staticmethod
    def get_max_value():
        """
        Gets the maximum possible value for the measure
        :return: The maximum possible value for the measure
        """
        return 1

    @staticmethod
    def increase_threshold(threshold, step):
        """
        Increase the threshold by the specified step
        :return: the new threshold
        """
        return threshold * (1 + step)

    @staticmethod
    def decrease_threshold(threshold, step):
        """
        Decrease the threshold by the specified step
        :return: the new threshold
        """
        return threshold * (1 - step)
