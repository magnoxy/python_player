from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

import cv2

from .filters import FiltersList
from .marca_tempo import VideoMarkerTime

class VideoDisplay(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Layout principal horizontal
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Lista vertical à esquerda
        times_marked = VideoMarkerTime(parent)
        self.left_list = times_marked
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

    def update_display(self):
        if not self.parent.frames_list:
            # Caso não tenha frames na lista, não faz nada
            return
        else:
            self.parent.current_frame = self.parent.frames_list[0]

        if not self.parent.frames_list or self.parent.current_frame is None:
            # self.roi_button.setEnabled(False)
            return

        # self.roi_button.setEnabled(True)
        # Dimensões do QLabel
        label_width = self.video_label.width()
        label_height = self.video_label.height()

        # Seleciona o primeiro frame da lista de frames
        self.parent.current_frame = self.parent.frames_list[0]

        # Dimensões do frame original
        frame_height, frame_width = self.parent.current_frame.shape[:2]

        # Calcula a proporção mantendo o aspect ratio
        frame_aspect_ratio = frame_width / frame_height
        label_aspect_ratio = label_width / label_height

        if label_aspect_ratio > frame_aspect_ratio:
            # Ajustar para caber na altura do QLabel
            new_height = label_height
            new_width = int(new_height * frame_aspect_ratio)
        else:
            # Ajustar para caber na largura do QLabel
            new_width = label_width
            new_height = int(new_width / frame_aspect_ratio)

        # Redimensiona o frame mantendo a proporção
        resized_frame = cv2.resize(self.parent.current_frame, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

        # Converte para RGB (OpenCV usa BGR por padrão)
        resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

        # Cria o QImage de forma robusta
        q_img = QImage(
            resized_frame.data,
            resized_frame.shape[1],
            resized_frame.shape[0],
            resized_frame.shape[1] * 3,  # Alinhamento correto para RGB
            QImage.Format_RGB888,
        )

        # Centraliza a imagem no QLabel
        pixmap = QPixmap.fromImage(q_img)
        self.video_label.setPixmap(pixmap)
        self.video_label.setAlignment(Qt.AlignCenter)


