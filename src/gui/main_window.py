import sys
import cv2
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QFileDialog, QHBoxLayout
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt

from ..filters.grayscale import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.setWindowTitle("Teti Player")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        self.layout = QVBoxLayout()
        self.setFixedSize(800, 600)
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
        self.play_button.setEnabled(False)  # Desabilitado até que um vídeo seja selecionado

        # Botão Aumentar Zoom
        self.zoom_in_button = QPushButton("Aumentar Zoom")
        controls_layout.addWidget(self.zoom_in_button)
        self.zoom_in_button.clicked.connect(self.zoom_in)

        # Botão Diminuir Zoom
        self.zoom_out_button = QPushButton("Diminuir Zoom")
        controls_layout.addWidget(self.zoom_out_button)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        
        self.checkbox_is_cascata = QPushButton("Cascata")
        controls_layout.addWidget(self.checkbox_is_cascata)
        self.checkbox_is_cascata.clicked.connect(self.toggle_cascata)
        
        # Dropdown Filtros
        self.filter_selector = QComboBox()
        self.filter_selector.addItems(["Sem Filtro","Grayscale", "Binário", "Sepia", "Blur", "aaa"])
        controls_layout.addWidget(self.filter_selector)

        self.layout.addLayout(controls_layout)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        
        self.isCascata = False

        self.is_playing = False
        self.cap = None
        self.video_path = None
        self.original_frame = None
        self.current_frame = None
        self.ref_frame = self.original_frame
        self.zoom_factor = 1.0
        self.max_zoom = 2.0
        self.min_zoom = 1.0

        self.setAcceptDrops(True)
        
        

    def open_file_dialog(self):
        mode = self.mode_selector.currentText()

        if mode == "Imagem":
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Selecione uma Imagem", "", "Imagens (*.png *.jpg *.jpeg *.bmp)"
            )
            if file_path:
                self.display_image(file_path)
        elif mode == "Vídeo":
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Selecione um Vídeo", "", "Vídeos (*.mp4 *.avi *.mkv *.mov)"
            )
            if file_path:
                self.video_path = file_path
                self.play_button.setEnabled(True)  # Habilita o botão Play
                self.load_video()
        elif mode == "Webcam":
            self.start_cam()
            
    def update_ref_frame(self):
        if(self.isCascata == True):
            self.ref_frame = self.current_frame
        else:
            self.ref_frame = self.original_frame
            
            
    def toggle_cascata(self):
        if self.isCascata == False:
            self.isCascata = True
            self.checkbox_is_cascata.setText("Cascata")
        elif self.isCascata == True:
            self.isCascata = False
            self.checkbox_is_cascata.setText("Independente")
            
        self.update_ref_frame()
        
    def select_filter(self):
        filter = self.filter_selector.currentText()
        
        if filter == "Sem Filtro":
            self.current_frame = self.original_frame
            self.update_display()
        elif filter == "Grayscale":
            grayscale_frame = converter_cinza(self.ref_frame)
            self.current_frame = grayscale_frame
            self.update_display()
        elif filter == "Binário":
            binary_frame = conversao_binaria(self.ref_frame)
            self.current_frame = binary_frame
            self.update_display()
        
        
            
    
    def apply_grayscale_filter(self):
        if self.current_frame is None:
            return
        self.original_image = self.current_frame
        
        frame_in_grayscale = converter_cinza(self.current_frame)
        
        self.current_frame = frame_in_grayscale
        self.update_display()
                
    def start_cam(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            
        self.cap = cv2.VideoCapture(0)
            
        if not self.cap.isOpened():
            print("Erro: Não foi possível abrir o vídeo.")
            return
        
        self.play_button.setEnabled(True)  # Habilita o botão Play
        self.toggle_play_pause()

    def display_image(self, image_path):
        self.cap = None
        self.current_frame = cv2.imread(image_path)
        self.original_frame = self.current_frame
        self.update_display()

    def load_video(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()  # Libera o vídeo anterior, se houver
        
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            print("Erro: Não foi possível abrir o vídeo.")

    def toggle_play_pause(self):
        if not self.cap or not self.cap.isOpened():
            return

        if self.is_playing:
            self.is_playing = False
            self.timer.stop()
            self.play_button.setText("Play")
            print("Vídeo pausado.")
        else:
            self.is_playing = True
            self.timer.start(30)  # Aproximadamente 30 FPS
            self.play_button.setText("Pause")
            print("Reproduzindo vídeo.")

    def zoom_in(self):
        if self.zoom_factor < self.max_zoom:
            self.zoom_factor += 0.1
            self.update_display()

    def zoom_out(self):
        if self.zoom_factor > self.min_zoom:
            self.zoom_factor -= 0.1
            self.update_display()

    def update_display(self):
        if self.current_frame is None:
            return

        # Dimensões originais do frame
        height, width = self.current_frame.shape[:2]

        # Calcula as novas dimensões com base no fator de zoom
        new_width = int(width * self.zoom_factor)
        new_height = int(height * self.zoom_factor)

        # Verifica se as dimensões calculadas são válidas
        if new_width <= 0 or new_height <= 0:
            print("Dimensão inválida durante o redimensionamento!")
            return

        # Redimensionar o frame com base no zoom
        resized_frame = cv2.resize(self.current_frame, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

        # Converter o frame para RGB e exibir
        resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        q_img = QImage(resized_frame.data, resized_frame.shape[1], resized_frame.shape[0], QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(q_img))

    def update_frame(self):
        if self.cap is None or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame
            self.update_display()
        else:
            self.timer.stop()  # Para o timer se o vídeo terminar
            self.is_playing = False
            self.play_button.setText("Play")
            print("Fim do vídeo.")

    def closeEvent(self, event):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        event.accept()

    # Métodos para drag and drop
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
