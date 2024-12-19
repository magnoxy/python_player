from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

from src.modifications_history.modifications_history import ModificationHistory
from .mode_selector import ModeSelector
from .cascade_checkbox import CascadeCheckbox
from .display import VideoDisplay

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
        
        # Display
        display = VideoDisplay(self)
        # Adiciona componentes ao layout principal
        layout.addLayout(header_layout)
        layout.addWidget(display)
        
        # Caminho do Arquivo
        self.file_path = None;
        
        # Frames
        self.frames_list = []
        self.original_frame = None;
        self.current_frame = None;
        
        # Histórico de Modificações
        self.history = ModificationHistory(self)
        self.modification = None
        
        # Alterações em Cascata
        self.cascade = False
        
    