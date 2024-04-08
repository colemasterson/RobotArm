import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLayout

class ServoDataWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.initUI()

    def initUI(self):
        # Set the window title and initial size
        self.setWindowTitle('Servo Data Display')
        self.setGeometry(100, 100, 300, 200)

        # Initialize with dummy data
        self.updateServoData([
            {"id": 1, "xyz": "0, 0, 0", "euler_xyz": "0, 0, 0"},
            {"id": 2, "xyz": "0, 0, 0", "euler_xyz": "0, 0, 0"},
            {"id": 3, "xyz": "0, 0, 0", "euler_xyz": "0, 0, 0"},
        ])

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def updateServoData(self, servos_data):
        # Clear the current layout first
        self.clearLayout(self.layout)

        # Create labels for each servo's data and add them to the layout
        for servo in servos_data:
            servo_label = QLabel(f"Servo: {servo['id']}\nXYZ: {servo['xyz']}\nEuler XYZ: {servo['euler_xyz']}")
            servo_label.setStyleSheet("QLabel { margin-top: 20px; margin-bottom: 20px; }")
            self.layout.addWidget(servo_label)

def main():
    app = QApplication(sys.argv)
    widget = ServoDataWidget()
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
