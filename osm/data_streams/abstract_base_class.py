from abc import ABC, abstractmethod


class AbstractBaseClass(ABC):
    @abstractmethod
    def get_name(self):
        """

        :return: the name of the type
        """
        pass

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
