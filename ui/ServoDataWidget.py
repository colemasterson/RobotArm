import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

class ServoDataWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.initUI()
        self.initTimer()

    def initUI(self):
        # Set the window title and initial size
        self.setWindowTitle('Servo Data Display')
        self.setGeometry(100, 100, 300, 200)
        self.updateServoData([])  # Start with an empty list for initial display

    def initTimer(self):
        # Initialize the QTimer
        self.timer = QTimer(self)
        # Connect timeout signal to the update function
        self.timer.timeout.connect(lambda: self.loadAndUpdateServoDataFromJSON('cam_position/current_position.json'))
        # Start the timer with an interval of 5000 milliseconds (5 seconds)
        self.timer.start(5000)

    def loadAndUpdateServoDataFromJSON(self, json_file_path):
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
                self.setData(data)
        except Exception as e:
            print(f"Error loading or updating data from JSON: {e}")

    def setData(self, data):
        servo_data = [{
            "id": key,
            "xyz": f"{value['tvec'][0]}, {value['tvec'][1]}, {value['tvec'][2]}",
            "euler_xyz": f"{value['euler_angles'][0]}, {value['euler_angles'][1]}, {value['euler_angles'][2]}"
        } for key, value in data.items()]
        self.updateServoData(servo_data)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def updateServoData(self, servos_data):
        self.clearLayout(self.layout)
        for servo in servos_data:
            servo_label = QLabel(f"Servo {servo['id']} - XYZ: {servo['xyz']} - Euler: {servo['euler_xyz']}")
            servo_label.setStyleSheet("QLabel { margin-top: 20px; margin-bottom: 20px; }")
            self.layout.addWidget(servo_label)

def main():
    app = QApplication(sys.argv)
    widget = ServoDataWidget()
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
