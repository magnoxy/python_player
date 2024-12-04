import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.setWindowTitle("Câmera com PyQt")
        self.setGeometry(100, 100, 800, 600)

        # Layout e QLabel para exibir os frames
        self.layout = QVBoxLayout()
        self.video_label = QLabel("Iniciando...")
        self.video_label.setStyleSheet("border: 1px solid black;")
        self.layout.addWidget(self.video_label)
        self.setLayout(self.layout)

        # Inicializa a captura da câmera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.video_label.setText("Erro ao acessar a câmera")
            return

        # Configura o timer para capturar frames periodicamente
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Aproximadamente 30 FPS

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Converte o frame para RGB e exibe no QLabel
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(q_img))
        else:
            self.video_label.setText("Erro ao capturar frame")

    def closeEvent(self, event):
        # Libera a câmera ao fechar
        if self.cap.isOpened():
            self.cap.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())
