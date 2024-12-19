from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QPushButton, QFileDialog
from PyQt5.QtGui import QIcon
import os

class ModeSelector(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Dropdown para selecionar Imagem, Vídeo ou Webcam
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Imagem", "Vídeo", "Webcam"])
        self.layout.addWidget(self.mode_selector)

        # Caminho para o ícone
        icons_path = os.path.join("src", "assets")
        icon_file = os.path.join(icons_path, "arquivo.png")
        icon_save = os.path.join(icons_path, "salvar.png")

        # Botão para abrir arquivo
        self.open_button = QPushButton(QIcon(icon_file), "")  # Passa o caminho do ícone
        self.layout.addWidget(self.open_button)
        
        self.save_button = QPushButton(QIcon(icon_save), "")
        self.layout.addWidget(self.save_button)

        # Conecta o botão ao método de abertura de diálogo
        self.open_button.clicked.connect(self.open_file_dialog)

    def open_file_dialog(self):
        mode = self.mode_selector.currentText()  # Obtém o modo selecionado no ComboBox
        file_path = None

        if mode == "Imagem":
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Selecione uma Imagem",
                "",
                "Imagens (*.png *.jpg *.jpeg *.bmp)"
            )
            if file_path:
                self.parent.file_path = file_path
                self.parent.reset_frames()
                # Atualiza o display para a imagem carregada
                self.parent.update_display()
        elif mode == "Vídeo":
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Selecione um Vídeo",
                "",
                "Vídeos (*.mp4 *.avi *.mkv *.mov)"
            )
            if file_path:
                self.parent.file_path = file_path
                self.parent.reset_frames()
                # Atualiza o display para o vídeo carregado
                self.parent.update_display()
        elif mode == "Webcam":
            self.parent.file_path = "Webcam"
            # Chame o método para iniciar a webcam, se implementado
