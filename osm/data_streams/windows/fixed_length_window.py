import collections

from osm.data_streams.windows.abstract_window import AbstractWindow


class FixedLengthWindow(AbstractWindow):

    def add(self, X):
        if isinstance(X, collections.Iterable):
            for x in X.__iter__():
                # for each instance create a new index
                super().add(x)
        else:
            super().add(X)

    def forget(self):
        # drop the first instance
        index_to_drop = self.window_data.index.levels[0][-self.window_size-1]
        self.window_data.drop(index=index_to_drop, inplace=True, level=0)

    def get_name(self):
        return "fixed_length_window"
