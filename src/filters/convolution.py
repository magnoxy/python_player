import cv2
import numpy as np

def apply_blur(image):
    return cv2.GaussianBlur(image, (5, 5), 0)

def apply_sharpen(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)
