from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QWidget, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

class Controls(QHBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
         # Botão Play/Pause
        self.play_button = QPushButton("▶️")
        self.addWidget(self.play_button)
        self.play_button.clicked.connect(self.parent.toggle_play_pause)
        self.play_button.setEnabled(False)

        # Botão Aumentar Zoom
        self.zoom_in_button = QPushButton("+ 🔍")
        self.addWidget(self.zoom_in_button)
        self.zoom_in_button.clicked.connect(self.parent.zoom_in)

        # Botão Diminuir Zoom
        self.zoom_out_button = QPushButton("- 🔍")
        self.addWidget(self.zoom_out_button)
        self.zoom_out_button.clicked.connect(self.parent.zoom_out)
        
        # Botão para selecionar ROI
        self.roi_button = QPushButton("Selecionar ROI")
        self.addWidget(self.roi_button)
        self.roi_button.clicked.connect(self.parent.select_roi)
        self.roi_button.setEnabled(False)

        # INÍCIO => BOTÕES DE VÍDEO
        # Botão de Diminuir a Velocidade de reprodução do vídeo.
        self.button_slowMode = QPushButton("- ⏬")
        self.addWidget(self.button_slowMode)
        self.button_slowMode.clicked.connect(self.parent.slow_mode_video)
        self.button_slowMode.setEnabled(False)  # Desabilitado até que um vídeo seja selecionado

        # Botão de Aumentar a Velocidade de reprodução do vídeo.
        self.button_fastMode = QPushButton("+ ⏩")
        self.addWidget(self.button_fastMode)
        self.button_fastMode.clicked.connect(self.parent.fast_mode_video)
        self.button_fastMode.setEnabled(False)

        # Botão de Reverso
        #self.reverse_button = QPushButton("Reverso")
        #controls_layout.addWidget(self.reverse_button)
        #self.reverse_button.clicked.connect(self.toggle_reverse)
        #self.reverse_button.setEnabled(False)
        #self.is_reversing = False

        self.button_cutMode = QPushButton("🔪 OFF")
        self.addWidget(self.button_cutMode)
        self.button_cutMode.clicked.connect(self.parent.toggleCutButton)
        self.button_cutMode.setEnabled(False)
        
                # Botão para alternar modo cascata
        self.checkbox_is_cascata = QPushButton("Independente")
        self.addWidget(self.checkbox_is_cascata)
        self.checkbox_is_cascata.clicked.connect(self.parent.toggle_cascata)

        # Dropdown Filtros
        self.filter_selector = QComboBox()
        self.filter_selector.addItems(["Sem Filtro", "Grayscale", "Binário", "Blur", "Sharpen", "Sobel", "Laplacian", "Canny", "Emboss"])
        self.addWidget(self.filter_selector)
        self.filter_selector.currentTextChanged.connect(self.parent.select_filter)
        
        # Botão para recortar imagem
        self.cut_image = QPushButton("Recortar")
        self.addWidget(self.cut_image)
        self.cut_image.clicked.connect(self.parent.clip_image)
        self.cut_image.setEnabled(False)

        self.save_imageOrVideo = QPushButton("Save")
        self.addWidget(self.save_imageOrVideo)
        self.save_imageOrVideo.clicked.connect(self.parent.saveFile)