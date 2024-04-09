import os

import cv2
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QLineEdit, QPushButton
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt
import config

# Worker class for moving servos and capturing images in a separate thread
class ServoMovementWorker(QObject):
    finished = pyqtSignal()  # Signal to indicate task completion

    def __init__(self, arm_interface, positions, camera_manager, pose_estimator, save_dir, primary_camera_index, secondary_camera_index):
        super().__init__()
        self.arm_interface = arm_interface
        self.positions = positions
        self.camera_manager = camera_manager
        self.pose_estimator = pose_estimator
        self.save_dir = save_dir
        self.primary_camera_index = primary_camera_index
        self.secondary_camera_index = secondary_camera_index

    def run(self):
        # Move the arm to the specified positions
        for position_index, position in enumerate(self.positions):
            self.arm_interface.set_servo_position(position_index + 1, position, wait=True)
        
        # Capture and save images from the primary camera
        for i in range(10):
            frame = self.camera_manager.get_frame(self.primary_camera_index)
           
            img_path = os.path.join(self.save_dir, "primary", f"x_image_{i + 1}.jpg")
            if frame is not None:
                cv2.imwrite(img_path, frame)
                print(f"Saved {img_path}")
        
        # Capture and save images from the secondary camera
        for i in range(10):
            frame = self.camera_manager.get_frame(self.secondary_camera_index)
            img_path = os.path.join(self.save_dir, "secondary", f"y_image_{i + 1}.jpg")
            if frame is not None:
                cv2.imwrite(img_path, frame)
                print(f"Saved {img_path} from secondary camera")
         # Recalculate the position
        self.pose_estimator.updatePos()
        self.finished.emit()
# Main widget class
class ServosControlWidget(QWidget):
    def __init__(self, arm_interface, camera_manager, pose_estimator):
        super().__init__()
        self.arm_interface = arm_interface
        self.camera_manager = camera_manager
        self.pose_estimator = pose_estimator
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.servo_controls = []

        for i in range(6):  # Assuming 6 servos
            servo_layout = QHBoxLayout()
            label = QLabel(f"Servo {i + 1}")
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(-125 * 4)
            slider.setMaximum(125 * 4)
            slider.setTickInterval(1)

            input_box = QLineEdit()
            input_box.setValidator(QDoubleValidator(-125.0, 125.0, 2))

            initial_value = 0.0
            input_box.setText(f"{initial_value}")
            slider.setValue(int(initial_value * 4))

            slider.valueChanged.connect(lambda value, i=i, lineEdit=input_box: self.sliderChanged(value, i, lineEdit))
            input_box.textChanged.connect(lambda value, i=i, sldr=slider: self.lineEditChanged(value, i, sldr))

            servo_layout.addWidget(label)
            servo_layout.addWidget(slider)
            servo_layout.addWidget(input_box)
            layout.addLayout(servo_layout)
            self.servo_controls.append((slider, input_box))

        run_button = QPushButton('Run')
        run_button.clicked.connect(self.applyPositions)
        layout.addWidget(run_button)

    def sliderChanged(self, value, servo_index, lineEdit):
        if not lineEdit.hasFocus():
            lineEdit.setText(str(value / 4))

    def lineEditChanged(self, value, servo_index, slider):
        if not self.servo_controls[servo_index][0].isSliderDown():
            slider.setValue(int(float(value) * 4) if value else 0)

    def applyPositions(self):
        positions = [float(input_box.text()) for _, input_box in self.servo_controls]
        
        save_dir = "cam_position/estimation_photos"  
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        self.thread = QThread()
        self.worker = ServoMovementWorker(self.arm_interface, positions, self.camera_manager , self.pose_estimator, save_dir,  primary_camera_index= config.camera_role_X, secondary_camera_index=config.camera_role_Y)
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        
        self.thread.start()