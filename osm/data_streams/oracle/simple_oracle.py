from osm.data_streams.oracle.oracle import Oracle


class SimpleOracle(Oracle):
    """
    A simple oracle where for every query the oracle provides an answer
    """

    def predict(self, X):
        self.queried += len(X)
        return super().predict(X)

    def get_name(self):
        return "simple_oracle"
