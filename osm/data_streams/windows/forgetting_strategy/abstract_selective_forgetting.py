from abc import ABC, abstractmethod

from osm.data_streams.abstract_base_class import AbstractBaseClass


class AbstractSelectiveForgetting(AbstractBaseClass):

    def __init__(self) -> None:
        """
        Abstract class that implements selective forgetting strategies
        """
        super().__init__()

    @abstractmethod
    def sample_data(self, data_to_forget, remaining_data):
        """
        Based on the forgetting strategy, samples data from the data to forget
        :param data_to_forget: The data to be forgotten
        :param remaining_data: The remaining data in the window
        :return: The sampled data
        """
        pass
