def adjust_speed(video, speed=1.0):
    frame_rate = int(video.get(cv2.CAP_PROP_FPS) * speed)
    video.set(cv2.CAP_PROP_FPS, frame_rate)
    return video
