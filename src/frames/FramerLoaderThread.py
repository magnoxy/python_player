from PyQt5.QtCore import QThread, pyqtSignal
import cv2

class FrameLoaderThread(QThread):
    frames_loaded = pyqtSignal(list)  # Signal to send the loaded frames back to the main thread

    def __init__(self, cap, parent=None):
        super().__init__(parent)
        self.cap = cap

    def run(self):
        frames_list = []
        cap = self.cap
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frames_list.append(frame)
        
        # Emit the signal to inform the main thread that the frames are loaded
        self.frames_loaded.emit(frames_list)
        cap.release()  # Don't forget to release the capture when done.

# No seu método onde você chama load_frames_list:
def load_frames_list(self):
    cap = self.cap
    self.loader_thread = FrameLoaderThread(cap)
    
    # Connect the signal to a method to handle the frames once they are loaded
    self.loader_thread.frames_loaded.connect(self.on_frames_loaded)
    
    # Start the thread
    self.loader_thread.start()

def on_frames_loaded(self, frames_list):
    print("Frames carregados com sucesso")
    print("Lista de Frames: ", frames_list)
    self.frames_list = frames_list  # Save the loaded frames or process further
