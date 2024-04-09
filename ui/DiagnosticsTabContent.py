from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton
import os
import os


from ui.BottomWidget import BottomWidget
from ui.CameraWidget import CameraWidget


class DiagnosticsTabContent(QWidget):
    def __init__(self, camera_manager):
        super().__init__()
        self.camera_manager = camera_manager
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        # Create the camera widgets for top left and top right
        camera_widget_left = CameraWidget("Camera Left", self.camera_manager, camera_index=4)
        camera_widget_right = CameraWidget("Camera Right",self.camera_manager, camera_index=6)
        
        # Create buttons for saving images
        save_button_left = QPushButton("Save Left Image")
        save_button_right = QPushButton("Save Right Image")
        
        # Connect buttons to the respective slot to save the current frame
        save_button_left.clicked.connect(lambda: camera_widget_left.save_current_frame("cam_position\estimation_photos\left_frame.jpg"))
        save_button_right.clicked.connect(lambda: camera_widget_right.save_current_frame("cam_position\estimation_photos\right_frame.jpg"))
        
        # Layout for top cameras and buttons
        top_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        
        left_layout.addWidget(camera_widget_left)
        left_layout.addWidget(save_button_left)
        
        right_layout.addWidget(camera_widget_right)
        right_layout.addWidget(save_button_right)
        
        top_layout.addLayout(left_layout)
        top_layout.addLayout(right_layout)
        
        layout.addLayout(top_layout)
        bottom_widget = BottomWidget()
        
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(bottom_widget)
        
        layout.addLayout(bottom_layout)
