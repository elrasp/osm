import pandas as pd
import numpy as np
from datetime import datetime
from sklearn import metrics
from sklearn.utils.multiclass import unique_labels
from osm.data_streams import constants as const


class EvaluationCriteria(object):
    """
    Class to calculate the evaluation metrics. Supported metrics:
    Accuracy
    Precision
    Recall
    F1-Score
    Log loss
    Class wise: Precision, Recall, F1-Score and Support
    """
    def __init__(self,
                 accuracy=True,
                 precision=True,
                 recall=True,
                 f1=True,
                 log_loss=True,
                 individual_metrics=True,
                 debug=True) -> None:

        self.individual_metrics = individual_metrics
        self.log_loss = log_loss
        self.f1 = f1
        self.precision = precision
        self.recall = recall
        self.accuracy = accuracy
        self.debug = debug

    def get_accuracy(self, stats, index, y_true, y_pred):
        """
        Calculates the accuracy
        :param stats: the stats dataframe
        :param index: row index in the stats dataframe
        :param y_true: the true labels
        :param y_pred: the predicted labels
        """
        if self.accuracy:
            stats.loc[index, (const.summary_level, const.accuracy)] = metrics.accuracy_score(y_true, y_pred)

    def get_precision(self, stats, index, y_true, y_pred, labels=None, average=None):
        """
        Calculates the precision
        :param stats: the stats dataframe
        :param index: row index in the stats dataframe
        :param y_true: the true labels
        :param y_pred: the predicted labels
        :param labels: the distinct class names
        :param average
        """
        if self.precision:
            stats.loc[index, (const.summary_level, const.precision)] = metrics.precision_score(y_true, y_pred,
                                                                                              labels=labels,
                                                                                              average=average)

    def get_recall(self, stats, index, y_true, y_pred, labels=None, average=None):
        """
        Calculates the recall
        :param stats: the stats dataframe
        :param index: row index in the stats dataframe
        :param y_true: the true labels
        :param y_pred: the predicted labels
        :param labels: the distinct class names
        :param average
        """
        if self.recall:
            stats.loc[index, (const.summary_level, const.recall)] = metrics.recall_score(y_true, y_pred,
                                                                                           labels=labels,
                                                                                           average=average)

    def get_f1(self, stats, index, y_true, y_pred, labels=None, average=None):
        """
        Calculates the f1 score
        :param stats: the stats dataframe
        :param index: row index in the stats dataframe
        :param y_true: the true labels
        :param y_pred: the predicted labels
        :param labels: the distinct class names
        :param average
        """
        if self.f1:
            stats.loc[index, (const.summary_level, const.f1)] = metrics.f1_score(y_true, y_pred,
                                                                                 labels=labels,
                                                                                 average=average)

    def get_log_loss(self, stats, index, y_true, y_pred_proba, labels=None):
        """
        Calculates the log loss
        :param stats: the stats dataframe
        :param index: row index in the stats dataframe
        :param y_true: the true labels
        :param y_pred_proba: the probabilities of prediction
        :param labels: the distinct class names
        """
        if self.log_loss and y_pred_proba is not None:
            try:
                value = metrics.log_loss(y_true, y_pred_proba, labels=labels)
            except ValueError:
                value = np.NaN

            stats.loc[index, (const.summary_level, const.log_loss)] = value

    def get_class_wise_metrics(self, index, y_true, y_pred, labels=None):
        """
        Calculates the precision, recall, f1 score and support of each class
        :param index: the index in the data stream for which the evaluation is done
        :param y_true: the true classes
        :param y_pred: the predicted labels
        :param labels: the distinct class names
        :return: the precision, recall, f1 score and support of each class
        """
        pd_index = pd.MultiIndex.from_product([[const.precision, const.recall, const.f1, const.support], labels])
        stats = pd.DataFrame(index=pd_index).T.copy()
        if self.individual_metrics:
            p, r, f, s = metrics.precision_recall_fscore_support(y_true, y_pred, labels=labels)
            for label, pr, re, fb, su in zip(labels, p, r, f, s):
                stats.loc[index, (const.precision, label)] = pr
                stats.loc[index, (const.recall, label)] = re
                stats.loc[index, (const.f1, label)] = fb
                stats.loc[index, (const.support, label)] = su
        return stats

    def get_criteria_names(self, y_predict_proba=None):
        criteria = []
        if self.accuracy:
            criteria.append(const.accuracy)
        if self.precision:
            criteria.append(const.precision)
        if self.recall:
            criteria.append(const.recall)
        if self.f1:
            criteria.append(const.f1)
        if self.log_loss and y_predict_proba is not None:
            criteria.append(const.log_loss)
        return criteria

    def evaluate(self, index, y_true, y_predict, y_predict_proba) -> pd.DataFrame:
        """
        Calculates the specified metrics
        :param index: the index in the data stream for which the evaluation is done
        :param y_true: The true labels
        :param y_predict: The predicted labels
        :param y_predict_proba: The probabilities of the predictions
        :return: The evaluation metrics
        """
        labels = unique_labels(y_true, y_predict)
        average = "weighted"

        pd_index = pd.MultiIndex.from_product(
            [[const.summary_level], self.get_criteria_names(y_predict_proba=y_predict_proba)])
        stats = pd.DataFrame(index=pd_index).T.copy()

        self.get_accuracy(stats, index, y_true, y_predict)
        self.get_precision(stats, index, y_true, y_predict, labels, average)
        self.get_recall(stats, index, y_true, y_predict, labels, average)
        self.get_f1(stats, index, y_true, y_predict, labels, average)
        self.get_log_loss(stats, index, y_true, y_predict_proba, labels)

        class_wise_metrics = self.get_class_wise_metrics(index, y_true, y_predict, labels)
        if not class_wise_metrics.empty:
            stats = stats.join(class_wise_metrics, how="inner")

        if self.debug:
            print(str.format("{0}: Index: {1}\tF1: {2}\tLog loss: {3}", str(datetime.now()),
                             index,
                             stats.loc[index, (const.summary_level, const.f1)],
                             stats.loc[index, (const.summary_level, const.log_loss)]))

        return stats
