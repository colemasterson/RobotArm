import sys
import os
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
from arm_control.arm_controller import RobotArmController
from ui.CameraManager import CameraManager
from cam_position.estimatePoseFolder import PoseEstimator

class MacroExecutionWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, robot_arm_controller, macro_names, camera_manager, pose_estimator, save_dir, primary_camera_index=0, secondary_camera_index=4):
        super().__init__()
        self.robot_arm_controller = robot_arm_controller
        self.macro_names = macro_names
        self.camera_manager = camera_manager
        self.pose_estimator = pose_estimator
        self.save_dir = save_dir
        self.primary_camera_index = primary_camera_index
        self.secondary_camera_index = secondary_camera_index

    def run(self):
        for name in self.macro_names:
            if name != 'None':
                self.robot_arm_controller.execute_macro(name)
        # Capture images from primary camera
        for i in range(10):
            frame = self.camera_manager.get_frame(self.primary_camera_index)
            if frame is not None: 
                img_path = os.path.join(self.save_dir, "primary", f"x_image_{i + 1}.jpg")
                cv2.imwrite(img_path, frame)
                print(f"Saved {img_path}")
            else:
                print(f"Failed to capture image {i + 1}")
        # Capture additional images from secondary camera (Camera 4)
        for i in range(10):
            frame = self.camera_manager.get_frame(self.secondary_camera_index)
            if frame is not None:
                # All images from secondary camera are labeled 'y'
                img_path = os.path.join(self.save_dir, "secondary", f"y_image_{i + 1}.jpg")
                cv2.imwrite(img_path, frame)
                print(f"Saved {img_path} from secondary camera")
            else:
                print(f"Failed to capture image {i + 1} from secondary camera")
        self.finished.emit()

        # call the pose estimation
        self.pose_estimator.updatePos()

class CreateMacroSequence(QWidget):
    def __init__(self, camera_manager, pose_estimator):
        super().__init__()
        self.camera_manager = camera_manager
        self.pose_estimator = pose_estimator
        self.robot_arm_controller = RobotArmController()
        self.robot_arm_controller.define_macros()
        self.initUI()
        
    def initUI(self):
        self.macro_widgets = {}
        self.header_label = QLabel('Create Macro Sequence')
        self.name_label = QLabel('Sequence Name:')
        self.name_line_edit = QLineEdit()
        name_horizontal_layout = QHBoxLayout()
        name_horizontal_layout.addWidget(self.name_label)
        name_horizontal_layout.addWidget(self.name_line_edit)
        
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.header_label)
        vertical_layout.addLayout(name_horizontal_layout)
        
        for macro_num in range(1, 9):  
            macro_label = QLabel(f'Macro {macro_num}:')
            macro_combobox = QComboBox()
            macro_combobox.setMinimumWidth(400)
            self.macro_widgets[f'macro_{macro_num}'] = macro_combobox

            macro_names = list(self.robot_arm_controller.macros.keys())
            macro_combobox.addItems(['None'] + macro_names)

            macro_layout = QHBoxLayout()
            macro_layout.addWidget(macro_label)
            macro_layout.addWidget(macro_combobox)
            vertical_layout.addLayout(macro_layout)

        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.on_save)
        vertical_layout.addWidget(self.save_button)
        
        self.run_custom_sequence_button = QPushButton('Run Custom Sequence')
        self.run_custom_sequence_button.clicked.connect(self.on_runMacroSequence)
        vertical_layout.addWidget(self.run_custom_sequence_button)

        self.run_preset_sequence_button = QPushButton('Run Preset Sequence')
        self.run_preset_sequence_button.clicked.connect(self.on_runPresetSequence)
        vertical_layout.addWidget(self.run_preset_sequence_button)

        self.runSequence_label = QLabel('Select Sequence:')
        self.runSequence_combobox = QComboBox()
        self.runSequence_combobox.setMinimumWidth(275)
        self.populate_sequences_combobox()
        
        runSequence_layout = QHBoxLayout()
        runSequence_layout.addWidget(self.runSequence_label)
        runSequence_layout.addWidget(self.runSequence_combobox)
        vertical_layout.addLayout(runSequence_layout)

        self.setLayout(vertical_layout)

    def on_save(self):
        sequence_name = self.name_line_edit.text()
        macro_names = [self.macro_widgets[f'macro_{macro_num}'].currentText() for macro_num in range(1, 9) if self.macro_widgets[f'macro_{macro_num}'].currentText() != 'None']
        self.robot_arm_controller.save_macro_sequence(sequence_name, macro_names)

    def populate_sequences_combobox(self):
        sequences_dir = os.path.join(os.path.dirname(__file__), "../arm_control/macro_sequences")
        sequences = [os.path.splitext(file)[0] for file in os.listdir(sequences_dir) if file.endswith('.json')]
        self.runSequence_combobox.clear()  
        self.runSequence_combobox.addItems(['None'] + sequences)

    def on_runPresetSequence(self):
        selected_sequence = self.runSequence_combobox.currentText()
        if selected_sequence and selected_sequence != 'None':
            macro_names = self.robot_arm_controller.load_macro_sequence(selected_sequence)
            self.execute_sequence(macro_names)

    def on_runMacroSequence(self):
        macro_names = [self.macro_widgets[f'macro_{macro_num}'].currentText() for macro_num in range(1, 9) if self.macro_widgets[f'macro_{macro_num}'].currentText() != 'None']
        self.execute_sequence(macro_names)

    def execute_sequence(self, macro_names):
        save_dir = "cam_position/estimation_photos"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Assuming the primary camera index is 2, and the secondary camera index for additional images is 4
        self.thread = QThread()
        self.worker = MacroExecutionWorker(self.robot_arm_controller, macro_names, self.camera_manager, self.pose_estimator, save_dir, primary_camera_index=2, secondary_camera_index=4)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    camera_manager = CameraManager()
    pose_estimator = PoseEstimator()
    widget = CreateMacroSequence(camera_manager, pose_estimator)
    widget.show()
    sys.exit(app.exec_())