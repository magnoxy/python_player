import sys
import cv2
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QFileDialog, QHBoxLayout
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt

from ..filters.grayscale import converter_cinza, conversao_binaria
from ..filters.convolution import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.setWindowTitle("Teti Player")
        self.setGeometry(100, 100, 1280, 800)

        # Layout principal
        self.layout = QVBoxLayout()
        self.setFixedSize(1280, 800)
        self.setLayout(self.layout)

        # Dropdown para selecionar Imagem ou Vídeo
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Imagem", "Vídeo", "Webcam"])
        self.layout.addWidget(self.mode_selector)

        # Botão para abrir arquivo
        self.open_button = QPushButton("Abrir Arquivo")
        self.layout.addWidget(self.open_button)
        self.open_button.clicked.connect(self.open_file_dialog)

        # Label para exibir frames de vídeo ou imagem
        self.video_label = QLabel("Exibição")
        self.video_label.setStyleSheet("border: 1px solid black;")
        self.layout.addWidget(self.video_label)

        # Botões de controle
        controls_layout = QHBoxLayout()

        # Botão Play/Pause
        self.play_button = QPushButton("Play")
        controls_layout.addWidget(self.play_button)
        self.play_button.clicked.connect(self.toggle_play_pause)
        self.play_button.setEnabled(False)

        # Botão Aumentar Zoom
        self.zoom_in_button = QPushButton("Aumentar Zoom")
        controls_layout.addWidget(self.zoom_in_button)
        self.zoom_in_button.clicked.connect(self.zoom_in)

        # Botão Diminuir Zoom
        self.zoom_out_button = QPushButton("Diminuir Zoom")
        controls_layout.addWidget(self.zoom_out_button)
        self.zoom_out_button.clicked.connect(self.zoom_out)

        # INÍCIO => BOTÕES DE VÍDEO
        # Botão de Diminuir a Velocidade de reprodução do vídeo.
        self.button_slowMode = QPushButton("- Velocidade")
        controls_layout.addWidget(self.button_slowMode)
        self.button_slowMode.clicked.connect(self.slow_mode_video)
        self.button_slowMode.setEnabled(False)  # Desabilitado até que um vídeo seja selecionado

        # Botão de Aumentar a Velocidade de reprodução do vídeo.
        self.button_fastMode = QPushButton("+ Velocidade")
        controls_layout.addWidget(self.button_fastMode)
        self.button_fastMode.clicked.connect(self.fast_mode_video)
        self.button_fastMode.setEnabled(False)

        # Botão de Reverso
        #self.reverse_button = QPushButton("Reverso")
        #controls_layout.addWidget(self.reverse_button)
        #self.reverse_button.clicked.connect(self.toggle_reverse)
        #self.reverse_button.setEnabled(False)
        #self.is_reversing = False

        # FIM => BOTÕES DE VÍDEO

        # Botão para alternar modo cascata
        self.checkbox_is_cascata = QPushButton("Independente")
        controls_layout.addWidget(self.checkbox_is_cascata)
        self.checkbox_is_cascata.clicked.connect(self.toggle_cascata)

        # Dropdown Filtros
        self.filter_selector = QComboBox()
        self.filter_selector.addItems(["Sem Filtro", "Grayscale", "Binário", "Blur", "Sharpen", "Sobel", "Laplacian", "Canny", "Emboss"])
        controls_layout.addWidget(self.filter_selector)
        self.filter_selector.currentTextChanged.connect(self.select_filter)

        self.layout.addLayout(controls_layout)

        # Timer para atualização de frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Inicialização de variáveis
        self.isCascata = False
        self.is_playing = False
        self.cap = None
        self.video_path = None
        self.original_frame = None
        self.current_frame = None
        self.ref_frame = None
        self.zoom_factor = 1.0
        self.max_zoom = 2.0
        self.min_zoom = 1.0

        # Suporte a drag and drop
        self.setAcceptDrops(True)
        self.playback_speed = 30    

    def open_file_dialog(self):
        mode = self.mode_selector.currentText()
        if mode == "Imagem":
            file_path, _ = QFileDialog.getOpenFileName(self, "Selecione uma Imagem", "", "Imagens (*.png *.jpg *.jpeg *.bmp)")
            if file_path:
                self.display_image(file_path)
                #desabilita botões de vídeo
                self.play_button.setEnabled(False)  
                self.button_fastMode.setEnabled(False)
                self.button_slowMode.setEnabled(False)
        elif mode == "Vídeo":
            file_path, _ = QFileDialog.getOpenFileName(self, "Selecione um Vídeo", "", "Vídeos (*.mp4 *.avi *.mkv *.mov)")
            if file_path:
                self.video_path = file_path
                #habilita botões de vídeo
                self.play_button.setEnabled(True)
                self.button_fastMode.setEnabled(True)
                self.button_slowMode.setEnabled(True)
                self.load_video()
        elif mode == "Webcam":
            self.start_cam()

    def toggle_cascata(self):
        self.isCascata = not self.isCascata
        self.checkbox_is_cascata.setText("Cascata" if self.isCascata else "Independente")
        self.update_ref_frame()

    def update_ref_frame(self):
        self.ref_frame = self.current_frame if self.isCascata else self.original_frame

    def select_filter(self):
        filter_name = self.filter_selector.currentText()
        if self.ref_frame is None:
            return

        if filter_name == "Sem Filtro":
            self.current_frame = self.original_frame
        elif filter_name == "Grayscale":
            self.current_frame = converter_cinza(self.ref_frame)
        elif filter_name == "Binário":
            self.current_frame = conversao_binaria(self.ref_frame)
        elif filter_name == "Blur":
            self.current_frame = converter_blur(self.ref_frame, 20, 20)
        elif filter_name == "Sharpen":
            self.current_frame = converter_sharpen(self.ref_frame)
        elif filter_name == "Sobel":
            self.current_frame = transformar_sobel_positvo(converter_sobel(self.ref_frame))
        elif filter_name == "Laplacian":
            self.current_frame = converter_laplacian(self.ref_frame)
        elif filter_name == "Canny":
            self.current_frame = converter_Canny(self.ref_frame, 50, 50)
        elif filter_name == "Emboss":
            self.current_frame = converter_emboss(self.ref_frame)

        self.update_display()

    def start_cam(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Erro: Não foi possível abrir a webcam.")
            return

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Largura (exemplo: 640 pixels)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        self.play_button.setEnabled(True)
        self.toggle_play_pause()

    def display_image(self, image_path):
        self.cap = None
        self.original_frame = cv2.imread(image_path)
        self.current_frame = self.original_frame
        self.ref_frame = self.original_frame
        self.update_display()

    def load_video(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()

        self.cap = cv2.VideoCapture(self.video_path)
        
        if not self.cap.isOpened():
            print("Erro: Não foi possível abrir o vídeo.")
        
        ret, frame = self.cap.read()
        if ret:
            self.original_frame = frame
            self.ref_frame = self.original_frame
            self.current_frame = self.original_frame

    def toggle_play_pause(self):
        if not self.cap or not self.cap.isOpened():
            return

        self.is_playing = not self.is_playing
        if self.is_playing:
            self.timer.start(30)  # Aproximadamente 30 FPS
            self.play_button.setText("Pause")
        else:
            self.timer.stop()
            self.play_button.setText("Play")

    def zoom_in(self):
        if self.zoom_factor < self.max_zoom:
            self.zoom_factor += 0.1
            self.update_display()

    def zoom_out(self):
        if self.zoom_factor > self.min_zoom:
            self.zoom_factor -= 0.1
            self.update_display()

    def slow_mode_video(self):
        self.playback_speed += 10  # Aumenta o intervalo em 10ms
        self.timer.setInterval(self.playback_speed)
        print(f"Velocidade reduzida: {self.playback_speed}ms por frame.")
    
    def fast_mode_video(self):
        if(self.playback_speed > 10):
            self.playback_speed -= 10
            self.timer.setInterval(self.playback_speed)
            print(f"Velocidade aumentada: {self.playback_speed}ms por frame.")
        else:
            print("Velocidade máxima atingida.")
    


    def update_display(self):
        if self.current_frame is None:
            return

        # Dimensões do QLabel
        label_width = self.video_label.width()
        label_height = self.video_label.height()

        # Dimensões do frame original
        frame_height, frame_width = self.current_frame.shape[:2]

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
        resized_frame = cv2.resize(self.current_frame, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

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

    def update_frame(self):
        if self.cap is None or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if ret:
            self.original_frame = frame
            self.ref_frame = self.current_frame if self.isCascata else self.original_frame
            self.select_filter()
            # self.update_display()
        else:
            self.timer.stop()
            self.is_playing = False
            self.play_button.setText("Play")

    def closeEvent(self, event):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        event.accept()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        file_url = event.mimeData().urls()[0].toLocalFile()
        if file_url.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            self.display_image(file_url)
        elif file_url.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
            self.video_path = file_url
            self.play_button.setEnabled(True)
            self.load_video()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_display()