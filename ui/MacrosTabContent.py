from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
import os
# from ui.PhotoWidget import PhotoWidget

class MacrosTabContent(QWidget):
    
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        def getLeftContent():
            label = QLabel('Content for Macros Control Tab', self)
            layout.addWidget(label)
        getLeftContent()
        right_layout = QHBoxLayout()
        # Add horizontal spacer to push the photo to the right
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        right_layout.addItem(spacer)
        
        # script_directory = os.path.dirname(os.path.realpath(__file__))
        # photo1_filename = os.path.join(script_directory, 'Image_Feed', 'OurRobot.png')
        # photo1_name = 'Camera View'

        # Create photo widgets with specified file names
        # photo1_widget = PhotoWidget(photo1_filename, photo1_name, target_height=300, target_width=500)
        # right_layout.addWidget(photo1_widget)

        layout.addLayout(right_layout)
