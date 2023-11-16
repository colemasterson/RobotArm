import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
import pyqtgraph.opengl as gl

from model.robot_simulation.start_robot import QtMain, RenderWindow, QtSliders

class ModelWidget(QWidget):
    def __init__(self, model_name):
        super(ModelWidget, self).__init__()

        # Create framework
        self.main_win = QtMain("Robot Modelling V4.0.1")
        np.set_printoptions(precision=1, suppress=True)

        # Add 3d renderer and label to framework
        view_3d = RenderWindow(self.main_win)
        self.main_win.hbox.addWidget(view_3d, 3)

        # Add popup window to framework
        self.main_win.pop = QtSliders(view_3d)

        # Add QtMain instance as a widget to this main application
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.main_win)
        
        model_label = QLabel(self)
        name_label = QLabel(model_name, self)
        
        self.layout.addWidget(model_label)

        self.setGeometry(100, 100, 500, 400)
        self.setWindowTitle('Main Application')
        self.show()

    # ... (rest of the code)
