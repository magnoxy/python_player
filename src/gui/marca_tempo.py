
from PyQt5.QtWidgets import QListWidget

class VideoMarkerTime(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setMaximumWidth(150)
        self.addItems(self.parent.timers_list)
