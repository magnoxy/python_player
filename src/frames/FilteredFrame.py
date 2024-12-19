from ..filters.grayscale import converter_cinza, conversao_binaria
from ..filters.convolution import *
import numpy as np
import cv2

def apply_filter_to_frame(frame, filter_name):
        if filter_name == "Sem Filtro":
            return frame
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
        
def normalizar_frame(frame):
    if frame is None:
        return None
    if len(frame.shape) == 2:  # Se for uma imagem em escala de cinza
        return cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)  # Converte para BGR
    return frame