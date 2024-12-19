from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from src.modifications_history.modifications_history import ModificationHistory
from .mode_selector import ModeSelector
from .cascade_checkbox import CascadeCheckbox
from .display import VideoDisplay

import cv2
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1280, 720)
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Python Player")
        
        # Cria o widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Cabeçalho
        header_layout = QHBoxLayout()
        
        modeSelectorLayout = ModeSelector(self)
        cascadeCheckBox = CascadeCheckbox(self)
        
        header_layout.setAlignment(Qt.AlignTop)
        header_layout.setContentsMargins(5, 5, 5, 5)
        header_layout.addWidget(modeSelectorLayout)
        header_layout.addStretch()  # Adiciona espaço expansível
        header_layout.addWidget(cascadeCheckBox)
        
        # Caminho do Arquivo
        self.file_path = None
        
        # Frames
        self.frames_list = []
        self.original_frame = None
        self.current_frame = None
        
        # Histórico de Modificações
        self.history = ModificationHistory(self)
        self.modification = None
        
        # Alterações em Cascata ?
        self.cascade = False
        
        # Tempos
        self.timer = QTimer()
        self.timers_list = []
        
        # Display
        self.display = VideoDisplay(self)
        # Adiciona componentes ao layout principal
        layout.addLayout(header_layout)
        layout.addWidget(self.display)
        
        # Conectar o arquivo_path ao método de atualização de exibição
        self.timer.timeout.connect(self.update_display)
    
    def update_display(self):
        if self.file_path:
            
            # Se for um vídeo
            if self.file_path.lower().endswith(('.mp4', '.avi', '.mov')):
                cap = cv2.VideoCapture(self.file_path)
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.frames_list.append(frame_rgb)
                cap.release()
            else:
                # Se for uma imagem
                frame_rgb = cv2.imread(self.file_path)
                # frame_rgb = cv2.cvtColor(frame_rgb, cv2.COLOR_BGR2RGB)
                self.frames_list.append(frame_rgb)
            
            self.display.update_display()

    def reset_frames(self):
        self.current_frame = None
        self.frames_list = []