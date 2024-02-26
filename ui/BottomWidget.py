from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
import os
# from ui.ModelWidget import ModelWidget
from ui.TextListWidget import TextListWidget
from PyQt5.QtCore import Qt
from model.ModelWidget import ModelWidget

class BottomWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        
        
        current_state_text_list = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
        current_state_info = TextListWidget(current_state_text_list)
        
        # current_model_widget = ModelWidget()
        current_model_widget = ModelWidget()

        # Create a QHBoxLayout for the bottom layout
        bottom_layout = QVBoxLayout(self)
        bottom_bottom_layout = QHBoxLayout()
        
        bottom_label = QLabel("Current State")
        
        bottom_layout.addWidget(bottom_label)
        bottom_label.setAlignment(Qt.AlignCenter)
        
        bottom_bottom_layout.addWidget(current_state_info)
        bottom_bottom_layout.addWidget(current_model_widget)
        
        bottom_layout.addLayout(bottom_bottom_layout)
        
        self.setLayout(bottom_layout)
