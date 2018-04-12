from osm.data_streams.windows.abstract_window import AbstractWindow


class NoWindow(AbstractWindow):
    def __init__(self) -> None:
        """
        Does not implement any windowing strategy. So it only keeps adding data
        """
        super().__init__(window_size=None, apply_windowing=False)

    def forget(self):
        """
        Does not forget anything
        :return:
        """
        pass

    def get_name(self):
        return "no_window"
