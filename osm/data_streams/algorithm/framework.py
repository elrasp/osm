import os
import pathlib
from datetime import datetime

import jsonpickle
import pandas as pd
import time
from sklearn.base import BaseEstimator
from sklearn.pipeline import FeatureUnion, Pipeline

import osm.data_streams.constants as const
from osm.data_streams.abstract_base_class import AbstractBaseClass
from osm.data_streams.active_learner.strategy.abstract_strategy import AbstractActiveLearningStrategy
from osm.data_streams.evaluation.strategy.abstract_evaluation_strategy import AbstractEvaluationStrategy
from osm.data_streams.evaluation.strategy.prequential import Prequential
from osm.data_streams.oracle.availability_aware_oracle import AvailabilityAwareOracle
from osm.data_streams.windows.abstract_window import AbstractWindow
from osm.data_streams.windows.no_window import NoWindow


class FrameWork(AbstractBaseClass):

    def get_name(self):
        return "framework"

    def __init__(self,
                 summary_file,
                 base_estimator,
                 feature_pipeline,
                 target_col_name,
                 ild_timepoint=None,
                 active_learner=None,
                 window=None,
                 evaluation_strategy=None,
                 debug=True) -> None:

        """
        Abstract class for the evaluation strategies in data streams
        :param summary_file: A pandas dataframe containing a column filename. Each file name is the relative path
        of the file from the directory of the summary_file. Each file contains data that needs to be processed. The
        index of the filename gives the order in which the files need to be processed in the data stream
        :param base_estimator: The base estimator
        :param feature_pipeline: The pipeline to build the features
        :param target_col_name: the name of the target column
        :param ild_timepoint: the timepoint until which the initially labeled data is considered
        :param active_learner: the active learner
        :param evaluation_strategy: the evaluation strategy to be used. Default: prequential evaluation
        :param window: The type of Window to use
        """
        super().__init__()
        if summary_file is None:
            raise ValueError("Please pass the summary file")

        if not os.path.isfile(summary_file):
            raise ValueError("The summary file does not exist")

        if not "".join(pathlib.Path(summary_file).suffixes) == ".pkl.gzip":
            raise ValueError("The summary file should have a valid extension (*.pkl.gzip)")

        if not isinstance(base_estimator, BaseEstimator):
            raise ValueError("The base_estimator must be an instance of BaseEstimator")

        if not hasattr(base_estimator, "predict_proba"):
            raise ValueError("The base_estimator should be able to predict probabilities")

        if not isinstance(feature_pipeline, FeatureUnion) and not isinstance(feature_pipeline, Pipeline):
            raise ValueError("The feature_pipeline must be an instance of FeatureUnion or Pipeline")

        if active_learner is not None and not isinstance(active_learner, AbstractActiveLearningStrategy):
            raise ValueError("The active_learner must be an instance of AbstractActiveLearningStrategy")

        if window is not None and not isinstance(window, AbstractWindow):
            raise ValueError("The window must be an instance of AbstractWindow")

        if evaluation_strategy is not None and not isinstance(evaluation_strategy, AbstractEvaluationStrategy):
            raise ValueError("the evaluation_strategy must be an instance of AbstractEvaluationStrategy")

        if window is None:
            # default is no windowing
            window = NoWindow()

        if evaluation_strategy is None:
            # default
            evaluation_strategy = Prequential(target_col_name)

        self.summary = None
        self.base_estimator = base_estimator
        self.feature_pipeline = feature_pipeline
        self.active_learner = active_learner
        self.window = window
        self.debug = debug
        self.ild_timepoint = ild_timepoint
        self.target_col_name = target_col_name
        self.evaluation_strategy = evaluation_strategy
        self.classes = None

        # paths
        self.summary_filename = os.path.basename(summary_file)
        self.dir = os.path.dirname(summary_file)

        oracle_availability = ""
        strategy = ""

        if active_learner is not None:
            oracle = active_learner.oracle
            strategy = active_learner.get_name()
            if isinstance(oracle, AvailabilityAwareOracle):
                oracle_availability = oracle.availability

        self.dir_result = self.create_dir(self.dir, "results")
        self.dir_result = self.create_dir(self.dir_result, strategy)
        self.dir_result = self.create_dir(self.dir_result, str(oracle_availability))

    @staticmethod
    def create_dir(path, dir):
        path = os.path.join(path, dir)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def __getstate__(self):
        state = super().__getstate__()
        del state["summary"]
        del state["feature_pipeline"]
        state["ild_timepoint"] = str(self.ild_timepoint)
        return state

    def initialize(self):
        """
        Initialize the data stream
        """

        if os.path.isfile(os.path.join(self.dir_result, self.summary_filename)):
            # restore if part of the stream is already processed
            self.log("Restoring the window state")
            self.restore_state()
        else:
            self.log("Initializing")

            # read the summary file
            self.summary = pd.read_pickle(os.path.join(self.dir, self.summary_filename))

            if not isinstance(self.summary, pd.DataFrame):
                raise ValueError("The summary file specified is not a dataframe")

            if self.summary.empty:
                raise ValueError("The summary file is empty")

            if const.filename_col not in self.summary.columns.values:
                raise ValueError("The summary file does not contain a column 'filename'")

            # flag in the summary to check if the file is processed
            self.summary[const.processed] = False

            # set the default initial labeled data to the first timepoint
            if self.ild_timepoint is None:
                self.ild_timepoint = self.summary.index.values[0]

            # get the initially labeled data
            ild = pd.DataFrame()
            timepoint = -1
            for index, row in self.summary.iterrows():
                if index > self.ild_timepoint:
                    break

                self.log(str.format("Adding data from {0} to the initially labeled data", index))

                data = pd.read_pickle(os.path.join(self.dir, row[const.filename_col]))
                ild = ild.append(data)
                self.summary.loc[index, const.processed] = True
                timepoint += 1

            # set the window data to be the ild
            self.window.set_index(timepoint)
            self.window.add(ild)

            # reset the index of the summary file
            self.summary.reset_index(inplace=True, drop=False)

            # create a second level for the summary table
            summary = {const.summary_level: self.summary}

            self.summary = pd.concat(summary, axis=1)

            # create the time statistics columns
            pd_index = pd.MultiIndex.from_product([[const.time_stats], [const.train_time, const.test_time, const.sample_time]])
            time_stats = pd.DataFrame(index=pd_index).T.copy()
            self.summary = pd.concat([self.summary, time_stats])

            # log the parameters
            self.log_parameters()

            # save the data
            self.save_state(index=timepoint)

        # get the distinct clases
        self.classes = sorted(self.window.get_window_data()[self.target_col_name].unique())

        # train the classifier with the ild
        self.train(index=max(self.window.get_window_data().index.levels[0]))

    def train(self, index, test_data=None):
        train_time = time.time()

        # log the window stats
        stats = self.window.get_window_stats(index=index, classes=self.classes.copy(), target_col_name=self.target_col_name)
        self.summary = self.summary.combine_first(stats)

        # get the training data
        train_data = self.window.get_window_data()

        # log to console the number of instances in the window
        self.log(str.format("Index: {0}\tTrain Data: {1}", index, len(train_data)))

        # create features
        train_feature = self.feature_pipeline.fit_transform(train_data, train_data[self.target_col_name])

        # train the classifier
        self.base_estimator.fit(train_feature, train_data[self.target_col_name])

        train_time = time.time() - train_time

        # log the time taken
        self.summary.loc[index, (const.time_stats, const.train_time)] = train_time

    def test(self, index, test_data):
        test_time = time.time()

        # evaluate the test data
        evaluation_stats = self.evaluation_strategy.evaluate(index=index,
                                                             classifier=self.base_estimator,
                                                             feature_pipeline=self.feature_pipeline,
                                                             test_data=test_data)

        # update the stats to the  summary table
        self.summary = self.summary.combine_first(evaluation_stats)

        test_time = time.time() - test_time

        # log the time taken
        self.summary.loc[index, (const.time_stats, const.test_time)] = test_time

    def sample_data(self, index, test_data):
        sample_time = time.time()

        # create the test feature
        test_features = self.feature_pipeline.transform(test_data)

        # get probabilities
        prob = self.base_estimator.predict_proba(test_features)

        # sample data
        sampled_data = self.active_learner.get_labels(data=test_data, proba=prob, index=index)

        # log the stats
        stats = self.active_learner.get_stats(index=index)
        self.summary = self.summary.combine_first(stats)

        sample_time = time.time() - sample_time

        # log the time taken
        self.summary.loc[index, (const.time_stats, const.sample_time)] = sample_time

        return sampled_data

    def get_next_timepoint(self):
        """
        Gets the data for the next timepoint
        :return: index, data
        """
        max_index = max(self.summary.index.values)
        for index, row in self.summary.iterrows():
            if row[(const.summary_level, const.processed)] or index > max_index:
                continue
            data = pd.read_pickle(
                os.path.join(self.dir, row[(const.summary_level, const.filename_col)]))
            yield index, data

    def process_data_stream(self):
        """
        Call this function to start processing the data stream
        """

        # initialize
        self.initialize()

        # get the data from the next timepoint
        for index, data in self.get_next_timepoint():

            # send console message
            self.log(message=str.format("Index: {0}\tProcess Started", index))

            # test data
            self.test(index=index, test_data=data)

            # sample data
            labeled_data = self.sample_data(index=index, test_data=data)

            # add labeled data to window
            self.window.add(labeled_data)

            # save the state
            self.save_state(index=index)

            # train for the next iteration
            self.train(index=index)

            # send console message
            self.log(message=str.format("Index: {0}\tProcess Completed", index))

    def save_state(self, index):
        """
        Saves the current progress and the data in the window
        """
        # mark as processed
        self.summary.loc[index, (const.summary_level, const.processed)] = True

        # save the data in the window
        self.summary.loc[:, :].to_pickle(os.path.join(self.dir_result, self.summary_filename))

        # save the summary file
        self.window.get_window_data().to_pickle(os.path.join(self.dir_result, const.window_data_filename))

    def restore_state(self):
        """
        Restore the state of the stream processing
        """
        # restore the summary file
        self.summary = pd.read_pickle(os.path.join(self.dir_result, self.summary_filename))

        index = max(self.summary[self.summary.loc[:, (const.summary_level, const.processed)]].index.values)

        # restore the window data
        data = pd.read_pickle(os.path.join(self.dir_result, const.window_data_filename))
        self.window.restore_window(index=index, data=data)

    def log(self, message):
        """
        Logs a message to the console
        :param message: the message
        """
        if self.debug:
            print(str.format("{0}: {1}", datetime.now(), message))

    def log_parameters(self):
        """
        Log the current parameters to a file called param.txt
        """
        # create the file
        f = open(os.path.join(self.dir_result, "param.txt"), "w")

        # convert to json using json pickle
        json_obj = jsonpickle.encode(self)

        # write the results to the file
        f.write(json_obj)
        f.close()
