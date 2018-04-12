from osm.data_streams.active_learner.measures.entropy import Entropy
from osm.data_streams.active_learner.measures.max_posterior import MaxPosterior
from osm.data_streams.active_learner.measures.max_margin import MaxMargin


def get_measure(measure='entropy'):
    """
    Method that returns a class of the specified measure
    """
    supported_measures = ['least_confident', 'max_margin', 'entropy']
    if measure not in supported_measures:
        raise ValueError("The specified measure is not supported. Supported: " + str(supported_measures))

    if measure == supported_measures[0]:
        return MaxPosterior()
    elif measure == supported_measures[1]:
        return MaxMargin()
    elif measure == supported_measures[2]:
        return Entropy()
    else:
        return None
