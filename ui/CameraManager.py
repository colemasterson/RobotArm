
import cv2
from threading import Lock

class CameraManager:
    def __init__(self):
        self.cameras = {}
        self.locks = {}
        #self.index_mapping = {}

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
        for cap in self.cameras.values():
            cap.release()
        self.cameras.clear()

    def _get_lock(self, camera_index):
        if camera_index not in self.locks:
            self.locks[camera_index] = Lock()
        return self.locks[camera_index]
    
    def is_camera_available(self, camera_index):
        # Attempt to open the camera with the specified index
        cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)  # Optionally specify a backend
        if not cap.isOpened():
            cap.release()  # Ensure the resource is cleaned up
            return False  # Camera couldn't be opened
        
        # Try to grab a frame to confirm the camera is functional
        ret, frame = cap.read()
        cap.release()  # Clean up the resource after checking
        
        # The camera is considered available if a frame was successfully grabbed
        return ret and frame is not None
    def reset(self):
        # Call release to clean up resources
        self.release()
        # Reinitialize any necessary state
        self.cameras = {}
        self.locks = {}