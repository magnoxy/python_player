def adjust_speed(video, speed=1.0):
    frame_rate = int(video.get(cv2.CAP_PROP_FPS) * speed)
    video.set(cv2.CAP_PROP_FPS, frame_rate)
    return video

def play_video(self, file_path):
    self.cap = cv2.VideoCapture(file_path)
    while True:
        ret, frame = self.cap.read()
        if not ret:
            break
        cv2.imshow("Vídeo", frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
