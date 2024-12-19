from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import Qt

class CascadeCheckbox(QCheckBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setText("Cascata")
        self.setChecked(False)
        self.stateChanged.connect(self.checkbox_changed)

    def checkbox_changed(self, state):
        if state == Qt.Checked:
            self.parent.cascade = True
        else:
            self.parent.cascade = False
    
