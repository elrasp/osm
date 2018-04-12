import pandas as pd

from osm.data_streams.evaluation.strategy.abstract_evaluation_strategy import AbstractEvaluationStrategy


class Prequential(AbstractEvaluationStrategy):
    """
    Implements the prequential (interleaved test-then-train method) in data streams
    """
    def evaluate(self, index, classifier, feature_pipeline, test_data=None) -> pd.DataFrame:
        """
        Evaluates using the specified strategy for data streams
        :param index: index
        :param classifier: the fitted classifier
        :param feature_pipeline: the fitted pipeline
        :param test_data: the test data
        :return: the evaluation stats
        """
        return super().evaluate(index=index,
                                classifier=classifier,
                                feature_pipeline=feature_pipeline,
                                test_data=test_data)

    def get_name(self):
        return "prequential_evaluation"
