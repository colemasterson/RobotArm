import sys
import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

class CameraWidget(QWidget):
    def __init__(self, widget_name, parent=None):
        super(CameraWidget, self).__init__(parent)

        self.video_capture = cv2.VideoCapture(2)  # Open the default camera (you can change the index if you have multiple cameras)

        self.image_label = QLabel(self)
        self.name_label = QLabel(widget_name, self)
        self.image_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)

        # Add name and image labels to a vertical layout
        layout.addWidget(self.name_label)
        layout.addWidget(self.image_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30 milliseconds (adjust as needed)
        self.setGeometry(100, 100, 800, 600)
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CameraWidget("Widget 1")
    window.setWindowTitle('Camera Stream Viewer')
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())
