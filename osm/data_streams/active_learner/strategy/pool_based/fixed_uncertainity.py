from osm.data_streams.active_learner.strategy.abstract_strategy import AbstractActiveLearningStrategy


class FixedUncertainty(AbstractActiveLearningStrategy):
    def __init__(self, budget, oracle, target_col_name, measure='entropy', debug=True, threshold=None) -> None:
        """
        Implements the fixed uncertainty sampling strategy
        :param budget: The budged
        :param oracle: The oracle
        :param target_col_name: The name of the target column
        :param measure: The information gain measure
        :param debug: If True prints debug messages to console
        :param threshold: the threshold to check against
        """
        super().__init__(budget, oracle, target_col_name, measure, debug)
        self.threshold = threshold

    def below_threshold(self, gain):
        """
        Queries the oracle to get the data using the fixed uncertainty strategy
        :param gain: the information gain if the instance is used
        :return: True if the instance is sampled randomly
        """

        # check the threshold
        return True if self.measure.check(gain, self.threshold) else False

    def get_name(self):
        return "fixed_uncertainty"
