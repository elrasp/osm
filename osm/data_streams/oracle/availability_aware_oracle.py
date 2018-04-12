import numpy as np
from sklearn.utils import shuffle
from osm.data_streams.oracle.oracle import Oracle


class AvailabilityAwareOracle(Oracle):

    def __init__(self, availability: float, batch=False, min_labels=0) -> None:
        """
        An Oracle that provides true labels based on its availability

        :param min_labels: The minimum number of labels the oracle must provide
        :param availability: Value indicates the availability of the Oracle.
        :param batch: True if the same oracle availability is considered for the entire batch.
        If False for each instance the oracle availability is considered
        """

        if availability < 0 or availability > 1:
            raise ValueError("Availability: Out of range. Possible values: [0,1]")
        super().__init__()
        self.availability = availability
        self.batch = batch
        self.min_samples = min_labels

    def predict(self, X):
        """
        Get labels
        :param X: {array-like, dense matrix}, shape = [n_samples], the instances for which labels need to be obtained
        :return: {array-like, dense matrix}, shape = [n_samples], labels of the provided instances. np.nan if oracle
        is not available
        """
        self.queried = len(X)
        to_query = []
        if self.batch:
            if self.is_available():
                to_query = X
        else:
            for index in X:
                if self.is_available():
                    to_query.append(index)

        # if we do not satisfy the minimum number of instances required
        min_required = min(len(self.data), int(self.min_samples))
        if len(to_query) < min_required:
            additionally_required = min_required - len(to_query)
            additionally_required_data = shuffle(self.data.drop(to_query), n_samples=additionally_required)
            to_query.append(additionally_required_data.index.values)

        return super().predict(to_query)

    def is_available(self):
        """
        Function to check the availability of the oracle
        :return: True if the oracle is available
        """
        return np.random.uniform(0, 1) <= self.availability

    def get_name(self):
        return "availability_aware_oracle"
