from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
import os
from ui.CameraWidget import CameraWidget
from ui.RunButtonWidget import RunButtonWidget
from ui.BottomWidget import BottomWidget
from PyQt5.QtCore import Qt
# from ui.TextListWidget import TextListWidget
from ui.ServosControlWidget import ServosControlWidget  # Make sure this path is correct
import config

class ServosTabContent(QWidget):
    def __init__(self, arm_interface, camera_manager, pose_estimator):
            super().__init__()
            self.initUI(arm_interface, camera_manager, pose_estimator)
            #self.camera_manager = camera_manager  

    def initUI(self, arm_interface, camera_manager, pose_estimator):
        layout = QVBoxLayout(self)
        
        # Add the top widget to contain the top-left and top-right widgets
        
        top_layout = QHBoxLayout()
        
        control_layout = QVBoxLayout()
        servo_control_widget = ServosControlWidget(arm_interface, camera_manager, pose_estimator)
        #layout.addWidget(servo_control_widget)
        control_layout.addWidget(servo_control_widget)
        top_layout.addLayout(control_layout)
        
        right_layout = QVBoxLayout()
        right_layout_lower = QHBoxLayout()
        
        # Add a label
        right_layout_label = QLabel("Camera View Name")
        right_layout_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(right_layout_label)
        
        # Add things to the lower layout
        right_layout.addLayout(right_layout_lower)
        
        example_text_list = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
        # camera_info = TextListWidget(example_text_list)
        # right_layout_lower.addWidget(camera_info)
        
        camera_widget = CameraWidget("Camera View", camera_manager, camera_index=  config.camera_role_Z)
        right_layout_lower.addWidget(camera_widget)
        
        
        top_layout.addLayout(right_layout)
        layout.addLayout(top_layout)
        
        # Add the bottom widget to contain the bottom widget 
        bottom_widget = BottomWidget()
        
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(bottom_widget)
        
        layout.addLayout(bottom_layout)
