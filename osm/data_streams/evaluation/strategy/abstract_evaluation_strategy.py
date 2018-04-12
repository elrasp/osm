from abc import abstractmethod

from pandas import DataFrame
from sklearn.base import BaseEstimator
from sklearn.pipeline import FeatureUnion, Pipeline

from osm.data_streams.abstract_base_class import AbstractBaseClass
from osm.data_streams.evaluation.evaluation_criteria import EvaluationCriteria


class AbstractEvaluationStrategy(AbstractBaseClass):

    def __init__(self, target_col_name, evaluation_criteria=None) -> None:
        """
        Abstract class to implement evaluation strategies in data streams
        :param target_col_name: the name of the target column
        :param evaluation_criteria: the evaluation criteria
        """
        super().__init__()
        if not evaluation_criteria is None and not isinstance(evaluation_criteria, EvaluationCriteria):
            raise ValueError("The evaluation criteria must be an instance of EvaluationCriteria")

        if evaluation_criteria is None:
            evaluation_criteria = EvaluationCriteria()

        self.target_col_name = target_col_name
        self.evaluation_criteria = evaluation_criteria

    @abstractmethod
    def evaluate(self, index, classifier, feature_pipeline, test_data=None):
        """
        Evaluates using the specified strategy for data streams
        :param index: index
        :param classifier: the fitted classifier
        :param feature_pipeline: the fitted pipeline
        :param test_data: the test data
        :return: the evaluation stats
        """
        if not isinstance(classifier, BaseEstimator):
            raise ValueError("The classifier must be an instance of BaseEstimator")

        if not isinstance(feature_pipeline, FeatureUnion) and not isinstance(feature_pipeline, Pipeline):
            raise ValueError("The feature_pipeline must be an instance of FeatureUnion or Pipeline")

        if not isinstance(test_data, DataFrame):
            raise ValueError("The test_data must be an instance of DataFrame")

        if test_data is None or test_data.empty:
            raise ValueError("The test_data is not provided")

        # create the test features
        test_features = feature_pipeline.transform(test_data)

        # get the predictions
        y_predict = classifier.predict(test_features)

        y_predict_proba = None
        if hasattr(classifier, "predict_proba"):
            y_predict_proba = classifier.predict_proba(test_features)

        return self.evaluation_criteria.evaluate(index=index,
                                                 y_predict=y_predict,
                                                 y_true=test_data[self.target_col_name],
                                                 y_predict_proba=y_predict_proba)
