import sys
import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

class CameraWidget(QWidget):
    def __init__(self, widget_name, camera_manager, camera_index=0, parent=None):
        super(CameraWidget, self).__init__(parent)
        self.camera_manager = camera_manager
        self.camera_index = camera_index

        self.image_label = QLabel(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update frequency in milliseconds
        self.setGeometry(100, 100, 500, 400)

    def update_frame(self):
        frame = self.camera_manager.get_frame(self.camera_index)
        # Convert frame to QImage and then to QPixmap before setting it on the label
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)

    def save_current_frame(self, file_path):
        # Use the last frame captured by the update loop to ensure consistency
        frame = self.camera_manager.get_frame(self.camera_index)
        if frame is not None:
            cv2.imwrite(file_path, frame)
