import numpy as np

from osm.data_streams.active_learner.strategy.pool_based.variable_uncertainity import VariableUncertainty


class RandomizedVariableUncertainty(VariableUncertainty):
    def __init__(self, budget, oracle, target_col_name, measure='entropy', debug=True, step=0.01, variance=1) -> None:
        """
        Implements the fixed uncertainty sampling strategy
        :param budget: The budged
        :param oracle: The oracle
        :param target_col_name: The name of the target column
        :param measure: The information gain measure
        :param debug: If True prints debug messages to console
        :param step: The step size with which the threshold varies
        :param variance: variance of normally distributed random variable
        """
        super().__init__(budget, oracle, target_col_name, measure, debug, step)
        self.variance = variance

    def get_threshold(self):
        """

        :return: randomized threshold
        """
        return self.threshold * np.random.normal(1, np.math.sqrt(self.variance))

    def get_name(self):
        return "variable_randomized_uncertainty"
