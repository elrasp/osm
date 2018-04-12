from osm.data_streams.windows.abstract_window import AbstractWindow
from osm.data_streams.windows.forgetting_strategy.abstract_selective_forgetting import AbstractSelectiveForgetting


class SlidingWindow(AbstractWindow):

    def __init__(self, window_size, index=0, forgetting_strategy=None) -> None:
        """
        Implementation of a sliding method
        :param window_size: int: The window size
        :param index: int: The starting index of the window. Default 0
        :param forgetting_strategy: AbstractSelectiveForgetting: the forgetting strategy to be used
        """
        if forgetting_strategy is not None and not isinstance(forgetting_strategy, AbstractSelectiveForgetting):
            raise ValueError("The forgetting strategy should be an instance of AbstractSelectiveForgetting")

        super().__init__(window_size, index)
        self.forgetting_strategy = forgetting_strategy

    def forget(self):
        """
        If the window is full forgets data from the first timepoint.
        If the minimum count is set ensures that minimum number of instances are available before forgetting
        :return:
        """
        index_to_drop = self.get_first_index()

        if self.forgetting_strategy is not None:
            # sample data using the specified forgetting strategy
            # the data that will be dropped
            data_to_drop = self.get_window_data(index_to_drop)

            # the remaining data in the window
            data_remaining = self.get_window_data(range(index_to_drop + 1, index_to_drop + self.window_size, 1))

            # get the sampled data
            sampled_data = self.forgetting_strategy.sample_data(data_to_drop, data_remaining)

            # add the sampled data to the window
            self.add_to_window(sampled_data)

        # forget data from the first timepoint
        self.window_data.drop(index=index_to_drop, inplace=True, level=0)

    def get_name(self):
        return "sliding_window"
