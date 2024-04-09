import sys
import cv2
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QMessageBox, QHBoxLayout, QComboBox, QLabel, QScrollArea, QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

import config  # 

class CameraFeedWidget(QWidget):
    def __init__(self, camera_index):
        super().__init__()
        self.camera_index = camera_index
        self.image_label = QLabel("Loading...")
        self.image_label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)
        

        self.cap = cv2.VideoCapture(camera_index)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Adjust update frequency as needed

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to a QPixmap and scale it to a new size.
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convert_to_Qt_format = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(convert_to_Qt_format)
            # Scale the pixmap to a new size while maintaining the aspect ratio.
            scaled_pixmap = pixmap.scaled(320, 260, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # New size: 640x480
            self.image_label.setPixmap(scaled_pixmap)
        else:
            self.image_label.setText("Failed to load frame.")

    def stop_feed(self):
        self.timer.stop()
        if self.cap.isOpened():
            self.cap.release()

class CameraSelectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Camera Roles")
        self.setMinimumSize(800, 600)
        self.available_cameras = []
        self.roles = ["Select Role", "X", "Y", "Z"]
        self.camera_widgets = []

        # Create a QScrollArea and its contents
        self.scroll_area = QScrollArea(self)
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area.setWidgetResizable(True)

        # This layout is for the scrollable contents
        self.scroll_layout = QVBoxLayout(self.scroll_area_widget_contents)

        # Discover and set up cameras within the scrollable area
        self.discover_cameras()
        self.setup_ui()

        # Set the scrollable widget to the scroll area
        self.scroll_area.setWidget(self.scroll_area_widget_contents)

        # This main layout is for the entire dialog, including the scroll area
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.scroll_area)

        # The confirm button is added to the main layout, outside the scroll area
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirm_and_close)
        self.main_layout.addWidget(self.confirm_button)

        # Set the main layout to the dialog
        self.setLayout(self.main_layout)

    def confirm_and_close(self):
        # Stop all camera feeds before closing the dialog.
        for camera_widget in self.camera_widgets:
            camera_widget.stop_feed()
        self.accept()  

    def discover_cameras(self):
        for i in range(10):  # Check a reasonable range of camera indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    self.available_cameras.append(i)
                cap.release()

    def setup_ui(self):
         for camera_index in self.available_cameras:
            camera_feed_widget = CameraFeedWidget(camera_index)
            self.camera_widgets.append(camera_feed_widget)

            combo = QComboBox()
            combo.addItems(self.roles)
            combo.currentIndexChanged.connect(lambda index, cam=camera_index: self.assign_role(index, cam))

            layout = QHBoxLayout()
            layout.addWidget(camera_feed_widget)
            layout.addWidget(combo)
            self.scroll_layout.addLayout(layout) 

    def assign_role(self, index, camera_index):
        if index > 0:
            role = self.roles[index]
            setattr(config, f'camera_role_{role}', camera_index)

    def confirm_selection(self):
        if None in [getattr(config, 'camera_role_X', None), getattr(config, 'camera_role_Y', None), getattr(config, 'camera_role_Z', None)]:
            QMessageBox.warning(self, "Incomplete Selection", "Please assign all roles before confirming.")
        else:
            self.accept()

    def closeEvent(self, event):
        for camera_widget in self.camera_widgets:
            camera_widget.stop_feed()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = CameraSelectionDialog()
    if dialog.exec_() == QDialog.Accepted:
        # Proceed with the application flow after the dialog is confirmed and closed.
        print("Dialog confirmed. Proceeding with application.")
    else:
        print("Dialog closed without confirmation. Exiting application.")
    sys.exit(app.exec_())
