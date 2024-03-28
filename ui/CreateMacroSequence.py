import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,  QComboBox, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from arm_control.arm_controller import RobotArmController
import json
import os


class CreateMacroSequence(QWidget):
    def __init__(self):
        super().__init__()
        self.robot_arm_controller = RobotArmController()
        self.robot_arm_controller.define_macros()
        self.initUI()
        #robot controller and macros defined
        
    def initUI(self):
        self.macro_widgets = {}
        self.header_label = QLabel('Create Macro Sequence')
        self.name_label = QLabel('Sequence Name:')
        self.name_line_edit = QLineEdit()
        name_horizontal_layout = QHBoxLayout()
        name_horizontal_layout.addWidget(self.name_label)
        name_horizontal_layout.addWidget(self.name_line_edit)
        
        vertical_layout_left = QVBoxLayout()
        vertical_layout_left.addWidget(self.header_label)
        vertical_layout_left.addLayout(name_horizontal_layout)
        
        for macro_num in range(1, 9):  # Assuming 8 macros for simplicity
            macro_label = QLabel(f'Macro {macro_num}:')
            macro_combobox = QComboBox()
            macro_combobox.setMinimumWidth(400)
            self.macro_widgets[f'macro_line_edit_{macro_num}'] = macro_combobox

            macro_names = list(self.robot_arm_controller.macros.keys())  # Make sure this matches your actual controller reference
            macro_names = "Test"
            macro_combobox.addItems(['None'] + macro_names)

            servo_layout = QHBoxLayout()
            servo_layout.addWidget(macro_label)
            servo_layout.addWidget(macro_combobox)
            vertical_layout_left.addLayout(servo_layout)

        # Create and connect the save button
        self.save_button = QPushButton('Save')
        self.save_button.setMaximumWidth(80)
        self.save_button.clicked.connect(self.on_save)
        vertical_layout_left.addWidget(self.save_button)
        
        # Create the first button for running custom sequences
        self.run_custom_sequence_button = QPushButton('Run Custom Sequence')
        self.run_custom_sequence_button.setMaximumWidth(200)
        self.run_custom_sequence_button.clicked.connect(self.on_runMacroSequence)
        vertical_layout_left.addWidget(self.run_custom_sequence_button)  # Add this button to the layout

        # Create the second button for running preset sequences
        self.run_preset_sequence_button = QPushButton('Run Preset Sequence')
        self.run_preset_sequence_button.setMaximumWidth(200)
        self.run_preset_sequence_button.clicked.connect(self.on_runPresetSequence)
        vertical_layout_left.addWidget(self.run_preset_sequence_button)  # Add this button to the layout too

        self.runSequence_label = QLabel('Select Sequence:')
        self.runSequence_combobox = QComboBox()
        self.runSequence_combobox.setMinimumWidth(275)
        self.populate_sequences_combobox()  # Populate with actual stored sequences
        
        runSequence_horiz_layout = QHBoxLayout()
        runSequence_horiz_layout.addWidget(self.runSequence_label)
        runSequence_horiz_layout.addWidget(self.runSequence_combobox)
        # It seems you want both buttons after the combobox, so they've been added directly to the main layout
        # If you want them next to the combobox, add them here instead
        
        vertical_layout_left.addLayout(runSequence_horiz_layout)

        vertical_layout_left.setAlignment(Qt.AlignLeft)
        self.setLayout(vertical_layout_left)


    def on_save(self):
        # Get the name for the sequence from a QLineEdit widget
        sequence_name = self.name_line_edit.text()

        # Collect macro names from the UI, assuming they're in QComboBoxes
        macro_names = []
        for macro_num in range(1, 9):  # Adjust the range based on your UI
            macro_combobox = self.macro_widgets[f'macro_line_edit_{macro_num}']
            macro_value = macro_combobox.currentText()
            if macro_value and macro_value != 'None':  # Only add non-empty and non-'None' values
                macro_names.append(macro_value)

        # Save the sequence using the arm controller
        self.robot_arm_controller.save_macro_sequence(sequence_name, macro_names)

    def populate_sequences_combobox(self):
        # Assuming this method populates the combobox with saved sequences
        sequences_dir = os.path.join(os.path.dirname(__file__), "../arm_control/macro_sequences")
        sequences = [os.path.splitext(file)[0] for file in os.listdir(sequences_dir) if file.endswith('.json')]
        self.runSequence_combobox.clear()  # Assuming this is the combobox instance name
        self.runSequence_combobox.addItems(['None'] + sequences)

    def on_runPresetSequence(self):
        selected_sequence = self.runSequence_combobox.currentText()
        if selected_sequence and selected_sequence != 'None':
            macro_names = self.robot_arm_controller.load_macro_sequence(selected_sequence)
            for name in macro_names:
                self.robot_arm_controller.execute_macro(name)
                # Consider adding delays or checks as needed
    
    def on_runMacroSequence(self):
         for macro_num in range(1, 9):
             macro_combobox = self.macro_widgets[f'macro_line_edit_{macro_num}']
             selected_macro = macro_combobox.currentText()
             if selected_macro != 'None':
                 self.robot_arm_controller.execute_macro(selected_macro)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = CreateMacroSequence()
    widget.show()
    sys.exit(app.exec_())
