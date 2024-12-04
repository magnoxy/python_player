#bibliotecas
import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget
)
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QImage

class ROISelector(QMainWindow):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
        self.original_frame = frame.copy()
        self.setWindowTitle("Seleção de ROI")
        self.setGeometry(100, 100, frame.shape[1], frame.shape[0])

        self.roi_start = None
        self.roi_end = None
        self.roi_rect = None
        self.is_selecting = False

        self.image_label = QLabel(self)
        self.image_label.setPixmap(self.convert_cv_to_pixmap(self.frame))
        self.image_label.setGeometry(0, 0, frame.shape[1], frame.shape[0])
        self.image_label.setScaledContents(True)
        self.image_label.setMouseTracking(True)

        self.save_button = QPushButton("Salvar ROI", self)
        self.save_button.setGeometry(10, self.frame.shape[0] - 50, 100, 30)
        self.save_button.clicked.connect(self.save_roi)
        self.save_button.setEnabled(False)

        self.cancel_button = QPushButton("Cancelar", self)
        self.cancel_button.setGeometry(120, self.frame.shape[0] - 50, 100, 30)
        self.cancel_button.clicked.connect(self.cancel_selection)

        self.roi_cropped = None

    def convert_cv_to_pixmap(self, cv_image):

        height, width, channel = cv_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        return QPixmap.fromImage(q_image)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.roi_start = event.pos()
            self.is_selecting = True

    def mouseMoveEvent(self, event):

        if self.is_selecting:
            self.roi_end = event.pos()
            self.update_roi()

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton and self.is_selecting:
            self.roi_end = event.pos()
            self.is_selecting = False
            self.update_roi()
            self.save_button.setEnabled(True)

    def update_roi(self):

        if self.roi_start and self.roi_end:
            self.frame = self.original_frame.copy()
            x1, y1 = self.roi_start.x(), self.roi_start.y()
            x2, y2 = self.roi_end.x(), self.roi_end.y()
            self.roi_rect = QRect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
            cv2.rectangle(self.frame, (self.roi_rect.left(), self.roi_rect.top()),
                          (self.roi_rect.right(), self.roi_rect.bottom()), (0, 255, 0), 2)
            self.image_label.setPixmap(self.convert_cv_to_pixmap(self.frame))

    def save_roi(self):

        if self.roi_rect:
            x, y, w, h = self.roi_rect.left(), self.roi_rect.top(), self.roi_rect.width(), self.roi_rect.height()
            self.roi_cropped = self.original_frame[y:y+h, x:x+w]
            file_path, _ = QFileDialog.getSaveFileName(self, "Salvar ROI", "", "Images (*.png *.jpg *.bmp)")
            if file_path:
                cv2.imwrite(file_path, self.roi_cropped)
                print(f"ROI salva em: {file_path}")
        self.close()

    def cancel_selection(self):

        self.roi_cropped = None
        self.close()

    def get_result(self):

        return self.roi_cropped if self.roi_cropped is not None else self.original_frame

def selecionar_roi_imagem(frame):
    app = QApplication(sys.argv)
    selector = ROISelector(frame)
    selector.show()
    app.exec_()
    imagem = selector.get_result()
    imagem_convertida = cv2.cvtColor(imagem,cv2.COLOR_BGR2RGB)
    return imagem_convertida