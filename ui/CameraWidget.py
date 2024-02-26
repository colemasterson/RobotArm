import sys
import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

class CameraWidget(QWidget):
    def __init__(self, widget_name, parent=None):
        super(CameraWidget, self).__init__(parent)

        # self.video_capture = cv2.VideoCapture(0)  # Open the default camera (you can change the index if you have multiple cameras)
        self.video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Open the default camera (you can change the index if you have multiple cameras)

        self.image_label = QLabel(self)

        layout = QVBoxLayout(self)

        # Add name and image labels to a vertical layout
        layout.addWidget(self.image_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30 milliseconds (adjust as needed)
        self.setGeometry(100, 100, 500, 400)
        self.show()

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            # Convert OpenCV image to QImage
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

            # Display the image
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.video_capture.release()
