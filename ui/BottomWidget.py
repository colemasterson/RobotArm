from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
import os
from ui.ModelWidget import ModelWidget
from ui.TextListWidget import TextListWidget
from PyQt5.QtCore import Qt

class BottomWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        
        current_state_text_list = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
        current_state_info = TextListWidget(current_state_text_list)
        
        current_model_widget = ModelWidget()
        
        final_state_text_list = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
        final_state_info = TextListWidget(final_state_text_list)
        
        final_model_widget = ModelWidget()

        # Create a QHBoxLayout for the bottom layout
        bottom_layout = QHBoxLayout(self)
        
        # Add Current State Info
        
        bottom_left_layout = QVBoxLayout()
        bottom_left_label = QLabel("Current State")
        bottom_left_layout.addWidget(bottom_left_label)
        
        bottom_left_label.setAlignment(Qt.AlignCenter)
        
        bottom_left_model_layout = QHBoxLayout()
        
        bottom_left_model_layout.addWidget(current_state_info)
        bottom_left_model_layout.addWidget(current_model_widget)
        
        bottom_left_layout.addLayout(bottom_left_model_layout)
        bottom_layout.addLayout(bottom_left_layout)
        
        # Add Final State Info
        
        bottom_right_layout = QVBoxLayout()
        bottom_right_label = QLabel("Final State")
        bottom_right_layout.addWidget(bottom_right_label)
        
        bottom_right_label.setAlignment(Qt.AlignCenter)
        
        bottom_right_model_layout = QHBoxLayout()
        
        bottom_right_model_layout.addWidget(final_state_info)
        bottom_right_model_layout.addWidget(final_model_widget)
        
        bottom_right_layout.addLayout(bottom_right_model_layout)
        bottom_layout.addLayout(bottom_right_layout)

        # Set the widget's layout
        self.setLayout(bottom_layout)
