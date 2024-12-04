#bibliotecas necessarias

import cv2
import numpy as np
import os
from PIL import Image, ImageFilter
from matplotlib import pyplot as plt


def selecionar_roi_imagem(frame):
    if frame is None:
        raise ValueError("Imagem inválida fornecida como parâmetro.")

    print("Selecione a região de interesse (ROI) na janela e pressione ENTER para confirmar ou ESC para cancelar.")
    roi = cv2.selectROI("Selecione a ROI", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Selecione a ROI")
    if roi == (0, 0, 0, 0):
        print("Nenhuma ROI foi selecionada.")
        return None

    x, y, w, h = roi
    roi_cortada = frame[int(y):int(y+h), int(x):int(x+w)]

    cv2.imshow("ROI Cortada", roi_cortada)
    print("Pressione qualquer tecla na janela de 'ROI Cortada' para continuar.")
    frame_cortado_convertido = cv2.cvtColor(roi_cortada, cv2.COLOR_BGR2RGB)
    cv2.waitKey(0)
    cv2.destroyWindow("ROI Cortada")

    salvar = input("Deseja salvar a ROI? (s/n): ").strip().lower()
    if salvar == 's':
        nome_arquivo = input("Digite o nome do arquivo para salvar (ex.: roi.jpg): ").strip()
        frame_cortado_convertido_convertido = cv2.cvtColor(frame_cortado_convertido, cv2.COLOR_RGB2BGR)
        cv2.imwrite(nome_arquivo, frame_cortado_convertido_convertido)
        print(f"ROI salva como '{nome_arquivo}'")
        print("Corte confirmado.")
        return frame_cortado_convertido
    else:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        print("Corte cancelado. Retornando a imagem original.")
        return frame