from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class PhotoWidget(QWidget):
    def __init__(self, photo_filename, photo_name, target_width=50, target_height=100):
        super().__init__()

        self.initUI(photo_filename, photo_name, target_width, target_height)

    def initUI(self, photo_filename, photo_name, target_width, target_height):
        # Create a QLabel for the image
        photo_label = QLabel(self)

        # Load the image using QPixmap
        pixmap = QPixmap(photo_filename)

        # Scale the image to the target width and height while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(target_width, target_height, Qt.KeepAspectRatio)

        photo_label.setPixmap(scaled_pixmap)

        # Create a QLabel for the image name
        name_label = QLabel(photo_name, self)

        # Create a QVBoxLayout to stack the labels vertically
        layout = QVBoxLayout(self)
        
        layout.addWidget(name_label)
        layout.addWidget(photo_label)

        # Center align the content horizontally within the widget
        layout.setAlignment(Qt.AlignHCenter)

