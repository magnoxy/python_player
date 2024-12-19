import sys
import cv2
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QFileDialog, QHBoxLayout, QSlider, QMessageBox
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt, QRect, QThread, pyqtSignal

from ..filters.grayscale import converter_cinza, conversao_binaria
from ..filters.convolution import *
from ..frames.FilteredFrame import apply_filter_to_frame, normalizar_frame

class MainWindow(QWidget):
    def __init__(self):
        super().__init__() 

        print("Iniciando o sistema")
        # Configurações da janela
        self.setWindowTitle("Teti Player")
        self.setGeometry(100, 100, 1920, 1080)

        # Layout principal
        self.layout = QVBoxLayout()
        self.setMinimumSize(1280, 800)
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
        self.play_button = QPushButton("⏯️")
        controls_layout.addWidget(self.play_button)
        self.play_button.clicked.connect(self.toggle_play_pause)
        self.play_button.setEnabled(False)
        self.play_button.setToolTip('Reproduzir/Pausar o vídeo')

        # Botão Aumentar Zoom
        self.zoom_in_button = QPushButton("➕ 🔍")
        controls_layout.addWidget(self.zoom_in_button)
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_in_button.setToolTip('Aumentar o zoom')

        # Botão Diminuir Zoom
        self.zoom_out_button = QPushButton("➖ 🔍")
        controls_layout.addWidget(self.zoom_out_button)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.zoom_out_button.setToolTip('Dimiuir o zoom')
        
        # Botão para selecionar ROI
        self.roi_button = QPushButton("📏 ROI")
        controls_layout.addWidget(self.roi_button)
        self.roi_button.clicked.connect(self.select_roi)
        self.roi_button.setEnabled(False)
        self.roi_button.setToolTip('Clique aqui para selecionar uma opção de corte')

        # INÍCIO => BOTÕES DE VÍDEO
        # Botão de Diminuir a Velocidade de reprodução do vídeo.
        self.button_slowMode = QPushButton("➖ ⏬")
        controls_layout.addWidget(self.button_slowMode)
        self.button_slowMode.clicked.connect(self.slow_mode_video)
        self.button_slowMode.setEnabled(False)  # Desabilitado até que um vídeo seja selecionad
        self.button_slowMode.setToolTip('Diminuir a velocidade de reprodução do vídeo')

        # Botão de Aumentar a Velocidade de reprodução do vídeo.
        self.button_fastMode = QPushButton("➕ ⏩")
        controls_layout.addWidget(self.button_fastMode)
        self.button_fastMode.clicked.connect(self.fast_mode_video)
        self.button_fastMode.setEnabled(False)
        self.button_fastMode.setToolTip('Aumentar a velocidade de reprodução do vídeo')  

        #Botão de Reverso
        self.reverse_button = QPushButton("◀")
        controls_layout.addWidget(self.reverse_button)
        self.reverse_button.clicked.connect(self.toggle_reverse)
        self.reverse_button.setEnabled(False)
        #self.is_reversing = False
        self.reverse_button.setToolTip('Reproduzir o vídeo em reverso')

        self.button_cutMode = QPushButton("🎬📎 OFF")
        controls_layout.addWidget(self.button_cutMode)
        self.button_cutMode.clicked.connect(self.toggleCutButton)
        self.button_cutMode.setEnabled(False)
        self.button_cutMode.setToolTip('Ative para cortar o vídeo pressionando a tecla de espaço')  

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
        
        # Botão para recortar imagem
        self.cut_image = QPushButton("Recortar")
        controls_layout.addWidget(self.cut_image)
        self.cut_image.clicked.connect(self.clip_image)
        self.cut_image.setEnabled(False)

        self.save_imageOrVideo = QPushButton("💾")
        controls_layout.addWidget(self.save_imageOrVideo)
        self.save_imageOrVideo.clicked.connect(self.saveFile)
        self.save_imageOrVideo.setEnabled(False)
        self.save_imageOrVideo.setToolTip('Clique para salvar a imagem ou vídeo atual')  

        self.layout.addLayout(controls_layout)

        # Timer para atualização de frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Inicialização de variáveis
        self.isCascata = False
        self.is_playing = False
        self.cap = None
        self.video_path = None
        self.virtual_original_image = None
        self.original_image = None
        self.original_frame = None
        self.current_frame = None
        self.ref_frame = None
        self.zoom_factor = 1.0
        self.max_zoom = 2.0
        self.min_zoom = 1.0
        
        # Variáveis de controle de ROI
        self.is_selecting_roi = False
        self.roi_start = None
        self.roi_end = None
        self.roi_rect = None
        self.roi_frame = None

        # Suporte a drag and drop
        self.setAcceptDrops(True)
        self.playback_speed = 30    

        #variaveís para controle de dos cortes de vídeo
        self.frames_cut = []
        self.cutting_is_on = False
        self.output_folder = "./src/frames"


        #variaveis para criar uma lista de frames ao carregar um vídeo
        #tentativa de utilizar threads em python (...que medo)
        self.frames_list = []
        self.frames_list_reversed = []
        self.is_reversing = False
        self.reverse_counter = 0


        #variaveis para controle de Interpolation
        self.interpolation = cv2.INTER_LINEAR

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
                self.button_cutMode.setEnabled(False)
                self.save_imageOrVideo.setEnabled(True)
        elif mode == "Vídeo":
            file_path, _ = QFileDialog.getOpenFileName(self, "Selecione um Vídeo", "", "Vídeos (*.mp4 *.avi *.mkv *.mov)")
            if file_path:
                #limpa os frames do vídeo anterior
                self.frames_list.clear()

                self.video_path = file_path
                #habilita botões de vídeo
                self.play_button.setEnabled(True)
                self.button_fastMode.setEnabled(True)
                self.button_slowMode.setEnabled(True)
                self.button_cutMode.setEnabled(True)
                self.save_imageOrVideo.setEnabled(True)
                self.reverse_button.setEnabled(True)
                self.load_video()
                self.load_frames_list()
        elif mode == "Webcam":
            self.start_cam()

    def toggle_cascata(self):
        self.isCascata = not self.isCascata
        
        if self.isCascata:
            text = "Independente"
        else:
            self.original_frame = self.current_frame
            text = "Cascata"
            
        self.checkbox_is_cascata.setText(text)
        self.update_ref_frame()

    def update_ref_frame(self):
        if self.isCascata:
            self.ref_frame = self.current_frame  # No modo cascata, use current_frame
        else:
            self.ref_frame = self.original_frame

    def select_filter(self):
        if self.ref_frame is None:
            return

        filter_name = self.filter_selector.currentText()
        
        if filter_name == "Sem Filtro":
            self.current_frame = self.original_image
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
        self.original_image = self.original_frame
        self.current_frame = self.original_frame
        self.ref_frame = self.original_frame
        
        self.filter_selector.setCurrentText("Sem Filtro")
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
            self.original_image = self.original_frame
            self.ref_frame = self.original_frame
            self.current_frame = self.original_frame
            self.timer.start(30)  # Aproximadamente 30 FPS
            self.play_button.setText("⏯️")
            self.update_display()
            
        self.filter_selector.setCurrentText("Sem Filtro")

    def toggle_play_pause(self):
        if not self.cap or not self.cap.isOpened():
            return

        self.is_playing = not self.is_playing
        if self.is_playing:
            self.timer.start(30)  # Aproximadamente 30 FPS
            self.play_button.setText("⏯️")
        else:
            self.timer.stop()
            self.play_button.setText("⏯️")

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

    def toggleCutButton(self):
        if(self.cutting_is_on):
            self.button_cutMode.setText("🔪 OFF")
            self.cutting_is_on = False
        else:
            self.cutting_is_on = True
            self.button_cutMode.setText("🔪 ON")

    def cutVideoByPressingSpaceBar(self, event):
        if(event.key() == Qt.Key_Space and self.cutting_is_on):
            self.frames_cut.append(self.current_frame)
            print("Frame cortado")
            print(len(self.frames_cut))

    def update_display(self):
        if self.current_frame is None:
            self.roi_button.setEnabled(False)
            return

        self.roi_button.setEnabled(True)
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

        self.update_ref_frame()
        # Centraliza a imagem no QLabel
        pixmap = QPixmap.fromImage(q_img)
        self.video_label.setPixmap(pixmap)
        self.video_label.setAlignment(Qt.AlignCenter)

    def update_frame(self):
        if self.cap is None or not self.cap.isOpened():
            return

        if self.is_reversing:
            if(self.reverse_counter == 0):
                self.timer.stop()
                self.reverse_counter = len(self.frames_list_reversed) - 1
                self.timer.start(30)
            self.original_frame = self.frames_list_reversed[self.reverse_counter]
            print(f"Reverse Counter: {self.reverse_counter}, Total Frames: {len(self.frames_list_reversed)}")
            self.reverse_counter -= 1
            self.current_frame = self.frames_list_reversed[self.reverse_counter]
            #self.update_ref_frame()
            #self.select_filter()
            self.update_display()
            return
         
        ret, frame = self.cap.read()
        if ret:
            self.original_frame = frame
            self.original_image = frame
            self.update_ref_frame()
            self.select_filter()
            if(self.roi_start or self.roi_end):
                self.crop_roi()

            # self.update_display()
        else:
            self.timer.stop()
            self.is_playing = False
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.reverse_counter = 0
            self.play_button.setText("▶️")
            
    def map_to_image_coordinates(self, pos):
        if self.current_frame is None:
            return None

        # Posição absoluta do QLabel
        label_global_pos = self.video_label.mapToGlobal(self.video_label.pos())
        window_global_pos = self.mapToGlobal(self.pos())
        # x_offset_label = label_global_pos.x() - window_global_pos.x()
        y_offset_label = label_global_pos.y() - window_global_pos.y()

        # Corrige as coordenadas do evento de mouse para serem relativas ao QLabel
        x_relative = pos.x() - 10
        y_relative = pos.y() - y_offset_label

        # Dimensões do QLabel
        label_width = self.video_label.width()
        label_height = self.video_label.height()

        # Dimensões da imagem atual
        frame_height, frame_width = self.current_frame.shape[:2]

        # Calcula o aspecto da imagem e do QLabel
        frame_aspect_ratio = frame_width / frame_height
        label_aspect_ratio = label_width / label_height

        # Calcula as margens para centralizar a imagem no QLabel
        if label_aspect_ratio > frame_aspect_ratio:
            # Ajuste pela altura do QLabel
            new_height = label_height
            new_width = int(new_height * frame_aspect_ratio)
            x_offset = (label_width - new_width) // 2
            y_offset = 0
        else:
            # Ajuste pela largura do QLabel
            new_width = label_width
            new_height = int(new_width / frame_aspect_ratio)
            x_offset = 0
            y_offset = (label_height - new_height) // 2

        # Normaliza as coordenadas do QLabel para a imagem
        x = (x_relative - x_offset) * frame_width / new_width
        y = (y_relative - y_offset) * frame_height / new_height

        # Retorna apenas se as coordenadas estiverem dentro dos limites da imagem
        if 0 <= x < frame_width and 0 <= y < frame_height:
            return int(x), int(y)
        return None
            
    def select_roi(self):
        if self.current_frame is not None:
            self.is_selecting_roi = True
            self.roi_start = None
            self.roi_end = None
            self.video_label.setCursor(Qt.CrossCursor)  # Altere o cursor para indicar a seleção
            
    def update_display_with_frame(self, frame): 
        if frame is None:
            return

        # Dimensões do QLabel
        label_width = self.video_label.width()
        label_height = self.video_label.height()

        # Dimensões do frame original
        frame_height, frame_width = frame.shape[:2]

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
        resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

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

    def update_roi_overlay(self):
        if self.roi_start and self.roi_end and self.ref_frame is not None:
            # Copia o frame atual para sobreposição
            frame_copy = self.ref_frame.copy()

            # Extrai coordenadas
            x1, y1 = self.roi_start
            x2, y2 = self.roi_end

            # Desenha o retângulo de seleção
            cv2.rectangle(
                frame_copy,
                (min(x1, x2), min(y1, y2)),
                (max(x1, x2), max(y1, y2)),
                (0, 255, 0),
                2
            )

            # Atualiza a exibição com o frame
            self.update_display_with_frame(frame_copy)

    def crop_roi(self):
        if self.roi_rect and self.current_frame is not None:
            # Coordenadas na escala do frame
            x, y, w, h = (
                self.roi_rect.left(),
                self.roi_rect.top(),
                self.roi_rect.width(),
                self.roi_rect.height(),
            )
            x1, y1 = int(x), int(y)
            x2, y2 = x1 + int(w), y1 + int(h)

            self.roi_frame = self.current_frame[y1:y2, x1:x2]
            self.virtual_original_image = self.original_image[y1:y2, x1:x2]
            self.current_frame = self.roi_frame

            # Atualiza o frame exibido
            self.cut_image.setEnabled(True)
            self.update_display()
            
    def clip_image(self):
        if self.roi_frame is None:
            print("nenhum frame selecionado")
            return
        
        self.current_frame = self.roi_frame
        self.original_frame = self.current_frame
        self.original_image = self.virtual_original_image
        self.update_ref_frame()
        self.roi_frame = None;
        self.cut_image.setEnabled(False)
        self.update_display()

    def cut_frame_with_roi(self, frame):
        x, y, w, h = (
                self.roi_rect.left(),
                self.roi_rect.top(),
                self.roi_rect.width(),
                self.roi_rect.height(),
            )
        x1, y1 = int(x), int(y)
        x2, y2 = x1 + int(w), y1 + int(h)
        return frame[y1:y2, x1:x2]
    
    # def retorna_altura_largura_do_corte(self, largura, altura):
    
        
            
    def mousePressEvent(self, event):
        if self.is_selecting_roi and event.button() == Qt.LeftButton:
            mapped_coords = self.map_to_image_coordinates(event.pos())
            if mapped_coords:
                self.roi_start = mapped_coords

    def mouseMoveEvent(self, event):
        if self.is_selecting_roi and self.roi_start:
            # Atualiza o ponto final e desenha o retângulo de ROI
            mapped_coords = self.map_to_image_coordinates(event.pos())
            if mapped_coords:
                self.roi_end = mapped_coords
                self.update_roi_overlay()

    def mouseReleaseEvent(self, event):
        if self.is_selecting_roi and event.button() == Qt.LeftButton:
            mapped_coords = self.map_to_image_coordinates(event.pos())
            if mapped_coords:
                self.roi_end = mapped_coords
                self.is_selecting_roi = False

                # Define o retângulo de ROI
                x1, y1 = self.roi_start
                x2, y2 = self.roi_end
                self.roi_rect = QRect(
                    min(x1, x2),
                    min(y1, y2),
                    abs(x2 - x1),
                    abs(y2 - y1),
                )
                self.video_label.setCursor(Qt.ArrowCursor)  # Restaura o cursor padrão
                self.crop_roi()

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
            self.load_frames_list()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_display()


    def saveFile (self, event):   
      mode = self.mode_selector.currentText()
      if self.current_frame is not None:
        if(mode == "Imagem"):
          file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo", "", "Imagens (*.png *.jpg *.jpeg *.bmp)")
          self.processSaveImage(file_path, self.current_frame)
        if(mode == "Vídeo"):
          file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo", "", "Vídeos (*.mp4 *.avi *.mkv *.mov)")
          print("file_path: ", file_path)
          if file_path:
              print("chamou a func process video")
              self.processSaveVideo(file_path)
          else:
             QMessageBox().warning(self, "Erro", "Nenhum caminhjo selecionado para exportar!")
      else:
          QMessageBox().warning(self, "Erro", "Nenhum frame selecionado para exportar!")

    def processSaveImage(self, file_path, frame):
        if file_path:
            if(file_path.endswith(('.png', '.jpg', '.jpeg', '.bmp'))):
                cv2.imwrite(file_path, self.current_frame)
            else: 
                file_path += ".png"
                cv2.imwrite(file_path, self.current_frame)
            QMessageBox().information(self, "Sucesso", "Arquivo salvo com sucesso!")
    
    def processSaveVideo(self, file_path):
        if not file_path.endswith(('.mp4', '.avi', '.mkv', '.mov')):
            file_path += ".avi"
        
        codec = cv2.VideoWriter_fourcc(*'MJPG')
        #codec = cv2.VideoWriter_fourcc(*'XVID') 
        #codec = cv2.VideoWriter_fourcc(*'mp4v')
        cap = self.cap
        largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        #se tem corte no vídeo, ajuste de largura e altura
        if(self.roi_rect and self.roi_start):
            x, y, w, h = (
                self.roi_rect.left(),
                self.roi_rect.top(),
                self.roi_rect.width(),
                self.roi_rect.height(),
            )
            largura = w
            altura = h
        out = cv2.VideoWriter(file_path, codec, self.playback_speed, (largura, altura))
        for frame in self.frames_list:
            frame_filtered = apply_filter_to_frame(frame, self.filter_selector.currentText())
            frame_filtered = normalizar_frame(frame_filtered)
            if(self.roi_start or self.roi_end):
                frame_filtered = self.cut_frame_with_roi(frame_filtered)
            out.write(frame_filtered)
        out.release()
        QMessageBox().information(self, "Sucesso", "Arquivo salvo com sucesso!")

    def processSaveWebcam(self, file_path):
        return 0

    def load_frames_list(self):
        cap = self.cap
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            self.frames_list.append(frame)
        self.frames_list_reversed = self.frames_list[::-1]
        self.reverse_counter = len(self.frames_list_reversed) - 1
        print("Frames carregados com sucesso")
        print("Lista de Frames: ", self.frames_list)
    
    def toggle_reverse(self):
        if(self.is_reversing):
            self.reverse_button.setText("◀ OFF")
            self.is_reversing = False
        else:
            self.is_reversing = True
            self.reverse_button.setText("◀ ON")
