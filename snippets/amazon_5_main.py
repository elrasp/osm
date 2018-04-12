import sys
from datetime import datetime
import os
import pandas as pd
import numpy as np
import plac
import warnings
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import chi2
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import MinMaxScaler

sys.path.append('../')
from osm.data_streams.active_learner.strategy.pool_based.random import Random
from osm.data_streams.active_learner.strategy.pool_based.variable_randomized_uncertainity import \
    RandomizedVariableUncertainty
from osm.data_streams.active_learner.strategy.pool_based.variable_uncertainity import VariableUncertainty
from osm.data_streams.evaluation.strategy.prequential import Prequential


import snippets.amazon_constants_columns as cols
import snippets.amazon_constants_file_paths as paths
from osm.data_streams.windows.sliding_window import SlidingWindow
from osm.data_streams.oracle.availability_aware_oracle import AvailabilityAwareOracle
from osm.data_streams.windows.forgetting_strategy.threshold import FixedThreshold
from osm.transformers.Selectors import TextSelector, StatsSelector, SelectDynamicKBest
from osm.data_streams.active_learner.strategy.pool_based.fixed_uncertainity import FixedUncertainty
from osm.data_streams.algorithm.framework import FrameWork


warnings.filterwarnings('ignore')
np.seterr(all='ignore')


def get_feature_pipeline():
    
    tfidf = Pipeline([
	('selector', TextSelector(key='ngrams')),
        ('vect', DictVectorizer()),
        ('kbest', SelectDynamicKBest(chi2, k_max=15000)),
        ('tfidf', TfidfTransformer())
    ])

    return tfidf



@plac.annotations(
    oracle_availability=("Oracle availability. Default: 0.1", "option", "a", float)
)
def main(oracle_availability=0.1):
    summary_file = os.path.join(paths.DIR_FILE_REVIEW_WEEKLY, "summary_converted" + paths.EXT_PKL)
    target_col_name = cols.STARS
    ild_timepoint = datetime(2011, 1, 10)

    

    # initialize oracle
    oracle = AvailabilityAwareOracle(availability=oracle_availability)

    # initialize active learner
    active_learners = [Random(budget=0.1, oracle=oracle, target_col_name=target_col_name),
                       FixedUncertainty(budget=0.1, oracle=oracle, target_col_name=target_col_name, threshold=0.9),
                       VariableUncertainty(budget=0.1, oracle=oracle, target_col_name=target_col_name, step=0.01),
                       RandomizedVariableUncertainty(budget=0.1, oracle=oracle, target_col_name=target_col_name,
                                                     step=0.01, variance=1)]


    for active_learner in active_learners:

        base_estimator = CalibratedClassifierCV(SGDClassifier(max_iter=1000, n_jobs=-1, class_weight="balanced"))

        # initialize window
        forgetting_strategy = FixedThreshold(min_count=3, classes=["negative", "neutral", "positive"], target_col_name=target_col_name)
        window = SlidingWindow(window_size=5, forgetting_strategy=forgetting_strategy)

        # initialize evaluation strategy
        eval_strategy = Prequential(target_col_name)

        # create the feature processing pipeline
        pipe = get_feature_pipeline()

        # build the framework
        framework = FrameWork(summary_file=summary_file,
                              base_estimator=base_estimator,
                              feature_pipeline=pipe,
                              target_col_name=target_col_name,
                              ild_timepoint=ild_timepoint,
                              active_learner=active_learner,
                              window=window,
                              evaluation_strategy=eval_strategy
                              )

        framework.process_data_stream()


if __name__ == '__main__':
    plac.call(main)
