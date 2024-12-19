from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem

from .filters import FiltersList

class VideoDisplay(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Layout principal horizontal
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Lista vertical à esquerda
        self.left_list = QListWidget()
        self.left_list.setMaximumWidth(150)  # Define largura máxima para a lista
        self.layout.addWidget(self.left_list)

        # Área de exibição do frame
        self.display_layout = QVBoxLayout()
        self.video_label = QLabel("Exibição")
        self.video_label.setStyleSheet("border: 1px solid black;")
        self.video_label.setMinimumSize(640, 480)  # Define um tamanho mínimo para o frame
        self.display_layout.addWidget(self.video_label)
        self.layout.addLayout(self.display_layout)

        # Lista vertical à direita
        filters = FiltersList(parent)
        self.right_list = filters
        self.layout.addWidget(self.right_list)
            
