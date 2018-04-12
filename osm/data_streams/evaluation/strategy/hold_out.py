import pandas as pd
from pandas import DataFrame

from osm.data_streams.evaluation.strategy.abstract_evaluation_strategy import AbstractEvaluationStrategy


class HoldOut(AbstractEvaluationStrategy):
    def __init__(self, target_col_name, test_data, evaluation_criteria=None) -> None:
        """
        Implements the hold out method for evaluating data streams
        :param target_col_name: the name of the target column
        :param test_data: the test data
        :param evaluation_criteria: the evaluation criteria
        """
        super().__init__(target_col_name, evaluation_criteria)
        if not isinstance(test_data, DataFrame):
            raise ValueError("The test_data must be an instance of DataFrame")

        if test_data is None or test_data.empty:
            raise ValueError("The test_data must be provided")

        self.test_data = test_data

    def evaluate(self, index, classifier, feature_pipeline, test_data=None) -> pd.DataFrame:
        """
        For hold out method we evaluate using the held out data
        :param index: index
        :param classifier: the fitted classifier
        :param feature_pipeline: the fitted pipeline
        :param test_data: the test data
        :return: the evaluation stats
        """
        return super().evaluate(index=index,
                                classifier=classifier,
                                feature_pipeline=feature_pipeline,
                                test_data=self.test_data) # test data is the held out data

    def get_name(self):
        return "hold_out_evaluation"
