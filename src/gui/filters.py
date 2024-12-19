from PyQt5.QtWidgets import QListWidget

from ..filters.convolution import *
from ..filters.grayscale import *

filters_list = [
                "Sem Filtro", 
                "Grayscale", 
                "Binário", 
                "Blur", 
                "Sharpen", 
                "Sobel", 
                "Laplacian", 
                "Canny", 
                "Emboss"
                ]

    
class FiltersList(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.addItems(filters_list)
        
        self.setMaximumWidth(150)
        
        self.currentItemChanged.connect(self.select_filter)
        
    def select_filter(self, i):
        if i.text() is None:
            return

        filter_name = i.text()
        
        if filter_name == "Sem Filtro":
            self.parent.history.add_entry("filtro", "Sem Filtro")
        elif filter_name == "Grayscale":
            self.parent.history.add_entry("filtro", "Grayscale")
        elif filter_name == "Binário":
            self.parent.history.add_entry("filtro", "Binário")
        elif filter_name == "Blur":
           self.parent.history.add_entry("filtro", "Blur")
        elif filter_name == "Sharpen":
            self.parent.history.add_entry("filtro", "Sharpen")
        elif filter_name == "Sobel":
            self.parent.history.add_entry("filtro", "Sobel")
        elif filter_name == "Laplacian":
            self.parent.history.add_entry("filtro", "Laplacian")
        elif filter_name == "Canny":
            self.parent.history.add_entry("filtro", "Canny")
        elif filter_name == "Emboss":
            self.parent.history.add_entry("filtro", "Emboss")
            
    def apply_filter(self, frame, filter_name):
        if frame is None:
            return
        
        if filter_name == "Sem Filtro":
            return self.parent.original_frame
        elif filter_name == "Grayscale":
            return converter_cinza(frame)
        elif filter_name == "Binário":
             return conversao_binaria(frame)
        elif filter_name == "Blur":
            return converter_blur(frame, 20, 20)
        elif filter_name == "Sharpen":
            return converter_sharpen(frame)
        elif filter_name == "Sobel":
            return transformar_sobel_positvo(converter_sobel(frame))
        elif filter_name == "Laplacian":
            return converter_laplacian(frame)
        elif filter_name == "Canny":
            return converter_Canny(frame, 50, 50)
        elif filter_name == "Emboss":
            return converter_emboss(frame)
        