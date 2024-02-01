import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt


class CreateMacroWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create widgets
        self.servo_widgets = {}
        self.header_label = QLabel('Create Macro')
        self.name_label = QLabel('Name:')
        self.name_line_edit = QLineEdit()
        name_horizontal_layout = QHBoxLayout()
        name_horizontal_layout.addWidget(self.name_label)
        name_horizontal_layout.addWidget(self.name_line_edit)
        
        vertical_layout_left = QVBoxLayout()
        vertical_layout_left.addWidget(self.header_label)
        vertical_layout_left.addLayout(name_horizontal_layout)
        
        #self.name_line_edit.setMaximumWidth(150)  # Adjust the value as needed
        for servo_num in range(1, 7):
            servo_label = QLabel(f'Servo {servo_num}:')
            servo_line_edit = QLineEdit()
            #servo_line_edit.setMaximumWidth(150)  # Adjust the value as needed

            # Store labels and line edits in the dictionary
            self.servo_widgets[f'servo_label_{servo_num}'] = servo_label
            self.servo_widgets[f'servo_line_edit_{servo_num}'] = servo_line_edit
            
            servo_layout = QHBoxLayout()
            servo_layout.addWidget(servo_label)
            servo_layout.addWidget(servo_line_edit)

            # Add the servo layout to the main vertical layout
            vertical_layout_left.addLayout(servo_layout)

        # Create a button to trigger an action
        self.save_button = QPushButton('Save')
        self.save_button.setMaximumWidth(80)
        self.save_button.clicked.connect(self.on_save)

        vertical_layout_left.addWidget(self.save_button)

        # Create vertical layout for the main layout
        vertical_layout_left.setAlignment(Qt.AlignLeft)

        # Set the layout for the main window
        self.setLayout(vertical_layout_left)

    def on_save(self):
        # Get the text from the QLineEdit and do something with it
        entered_name = self.name_line_edit.text()
        for servo_num in range(1, 7):
            servo_line_edit = self.servo_widgets[f'servo_line_edit_{servo_num}']
            servo_value = servo_line_edit.text()
        print(f"Entered Name: {entered_name}")

        #Todo You can store the entered name in a variable or perform any other actions here

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = CreateMacroWidget()
    widget.show()
    sys.exit(app.exec_())
