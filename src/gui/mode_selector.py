from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QPushButton
from PyQt5.QtGui import QIcon
import os

class ModeSelector(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Dropdown para selecionar Imagem ou Vídeo
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Imagem", "Vídeo", "Webcam"])
        self.layout.addWidget(self.mode_selector)

        # Caminho para o ícone
        icon_path = os.path.join("src", "assets", "arquivo.png")

        # Botão para abrir arquivo
        self.open_button = QPushButton(QIcon(icon_path), "")  # Passa o caminho do ícone
        self.layout.addWidget(self.open_button)

        # self.open_button.clicked.connect(self.parent.open_file_dialog)
