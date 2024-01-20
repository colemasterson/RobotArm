import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt  # Add this line to import Qt

from arm_control.hello_world import hello_world

class RunButtonWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create a QVBoxLayout to organize the widget
        layout = QVBoxLayout()

        # Create a QPushButton with the label "Run"
        run_button = QPushButton("Run", self)

        # Set the size of the button
        run_button.setFixedSize(800, 200)  # Adjust the width and height as needed

        # Set the background color of the button to green
        run_button.setStyleSheet("background-color: green; color: white; border-radius: 10px;")

        # Set the font size of the button text
        font = run_button.font()
        font.setPointSize(16)  # Adjust the font size as needed
        run_button.setFont(font)

        # Connect the button's clicked signal to the custom run_function
        run_button.clicked.connect(self.run_function)

        # Add the button to the layout and center it
        layout.addWidget(run_button, alignment=Qt.AlignCenter)

        # Set the layout for the main widget
        self.setLayout(layout)

        # Set the size and title of the main widget
        self.setGeometry(300, 300, 300, 200)

    def run_function(self):
        hello_world()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = RunButtonWidget()
    sys.exit(app.exec_())
