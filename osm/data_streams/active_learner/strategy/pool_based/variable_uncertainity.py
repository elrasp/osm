from osm.data_streams.active_learner.strategy.abstract_strategy import AbstractActiveLearningStrategy


class VariableUncertainty(AbstractActiveLearningStrategy):
    def __init__(self, budget, oracle, target_col_name, measure='entropy', debug=True, step=0.01) -> None:
        """
        Implements the fixed uncertainty sampling strategy
        :param budget: The budged
        :param oracle: The oracle
        :param target_col_name: The name of the target column
        :param measure: The information gain measure
        :param debug: If True prints debug messages to console
        :param step: The step size with which the threshold varies
        """
        super().__init__(budget, oracle, target_col_name, measure, debug)

        if step <= 0 or step > 1:
            raise ValueError("The step size should be in the range (0,1]")

        self.threshold = self.measure.get_max_value()
        self.step = step

    def below_threshold(self, gain):
        """
        Queries the oracle to get the data using the variable uncertainty strategy
        :param gain: the information gain if the instance is used
        :return: True if the instance is sampled randomly
        """

        # check the threshold
        if self.measure.check(gain, self.get_threshold()):
            # certainty bad decrease the threshold
            self.threshold = self.measure.decrease_threshold(self.threshold, self.step)
            return True
        else:
            # certainty good increase the threshold
            self.threshold = self.measure.increase_threshold(self.threshold, self.step)
            return False

    def get_threshold(self):
        """

        :return: the threshold to check with
        """
        return self.threshold

    def get_name(self):
        return "variable_uncertainty"
