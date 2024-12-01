import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.setWindowTitle("Teti Player")
        self.setGeometry(100, 100, 200, 300)

        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Exibição do vídeo
        self.video_label = QLabel("Video Frame")
        self.layout.addWidget(self.video_label)

        # Botão Play
        self.play_button = QPushButton("Play")
        self.layout.addWidget(self.play_button)

        # Conectar botão Play ao método de reprodução
        self.play_button.clicked.connect(self.play_video)

        # Timer para atualizar frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Carregar vídeo (use seu caminho de vídeo aqui)
        self.video_path = "C:/Users/edson.neto/Documents/Projetos/Teti_Player/src/assets/video.mp4"  # Substitua pelo caminho correto
        self.cap = cv2.VideoCapture(self.video_path)

    def play_video(self):
      if self.cap.isOpened():
          print("Vídeo carregado com sucesso.")
          self.timer.start(30)  # Aproximadamente 30 FPS
      else:
          print("Erro: Não foi possível abrir o vídeo.")


    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Converte o frame para formato RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            step = channel * width
            q_img = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(q_img))
        else:
            self.timer.stop()  # Para o timer se não houver mais frames

    def closeEvent(self, event):
        # Libera o vídeo ao fechar a janela
        if self.cap.isOpened():
            self.cap.release()
        event.accept()
