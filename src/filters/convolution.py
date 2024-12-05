import cv2
import numpy as np

def apply_blur(image):
    return cv2.GaussianBlur(image, (5, 5), 0)

def apply_sharpen(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)


## Libs necessarias
# import cv2
#import numpy as np
#import os
#from PIL import Image, ImageFilter
#from matplotlib import pyplot as plt

def converter_sobel(frame):
    frame_convertido = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_gray = cv2.cvtColor(frame_convertido, cv2.COLOR_RGB2GRAY)
    frame_sobelx = cv2.Sobel(src=frame_gray, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=3)
    frame_sobely = cv2.Sobel(src=frame_gray, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=3)
    frame_sobelxy = cv2.addWeighted(frame_sobelx, 0.5, frame_sobely, 0.5, 0)

    # CASO SEJA FEITA UMA OPERAÇÃO EM CASCATA COM UM FILTRO DEPOIS DO SOBEL, É PRECISO PASSAR PELA FUNÇÃO transformar_sobel_positvo
    # PARA PODER NÃO OCORRER ERROS COM O CV2

    return frame_sobelxy

def transformar_sobel_positvo (frame):
    return cv2.convertScaleAbs(frame)

def converter_laplacian(frame):
    frame_convertida = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_gray = cv2.cvtColor(frame_convertida, cv2.COLOR_RGB2GRAY)
    frame_laplacean = cv2.Laplacian(frame_gray, cv2.CV_64F, ksize=3)

    # Normalizar para intervalo 0-255 e converter para uint8
    frame_laplacean = cv2.convertScaleAbs(frame_laplacean)

    return frame_laplacean

## É PRECISO PASSAR OS PARAMETROS DE INTENSIDADE: 1 - 300
def converter_Canny(frame, limiar_min,limiar_max):
    frame_convertido = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_gray = cv2.cvtColor(frame_convertido, cv2.COLOR_RGB2GRAY)
    img = cv2.GaussianBlur(frame_gray, (3, 3), 3, 3)
    frame_canny = cv2.Canny(img, limiar_min, limiar_max)
    return frame_canny

## É PRECISO PASSAR OS PARAMETROS DE INTENSIDADE: 1 - 50
def converter_blur(frame, desfoque_horizontal, desfoque_vertical):
    # frame_convertido = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_blur = cv2.blur(frame, ksize=(desfoque_horizontal, desfoque_vertical))
    return frame_blur

def converter_sharpen(frame):
    sharpen_kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])
    # frame_convertida = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_sharp = cv2.filter2D(frame, ddepth=-1,kernel=sharpen_kernel)
    return frame_sharp

def converter_emboss(frame):
    frame_convertido = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_gray = cv2.cvtColor(frame_convertido, cv2.COLOR_RGB2GRAY)
    emboss_kernel = np.array([[-2, -1, 0],
                          [-1,  1, 1],
                          [ 0,  1, 2]])
    frame_emboss = cv2.filter2D(frame_gray, -1, emboss_kernel)
    frame_emboss = cv2.normalize(frame_emboss, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    return frame_emboss





