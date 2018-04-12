import pandas as pd
import numpy as np
from abc import ABC, abstractmethod

from osm.data_streams.abstract_base_class import AbstractBaseClass
import osm.data_streams.constants as const


class AbstractWindow(AbstractBaseClass):
    def __init__(self, window_size, index=0, apply_windowing=True) -> None:
        """

        :param window_size: int: The window size
        :param index: int: The start index to use. As data is added to the window, the index is incremented
        :param apply_windowing: bool: If false does not apply any windowing
        """
        super().__init__()

        if apply_windowing and (window_size is None or window_size == 0):
            raise ValueError("Please specify the window size")
        self.window_size = window_size
        self.window_data = None
        self.index = index
        self.apply_windowing = apply_windowing

    def __getstate__(self):
        state = super().__getstate__()
        del state['window_data']
        del state['index']
        return state

    def get_window_size(self):
        """
        Gets the configured window size
        :return: the configure window size
        """
        return self.window_size

    def get_window_data(self, index=None):
        """
        Returns the window data for the specified index
        :param index: {int, range}
        :return: the window data for the specified index
        """
        if self.window_data is None:
            raise ValueError("The window is not initialized")
        if index is None:
            index = self.window_data.index.values
        elif isinstance(index, range):
            index = list(index)
        return self.window_data.loc[index, :]

    def get_first_index(self):
        """
        Returns the first index of the window
        :return: the first index of the window
        """
        if self.window_data is not None and not self.window_data.empty:
            return self.window_data.index.levels[0][0]
        else:
            return self.index

    def get_last_index(self):
        """
        Returns the last index of the window
        :return: the last index of the window
        """
        if self.window_data is not None and not self.window_data.empty:
            return self.window_data.index.levels[0][-1]
        else:
            return self.index

    def is_full(self):
        """
        Checks if the window is full
        :return: True if the window is full
        """
        if self.window_data is not None:
            return not self.window_data.empty and len(self.window_data.index.get_level_values(0).unique()) == self.window_size
        else:
            raise ValueError("The window is not initialized")

    def add(self, X):
        """
        Adds the data to the window and forgets data if the window is full
        :param X: The data to be added
        :return:
        """
        # initialize the window
        if self.window_data is None:
            self.window_data = pd.DataFrame()

        # forget the data from the window if the window is full and if we have something to add
        if not X.empty and self.apply_windowing and self.is_full():
            self.forget()

        # add the data to the window
        self.add_to_window(X)

        # increment the index
        self.index = self.index + 1

    def add_to_window(self, X):
        """
        Adds the data to the  window
        :param X: The data to add to the window
        """
        if X is None or X.empty:
            return
        data = {self.index: X}
        self.window_data = self.window_data.append(pd.concat(data))

    def restore_window(self, index, data):
        """
        Restores the window data
        :param data: the data with which the window is initialized
        """
        self.window_data = data
        self.index = index

    def set_index(self, index):
        """
        sets the start index of the window
        :param index: the start index of the window
        :return:
        """
        self.index = index

    def get_window_stats(self, index:int, classes: list, target_col_name: str) -> pd.DataFrame:
        """
        Gets the window statistics for the specified classes
        :param index: index for the stats
        :param classes: the classes for which the statistics need to be extracted
        :param target_col_name: the name of the target column
        :return: the window statistics
        """
        classes.insert(0, const.total)
        pd_index = pd.MultiIndex.from_product([[const.window_stats], classes])
        stats = pd.DataFrame(index=pd_index).T.copy()

        data = self.get_window_data()

        other_columns = list(data.columns.values)
        other_columns.remove(target_col_name)

        counts = dict(data.groupby(by=target_col_name).count()[other_columns[0]])

        for clazz in classes:
            if clazz == const.total:
                value = np.sum(list(counts.values()))
            else:
                value = counts.get(clazz)
            stats.loc[index, (const.window_stats, clazz)] = value

        return stats

    @abstractmethod
    def forget(self):
        """
        Forget data from the window
        :return:
        """
        pass
