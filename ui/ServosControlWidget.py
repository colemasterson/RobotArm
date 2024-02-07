from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QLineEdit, QPushButton)
from PyQt5.QtGui import QDoubleValidator 
from PyQt5.QtCore import Qt

class ServosControlWidget(QWidget):
    def __init__(self, arm_interface):
        super().__init__()
        self.arm_interface = arm_interface
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.servo_controls = []
        
        for i in range(6):  # Assuming 6 servos
            servo_layout = QHBoxLayout()
            label = QLabel(f"Servo {i+1}")
            slider = QSlider(Qt.Horizontal)
            
            # Adjusting the slider range for -125.0 to 125.0 with 0.25 steps
            slider.setMinimum(-125 * 4)
            slider.setMaximum(125 * 4)
            slider.setTickInterval(1)  # Represents 0.25 degrees
            
            input_box = QLineEdit()
            input_box.setValidator(QDoubleValidator(-125.0, 125.0, 2))  # Allows floating point within range
            
            # Connect slider and input box to update each other
            slider.valueChanged.connect(lambda value, lineEdit=input_box: lineEdit.setText(str(value / 4)))
            input_box.textChanged.connect(lambda value, sldr=slider: sldr.setValue(int(float(value) * 4) if value else 0))
            
            servo_layout.addWidget(label)
            servo_layout.addWidget(slider)
            servo_layout.addWidget(input_box)
            layout.addLayout(servo_layout)
            self.servo_controls.append((slider, input_box))

        run_button = QPushButton('Run')
        run_button.clicked.connect(self.applyPositions)
        layout.addWidget(run_button)

    def applyPositions(self):
        for i, (slider, input_box) in enumerate(self.servo_controls):
            position = float(input_box.text())
            self.arm_interface.set_servo_position(i+1, position, wait=True)
