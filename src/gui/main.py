from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

from src.modificationsHistory.modificationsHistory import ModificationHistory
from .mode_selector import ModeSelector
from .cascade_checkbox import CascadeCheckbox

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
        
        # Adiciona o cabeçalho ao layout principal
        layout.addLayout(header_layout)
        
        # Outras inicializações
        self.history = ModificationHistory()
        self.modification = None
        self.cascade = False
