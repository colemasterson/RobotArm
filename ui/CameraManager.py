import cv2
from threading import Lock

class CameraManager:
    def __init__(self):
        self.cameras = {}
        self.locks = {}

    def get_frame(self, camera_index):
        with self._get_lock(camera_index):
            if camera_index not in self.cameras:
                # Lazy initialization of camera
                self.cameras[camera_index] = cv2.VideoCapture(camera_index)
                if not self.cameras[camera_index].isOpened():
                    raise ValueError(f"Could not open camera with index {camera_index}")
            ret, frame = self.cameras[camera_index].read()
            if not ret:
                raise ValueError(f"Could not read frame from camera {camera_index}")
            return frame

    def release(self):
        for index, cap in self.cameras.items():
            cap.release()
        self.cameras.clear()

    def _get_lock(self, camera_index):
        if camera_index not in self.locks:
            self.locks[camera_index] = Lock()
        return self.locks[camera_index]
