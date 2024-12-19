import cv2

def apply_grayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def converter_cinza(frame):
    frame_convertido = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame_cinza = cv2.cvtColor(frame_convertido,cv2.COLOR_RGB2GRAY)
    return frame_cinza

def conversao_binaria(frame):
    frame_convertido = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame_cinza = cv2.cvtColor(frame_convertido,cv2.COLOR_RGB2GRAY)
    _, frame_binario = cv2.threshold(frame_cinza, 127, 255, cv2.THRESH_BINARY)
    return frame_binario

# A GERAÇÃO DE IMAGENS DE COR É RODANDO O PROPRIO FRAME