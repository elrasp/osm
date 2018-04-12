import numpy as np
import pandas as pd
from sklearn.utils import shuffle
from sklearn.utils.multiclass import unique_labels

from osm.data_streams.windows.forgetting_strategy.abstract_selective_forgetting import AbstractSelectiveForgetting


class Threshold(AbstractSelectiveForgetting):

    def __init__(self, threshold, classes, target_col_name) -> None:
        """
        Before forgetting ensures that a fixed minimum number of instances
        from every class is available as mentioned by the thresholds
        :param threshold: dict: the minimum number of instances that each class should contain
        :param classes: the list of distinct classes
        :param target_col_name: the column name of the target
        """
        super().__init__()
        self.target_col_name = target_col_name
        self.classes = classes
        self.threshold = threshold

    def __getstate__(self):
        state = super().__getstate__()
        state["threshold"] = [value for value in self.threshold]
        return state

    def get_name(self):
        return "threshold_forgetting"

    def sample_data(self, data_to_forget, remaining_data):
        """
        Samples the required the number of instances from the data_to_forget
        so that each class has a minimum number of instances
        :param data_to_forget: the data to forget
        :param remaining_data: the remaining data in the window
        :return:
        """
        # check if there is sufficient data
        required_data = self.get_required_data(remaining_data)

        # sample the required data from the data that will be dropped
        sampled_data = pd.DataFrame()
        if not required_data.empty:
            for clazz, count in required_data.iteritems():
                # get the data from the class
                clazz_data = data_to_forget[data_to_forget[self.target_col_name] == clazz]

                # sample data randomly
                instances = shuffle(clazz_data, n_samples=min(max(0, int(count)), len(clazz_data)))

                sampled_data = sampled_data.append(instances)
        return sampled_data

    def get_required_data(self, data):
        """
        Check if the data has sufficient instances from every class and gives a count of additional instances required
        from every class
        :param data: The data to be checked
        :return: The number of instances to be sampled from every class to satisfy the minimum count required
        """

        # check if all the labels are there in the sampled data
        data_labels = unique_labels(data[self.target_col_name])

        # check if the next window has samples from all classes
        try:
            same_labels = (self.classes == data_labels).all()
        except:
            same_labels = False

        class_count = data.groupby(self.target_col_name)[self.target_col_name].count()
        class_count = self.threshold - class_count
        if not same_labels:
            indices = np.isnan(class_count)
            class_count[indices] = self.threshold[indices]

        return class_count


class FixedThreshold(Threshold):
    def __init__(self, min_count, classes, target_col_name) -> None:
        """
        Fixed number of instances that should be available in the window
        :param min_count: the min number of instances
        :param classes: the distinct classes
        :param target_col_name: the column name of the target
        """
        threshold = {clazz: min_count for clazz in classes}
        threshold = pd.Series(threshold)
        super().__init__(threshold, classes, target_col_name)

    def get_name(self):
        return "fixed_threshold_forgetting"
