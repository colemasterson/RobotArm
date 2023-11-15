from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PhotoWidget import PhotoWidget  # Assuming you have the PhotoWidget class in a file named photo_widget.py
import os

class BottomWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create photo widgets for the bottom layout
        script_directory = os.path.dirname(os.path.realpath(__file__))
        photo2_filename = os.path.join(script_directory, 'Image_Feed', 'OurRobot.png')
        photo2_name = 'Current State'
        photo3_filename = os.path.join(script_directory, 'Image_Feed', 'OurRobot.png')
        photo3_name = 'Final State'
        
        photo2_widget = PhotoWidget(photo2_filename, photo2_name, target_width=400, target_height=500)
        photo3_widget = PhotoWidget(photo3_filename, photo3_name, target_width=400, target_height=500)

        # Create a QHBoxLayout for the bottom layout
        bottom_layout = QHBoxLayout(self)
        bottom_layout.addWidget(photo2_widget)
        bottom_layout.addWidget(photo3_widget)

        # Set the widget's layout
        self.setLayout(bottom_layout)

