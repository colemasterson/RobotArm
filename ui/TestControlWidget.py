from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
import os
from ui.PhotoWidget import PhotoWidget
from ui.CameraWidget import CameraWidget
from ui.RunButtonWidget import RunButtonWidget
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSpinBox, QLabel, QHBoxLayout
from arm_controller import RobotArmController

class RunButtonWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.arm_controller = RobotArmController()  # Initialize the arm controller
        self.servo_spin_boxes = {}  # Dictionary to hold the spin boxes for each servo

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create spin boxes and labels for each servo
        for servo_id in range(1, 7):  # Assuming 6 servos
            servo_layout = QHBoxLayout()
            label = QLabel(f"Servo {servo_id}:")
            spin_box = QSpinBox()
            spin_box.setRange(-90, 90)  # Set the range for the spin box
            self.servo_spin_boxes[servo_id] = spin_box

            servo_layout.addWidget(label)
            servo_layout.addWidget(spin_box)
            layout.addLayout(servo_layout)

        # Create the execute button
        execute_button = QPushButton("Execute Movement", self)
        execute_button.setFixedSize(200, 50)
        execute_button.clicked.connect(self.execute_movement)

        layout.addWidget(execute_button)

        self.setLayout(layout)
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Servo Control')

    def execute_movement(self):
        for servo_id, spin_box in self.servo_spin_boxes.items():
            delta = spin_box.value()
            self.arm_controller.adjust_servo_angle(servo_id, delta)

        # Reset the spin boxes after execution
        for spin_box in self.servo_spin_boxes.values():
            spin_box.setValue(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = RunButtonWidget()
    sys.exit(app.exec_())
'''

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSpinBox, QLabel, QHBoxLayout
from arm_controller import RobotArmController  # Import your RobotArmController class

class RunButtonWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.arm_controller = RobotArmController()  # Initialize the arm controller
        self.servo_spin_boxes = {}  # Dictionary to hold the spin boxes for each servo

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create spin boxes and labels for each servo
        for servo_id in range(1, 7):  # Assuming 6 servos
            servo_layout = QHBoxLayout()
            label = QLabel(f"Servo {servo_id}:")
            spin_box = QSpinBox()
            spin_box.setRange(-90, 90)  # Set the range for the spin box
            self.servo_spin_boxes[servo_id] = spin_box

            servo_layout.addWidget(label)
            servo_layout.addWidget(spin_box)
            layout.addLayout(servo_layout)

        # Create the execute button
        execute_button = QPushButton("Execute Movement", self)
        execute_button.setFixedSize(200, 50)
        execute_button.clicked.connect(self.execute_movement)

        layout.addWidget(execute_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Servo Control')

    def execute_movement(self):
        for servo_id, spin_box in self.servo_spin_boxes.items():
            delta = spin_box.value()
            self.arm_controller.adjust_servo_angle(servo_id, delta)

        # Reset the spin boxes after execution
        for spin_box in self.servo_spin_boxes.values():
            spin_box.setValue(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = RunButtonWidget()
    sys.exit(app.exec_())
'''