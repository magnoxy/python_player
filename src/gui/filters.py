from PyQt5.QtWidgets import QListWidget

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
            self.parent.history.add_entry("Filtro", "Sem Filtro")
        elif filter_name == "Grayscale":
            self.parent.history.add_entry("Filtro", "Grayscale")
        elif filter_name == "Binário":
            self.parent.history.add_entry("Filtro", "Binário")
        elif filter_name == "Blur":
           self.parent.history.add_entry("Filtro", "Blur")
        elif filter_name == "Sharpen":
            self.parent.history.add_entry("Filtro", "Sharpen")
        elif filter_name == "Sobel":
            self.parent.history.add_entry("Filtro", "Sobel")
        elif filter_name == "Laplacian":
            self.parent.history.add_entry("Filtro", "Laplacian")
        elif filter_name == "Canny":
            self.parent.history.add_entry("Filtro", "Canny")
        elif filter_name == "Emboss":
            self.parent.history.add_entry("Filtro", "Emboss")
        