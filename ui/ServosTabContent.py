from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
import os
from ui.PhotoWidget import PhotoWidget
from ui.CameraWidget import CameraWidget
from ui.RunButtonWidget import RunButtonWidget

class ServosTabContent(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        def getLeftContent():
            control_layout = QVBoxLayout(self)
            # label = QLabel('Content for Servos Control Tab', self)
            # control_layout.addWidget(label)
            
            run_button = RunButtonWidget()
            control_layout.addWidget(run_button)
            control_layout.setContentsMargins(0, 0, 0, 0)
            
            layout.addLayout(control_layout)
            
        getLeftContent()
        
        right_layout = QHBoxLayout()
        # Add horizontal spacer to push the photo to the right
        # spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # right_layout.addItem(spacer)
        
        # script_directory = os.path.dirname(os.path.realpath(__file__))
        # photo1_filename = os.path.join(script_directory, 'Image_Feed', 'OurRobot.png')

        # Create photo widgets with specified file names
        # photo1_widget = PhotoWidget(photo1_filename, photo1_name, target_height=300, target_width=500)
        # right_layout.addWidget(photo1_widget)
        
        camera_name = "Camera View"
        
        camera_widget = CameraWidget(camera_name)
        right_layout.addWidget(camera_widget)

        layout.addLayout(right_layout)
