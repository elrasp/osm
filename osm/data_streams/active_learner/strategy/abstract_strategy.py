from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
from datetime import datetime

from osm.data_streams.abstract_base_class import AbstractBaseClass
from osm.data_streams.active_learner.measures.measures_factory import get_measure
from osm.data_streams.oracle.oracle import Oracle
import osm.data_streams.constants as const


class AbstractActiveLearningStrategy(AbstractBaseClass):
    def __init__(self, budget, oracle, target_col_name, measure='entropy', debug=True) -> None:
        """
        Abstract class to implement several pool based strategies
        :param budget: The budged
        :param oracle: The oracle
        :param target_col_name: The name of the target column
        :param measure: The information gain measure
        :param debug: If True prints debug messages to console
        """
        super().__init__()

        if not isinstance(budget, np.float):
            raise ValueError("The budget should be a float between [0,1]")

        if budget < 0 or budget > 1:
            raise ValueError("The budget should be a float between [0,1]")

        if not isinstance(oracle, Oracle):
            raise ValueError("The oracle should be an instance of Oracle")

        self.budget = budget
        self.target_col_name = target_col_name
        self.oracle = oracle
        self.measure = get_measure(measure)
        self.debug = debug

    def get_labels(self, data, proba=None, index=0):
        """
        Queries the oracle to get the data
        :param proba: The predicted probabilities
        :param data: the data to query
        :param index: the index in the data stream
        :return: the queries answered by the oracle
        """
        if proba is None and self.get_name() is not "random":
            raise ValueError("Please provide the probabilities")

        if len(data) != len(proba):
            raise ValueError("The data and proba arrays do not match in length")

        # give the labels to the oracle
        self.oracle.fit(data, data[self.target_col_name])

        if hasattr(data, "iterrows"):
            # calculate the information gain measure
            gain = self.measure.calculate(proba)

            indices = []
            gain_index = 0
            for index, row in data.iterrows():
                # check the budget
                if len(indices)/len(data) >= self.budget:
                    break
                # check the threshold
                if self.below_threshold(gain[gain_index]):
                    indices.append(index)
                gain_index += 1

            labeled = self.oracle.predict(indices)
            return labeled if labeled.empty else data.loc[labeled.index.values, :]
        else:
            raise ValueError("A pandas dataframe expected")

    @abstractmethod
    def below_threshold(self, gain):
        """
        Checks if the gain is below the threshold for different strategies
        :param gain: the information gain if the instance is used
        :return: True if below the threshold else False
        """
        pass

    def get_stats(self, index=0):
        """
        Generates stats of how many queries were answered by the oracle
        and the total cost of labeling
        :param index: the index in the data stream for which the stats
        are required
        :return: the cost of labeling, number of queries, number of answered queries
        """
        pd_index = pd.MultiIndex.from_product([[const.active_learner_stats], [const.queried, const.answered, const.cost]])
        stats = pd.DataFrame(index=pd_index).T.copy()
        stats.loc[index, (const.active_learner_stats, const.cost)] = self.oracle.get_cost()
        stats.loc[index, (const.active_learner_stats, const.queried)] = self.oracle.get_total_queried()
        stats.loc[index, (const.active_learner_stats, const.answered)] = self.oracle.get_total_answered()

        if self.debug:
            print(str.format("{0}: Index: {1}\tQueried: {2}\tAnswered: {3}\tCost: {4}",
                  str(datetime.now()),
                  index,
                  self.oracle.get_total_queried(),
                  self.oracle.get_total_answered(),
                  self.oracle.get_cost()))

        return stats
