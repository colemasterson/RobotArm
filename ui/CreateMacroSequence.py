import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,  QComboBox, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt


class CreateMacroSequence(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create widgets
        self.macro_widgets = {}
        self.header_label = QLabel('Create Macro Secuence')
        self.name_label = QLabel('Sequence Name:')
        self.name_line_edit = QLineEdit()
        name_horizontal_layout = QHBoxLayout()
        name_horizontal_layout.addWidget(self.name_label)
        name_horizontal_layout.addWidget(self.name_line_edit)
        
        vertical_layout_left = QVBoxLayout()
        vertical_layout_left.addWidget(self.header_label)
        vertical_layout_left.addLayout(name_horizontal_layout)
        
        #self.name_line_edit.setMaximumWidth(150)  # Adjust the value as needed
        for macro_num in range(1, 6):
            macro_label = QLabel(f'Macro {macro_num}:')
            macro_combobox = QComboBox()
            macro_combobox.setMinimumWidth(400)
            #Todo GetCurentMacros()
            macro_combobox.addItems(['None', 'Macro1 (Up)', 'Macro2 (Down)', 'Macro3 (Left)', 'Macro4 (Right)'])
            # Store labels and line edits in the dictionary
            self.macro_widgets[f'macro_label_{macro_num}'] = macro_label
            self.macro_widgets[f'macro_line_edit_{macro_num}'] = macro_combobox
            
            servo_layout = QHBoxLayout()
            servo_layout.addWidget(macro_label)
            servo_layout.addWidget(macro_combobox)

            # Add the servo layout to the main vertical layout
            vertical_layout_left.addLayout(servo_layout)

        # Create a button to trigger an action
        self.save_button = QPushButton('Save')
        self.save_button.setMaximumWidth(80)
        self.save_button.clicked.connect(self.on_save)
        
        self.run_sequence_button = QPushButton('Run Sequence')
        self.run_sequence_button.setMaximumWidth(150)
        self.run_sequence_button.clicked.connect(self.on_runMacroSequence)

        runSequence_label = QLabel('Select Sequence:')
        runSequence_combobox = QComboBox()
        runSequence_combobox.setMinimumWidth(275)
        runSequence_combobox.addItems(['None', 'Sequence1 (Pick Up Item)', 'Sequence2 (Put Down Item)']) #Todo use actual stored sequences
        
        runSequence_horiz_layout = QHBoxLayout()
        runSequence_horiz_layout.addWidget(runSequence_label)
        runSequence_horiz_layout.addWidget(runSequence_combobox)
        runSequence_horiz_layout.addWidget(self.run_sequence_button)
        
        
        vertical_layout_left.addWidget(self.save_button)
        vertical_layout_left.addLayout(runSequence_horiz_layout)

        # Create vertical layout for the main layout
        vertical_layout_left.setAlignment(Qt.AlignLeft)

        # Set the layout for the main window
        self.setLayout(vertical_layout_left)

    def on_save(self):
        # Get the text from the QLineEdit and do something with it
        entered_name = self.name_line_edit.text()
        for macro_num in range(1, 6):
            macro_line_edit = self.macro_widgets[f'macro_line_edit_{macro_num}']
            macro_value = macro_line_edit.text()
            #Todo: Store macro_values
        print(f"Entered Name: {entered_name}")
    
    def on_runMacroSequence(self):
        #Todo Call Actual Run Sequence
        print(f"Run Sequence")
        # print something out
        # You can store the entered name in a variable or perform any other actions here

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = CreateMacroSequence()
    widget.show()
    sys.exit(app.exec_())
