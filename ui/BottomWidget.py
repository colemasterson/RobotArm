from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from ui.PhotoWidget import PhotoWidget  # Assuming you have the PhotoWidget class in a file named photo_widget.py
import os
from ui.ModelWidget import ModelWidget

class BottomWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        cmodel_name = 'Current State'
        fmodel_name = 'Final State'
        
        current_model_widget = ModelWidget("Current State")
        final_model_widget = ModelWidget("Final State")

        # Create a QHBoxLayout for the bottom layout
        bottom_layout = QHBoxLayout(self)
        
        bottom_layout.addWidget(current_model_widget)
        bottom_layout.addWidget(final_model_widget)
        
        current_model_widget.setContentsMargins(0,0,0,0)
        final_model_widget.setContentsMargins(0,0,0,0)
        bottom_layout.setContentsMargins(0,0,0,0)

        # Set the widget's layout
        self.setLayout(bottom_layout)
