from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton
import config
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
        camera_widget_left = CameraWidget("Camera X", self.camera_manager, camera_index= config.camera_role_X)
        camera_widget_right = CameraWidget("Camera Y",self.camera_manager, camera_index=config.camera_role_Y)
        
       
        # Layout for top cameras and buttons
        top_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        
        left_layout.addWidget(camera_widget_left)
        
        right_layout.addWidget(camera_widget_right)

        top_layout.addLayout(left_layout)
        top_layout.addLayout(right_layout)
        
        layout.addLayout(top_layout)
        bottom_widget = BottomWidget()
        
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(bottom_widget)
        
        layout.addLayout(bottom_layout)
