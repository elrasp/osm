import numpy as np

from osm.data_streams.active_learner.strategy.abstract_strategy import AbstractActiveLearningStrategy


class Random(AbstractActiveLearningStrategy):
    def below_threshold(self, gain):
        """
        Queries the oracle to get the data using the random strategy
        :param gain: the information gain if the instance is used
        :return: True if the instance is sampled randomly
        """

        return True if np.random.uniform(0, 1) <= self.budget else False

    def get_name(self):
        return "random"
